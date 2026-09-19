from __future__ import annotations
import argparse,json
from pathlib import Path
import pandas as pd
from common import RUNS

def resolve(x): return RUNS/(RUNS/'LATEST').read_text().strip() if x=='latest' else RUNS/x

def main():
    ap=argparse.ArgumentParser();ap.add_argument('runs',nargs='+');ap.add_argument('--out',default='comparison.csv');a=ap.parse_args()
    rows=[]
    for rname in a.runs:
        run=resolve(rname); s=json.loads((run/'summary.json').read_text(encoding='utf-8')); m=json.loads((run/'manifest.json').read_text(encoding='utf-8'))
        rows.append({'run_id':m['run_id'],'dataset_mode':m['dataset_mode'],'image_mode':m['image_mode'],'years':','.join(map(str,m.get('years',[]))),'n':s['n_success'],'accuracy_exact_set':s['accuracy_exact_set'],'single_select_n':s['single_select_n'],'multi_select_n':s['multi_select_n'],'median_latency_ms':s['latency_ms'].get('p50'),'p95_latency_ms':s['latency_ms'].get('p95')})
    df=pd.DataFrame(rows);out=RUNS/a.out;df.to_csv(out,index=False,encoding='utf-8-sig');print(out);print(df.to_string(index=False))
if __name__=='__main__':main()
