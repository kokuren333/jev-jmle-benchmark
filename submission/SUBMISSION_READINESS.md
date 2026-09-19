# Submission-readiness assessment (v0.4)

## Current status

The project is strong enough for a public technical report/preprint **now**, but I would not yet call it maximally defensible for peer review. The remaining gaps are tractable and mostly inexpensive.

### Ready now
- Complete 2018–2026 option-choice benchmark (n=3,556).
- Image-dependency stratification.
- Item-level native probability analysis on single-select items.
- Latency and recorded cost.
- Conservative 112th–120th examination reconstruction.
- Reproducible code and hashes.
- English and Japanese manuscripts.

### Highest-priority blockers for journal submission
1. Repeatability/stability of a closed API model.
2. Sensitivity analysis for the nonstandard multi-answer top-k protocol.
3. Manual audit of high-confidence errors and data-quality artifacts.
4. Preferably one matched generative-model comparator.
5. Final verification of every bibliographic citation and official passing threshold.

## New no-API sensitivity analysis

A deterministic 5-fold held-out selective-prediction analysis was added. In each fold, a threshold was selected only on the other four folds as the lowest confidence threshold achieving >=99% empirical accepted accuracy (minimum 100 accepted items). Across held-out folds, 2072/2093 accepted predictions were correct: **99.00%** accuracy (Wilson 95% CI 98.47%–99.34%) at **67.6%** coverage. Selected thresholds were [0.92, 0.9, 0.9, 0.92, 0.9].

This materially strengthens the selective-prediction section compared with an entirely in-sample threshold, but remains retrospective and should not be described as prospective clinical validation.

## Preferred journal strategy

**Primary target: JMIR Medical Education, Original Paper.** It is the clearest thematic fit and has already published JMLE/LLM evaluations. Current instructions require IMRD structure, funding/COI/data availability sections, and disclosure of generative-AI use. The current Original Paper APF is US$2,750; the fee schedule states that authors may request a waiver with compelling justification in the cover letter.

**Stretch target: PLOS Digital Health.** Broader digital-health impact, but a matched comparator and repeatability experiment would make the submission substantially stronger. PLOS also expects underlying result data and author-generated code to be publicly available where possible.

**Preprint/archival path:** GitHub -> tagged Release -> Zenodo DOI -> preprint -> journal submission. A preprint is compatible with JMIR in principle if disclosed in the cover letter.
