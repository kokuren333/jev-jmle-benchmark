from __future__ import annotations
import argparse,json,re
from pathlib import Path
import pandas as pd
from common import RUNS,DATA,dump_json,load_jsonish

# Published MHLW thresholds. Formal pass/fail also depends on prohibited choices, whose identities are not public.
RULES={
 2018:{'exam':112,'req_cut':160,'req_max':200,'gen_cut':208,'gen_max':299,'contra_max':3},
 2019:{'exam':113,'req_cut':160,'req_max':200,'gen_cut':209,'gen_max':296,'contra_max':3},
 2020:{'exam':114,'req_cut':158,'req_max':197,'gen_cut':217,'gen_max':299,'contra_max':3},
 2021:{'exam':115,'req_cut':160,'req_max':200,'gen_cut':209,'gen_max':300,'contra_max':3},
 2022:{'exam':116,'req_cut':158,'req_max':197,'gen_cut':214,'gen_max':297,'contra_max':3},
 2023:{'exam':117,'req_cut':160,'req_max':200,'gen_cut':220,'gen_max':295,'contra_max':2},
 2024:{'exam':118,'req_cut':160,'req_max':200,'gen_cut':230,'gen_max':300,'contra_max':3},
 2025:{'exam':119,'req_cut':160,'req_max':200,'gen_cut':221,'gen_max':300,'contra_max':3},
 2026:{'exam':120,'req_cut':160,'req_max':200,'gen_cut':224,'gen_max':300,'contra_max':3},
}

def resolve(x): return RUNS/(RUNS/'LATEST').read_text().strip() if x=='latest' else RUNS/x
def read_items(run): return [json.loads(x) for x in (run/'items.jsonl').read_text(encoding='utf-8').splitlines() if x.strip() and json.loads(x).get('status')=='ok']
def points_for(block,number):
    block=str(block or '').upper(); number=int(number or 0)
    if block in ('B','E'): return ('required',1 if number<=25 else 3)
    if block in ('A','C','D','F'): return ('general_clinical',1)
    return ('unknown',0)
def parse_num(qid):
    m=re.search(r'([A-F])(\d+)$',str(qid)); return (m.group(1),int(m.group(2))) if m else (None,0)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--both',required=True,help='Merged both-derived run');ap.add_argument('--out',default='official_reconstruction');a=ap.parse_args()
    run=resolve(a.both); rs=read_items(run); pred={r['question_id']:r for r in rs}
    allq=json.loads((DATA/'jmedqa_all.json').read_text(encoding='utf-8'))
    rows=[]; detail=[]
    for year,rule in RULES.items():
        yr=[q for q in allq if int(q.get('year') or 0)==year]
        obs_req=obs_gen=0; miss_req=miss_gen=0; n_option=n_numeric=0
        for q in yr:
            qid=str(q.get('problem_unique_id') or q.get('id')); block=str(q.get('section') or '')
            _,num=parse_num(qid); bucket,pts=points_for(block,num)
            mode=str(q.get('answer_mode') or '').lower(); rec=pred.get(qid)
            if mode=='option':
                n_option+=1
                if rec is None: continue
                got=pts if rec.get('correct') else 0
                if bucket=='required': obs_req+=got
                elif bucket=='general_clinical': obs_gen+=got
                detail.append({'year':year,'exam':rule['exam'],'question_id':qid,'bucket':bucket,'points':pts,'evaluated':True,'correct':bool(rec.get('correct'))})
            else:
                n_numeric+=1
                if bucket=='required': miss_req+=pts
                elif bucket=='general_clinical': miss_gen+=pts
                detail.append({'year':year,'exam':rule['exam'],'question_id':qid,'bucket':bucket,'points':pts,'evaluated':False,'correct':None})
        # Published denominator reductions are treated conservatively because item-level adjudication may include exclusion/alternate-credit rules.
        req_adjust=max(0,200-rule['req_max']);gen_adjust=max(0,300-rule['gen_max'])
        req_lo=max(0,obs_req-req_adjust); req_hi=obs_req+miss_req
        gen_lo=max(0,obs_gen-gen_adjust); gen_hi=obs_gen+miss_gen
        req_status='PASS_GUARANTEED' if req_lo>=rule['req_cut'] else ('FAIL_GUARANTEED' if req_hi<rule['req_cut'] else 'INDETERMINATE')
        gen_status='PASS_GUARANTEED' if gen_lo>=rule['gen_cut'] else ('FAIL_GUARANTEED' if gen_hi<rule['gen_cut'] else 'INDETERMINATE')
        threshold='PASS_GUARANTEED' if req_status=='PASS_GUARANTEED' and gen_status=='PASS_GUARANTEED' else ('FAIL_GUARANTEED' if 'FAIL_GUARANTEED' in (req_status,gen_status) else 'INDETERMINATE')
        rows.append({'year':year,'exam':rule['exam'],'option_items_evaluated':n_option,'non_option_items_omitted':n_numeric,'required_observed_score':obs_req,'required_missing_possible_points':miss_req,'required_official_adjustment_points':req_adjust,'required_score_lower':req_lo,'required_score_upper':req_hi,'required_cut':rule['req_cut'],'required_official_max':rule['req_max'],'required_status':req_status,'general_observed_score':obs_gen,'general_missing_possible_points':miss_gen,'general_official_adjustment_points':gen_adjust,'general_score_lower':gen_lo,'general_score_upper':gen_hi,'general_cut':rule['gen_cut'],'general_official_max':rule['gen_max'],'general_status':gen_status,'published_score_threshold_status':threshold,'prohibited_choice_limit':rule['contra_max'],'formal_pass_status':'INDETERMINATE (prohibited-choice identities are not public)'})
    out=RUNS/a.out;out.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'official_reconstruction_by_year.csv',index=False,encoding='utf-8-sig');pd.DataFrame(detail).to_csv(out/'official_item_accounting.csv',index=False,encoding='utf-8-sig')
    dump_json(out/'official_reconstruction.json',rows)
    md=['# Official-style reconstruction by exam year','', 'This is a conservative reconstruction from Jev-evaluable option-choice items. Non-option items are represented as score intervals (all wrong to all correct). Published denominator reductions are also handled conservatively. Formal pass/fail is never asserted because prohibited-choice identities are not public.','', '| Year | Exam | Required score range / cut | General-clinical range / cut | Published score thresholds | Formal pass |','|---:|---:|---:|---:|---|---|']
    for r in rows: md.append(f"| {r['year']} | {r['exam']} | {r['required_score_lower']}–{r['required_score_upper']} / {r['required_cut']} | {r['general_score_lower']}–{r['general_score_upper']} / {r['general_cut']} | {r['published_score_threshold_status']} | INDETERMINATE |")
    (out/'OFFICIAL_RECONSTRUCTION.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(out)
if __name__=='__main__':main()
