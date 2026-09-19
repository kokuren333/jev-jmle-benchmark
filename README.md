# Jev × Japanese Medical Licensing Examination benchmark

Research code and reproducibility artifacts for:

> **Ren Matsushita, MD.** *Benchmarking a Structured Probabilistic Decision Model on Nine Years of the Japanese Medical Licensing Examination: Accuracy, Missing-Visual-Information Robustness, Calibration, Selective Prediction, Latency, and Cost.*

**Status:** submission-candidate repository, v0.4 (not peer reviewed).

## Main result

The completed primary run evaluated 3,556 option-choice JMedQA items from 2018–2026. Exact-set accuracy was 88.58% (3,150/3,556). See `paper/` for the manuscript and `results/` for derived result files.

## Reproducibility

1. Create a Python environment.
2. Install `environment/requirements.txt`.
3. Set `OPENROUTER_API_KEY`.
4. Run `scripts/download_data.py` to fetch the public benchmark sources.
5. Run benchmark scripts following `protocol/PROTOCOL.md`.

The repository intentionally **does not redistribute JMedQA question text or examination images**. Those materials must be obtained from their upstream sources and used under the applicable MHLW/JMedQA terms. The included `results/primary/items.jsonl` contains question identifiers, predictions/probabilities, correctness, latency, and usage metadata, but no question text.

## Repository layout

- `scripts/` — benchmark, scoring, visualization, statistical and reconstruction code
- `protocol/` — evaluation protocol and limitations
- `results/primary/` — item-level derived outputs and aggregate results (no question text)
- `results/statistical_analysis/` — statistical summaries and sensitivity analyses
- `results/official_reconstruction/` — conservative examination-by-examination score reconstruction
- `paper/` — English/Japanese manuscripts, figures, tables, terminology report
- `submission/` — journal submission preparation documents

## Important limitations

This is a benchmark of constrained medical option selection, not a demonstration of autonomous clinical competence. Image-referenced items were evaluated with images withheld. Multi-answer Choice probabilities were ranked top-k and are not treated as calibrated multilabel probabilities. Training-data contamination cannot be excluded for a closed model evaluated on publicly released examination questions.

## Licensing

Author-generated code is released under the MIT License (`LICENSE-CODE`). Author-generated manuscript text and figures are released under CC BY 4.0 (`LICENSE-DOCS`). Third-party datasets, examination content, model outputs, and provider materials are **not relicensed**; see `THIRD_PARTY_NOTICES.md`.
