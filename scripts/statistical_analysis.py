from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import chi2_contingency, mannwhitneyu, fisher_exact, spearmanr
from common import RUNS, dump_json

SEED=20260919

def resolve(x): return RUNS/(RUNS/'LATEST').read_text().strip() if x=='latest' else RUNS/x

def items(run): return [json.loads(x) for x in (run/'items.jsonl').read_text(encoding='utf-8').splitlines() if x.strip() and json.loads(x).get('status')=='ok']
def wilson(k,n,z=1.95996398454):
    if n==0:return [None,None]
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [c-h,c+h]
def prop_diff_ci(k1,n1,k0,n0,z=1.95996398454):
    p1,p0=k1/n1,k0/n0; d=p1-p0; se=math.sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0); return [d-z*se,d+z*se]
def effect(k1,n1,k0,n0):
    p1,p0=k1/n1,k0/n0
    table=np.array([[k1,n1-k1],[k0,n0-k0]])
    _,pchi,_,_=chi2_contingency(table,correction=False)
    # Haldane-Anscombe only if needed
    a,b,c,d=map(float,[k1,n1-k1,k0,n0-k0])
    if min(a,b,c,d)==0:a+=.5;b+=.5;c+=.5;d+=.5
    orr=(a*d)/(b*c); seor=math.sqrt(1/a+1/b+1/c+1/d); or_ci=[math.exp(math.log(orr)-1.96*seor),math.exp(math.log(orr)+1.96*seor)]
    rr=p1/p0 if p0 else math.inf; serr=math.sqrt(max(0,1/k1-1/n1+1/k0-1/n0)) if k1 and k0 else math.inf
    rr_ci=[math.exp(math.log(rr)-1.96*serr),math.exp(math.log(rr)+1.96*serr)] if math.isfinite(rr) and math.isfinite(serr) else [None,None]
    h=2*(math.asin(math.sqrt(p1))-math.asin(math.sqrt(p0)))
    return {'risk1':p1,'risk0':p0,'difference_pp':100*(p1-p0),'difference_95ci_pp':[100*x for x in prop_diff_ci(k1,n1,k0,n0)],'risk_ratio':rr,'risk_ratio_95ci':rr_ci,'odds_ratio':orr,'odds_ratio_95ci':or_ci,'cohen_h':h,'chi_square_p':pchi}
def per_item_metrics(rs):
    out=[]
    for r in rs:
        probs=r.get('probabilities') or {}; gold=r.get('gold') or []
        conf=max(probs.values()) if probs else np.nan
        nll=np.nan; brier=np.nan
        if r.get('select_k')==1 and probs and gold:
            g=gold[0]; pg=max(float(probs.get(g,1e-15)),1e-15); nll=-math.log(pg); brier=sum((float(v)-(1.0 if k==g else 0.0))**2 for k,v in probs.items())
        out.append({'question_id':r.get('question_id'),'year':r.get('year'),'correct':int(bool(r.get('correct'))),'latency_ms':float(r.get('latency_ms')),'confidence':conf,'nll':nll,'brier':brier,'select_k':r.get('select_k'),'image_dependency':r.get('image_dependency'),'clinical_area':r.get('clinical_area')})
    return pd.DataFrame(out)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--no-image',required=True);ap.add_argument('--image-only',required=True);ap.add_argument('--both',default=None);ap.add_argument('--out',default='statistical_analysis');a=ap.parse_args()
    r0,r1=resolve(a.no_image),resolve(a.image_only); d0,d1=per_item_metrics(items(r0)),per_item_metrics(items(r1))
    out=RUNS/a.out;out.mkdir(exist_ok=True)
    k0,n0=int(d0.correct.sum()),len(d0);k1,n1=int(d1.correct.sum()),len(d1)
    result={'no_image':{'n':n0,'correct':k0,'accuracy':k0/n0,'wilson95':wilson(k0,n0)},'image_only':{'n':n1,'correct':k1,'accuracy':k1/n1,'wilson95':wilson(k1,n1)},'image_minus_no_image':effect(k1,n1,k0,n0)}
    u,p=mannwhitneyu(d1.latency_ms,d0.latency_ms,alternative='two-sided');result['latency_mann_whitney']={'U':float(u),'p':float(p),'median_no_image_ms':float(d0.latency_ms.median()),'median_image_ms':float(d1.latency_ms.median())}
    # image dependency vs no-image baseline
    deps=[]
    for dep,g in d1.groupby('image_dependency',dropna=False):
        kk,nn=int(g.correct.sum()),len(g); e=effect(kk,nn,k0,n0);deps.append({'image_dependency':str(dep),'n':nn,'correct':kk,'accuracy':kk/nn,'wilson_low':wilson(kk,nn)[0],'wilson_high':wilson(kk,nn)[1],**e})
    pd.DataFrame(deps).to_csv(out/'image_dependency_vs_no_image.csv',index=False,encoding='utf-8-sig')
    # year tables and heterogeneity/trend on aggregate accuracy
    years=[]
    for label,df in [('no-image',d0),('image-only',d1),('both',pd.concat([d0,d1],ignore_index=True))]:
        for y,g in df.groupby('year'):
            kk,nn=int(g.correct.sum()),len(g);ci=wilson(kk,nn);years.append({'condition':label,'year':int(y),'n':nn,'correct':kk,'accuracy':kk/nn,'wilson_low':ci[0],'wilson_high':ci[1],'median_latency_ms':float(g.latency_ms.median())})
    yd=pd.DataFrame(years);yd.to_csv(out/'yearly_accuracy.csv',index=False,encoding='utf-8-sig')
    for label,g in yd.groupby('condition'):
        rho,pv=spearmanr(g.year,g.accuracy);result[f'year_trend_{label}']={'spearman_rho':float(rho),'p':float(pv)}
    # select-k table
    bothdf=pd.concat([d0.assign(condition='no-image'),d1.assign(condition='image-only')],ignore_index=True)
    agg=bothdf.groupby(['condition','select_k'],dropna=False).agg(n=('correct','size'),correct=('correct','sum'),accuracy=('correct','mean'),median_latency_ms=('latency_ms','median')).reset_index();agg.to_csv(out/'select_k_analysis.csv',index=False,encoding='utf-8-sig')
    # domain table
    dom=bothdf.groupby(['condition','clinical_area'],dropna=False).agg(n=('correct','size'),correct=('correct','sum'),accuracy=('correct','mean'),median_latency_ms=('latency_ms','median')).reset_index();dom.to_csv(out/'domain_analysis.csv',index=False,encoding='utf-8-sig')
    dump_json(out/'statistical_summary.json',result)
    lines=['# Statistical analysis','',f'- No-image: {k0}/{n0} = {k0/n0:.2%}',f'- Image-referenced, image-withheld: {k1}/{n1} = {k1/n1:.2%}',f'- Difference (image − no-image): {result["image_minus_no_image"]["difference_pp"]:.2f} percentage points (95% CI {result["image_minus_no_image"]["difference_95ci_pp"][0]:.2f} to {result["image_minus_no_image"]["difference_95ci_pp"][1]:.2f})',f'- Risk ratio: {result["image_minus_no_image"]["risk_ratio"]:.3f}',f'- Odds ratio: {result["image_minus_no_image"]["odds_ratio"]:.3f}',f'- Chi-square p: {result["image_minus_no_image"]["chi_square_p"]:.3g}',f'- Latency Mann–Whitney p: {p:.3g}','','See CSV files for year, domain, image-dependency, and top-k stratification.','', 'Caution: no-image and image-referenced questions are different item sets, so the unadjusted contrast is associative rather than a randomized causal effect.']
    (out/'STATISTICAL_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(out)
if __name__=='__main__':main()
