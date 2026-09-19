# Benchmarking a Structured Probabilistic Decision Model on Nine Years of the Japanese Medical Licensing Examination: Accuracy, Missing-Visual-Information Robustness, Calibration, Selective Prediction, Latency, and Cost

**Ren Matsushita, MD**  
Independent Researcher

**Manuscript status:** full draft v0.3 based on completed primary benchmark runs; not yet peer reviewed.

## Abstract

### Background
Large language models (LLMs) have reached or exceeded passing-level performance on medical licensing examinations, including the Japanese Medical Licensing Examination (JMLE). However, licensing-exam accuracy alone provides limited information about uncertainty, operational latency, cost, and behavior when clinically relevant information is missing. Jev is a recently released text-only structured decision model that does not generate free-form prose; its Choice interface returns one selected option and a probability distribution over predefined options.

### Objective
To characterize the performance of a structured probabilistic decision model on nine years of JMLE-derived questions, with emphasis on accuracy, sensitivity to missing visual information, probability quality, selective prediction, latency, cost, and conservative reconstruction of official score thresholds.

### Methods
We evaluated `typesafe/jev-1.13` (returned build `typesafe/jev-1.13-20260917`) through the OpenRouter Decisions API on JMedQA questions from 2018–2026. Of 3,581 questions, 25 numeric-response items were excluded, leaving 3,556 option-choice items. Single-answer items were scored by top-1 choice. For multiple-answer items, the prespecified number of answers was selected by top-k ranking of returned Choice probabilities and scored by exact set match. Two complementary runs evaluated 2,582 no-image-reference items and 974 image-referenced items with images withheld; these were merged without repeat inference. Accuracy was summarized with Wilson 95% confidence intervals. Image-dependency strata were analyzed separately. Probability calibration and selective prediction were evaluated only on 3,097 single-select items using negative log loss, multiclass Brier score, expected calibration error (ECE), confidence–correctness AUROC, and risk–coverage curves. Wall-clock API latency and recorded API cost were measured. Published Ministry of Health, Labour and Welfare score thresholds were used for conservative examination-by-examination reconstruction; formal pass/fail was not asserted because contraindicated-choice identities are not public.

### Results
Jev answered 3,150/3,556 option-choice questions correctly (**88.58%**, Wilson 95% CI 87.50%–89.59%). Accuracy was 91.75% (2,369/2,582) in the no-image-reference run and 80.18% (781/974) in the image-referenced/image-withheld run, a difference of −11.57 percentage points (95% CI −14.28 to −8.85; P<0.001), although these were nonpaired item sets. By JMedQA image-dependency annotation, accuracy was 91.75% for `none` (2,370/2,583), 92.09% for `enough text` (617/670), 59.30% for `not enough text` (102/172), 49.19% for `image question` (61/124), and 0% for `image only` (0/7). The `enough text` stratum did not differ materially from `none` (+0.34 percentage points; 95% CI −2.16 to +2.47). On single-select items, accuracy was 88.89%, returned top-choice probability discriminated correct from incorrect responses with AUROC 0.918, and 10-bin ECE was 0.014. At an in-sample probability threshold of 0.90, coverage was 68.5% and selective accuracy was 99.01% (21 errors among 2,121 accepted responses). Median wall-clock latency was 820.7 ms overall; no-image and image-withheld medians were similar (820.3 vs 822.6 ms; Mann–Whitney P=.297). The recorded API cost for all 3,556 questions was approximately US$0.120, or US$0.0338 per 1,000 questions. Conservative lower-bound reconstructed scores exceeded published required and general/clinical score thresholds for each 112th–120th JMLE, but formal pass status remained indeterminate because contraindicated-choice identities are undisclosed.

### Conclusions
A structured probabilistic decision model achieved high accuracy on nine years of JMLE option-choice questions at low measured API cost and subsecond median wall-clock latency. Performance was preserved on image-associated questions judged answerable from text but declined sharply when visual information was required. Returned Choice probabilities strongly discriminated correct from incorrect single-select answers and supported high-accuracy selective prediction in this retrospective benchmark. These findings characterize benchmark behavior, not clinical competence or autonomous safety. Prospective calibration, multimodal comparison, repeated-run stability, and direct generative-LLM baselines are required before clinical or comparative deployment claims.

**Keywords:** Japanese Medical Licensing Examination; medical question answering; uncertainty calibration; selective prediction; decision model; clinical artificial intelligence; confidence; benchmark

## Introduction

Medical licensing examinations have become a common stress test for language models. Early work established that general-purpose and medically adapted LLMs could answer USMLE-style questions at or above passing levels, and subsequent studies demonstrated substantial performance on the Japanese National Medical Licensing Examination [1,4]. Tanaka and colleagues reported that GPT-4 reached passing-level scores on selected text questions from the 117th JMLE after prompt optimization [1]. Miyazaki and colleagues later reported 93.2% accuracy for GPT-4o on the 118th JMLE, including comparable performance on text-only and image-based questions when the corresponding images were supplied [2]. These results show that licensing-exam performance is no longer sufficient, by itself, to discriminate clinically relevant properties of modern models.

Recent evaluation frameworks have therefore shifted toward uncertainty, realistic task coverage, and deployment characteristics. MedHELM explicitly argues that near-perfect licensing-exam performance does not capture the diversity of real clinical work [6], while HealthBench emphasizes realistic, physician-authored criteria rather than examination accuracy alone [7]. Work on medical LLM uncertainty has also shown that token-level probabilities can be more informative than verbalized confidence for identifying incorrect answers [5], and selective prediction has been proposed as a mechanism for deferring low-confidence cases to humans or more capable systems [4,5,9].

Jev differs from conventional generative LLMs in a way that makes these questions particularly relevant. Rather than generating an explanation or answer string, its Choice interface evaluates a fixed set of alternatives and returns a selected option, a probability for every option, and a confidence value [11]. TypeSafe describes Jev as a “System One” model; because this is vendor terminology rather than an established scientific model class, we refer to it here more conservatively as a **structured probabilistic decision model**. The model is text-only, making it possible to study how its behavior changes when examination items require visual information.

JMedQA provides a useful setting for this analysis because it contains JMLE-derived questions from 2018–2026 and explicitly annotates image dependence as `none`, `enough text`, `not enough text`, `image question`, or `image only` [3]. This permits a more granular missing-information analysis than a simple image-present/image-absent comparison.

### Research questions

We prespecified four primary research questions:

**RQ1. Accuracy and operational performance:** How accurately, quickly, and cheaply does a structured probabilistic decision model answer JMLE option-choice questions across nine examination years?

**RQ2. Missing visual information:** Under a text-only, image-withheld evaluation, how does performance vary with the degree of image dependence, and is performance preserved when text alone is annotated as sufficient?

**RQ3. Uncertainty and selective prediction:** Do returned Choice probabilities discriminate correct from incorrect answers, are they reasonably calibrated on single-select questions, and can confidence-based deferral produce a high-accuracy accepted subset?

**RQ4. Robustness and exam reconstruction:** How stable is performance across examination years, clinical areas, and answer cardinality, and do conservative reconstructed scores exceed published JMLE score thresholds?

The novelty of the study is therefore not a claim that another AI can “pass” the JMLE. Rather, it is the joint characterization of a non-generative structured decision model across **nine years**, **graded visual-information dependence**, **native option probabilities**, **selective prediction**, and **latency/cost**, while explicitly separating examination performance from clinical competence.

## Methods

### Study design and data source

This was a retrospective benchmark study using publicly available examination-derived data. JMedQA contains 3,581 questions from the 112th–120th JMLE (2018–2026), with structured answer choices, clinical-area metadata, and image-dependency annotations [3]. No patient-level data were used.

Twenty-five numeric-response questions were excluded because Jev Choice requires a predefined answer set. The remaining 3,556 option-choice items constituted the analysis set. All option-choice items in the evaluated JMedQA release had five presented options. There were 3,097 single-answer items, 368 two-answer items, 90 three-answer items, and 1 four-answer item. Calculation questions were retained if they had selectable options.

### Model and API

Inference used the fixed route `typesafe/jev-1.13` through OpenRouter's Decisions API. The returned serving build was `typesafe/jev-1.13-20260917`, with TypeSafe as provider. The Jev Choice primitive returns a selected option and a probability distribution across supplied options [11,12]. The benchmark stored the full response, returned model identifier, provider, token usage, per-call cost, and wall-clock latency.

No role prompting (“you are a doctor”), chain-of-thought request, few-shot examples, retrieval, tool use, or external medical reference material was supplied.

### Answer scoring

For single-answer items, the model's highest-probability option was scored against the gold answer. For multiple-answer items, the benchmark ranked probabilities over the original options and selected the top k options, where k equaled the number of gold answers. Exact set equality was required for correctness.

This top-k procedure preserves the original answer choices but has an important limitation: Jev Choice represents mutually exclusive alternatives, whereas multi-answer examination items are multilabel. Therefore, multiple-answer exact-set accuracy is reported descriptively, but probability-calibration analyses were restricted to single-answer items.

### Image conditions

Jev is text-only; no examination images were supplied. Two complementary runs were performed: an operational no-image-reference subset (n=2,582) and an image-referenced/image-withheld subset (n=974). The two runs were merged to form the full 3,556-item dataset without repeat inference.

The primary missing-information analysis used JMedQA's `image_dependency` annotation directly: `none`, `enough text`, `not enough text`, `image question`, and `image only`. One item (2023C074) was operationally tagged as image-referenced by the benchmark helper but carried `image_dependency=none`; this explains the one-item discrepancy between the binary no-image count (2,582) and the annotation-based `none` count (2,583).

### Outcomes

The primary outcome was exact-set accuracy. Secondary outcomes were Wilson 95% confidence intervals, wall-clock latency, recorded API cost, performance by year, clinical area, image dependency, and answer cardinality.

For single-select items only, we assessed negative log loss, multiclass Brier score, 10-bin equal-width ECE, top-choice-probability AUROC for predicting correctness, reliability curves, and risk–coverage curves. Confidence-threshold results were treated as retrospective descriptive analyses rather than validated deployment thresholds.

### Statistical analysis

Accuracy confidence intervals used the Wilson method. Binary image-condition accuracy differences were summarized with Newcombe confidence intervals and a chi-square test; image-dependency strata were compared with the `none` stratum using Fisher exact tests because some strata were small. Latency distributions were compared with the Mann–Whitney U test. Annual trend was explored with Spearman rank correlation across the nine yearly aggregate accuracies. Clinical-area heterogeneity was evaluated with a chi-square test; per-domain Fisher tests versus the remainder of the dataset were exploratory and adjusted using the Benjamini–Hochberg false-discovery-rate procedure.

All P values are descriptive in this benchmark context. No causal interpretation is assigned to comparisons between nonrandomized item groups.

### Official-style examination reconstruction

Published Ministry of Health, Labour and Welfare thresholds for the 112th–120th JMLE were applied to each year [10]. Because numeric-response items were excluded and some years included official scoring exclusions, score intervals were used where necessary. A year's published score thresholds were considered conservatively exceeded only when the reconstructed lower bound exceeded the published cutoff. Formal pass/fail status was not assigned because the identities of contraindicated choices are not public.

### Ethical considerations

The study used publicly available examination questions and contained no human participant or patient data. Institutional review board approval was therefore not sought.

## Results

### Overall performance

Across all 3,556 option-choice questions, Jev answered 3,150 correctly (88.58%; Wilson 95% CI 87.50%–89.59%). Accuracy on single-select questions was 88.89% (2,753/3,097). Exact-set accuracy on two-answer questions was 86.41% (318/368), and on three-answer questions was 86.67% (78/90); the sole four-answer item was answered correctly.

Annual exact-set accuracy ranged from 85.68% on the 115th examination (2021) to 90.91% on the 118th examination (2024). There was no statistically demonstrable monotonic temporal trend across the nine annual aggregates (Spearman rho=0.533, P=.139).

### Missing visual information

The operational no-image-reference subset achieved 91.75% accuracy (2,369/2,582; 95% CI 90.63%–92.75%), whereas the image-referenced/image-withheld subset achieved 80.18% (781/974; 95% CI 77.57%–82.57%). The difference was −11.57 percentage points (95% CI −14.28 to −8.85; P<.001). Because these are different examination items, this comparison does not estimate the causal effect of removing an image.

The image-dependency analysis clarified the pattern. Accuracy was 91.75% for `none` (2,370/2,583), 92.09% for `enough text` (617/670), 59.30% for `not enough text` (102/172), 49.19% for `image question` (61/124), and 0% for `image only` (0/7). Relative to `none`, `enough text` differed by only +0.34 percentage points (95% CI −2.16 to +2.47), whereas `not enough text` was −32.45 percentage points (95% CI −39.99 to −25.30) and `image question` was −42.56 percentage points (95% CI −51.26 to −33.80).

### Probability quality and selective prediction

Calibration analyses were restricted to the 3,097 single-select items. The top-choice probability discriminated correct from incorrect responses with AUROC 0.918. Ten-bin ECE was 0.014. The full single-select NLL and multiclass Brier results are provided in Table 5 and the supplementary analysis.

Confidence-based deferral produced a steep risk–coverage trade-off. At a probability threshold of 0.90, the model answered 2,121/3,097 single-select items (68.5% coverage) with 99.01% accuracy; 21 accepted answers were incorrect. At 0.95, coverage was 59.9% with 99.57% accuracy (8 errors). At 0.99, coverage was 43.3% with 99.85% accuracy (2 errors). These values were measured and selected on the same benchmark and therefore do not establish prospective error guarantees.

### Latency and cost

Overall median wall-clock latency was 820.7 ms and p95 latency was 1,061.0 ms. Median latency was 820.3 ms in the no-image-reference run and 822.6 ms in the image-referenced/image-withheld run (Mann–Whitney P=.297).

The 3,556 calls used 2,858,460 recorded input tokens and cost approximately US$0.120 in total, corresponding to roughly US$0.0338 per 1,000 questions under the recorded run pricing. These are API-level measurements and should not be interpreted as model-only compute latency or provider-internal inference cost.

### Clinical-area heterogeneity

Accuracy differed across 31 clinical-area labels (global chi-square=69.68, 30 df, P<.001). After Benjamini–Hochberg correction in exploratory one-domain-versus-rest comparisons, endocrine/metabolic disorders, nephrology, and collagen diseases showed higher-than-rest signals, whereas no low-performing domain retained strong evidence after correction except that obstetrics/gynecology approached the FDR threshold. These comparisons are exploratory because domains differ in question composition, image dependence, and sample size.

### Official-style reconstruction

For each of the 112th–120th examinations, conservative lower-bound reconstructed required-section and general/clinical scores exceeded that year's published score thresholds. For example, the 118th examination reconstructed to 190/200 in the required section and 266–269/300 in general/clinical questions; the 120th reconstructed to 181/200 and 266–269/300, respectively. Nevertheless, formal pass/fail remained indeterminate for every year because contraindicated-choice identities are undisclosed and some non-option or excluded items could not be scored identically to an examinee.

## Discussion

### Principal findings

This study provides a nine-year evaluation of a structured probabilistic decision model on JMLE-derived option-choice questions. Four findings stand out. First, overall exact-set accuracy was 88.6%, with conservative reconstructed score thresholds exceeded in every examination year. Second, the apparent penalty on image-associated questions was almost entirely concentrated in items for which text was insufficient or visual interpretation was explicitly required; image-associated items annotated as answerable from text performed essentially identically to non-image-dependent items. Third, the model's native Choice probabilities were highly discriminative of correctness on single-select items and supported a favorable retrospective risk–coverage curve. Fourth, these decisions were obtained with a median API wall-clock latency of approximately 0.82 seconds and a recorded total cost of roughly twelve US cents for all 3,556 questions.

### Comparison with prior work

The overall accuracy should not be interpreted as establishing superiority over generative LLMs. Prior JMLE studies used different years, prompts, modality access, and scoring subsets. Tanaka et al. reported passing-level GPT-4 performance on selected text questions from the 117th JMLE [1], whereas Miyazaki et al. reported 93.2% overall accuracy for GPT-4o on the 118th examination with images supplied for image questions [2]. The present model received no images and produced no free-form clinical explanations, making direct rank-order comparison inappropriate.

The more distinctive contribution is uncertainty behavior. Bentegeac et al. showed that token response probabilities generally discriminated medical-answer correctness better than verbalized confidence across several LLMs [5]. Here, Jev's Choice probability is a native decision output rather than a token log probability extracted from a generative completion. On single-select JMLE items it achieved an AUROC of 0.918 for correctness discrimination, suggesting that structured option probabilities may be useful for triage or model routing. This result aligns conceptually with prior work advocating selective prediction in medical AI [4,5,9], but our in-sample thresholds are not validated safety controls.

The image-dependency gradient also helps separate medical knowledge from missing-input failure. GPT-4o's 118th-JMLE study found similar performance on text and image questions when images were actually supplied [2]. By contrast, our text-only model retained 92.1% accuracy on image-associated questions when text alone was annotated as sufficient, but fell to 59.3% or 49.2% when visual information was needed. This pattern is consistent with an information-availability interpretation rather than a generic “image-question difficulty” effect. A paired multimodal experiment on the same items would be required to quantify the causal contribution of images.

### What this study does not show

High licensing-exam accuracy is not equivalent to clinical competence. Contemporary frameworks such as MedHELM and HealthBench emphasize that clinical work includes information gathering, open-ended diagnostic reasoning, treatment planning, communication, documentation, and adaptation under uncertainty [6,7]. Script-concordance research similarly evaluates how decisions change when new information arrives rather than whether a static MCQ answer is correct [8]. The present benchmark therefore measures constrained medical question answering and uncertainty behavior, not independent clinical practice.

### Adversarial interpretation

A skeptical reviewer could reasonably argue that this study is “only another exam benchmark.” That critique is valid if the paper is framed around passing scores. The manuscript's defensible contribution instead lies in three dimensions that are not captured by a pass/fail headline: (1) native per-option probabilities and selective prediction; (2) explicit degradation under graded missing visual information; and (3) operational latency/cost of a decision-only interface. If these elements were removed, the study's novelty would be limited.

A second challenge is data contamination. JMLE questions are publicly available, and the model's training corpus is undisclosed. Stable performance from 2018–2026 does not rule out memorization. The annual trend analysis found no clear monotonic decline on newer exams, but it is too weak to prove absence of contamination. A future benchmark should include newly authored or prospectively embargoed questions.

A third challenge is the multi-answer protocol. Top-k ranking of a mutually exclusive Choice distribution is a pragmatic ranking rule, not a calibrated multilabel model. The exact-set results are useful operationally but should not be used for probability-calibration claims. A sensitivity experiment using independent binary (`Noul`) judgments per option is a priority before journal submission.

### Limitations

This study has several limitations. Jev is a closed commercial model, so architecture, training data, and contamination cannot be independently audited. The study evaluated a single model build on a single day through an API gateway; repeated-run stability was not measured. No direct generative-model baseline was run under identical JMedQA conditions. Images were withheld rather than supplied, so the study does not evaluate multimodal capability. Image-condition comparisons are nonpaired and may be confounded by item difficulty and specialty composition. JMedQA itself notes that a small number of extraction or annotation errors may remain [3]. The binary image helper and image-dependency annotation disagreed for one item. Selective-prediction thresholds were evaluated in-sample and are not prospectively calibrated. Multi-answer top-k scoring is not probabilistically equivalent to multilabel inference. Finally, official-style reconstruction cannot establish formal pass status because contraindicated-choice identities are not public.

### Future work

Before a journal submission, three additions would substantially strengthen the study: (1) rerun a stratified subset several times to quantify decision and probability stability; (2) re-evaluate multi-answer questions using independent per-option binary judgments; and (3) benchmark one or more generative LLMs on a prespecified matched subset under identical text-only conditions, reporting accuracy, latency, cost, and uncertainty where accessible. A prospective held-out calibration split should also be used to choose selective-prediction thresholds and then test them on untouched data.

## Conclusions

Jev demonstrated high option-choice accuracy across nine years of the Japanese Medical Licensing Examination, with performance preserved when text contained sufficient information and sharply reduced when unseen visual information was required. Its native per-option probabilities were informative for correctness and retrospective selective prediction, while API latency and cost were low in this benchmark. These properties make structured decision models an interesting object of medical-AI evaluation, but licensing-exam performance cannot establish clinical competence, and probability-based routing requires prospective validation before use in health care.

## Data availability

The benchmark is based on JMedQA, a public dataset derived from Japanese Ministry of Health, Labour and Welfare examination materials. The analysis pipeline should be released with exact run manifests, item-level Jev outputs where permitted, hash values, and scripts necessary to reproduce all tables and figures.

## Code availability

Code release recommended via a public GitHub repository with a versioned release archived on Zenodo.

## Funding

No external funding was reported for this independent study.

## Conflicts of interest

The author should disclose any financial or nonfinancial relationship with TypeSafe, OpenRouter, JMedQA maintainers, or other relevant entities. If none: “The author declares no competing interests.”

## Author contributions

Ren Matsushita: Conceptualization, Methodology, Software, Formal Analysis, Investigation, Visualization, Writing – Original Draft, Writing – Review & Editing.

## Use of AI-assisted tools

**Draft disclosure placeholder:** Generative AI tools were used to assist with code development, statistical-analysis drafting, literature discovery, and manuscript language editing. The author reviewed the analysis, verified source material, and takes responsibility for the final manuscript. This statement must be adapted to the target journal's current policy before submission.

## References

See `references.md`.
