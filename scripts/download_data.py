from __future__ import annotations
import json, requests
from common import DATA, dump_json, sha256_file

JMLE_URL='https://raw.githubusercontent.com/naoto-iwase/JMLE2026-Bench/main/jmle2026_dataset.json'

def main():
    meta={}
    out=DATA/'jmle2026_dataset.json'
    r=requests.get(JMLE_URL,timeout=60); r.raise_for_status(); out.write_bytes(r.content)
    meta.update({'jmle_url':JMLE_URL,'jmle_sha256':sha256_file(out)})

    from datasets import load_dataset
    ds=load_dataset('SIP-med-LLM/JMedQA',split='benchmark')
    rows=[dict(x) for x in ds]
    j=DATA/'jmedqa_all.json'
    j.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    meta.update({'jmedqa_rows':len(rows),'jmedqa_years':sorted({int(x['year']) for x in rows if x.get('year')}),'jmedqa_sha256':sha256_file(j)})
    dump_json(DATA/'provenance.json',meta)
    print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
