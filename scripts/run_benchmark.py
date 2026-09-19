from __future__ import annotations
import argparse, datetime as dt, json, os, platform, random, time, re
from pathlib import Path
import requests
from common import DATA,RUNS,parse_choices,norm_answer,topk_from_probs,dump_json,sha256_file,load_jsonish,has_image_reference

ENDPOINT='https://openrouter.ai/api/alpha/decisions'
MODEL='typesafe/jev-1.13'

def request_jev(key,state,criteria,max_retries=3):
    payload={'model':MODEL,'state':state,'questions':{'answer':{'type':'choice','instructions':'Choose the medically correct option. For questions requiring multiple answers, assess every original option independently; the benchmark will select the top-k options from the returned probability distribution.','criteria':criteria}}}
    headers={'Authorization':f'Bearer {key}','Content-Type':'application/json','X-OpenRouter-Title':'Jev JMedQA Benchmark'}
    attempts=[]; total0=time.perf_counter_ns()
    for i in range(max_retries):
        t0=time.perf_counter_ns()
        try:
            r=requests.post(ENDPOINT,headers=headers,json=payload,timeout=120)
            ms=(time.perf_counter_ns()-t0)/1e6
            attempts.append({'attempt':i+1,'status':r.status_code,'latency_ms':ms})
            if r.ok:
                return r.json(), attempts, (time.perf_counter_ns()-total0)/1e6, payload
            if r.status_code not in (429,500,502,503,504): r.raise_for_status()
        except requests.RequestException as e:
            attempts.append({'attempt':i+1,'error':repr(e),'latency_ms':(time.perf_counter_ns()-t0)/1e6})
        if i+1<max_retries: time.sleep(2**i + random.random()*0.2)
    raise RuntimeError(f'API failed after {max_retries} attempts: {attempts}')

def image_ok(row, mode):
    has=has_image_reference(row)
    return {'no-image':not has,'image-only':has,'both':True}[mode]

def load_multiyear(years,image_mode):
    src=DATA/'jmedqa_all.json'; rows=json.loads(src.read_text(encoding='utf-8'))
    eligible=[]; excluded=[]
    for q in rows:
        qid=str(q.get('problem_unique_id') or q.get('id'))
        year=int(q.get('year') or 0)
        if years and year not in years: continue
        # Only non-option/numeric-answer items are excluded. Calculation MCQs remain eligible.
        if str(q.get('answer_mode')).lower()!='option':
            excluded.append({'id':qid,'reason':'non_option_answer_mode'}); continue
        opts={str(k).lower():str(v) for k,v in load_jsonish(q.get('options_json'),{}).items()}
        gold=norm_answer(load_jsonish(q.get('answer_json'),[]))
        if not opts or not gold:
            excluded.append({'id':qid,'reason':'missing_options_or_gold'}); continue
        if not image_ok(q,image_mode): continue
        k=int(q.get('answer_count') or len(gold) or 1)
        if k<1 or k>len(opts):
            excluded.append({'id':qid,'reason':'invalid_answer_count'}); continue
        eligible.append({'question_id':qid,'year':year,'block':q.get('section'),'number':int(re.sub(r'\D','',qid[-3:]) or 0),'question':q.get('question') or '', 'question_raw':q.get('question_raw') or q.get('question') or '', 'options':opts,'gold':gold,'select_k':k,'clinical_area':q.get('clinical_area'),'image_dependency':q.get('image_dependency'),'has_image_reference':has_image_reference(q),'is_calc':bool(q.get('is_calc')),'is_linked':bool(q.get('is_linked')),'is_case_based':bool(q.get('is_case_based')),'has_unpublished_image':bool(q.get('has_unpublished_image'))})
    return src,eligible,excluded

def load_official120(image_mode):
    src=DATA/'jmle2026_dataset.json'; rows=json.loads(src.read_text(encoding='utf-8'))
    # metadata from JMedQA 2026
    meta={}
    jp=DATA/'jmedqa_all.json'
    if jp.exists():
        for x in json.loads(jp.read_text(encoding='utf-8')):
            if int(x.get('year') or 0)==2026:
                pu=str(x.get('problem_unique_id','')); m=re.match(r'2026([A-F])(\d+)$',pu)
                if m: meta[f'120{m.group(1)}-{int(m.group(2))}']=x
    eligible=[];excluded=[]
    for q in rows:
        qid=q.get('question_id'); mrow=meta.get(qid,{})
        if q.get('question_type')!='multiple_choice':
            excluded.append({'id':qid,'reason':'non_option_answer_mode'}); continue
        stem,opts=parse_choices(q.get('question_text',''))
        if not opts:
            excluded.append({'id':qid,'reason':'choice_parse_error'}); continue
        gold=norm_answer(q.get('answer',[])); k=int(q.get('num_choices_to_select') or len(gold) or 1)
        hasimg=bool(q.get('requires_image')) or has_image_reference(mrow)
        if image_mode=='no-image' and hasimg: continue
        if image_mode=='image-only' and not hasimg: continue
        eligible.append({'question_id':qid,'year':2026,'block':q.get('block'),'number':int(q.get('number')),'question':stem,'question_raw':stem,'options':opts,'gold':gold,'select_k':k,'clinical_area':mrow.get('clinical_area'),'image_dependency':mrow.get('image_dependency') or ('image_reference' if hasimg else 'none'),'has_image_reference':hasimg,'is_calc':bool(mrow.get('is_calc')),'is_linked':bool(mrow.get('is_linked')),'is_case_based':bool(mrow.get('is_case_based')),'has_unpublished_image':bool(mrow.get('has_unpublished_image'))})
    return src,eligible,excluded

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset',choices=['multi-year','official120'],default='multi-year')
    ap.add_argument('--image-mode',choices=['no-image','image-only','both'],default='both')
    ap.add_argument('--years',default='2018-2026',help='e.g. 2018-2026 or 2024,2025,2026; ignored for official120')
    ap.add_argument('--limit',type=int)
    args=ap.parse_args()
    key=os.getenv('OPENROUTER_API_KEY')
    if not key: raise SystemExit('Set OPENROUTER_API_KEY')
    years=set()
    if args.dataset=='multi-year':
        for part in args.years.split(','):
            part=part.strip()
            if '-' in part:
                a,b=map(int,part.split('-',1)); years.update(range(a,b+1))
            elif part: years.add(int(part))
        src,eligible,excluded=load_multiyear(years,args.image_mode)
    else:
        src,eligible,excluded=load_official120(args.image_mode)
    if args.limit: eligible=eligible[:args.limit]
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+args.dataset+'_'+args.image_mode
    run=RUNS/stamp; (run/'raw').mkdir(parents=True)
    manifest={'run_id':stamp,'dataset_mode':args.dataset,'image_mode':args.image_mode,'years':sorted(years) if years else [2026],'endpoint':ENDPOINT,'requested_model':MODEL,'dataset_sha256':sha256_file(src),'protocol_sha256':sha256_file(Path(__file__).resolve().parents[1]/'PROTOCOL.md'),'started_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'python':platform.python_version(),'platform':platform.platform(),'concurrency':1,'multi_select_rule':'top-k over original-option probabilities; k=gold answer_count / exam metadata','image_input':'never supplied to Jev; image-only means image-referenced questions evaluated under image-withheld text-only condition'}
    dump_json(run/'manifest.json',manifest); dump_json(run/'excluded.json',excluded)
    out=(run/'items.jsonl').open('w',encoding='utf-8'); builds=set();providers=set()
    for idx,q in enumerate(eligible,1):
        # Original options are always the decision choices, including multi-select items.
        criteria=q['options']
        state={'question_id':q['question_id'],'question':q['question'],'original_options':q['options'],'select_exactly':q['select_k'],'image_condition':'withheld' if q['has_image_reference'] else 'not_present'}
        rec={k:q.get(k) for k in ['question_id','year','block','number','clinical_area','image_dependency','has_image_reference','is_calc','is_linked','is_case_based','has_unpublished_image','select_k']}
        rec.update({'n_original_choices':len(q['options']),'gold':list(q['gold'])})
        try:
            data,attempts,total_ms,payload=request_jev(key,state,criteria)
            ans=data['answers']['answer']; probs={str(k).lower():float(v) for k,v in (ans.get('probabilities') or {}).items()}
            pred=topk_from_probs(probs,q['select_k'])
            rec.update({'api_top1_choice':str(ans.get('choice','')).lower(),'prediction':list(pred),'correct':pred==q['gold'],'probabilities':probs,'latency_ms':attempts[-1]['latency_ms'],'elapsed_total_ms':total_ms,'attempts':attempts,'response_model':data.get('model'),'provider':data.get('provider'),'usage':data.get('usage'),'status':'ok'})
            builds.add(str(data.get('model')));providers.add(str(data.get('provider')));dump_json(run/'raw'/f"{q['question_id']}.json",data)
        except Exception as e: rec.update({'status':'error','error':repr(e)})
        out.write(json.dumps(rec,ensure_ascii=False)+'\n');out.flush();print(f'[{idx}/{len(eligible)}] {q["question_id"]} {rec["status"]}')
    out.close();manifest.update({'finished_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'n_eligible':len(eligible),'n_excluded':len(excluded),'response_models':sorted(builds),'providers':sorted(providers)});dump_json(run/'manifest.json',manifest)
    (RUNS/'LATEST').write_text(stamp,encoding='utf-8');print(run)
if __name__=='__main__':main()
