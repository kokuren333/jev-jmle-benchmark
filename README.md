# Jev x Japanese Medical Licensing Examination benchmark

Research code and reproducibility artifacts for the manuscript:

> **Ren Matsushita, MD.** *Information Sufficiency and Selective Prediction in a Structured Probabilistic Decision Model: Nine Years of the Japanese Medical Licensing Examination.*

**Status:** Prepared for the GitHub whitepaper release `v1.0.0`. The work is a research benchmark and is not a clinical validation study.

## Main result

The completed primary run evaluated 3,556 option-choice JMedQA items from 2018-2026. Exact-set accuracy was 88.58% (3,150/3,556). The main finding was that performance aligned more closely with JMedQA's text-information sufficiency annotations than with the mere presence of an image reference. Native per-option probabilities also supported retrospective selective prediction on single-select items.

## Reproducibility

1. Create a Python environment.
2. Install the frozen dependencies in `environment/requirements-lock.txt` when available; otherwise use `environment/requirements.txt`.
3. Set `OPENROUTER_API_KEY`.
4. Run `scripts/download_data.py` to fetch the public benchmark sources.
5. Run benchmark scripts following `protocol/PROTOCOL.md`.

The repository intentionally **does not redistribute JMedQA question text or examination images**. Those materials must be obtained from their upstream sources and used under the applicable terms. The included item-level derived outputs contain identifiers, predictions/probabilities, correctness, latency, and usage metadata, but no question text.

## Software, typesetting, and publication provenance

The benchmark and statistical workflow used Python 3.12.10 with the frozen
environment recorded in `environment/requirements-lock.txt`, including
NumPy 2.5.3, pandas 2.3.3, SciPy 1.18.1, Matplotlib 3.11.2, requests 2.34.2,
and datasets 4.8.5. Source control and release preparation use Git and
GitHub. The manuscript and Japanese companion were prepared with
python-docx and converted to PDF with LibreOffice Writer 25.2.3.2 (x86_64).

The English PDF uses embedded Liberation Serif and Liberation Sans fonts. The
Japanese PDF uses embedded Noto Serif CJK JP and Noto Sans CJK JP fonts, with
limited fallback glyph coverage from Carlito and Noto Sans CJK HK. The
terminology guide uses Noto Serif CJK JP and Noto Sans CJK JP. The English and
Japanese manuscripts are US Letter PDFs (9 pages each); the terminology
guide is a three-page landscape A4 PDF. The PDFs are PDF 1.7, tagged, and
contain embedded font subsets.

Figures were produced or revised with Matplotlib-based tooling. The
repository visualization script uses 180 dpi PNG output, but the final four
redesigned manuscript figures are not asserted to be byte-identical to a
single run of that script, and no explicit Matplotlib font family is claimed
for those final figures.

Generative AI tools were used as disclosed in the manuscript for code
development, statistical workflow design, literature discovery, language
editing, figure redesign, and manuscript drafting. The author reviewed the
analyses, numerical results, references, interpretations, and final manuscript
and assumes responsibility for the work.

The public whitepaper is available as PDF in `paper/whitepaper/`. The
English Markdown source is included for inspection; the Japanese PDF is the
canonical Japanese publication artifact.

- [English whitepaper PDF](paper/whitepaper/Jev_JMLE_Whitepaper_EN_v1.0.pdf)
- [Japanese whitepaper PDF](paper/whitepaper/Jev_JMLE_Whitepaper_JA_v1.0.pdf)
- [English Markdown source](paper/manuscript_en.md)

## Repository layout

- `scripts/` - benchmark, scoring, visualization, statistical and reconstruction code
- `protocol/` - evaluation protocol and limitations
- `results/primary/` - item-level derived outputs and aggregate results (no question text)
- `results/statistical_analysis/` - statistical summaries and sensitivity analyses
- `results/official_reconstruction/` - conservative examination-by-examination score reconstruction
- `paper/` - public whitepaper source, PDFs, final/legacy figures, tables, and terminology report
- `docs/` - publication notes and release instructions

## Important limitations

This is a benchmark of constrained medical option selection, not a demonstration of autonomous clinical competence. No images were supplied. JMedQA's dataset-provided `image_dependency` annotations were used for stratification; detailed annotator/adjudication procedures and inter-rater reliability are not reported in the public dataset card. Multi-answer Choice probabilities were ranked top-k and are not treated as calibrated multilabel probabilities. Training-data contamination cannot be excluded for a closed model evaluated on publicly released examination questions.

## Licensing

Author-generated code is released under the MIT License (`LICENSE-CODE`). Author-generated manuscript text and figures are released under CC BY 4.0 (`LICENSE-DOCS`). Third-party datasets, examination content, model outputs, and provider materials are **not relicensed**; see `THIRD_PARTY_NOTICES.md`.

## Public whitepaper

The intended canonical public version is the GitHub repository at
https://github.com/kokuren333/jev-jmle-benchmark. The release tag `v1.0.0`
identifies the whitepaper and its corresponding reproducibility artifacts.
No Zenodo deposit or DOI is required for this publication route.
