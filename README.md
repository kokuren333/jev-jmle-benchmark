# Jev x Japanese Medical Licensing Examination benchmark

Research code and reproducibility artifacts for the manuscript:

> **Ren Matsushita, MD.** *Information Sufficiency and Selective Prediction in a Structured Probabilistic Decision Model: Nine Years of the Japanese Medical Licensing Examination.*

**Status:** Submitted to medRxiv as `MEDRXIV/2026/363463` (Version 1); screening in progress. Not peer reviewed.

## Main result

The completed primary run evaluated 3,556 option-choice JMedQA items from 2018-2026. Exact-set accuracy was 88.58% (3,150/3,556). The main finding was that performance aligned more closely with JMedQA's text-information sufficiency annotations than with the mere presence of an image reference. Native per-option probabilities also supported retrospective selective prediction on single-select items.

## Reproducibility

1. Create a Python environment.
2. Install the frozen dependencies in `environment/requirements-lock.txt` when available; otherwise use `environment/requirements.txt`.
3. Set `OPENROUTER_API_KEY`.
4. Run `scripts/download_data.py` to fetch the public benchmark sources.
5. Run benchmark scripts following `protocol/PROTOCOL.md`.

The repository intentionally **does not redistribute JMedQA question text or examination images**. Those materials must be obtained from their upstream sources and used under the applicable terms. The included item-level derived outputs contain identifiers, predictions/probabilities, correctness, latency, and usage metadata, but no question text.

## Repository layout

- `scripts/` - benchmark, scoring, visualization, statistical and reconstruction code
- `protocol/` - evaluation protocol and limitations
- `results/primary/` - item-level derived outputs and aggregate results (no question text)
- `results/statistical_analysis/` - statistical summaries and sensitivity analyses
- `results/official_reconstruction/` - conservative examination-by-examination score reconstruction
- `paper/` - manuscript source, Japanese translation, figures, tables, terminology report
- `submission/` - submission preparation documents

## Important limitations

This is a benchmark of constrained medical option selection, not a demonstration of autonomous clinical competence. No images were supplied. JMedQA's dataset-provided `image_dependency` annotations were used for stratification; detailed annotator/adjudication procedures and inter-rater reliability are not reported in the public dataset card. Multi-answer Choice probabilities were ranked top-k and are not treated as calibrated multilabel probabilities. Training-data contamination cannot be excluded for a closed model evaluated on publicly released examination questions.

## Licensing

Author-generated code is released under the MIT License (`LICENSE-CODE`). Author-generated manuscript text and figures are released under CC BY 4.0 (`LICENSE-DOCS`). Third-party datasets, examination content, model outputs, and provider materials are **not relicensed**; see `THIRD_PARTY_NOTICES.md`.

## Preprint

The medRxiv submission is currently undergoing screening. After posting, add the public medRxiv URL/DOI here and update `CITATION.cff` accordingly.
