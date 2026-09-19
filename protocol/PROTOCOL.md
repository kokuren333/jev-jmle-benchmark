# Protocol: Jev on Japanese Medical Licensing Examination Questions

## Objective
Evaluate Jev's option-selection performance, latency, probability calibration (where statistically appropriate), and robustness across medical domains, years, image dependence, and answer multiplicity.

## Datasets
- Multi-year: JMedQA benchmark split, 2018–2026.
- 120th reconstruction: JMLE2026-Bench, with JMedQA metadata joined where available.

## Inclusion / exclusion
Include every item whose ground-truth answer mode is selection from explicit options. Do **not** require exactly five options. Do **not** exclude calculation items when they are option-choice items. Exclude numeric/free-response/non-option items and malformed records lacking options or gold answers.

## Multiple-answer protocol
For each item, the criteria presented to Jev are the original options only. Let `k` be the dataset/exam-required number of correct answers. Rank the returned option probabilities descending and choose exactly top-k. Score by exact set match. This avoids generating artificial combination choices and preserves a common decision space across single- and multi-answer items.

## Image-condition protocol
Run three prespecified subsets:
1. `no-image`: no image reference.
2. `image-only`: image-referenced questions only, but images withheld from Jev.
3. `both`: union of the above.

The `image-only` condition must always be described as **image-withheld text-only evaluation**. It is not evidence of image understanding. Report JMedQA `image_dependency` strata separately, especially `enough text` versus `not enough text`, `image only`, and `image question`.

## Primary metrics
- Exact-set accuracy with Wilson 95% CI.
- Wall-clock API latency: mean, p50, p90, p95, p99.
- Number and rate of API failures/retries.

## Secondary metrics
- Year, section, clinical area, image presence, image dependency, select-k and calculation-status subgroup accuracy.
- NLL and multiclass Brier score for single-answer items only.
- Confidence/ECE is exploratory when multi-answer items are pooled, because the returned probabilities are a single-choice distribution and are repurposed for top-k ranking.

## 120th official-style reconstruction
Use the published 500-point structure: required blocks B/E and general/clinical blocks A/C/D/F. Report whether published score thresholds are met only for a complete 400-item run. Never report a formal official pass/fail because prohibited-choice identities are not public.

## Reproducibility
Pin requested model ID, retain actual returned model/build/provider, save raw responses, dataset SHA-256, protocol SHA-256, UTC timestamps, Python/platform metadata, and all attempt-level latencies. Primary runs use concurrency=1. No failed item may silently become an incorrect answer; failures are reported separately.

## Visualization outputs

Each completed run can additionally be rendered into static figures using `scripts/visualize.py`. The visualization step is downstream of scoring and does not alter the benchmark outputs; it only reads `summary.json`, `items.jsonl`, and the stratified CSV files produced by `scripts/score.py`.
