from __future__ import annotations
import argparse, json, datetime as dt
from pathlib import Path
from common import RUNS, dump_json


def resolve(x:str)->Path:
    return RUNS/(RUNS/'LATEST').read_text().strip() if x=='latest' else RUNS/x

def read_items(run:Path):
    return [json.loads(x) for x in (run/'items.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser(description='Merge complementary no-image and image-only runs into a derived both run without new API calls.')
    ap.add_argument('no_image_run'); ap.add_argument('image_only_run')
    ap.add_argument('--name', default=None)
    a=ap.parse_args()
    r0,r1=resolve(a.no_image_run),resolve(a.image_only_run)
    m0=json.loads((r0/'manifest.json').read_text(encoding='utf-8')); m1=json.loads((r1/'manifest.json').read_text(encoding='utf-8'))
    if m0.get('dataset_mode')!='multi-year' or m1.get('dataset_mode')!='multi-year': raise SystemExit('Both inputs must be multi-year runs')
    if m0.get('image_mode')!='no-image' or m1.get('image_mode')!='image-only': raise SystemExit('Expected no-image then image-only runs')
    if m0.get('dataset_sha256')!=m1.get('dataset_sha256'): raise SystemExit('Dataset hashes differ')
    if m0.get('years')!=m1.get('years'): raise SystemExit('Year ranges differ')
    rows=read_items(r0)+read_items(r1)
    byid={}
    dup=[]
    for r in rows:
        qid=r.get('question_id')
        if qid in byid: dup.append(qid)
        byid[qid]=r
    if dup: raise SystemExit(f'Duplicate question IDs across runs: {dup[:10]}')
    rows=sorted(byid.values(), key=lambda r:(int(r.get('year') or 0), str(r.get('block') or ''), int(r.get('number') or 0)))
    stamp=a.name or dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_multi-year_both-derived'
    out=RUNS/stamp; out.mkdir(parents=True,exist_ok=False)
    with (out/'items.jsonl').open('w',encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    man={
        'run_id':stamp,'dataset_mode':'multi-year','image_mode':'both','derived':True,
        'source_runs':[m0['run_id'],m1['run_id']], 'years':m0.get('years'),
        'requested_model':m0.get('requested_model'), 'dataset_sha256':m0.get('dataset_sha256'),
        'protocol_sha256':m0.get('protocol_sha256'), 'concurrency':1,
        'n_eligible':len(rows), 'response_models':sorted(set(m0.get('response_models',[])+m1.get('response_models',[]))),
        'providers':sorted(set(m0.get('providers',[])+m1.get('providers',[]))),
        'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'derivation':'Union of completed no-image and image-only runs; no additional Jev requests.'
    }
    dump_json(out/'manifest.json',man); dump_json(out/'excluded.json',[])
    (RUNS/'LATEST').write_text(stamp,encoding='utf-8')
    print(out)
if __name__=='__main__': main()
