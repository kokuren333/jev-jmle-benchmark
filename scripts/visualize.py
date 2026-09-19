
from __future__ import annotations
import argparse, json, math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import RUNS


def resolve(x: str) -> Path:
    return RUNS / (RUNS / 'LATEST').read_text().strip() if x == 'latest' else RUNS / x


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def load_csv_if_exists(path: Path) -> pd.DataFrame | None:
    return pd.read_csv(path) if path.exists() else None


def save_bar(df: pd.DataFrame, xcol: str, ycol: str, out: Path, title: str, xlabel: str = '', ylabel: str = ''):
    if df is None or df.empty or xcol not in df.columns or ycol not in df.columns:
        return
    plt.figure(figsize=(8, 4.8))
    xs = [str(x) for x in df[xcol].tolist()]
    ys = df[ycol].astype(float).tolist()
    pos = np.arange(len(xs))
    plt.bar(pos, ys)
    plt.xticks(pos, xs, rotation=45, ha='right')
    plt.title(title)
    plt.xlabel(xlabel or xcol)
    plt.ylabel(ylabel or ycol)
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()


def save_dual_bar(df: pd.DataFrame, xcol: str, ycol1: str, ycol2: str, out: Path, title: str, y1label: str, y2label: str):
    if df is None or df.empty or any(c not in df.columns for c in [xcol, ycol1, ycol2]):
        return
    xs = [str(x) for x in df[xcol].tolist()]
    a = df[ycol1].astype(float).to_numpy()
    b = df[ycol2].astype(float).to_numpy()
    pos = np.arange(len(xs))
    width = 0.38
    fig, ax1 = plt.subplots(figsize=(9, 4.8))
    ax1.bar(pos - width / 2, a, width=width)
    ax1.set_ylabel(y1label)
    ax1.set_xlabel(xcol)
    ax1.set_xticks(pos)
    ax1.set_xticklabels(xs, rotation=45, ha='right')
    ax1.set_title(title)
    ax2 = ax1.twinx()
    ax2.plot(pos + width / 2, b, marker='o')
    ax2.set_ylabel(y2label)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def reliability_bins(rows: list[dict], n_bins: int = 10):
    confs, corrs = [], []
    for r in rows:
        if r.get('status') != 'ok':
            continue
        probs = r.get('probabilities') or {}
        if not probs:
            continue
        confs.append(max(float(p) for p in probs.values()))
        corrs.append(1.0 if r.get('correct') else 0.0)
    if not confs:
        return pd.DataFrame(columns=['bin_left', 'bin_right', 'mean_confidence', 'accuracy', 'n'])
    confs = np.array(confs, dtype=float)
    corrs = np.array(corrs, dtype=float)
    bins = np.linspace(0, 1, n_bins + 1)
    out = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        if hi < 1:
            m = (confs >= lo) & (confs < hi)
        else:
            m = (confs >= lo) & (confs <= hi)
        if m.any():
            out.append({
                'bin_left': float(lo),
                'bin_right': float(hi),
                'mean_confidence': float(confs[m].mean()),
                'accuracy': float(corrs[m].mean()),
                'n': int(m.sum()),
            })
    return pd.DataFrame(out)


def confidence_correctness(rows: list[dict]):
    correct, incorrect = [], []
    for r in rows:
        if r.get('status') != 'ok':
            continue
        probs = r.get('probabilities') or {}
        if not probs:
            continue
        c = max(float(p) for p in probs.values())
        (correct if r.get('correct') else incorrect).append(c)
    return np.array(correct, dtype=float), np.array(incorrect, dtype=float)


def visualize_run(run_name: str):
    run = resolve(run_name)
    figures = run / 'figures'
    figures.mkdir(exist_ok=True)

    summary = load_json(run / 'summary.json')
    manifest = load_json(run / 'manifest.json')
    rows = [json.loads(x) for x in (run / 'items.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]

    by_year = load_csv_if_exists(run / 'by_year.csv')
    by_block = load_csv_if_exists(run / 'by_block.csv')
    by_domain = load_csv_if_exists(run / 'by_domain.csv')
    by_img_dep = load_csv_if_exists(run / 'by_image_dependency.csv')
    by_img_pres = load_csv_if_exists(run / 'by_image_presence.csv')
    by_select_k = load_csv_if_exists(run / 'by_select_k.csv')
    by_calc = load_csv_if_exists(run / 'by_calc.csv')

    # Accuracy views
    if by_year is not None and not by_year.empty:
        by_year = by_year.sort_values('year')
        save_bar(by_year, 'year', 'accuracy', figures / 'accuracy_by_year.png', 'Accuracy by year', 'Year', 'Exact-set accuracy')
        save_dual_bar(by_year, 'year', 'accuracy', 'median_latency_ms', figures / 'accuracy_latency_by_year.png', 'Accuracy and median latency by year', 'Exact-set accuracy', 'Median latency (ms)')

    if by_block is not None and not by_block.empty:
        save_bar(by_block, 'block', 'accuracy', figures / 'accuracy_by_block.png', 'Accuracy by block', 'Block', 'Exact-set accuracy')

    if by_domain is not None and not by_domain.empty:
        order = by_domain.sort_values(['n', 'clinical_area'], ascending=[False, True]).head(15)
        save_bar(order, 'clinical_area', 'accuracy', figures / 'accuracy_by_domain_top15.png', 'Accuracy by clinical area (top 15 by n)', 'Clinical area', 'Exact-set accuracy')

    if by_img_dep is not None and not by_img_dep.empty:
        save_bar(by_img_dep, 'image_dependency', 'accuracy', figures / 'accuracy_by_image_dependency.png', 'Accuracy by image dependency', 'Image dependency', 'Exact-set accuracy')

    if by_img_pres is not None and not by_img_pres.empty:
        by_img_pres['has_image_reference'] = by_img_pres['has_image_reference'].map(lambda x: 'image-ref' if str(x).lower() == 'true' else 'no-image-ref')
        save_bar(by_img_pres, 'has_image_reference', 'accuracy', figures / 'accuracy_by_image_presence.png', 'Accuracy by image presence', 'Image reference', 'Exact-set accuracy')
        save_bar(by_img_pres, 'has_image_reference', 'median_latency_ms', figures / 'latency_by_image_presence.png', 'Median latency by image presence', 'Image reference', 'Median latency (ms)')

    if by_select_k is not None and not by_select_k.empty:
        by_select_k = by_select_k.sort_values('select_k')
        save_bar(by_select_k, 'select_k', 'accuracy', figures / 'accuracy_by_select_k.png', 'Accuracy by number of required answers (k)', 'k', 'Exact-set accuracy')

    if by_calc is not None and not by_calc.empty:
        by_calc['is_calc'] = by_calc['is_calc'].map(lambda x: 'calc' if str(x).lower() == 'true' else 'non-calc')
        save_bar(by_calc, 'is_calc', 'accuracy', figures / 'accuracy_by_calc.png', 'Accuracy by calculation flag', 'Question type', 'Exact-set accuracy')

    # Latency distribution
    latencies = [float(r['latency_ms']) for r in rows if r.get('status') == 'ok' and r.get('latency_ms') is not None]
    if latencies:
        plt.figure(figsize=(7, 4.5))
        plt.hist(latencies, bins=30)
        plt.xlabel('Wall-clock latency (ms)')
        plt.ylabel('Items')
        plt.title('Latency distribution')
        plt.tight_layout()
        plt.savefig(figures / 'latency_histogram.png', dpi=180)
        plt.close()

    # Calibration / confidence
    calib = reliability_bins(rows, n_bins=10)
    if not calib.empty:
        plt.figure(figsize=(5.5, 5.5))
        plt.plot([0, 1], [0, 1], linestyle='--')
        plt.plot(calib['mean_confidence'], calib['accuracy'], marker='o')
        for _, row in calib.iterrows():
            plt.annotate(str(int(row['n'])), (row['mean_confidence'], row['accuracy']))
        plt.xlabel('Mean confidence in bin')
        plt.ylabel('Observed accuracy')
        plt.title('Reliability diagram (top-1 confidence)')
        plt.tight_layout()
        plt.savefig(figures / 'reliability_diagram.png', dpi=180)
        plt.close()
        calib.to_csv(figures / 'reliability_bins.csv', index=False, encoding='utf-8-sig')

    c_ok, c_ng = confidence_correctness(rows)
    if len(c_ok) or len(c_ng):
        plt.figure(figsize=(7, 4.5))
        bins = np.linspace(0, 1, 21)
        if len(c_ok):
            plt.hist(c_ok, bins=bins, alpha=0.7, label='Correct')
        if len(c_ng):
            plt.hist(c_ng, bins=bins, alpha=0.7, label='Incorrect')
        plt.xlabel('Top-1 confidence')
        plt.ylabel('Items')
        plt.title('Confidence distribution by correctness')
        plt.legend()
        plt.tight_layout()
        plt.savefig(figures / 'confidence_by_correctness.png', dpi=180)
        plt.close()

    # Figure index markdown
    lines = [
        '# Visualization index',
        '',
        f'- Run ID: `{manifest.get("run_id")}`',
        f'- Dataset mode: `{manifest.get("dataset_mode")}`',
        f'- Image mode: `{manifest.get("image_mode")}`',
        '',
        'Generated figures are stored in this directory.',
        '',
        '## Summary',
        '',
        f'- Exact-set accuracy: {summary.get("accuracy_exact_set"):.3%}' if summary.get('accuracy_exact_set') is not None else '- Exact-set accuracy: n/a',
        f'- Median latency: {summary.get("latency_ms", {}).get("p50", float("nan")):.1f} ms',
        f'- p95 latency: {summary.get("latency_ms", {}).get("p95", float("nan")):.1f} ms',
        '',
        '## Files',
        '',
    ]
    for p in sorted(figures.iterdir()):
        lines.append(f'- `{p.name}`')
    (figures / 'INDEX.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(figures)


def visualize_compare(run_names: list[str], labels: list[str] | None, out_name: str):
    rows = []
    for i, run_name in enumerate(run_names):
        run = resolve(run_name)
        summary = load_json(run / 'summary.json')
        manifest = load_json(run / 'manifest.json')
        label = labels[i] if labels and i < len(labels) else manifest.get('image_mode', run_name)
        rows.append({
            'label': label,
            'run_id': manifest.get('run_id'),
            'dataset_mode': manifest.get('dataset_mode'),
            'image_mode': manifest.get('image_mode'),
            'n_success': summary.get('n_success'),
            'accuracy_exact_set': summary.get('accuracy_exact_set'),
            'median_latency_ms': summary.get('latency_ms', {}).get('p50'),
            'p95_latency_ms': summary.get('latency_ms', {}).get('p95'),
            'single_select_nll': summary.get('single_select_nll'),
            'ece': summary.get('top1_confidence_ece_10bin_exploratory'),
        })
    df = pd.DataFrame(rows)
    out_dir = RUNS / out_name
    out_dir.mkdir(exist_ok=True)
    df.to_csv(out_dir / 'comparison_summary.csv', index=False, encoding='utf-8-sig')

    # Accuracy comparison
    xs = np.arange(len(df))
    labels_plot = df['label'].astype(str).tolist()
    plt.figure(figsize=(7, 4.5))
    plt.bar(xs, df['accuracy_exact_set'].astype(float).tolist())
    plt.xticks(xs, labels_plot, rotation=20, ha='right')
    plt.ylabel('Exact-set accuracy')
    plt.title('Accuracy comparison across runs')
    plt.tight_layout()
    plt.savefig(out_dir / 'compare_accuracy.png', dpi=180)
    plt.close()

    # Latency comparison
    plt.figure(figsize=(7, 4.5))
    plt.bar(xs, df['median_latency_ms'].astype(float).tolist())
    plt.xticks(xs, labels_plot, rotation=20, ha='right')
    plt.ylabel('Median latency (ms)')
    plt.title('Median latency comparison across runs')
    plt.tight_layout()
    plt.savefig(out_dir / 'compare_median_latency.png', dpi=180)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.bar(xs, df['p95_latency_ms'].astype(float).tolist())
    plt.xticks(xs, labels_plot, rotation=20, ha='right')
    plt.ylabel('p95 latency (ms)')
    plt.title('p95 latency comparison across runs')
    plt.tight_layout()
    plt.savefig(out_dir / 'compare_p95_latency.png', dpi=180)
    plt.close()

    if df['ece'].notna().any():
        plt.figure(figsize=(7, 4.5))
        plt.bar(xs, df['ece'].fillna(0).astype(float).tolist())
        plt.xticks(xs, labels_plot, rotation=20, ha='right')
        plt.ylabel('ECE (10-bin, exploratory)')
        plt.title('Calibration comparison across runs')
        plt.tight_layout()
        plt.savefig(out_dir / 'compare_ece.png', dpi=180)
        plt.close()

    (out_dir / 'INDEX.md').write_text(
        '# Comparison visualizations\n\n' + '\n'.join(f'- `{p.name}`' for p in sorted(out_dir.iterdir()) if p.name != 'INDEX.md') + '\n',
        encoding='utf-8'
    )
    print(out_dir)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    p1 = sub.add_parser('run', help='Generate figures for a single run')
    p1.add_argument('--run', default='latest')

    p2 = sub.add_parser('compare', help='Generate comparison figures across multiple runs')
    p2.add_argument('runs', nargs='+')
    p2.add_argument('--labels', nargs='*', default=None)
    p2.add_argument('--out', default='comparison_figures')

    a = ap.parse_args()
    if a.cmd == 'run':
        visualize_run(a.run)
    else:
        visualize_compare(a.runs, a.labels, a.out)


if __name__ == '__main__':
    main()
