from __future__ import annotations
import json,collections
from common import DATA,parse_choices,load_jsonish,has_image_reference

def main():
    out={}
    jpath=DATA/'jmedqa_all.json'
    if jpath.exists():
        rows=json.loads(jpath.read_text(encoding='utf-8'));s=collections.Counter();bad=[]
        for q in rows:
            s['total']+=1;s['answer_mode:'+str(q.get('answer_mode'))]+=1;s['year:'+str(q.get('year'))]+=1
            s['image_ref:'+str(has_image_reference(q))]+=1;s['image_dependency:'+str(q.get('image_dependency'))]+=1
            if str(q.get('answer_mode')).lower()=='option':
                opts=load_jsonish(q.get('options_json'),{});ans=load_jsonish(q.get('answer_json'),[])
                s['nchoices:'+str(len(opts))]+=1;s['select:'+str(q.get('answer_count') or len(ans))]+=1
                if not opts or not ans:bad.append(q.get('problem_unique_id'))
        out['jmedqa']={'stats':dict(s),'bad_option_rows':bad[:50],'n_bad':len(bad)}
    p=DATA/'jmle2026_dataset.json'
    if p.exists():
        rows=json.loads(p.read_text(encoding='utf-8'));s=collections.Counter();bad=[]
        for q in rows:
            s['total']+=1;s['image:'+str(bool(q.get('requires_image')))]+=1;s['type:'+str(q.get('question_type'))]+=1
            if q.get('question_type')=='multiple_choice':
                _,opts=parse_choices(q.get('question_text',''));s['nchoices:'+str(len(opts) if opts else 0)]+=1;s['select:'+str(q.get('num_choices_to_select'))]+=1
                if not opts:bad.append(q.get('question_id'))
        out['jmle2026']={'stats':dict(s),'bad_choice_rows':bad[:50],'n_bad':len(bad)}
        if len(rows)!=400: raise SystemExit('Expected 400 JMLE2026 rows')
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
