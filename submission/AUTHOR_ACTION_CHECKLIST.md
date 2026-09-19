# Author action checklist before journal submission

## Identity / metadata
- [ ] Create or confirm an ORCID and add it to `CITATION.cff` and manuscript metadata.
- [ ] Choose a stable corresponding-author email.
- [ ] Decide the public affiliation wording (e.g., `Independent Researcher, [City], Japan`).
- [ ] Confirm the exact competing-interest statement, including any relationship with TypeSafe/OpenRouter/JMedQA maintainers.
- [ ] Confirm funding (`No external funding` if accurate) and who would pay an APC if accepted.

## Freeze reproducibility environment
Run in the original benchmark virtual environment:

```powershell
python --version > environment_python_version.txt
pip freeze > requirements-lock.txt
```

Commit those files before creating the archival release.

## Additional experiments recommended before peer-reviewed submission
- [ ] **Repeatability:** repeat the full 3,556-question evaluation twice more under the same fixed model route if feasible. This costs little and takes roughly one wall-clock hour per full sequential run at the observed latency. Preserve returned build IDs.
- [ ] **Multi-answer sensitivity:** rerun the 459 multi-answer items using independent per-option binary/Noul judgments; compare exact-set accuracy and ranking agreement against Choice top-k.
- [ ] **Manual error audit:** review all high-confidence errors in `results/statistical_analysis/high_confidence_error_audit_template.csv` against the original source/answer key.
- [ ] **Matched baseline (strongly recommended):** run at least one generative LLM on a preregistered/locked stratified subset under the same text-only input condition, measuring accuracy, latency, and cost.

## AI-assisted manuscript preparation
- [ ] Preserve/export the complete ChatGPT conversation(s) used for scientific ideation, code, analysis, and manuscript drafting. JMIR's current policy asks authors to retain and may request prompts/responses/transcripts.
- [ ] Review every reference manually against the source.
- [ ] Rewrite/approve all scientific interpretations in your own words; you remain accountable for every statement.

## Repository / archival
- [ ] Create a public GitHub repository (suggested name: `jev-jmle-benchmark`).
- [ ] Replace `OWNER` in `CITATION.cff` with the GitHub account/organization.
- [ ] Push code and derived results. Do not commit API keys, downloaded JMedQA question text/images, or raw provider responses until licensing is confirmed.
- [ ] Connect the repository to Zenodo.
- [ ] Create a tagged GitHub Release (e.g., `v1.0.0-paper`).
- [ ] Record the Zenodo DOI in the README, manuscript Data/Code Availability section, and `CITATION.cff`.

## Submission
- [ ] Decide primary target journal.
- [ ] Generate target-journal DOCX and cover letter.
- [ ] Add DOI/repository URL only after archival record exists.
- [ ] Submit only after repository and manuscript point to the same immutable release/hash.
