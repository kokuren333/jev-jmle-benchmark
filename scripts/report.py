from __future__ import annotations
import argparse,json
import numpy as np, matplotlib.pyplot as plt
from common import RUNS

def resolve(x): return RUNS/(RUNS/'LATEST').read_text().strip() if x=='latest' else RUNS/x

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',default='latest');a=ap.parse_args();run=resolve(a.run)
    s=json.loads((run/'summary.json').read_text(encoding='utf-8'));m=json.loads((run/'manifest.json').read_text(encoding='utf-8'))
    rows=[json.loads(x) for x in (run/'items.jsonl').read_text(encoding='utf-8').splitlines() if x.strip() and json.loads(x).get('status')=='ok']
    l=[r['latency_ms'] for r in rows]
    if l:
        plt.figure(figsize=(7,4));plt.hist(l,bins=30);plt.xlabel('Wall-clock latency (ms)');plt.ylabel('Items');plt.tight_layout();plt.savefig(run/'latency_hist.png',dpi=180);plt.close()
    ci=s['accuracy_wilson95']; acc=s['accuracy_exact_set']
    lines=[f'# Jev medical licensing benchmark report','',f'- Run: `{m["run_id"]}`',f'- Dataset mode: `{m["dataset_mode"]}`',f'- Image mode: `{m["image_mode"]}`',f'- Requested model: `{m["requested_model"]}`',f'- Response model(s): `{", ".join(m.get("response_models",[]))}`',f'- Dataset SHA-256: `{m["dataset_sha256"]}`',f'- Protocol SHA-256: `{m["protocol_sha256"]}`','', '## Results','',f'- Exact-set accuracy: **{acc:.3%}** ({s["n_correct_exact_set"]}/{s["n_success"]}); Wilson 95% CI {ci[0]:.3%}–{ci[1]:.3%}',f'- Single-select items: {s["single_select_n"]}',f'- Multi-select items (top-k): {s["multi_select_n"]}',f'- Median latency: **{s["latency_ms"].get("p50",float("nan")):.1f} ms**',f'- p95 latency: **{s["latency_ms"].get("p95",float("nan")):.1f} ms**','']
    if s.get('single_select_nll') is not None: lines += [f'- Single-select NLL: {s["single_select_nll"]:.4f}',f'- Single-select multiclass Brier: {s["single_select_multiclass_brier"]:.4f}']
    lines += ['', '## Interpretation', '', 'For multi-select questions, the model is given the original options once. The benchmark ranks the returned per-option probabilities and selects exactly k options (top-k), where k is the required answer count. Correctness requires exact set match.', '', 'For image-referenced questions, Jev receives no image. `image-only` therefore means an image-referenced, image-withheld text-only condition, not multimodal performance. Results are additionally stratified by JMedQA image_dependency.']
    if s.get('official_style'):
        o=s['official_style'];lines += ['', '## 120th official-style scoring','',f'- Required: {o["required_score"]}/{o["required_max"]}',f'- General/clinical: {o["general_clinical_score"]}/{o["general_clinical_max"]}',f'- Published score thresholds pass: {o["published_thresholds_pass"]}',f'- Official pass status: **{o["official_pass_status"]}**','','Formal pass/fail cannot be established because prohibited-choice identities are not public.']
    (run/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(run/'report.md')
if __name__=='__main__':main()
