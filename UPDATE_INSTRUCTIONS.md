# Repository update instructions

This bundle contains only files that should be synchronized with the current public repository after the v1.0 manuscript was prepared and submitted to medRxiv.

## Replace/update

- `README.md`
  - updates the manuscript title used in the v1.0 PDF
  - records medRxiv submission ID `MEDRXIV/2026/363463`
  - changes status from "submission candidate" to "submitted / screening / not peer reviewed"
  - adds the JMedQA image-dependency annotation caveat
- `CITATION.cff`
  - fixes the placeholder repository URL (`OWNER` -> `kokuren333`)
  - bumps the repository metadata to 0.4.1
- `paper/manuscript_en.md`
  - regenerated from the final v1.0 English DOCX so the repository source matches the submitted manuscript text
- `paper/manuscript_ja.md`
  - regenerated from the final v1.0 Japanese DOCX
- `paper/terminology_report_ja.md`
  - retained as the source for the companion Japanese terminology guide
- `paper/figures/*`
  - these four English figures are the figures used in the final v1.0 manuscript
  - Japanese equivalents are under `paper/figures/ja/`

## Legacy figures in the current repository

The earlier repository contains six older figures. The submitted v1.0 manuscript uses four redesigned figures instead. Treat these older files as legacy unless you intentionally want to retain them for history:

- `figure2_image_dependency_accuracy.png`
- `figure3_yearly_accuracy.png`
- `figure4_risk_coverage.png`
- `figure5_reliability.png`
- `figure6_official_style_scores.png`

The final four-figure set in this bundle is:

1. `figure1_study_flow.png`
2. `figure2_information_sufficiency.png`
3. `figure3_selective_prediction.png`
4. `figure4_yearly_accuracy.png`

## Important medRxiv note

The manuscript PDF title and the title entered in medRxiv submission metadata are not identical. Do not create a duplicate medRxiv submission to fix this. If medRxiv returns the manuscript or asks for clarification, reconcile the titles then. After the preprint is posted, use the title and DOI shown on the public medRxiv record as the canonical citation metadata.

## After medRxiv posts the preprint

Update:

- `README.md` with the public preprint URL and DOI
- `CITATION.cff` with a preferred citation / DOI
- GitHub release tag (for example `v1.0.0`)
- Zenodo archive metadata, if you archive the software/reproducibility package
