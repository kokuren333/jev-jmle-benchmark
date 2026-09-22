from __future__ import annotations
import argparse,json,math
import numpy as np,pandas as pd
from common import RUNS,dump_json

def resolve(x): return RUNS/(RUNS/'LATEST').read_text().strip() if x=='latest' else RUNS/x

def wilson(k,n,z=1.95996398454):
    if n==0:return [None,None]
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [c-h,c+h]

def official_points(r):
    if not r['correct']: return 0
    if r['block'] in ['B','E']: return 1 if int(r['number'])<=25 else 3
    if r['block'] in ['A','C','D','F']: return 1
    return 0

def subset(df,col):
    if df.empty:return []
    return df.groupby(col,dropna=False).agg(n=('correct','size'),correct=('correct','sum'),accuracy=('correct','mean'),median_latency_ms=('latency_ms','median')).reset_index()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',default='latest');a=ap.parse_args();run=resolve(a.run)
    manifest=json.loads((run/'manifest.json').read_text(encoding='utf-8'))
    rows=[json.loads(x) for x in (run/'items.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];ok=[r for r in rows if r.get('status')=='ok'];n=len(ok);k=sum(r['correct'] for r in ok)
    l=np.array([r['latency_ms'] for r in ok]) if ok else np.array([])
    top1_conf=[];corr=[];single_conf=[];single_corr=[];nll_single=[];brier_single=[]
    for r in ok:
        probs=r.get('probabilities') or {}; top1_conf.append(max(probs.values()) if probs else float('nan'));corr.append(int(r['correct']))
        if r.get('select_k')==1 and probs:
            single_conf.append(max(float(p) for p in probs.values()));single_corr.append(int(r['correct']))
            g=r['gold'][0];pg=max(float(probs.get(g,1e-15)),1e-15);nll_single.append(-math.log(pg));brier_single.append(sum((float(p)-(1.0 if a==g else 0.0))**2 for a,p in probs.items()))
    ece=0.0
    if single_conf:
        c=np.array(single_conf,dtype=float);y=np.array(single_corr);valid=~np.isnan(c);c=c[valid];y=y[valid]
        for lo,hi in zip(np.linspace(0,1,11)[:-1],np.linspace(0,1,11)[1:]):
            m=(c>=lo)&((c<hi) if hi<1 else (c<=hi))
            if m.any():ece+=m.mean()*abs(c[m].mean()-y[m].mean())
    official=None
    if manifest.get('dataset_mode')=='official120':
        req=sum(official_points(r) for r in ok if r['block'] in ['B','E']);gen=sum(official_points(r) for r in ok if r['block'] in ['A','C','D','F'])
        complete=(manifest.get('image_mode')=='both' and len({r['question_id'] for r in ok})==400)
        official={'complete_400':complete,'required_score':req,'required_max':200,'general_clinical_score':gen,'general_clinical_max':300,'published_thresholds_pass':(req>=160 and gen>=224) if complete else None,'official_pass_status':'INDETERMINATE (prohibited-choice identities are not public)' if complete else 'NOT_ASSESSED (not a complete 400-item run)'}
    summary={'dataset_mode':manifest.get('dataset_mode'),'image_mode':manifest.get('image_mode'),'n_attempted':len(rows),'n_success':n,'n_correct_exact_set':k,'accuracy_exact_set':k/n if n else None,'accuracy_wilson95':wilson(k,n),'single_select_n':sum(r.get('select_k')==1 for r in ok),'multi_select_n':sum(r.get('select_k',1)>1 for r in ok),'latency_ms':({'mean':float(l.mean()),'p50':float(np.percentile(l,50)),'p90':float(np.percentile(l,90)),'p95':float(np.percentile(l,95)),'p99':float(np.percentile(l,99))} if n else {}),'single_select_nll':float(np.mean(nll_single)) if nll_single else None,'single_select_multiclass_brier':float(np.mean(brier_single)) if brier_single else None,'top1_confidence_ece_10bin_exploratory':float(ece) if single_conf else None,'official_style':official}
    dump_json(run/'summary.json',summary)
    df=pd.DataFrame(ok)
    for col,name in [('year','by_year.csv'),('block','by_block.csv'),('clinical_area','by_domain.csv'),('image_dependency','by_image_dependency.csv'),('has_image_reference','by_image_presence.csv'),('select_k','by_select_k.csv'),('is_calc','by_calc.csv')]:
        if col in df.columns and not df.empty:
            subset(df,col).to_csv(run/name,index=False,encoding='utf-8-sig')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
