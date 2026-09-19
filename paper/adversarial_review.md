# Adversarial Review Memo (v0.2)

## Bottom line

The current dataset is strong enough for a credible technical white paper and likely a preprint. A peer-reviewed original article is plausible, but three vulnerabilities should be addressed before making comparative or clinical claims: **training-data contamination, multi-answer probability semantics, and absence of an identical-condition baseline/repeatability study**.

## Reviewer attack 1: “This is just another licensing-exam paper.”

**Force of critique:** High. GPT-4 and GPT-4o have already been evaluated on JMLE. “Jev passed the exam” is not novel.

**Defense:** Make the paper about structured probabilistic decision behavior, not passing. The strongest novel axes are native option probabilities, selective prediction, graded missing-visual-information response, and measured latency/cost over nine years.

**Required wording:** Never title the paper “Jev passes the JMLE.”

## Reviewer attack 2: “The model may have memorized these public questions.”

**Force:** Very high. Jev is closed; training data are unknown.

**Defense:** Explicit contamination limitation; year-trend analysis does not show a monotonic decline but cannot rule out contamination. Add a prospective set of newly authored questions if feasible.

## Reviewer attack 3: “The image comparison is confounded.”

**Force:** High for the 91.75% vs 80.18% binary comparison. These are different questions.

**Defense:** Treat binary difference as descriptive. Make the image-dependency gradient the primary result. The near-equivalence of `none` and `enough text` is particularly informative. Best future experiment: same image-associated questions with and without image using a multimodal comparator. Jev itself cannot receive images.

## Reviewer attack 4: “Top-k on a mutually exclusive Choice distribution is not a valid multilabel probability model.”

**Force:** High.

**Defense:** Restrict all calibration/probability claims to single-select items, as v0.2 does. Report multi-answer exact-set accuracy only as a ranking heuristic. Add a Noul-per-option sensitivity analysis before journal submission.

## Reviewer attack 5: “ECE=0.014 proves calibration.”

**Force:** Moderate to high. ECE is bin-dependent and can look artificially good.

**Defense:** Report ECE together with NLL, multiclass Brier, reliability curves, AUROC, and risk–coverage. Avoid “well calibrated” as a categorical claim. Use “low 10-bin ECE in this retrospective dataset.”

## Reviewer attack 6: “99% selective accuracy sounds like a safety guarantee.”

**Force:** Very high if phrased carelessly.

**Defense:** The threshold was examined on the same dataset. Call it a retrospective risk–coverage result, not a deployment rule. For a safety claim, split calibration/test sets or use prospective risk control.

## Reviewer attack 7: “Subsecond latency is not model latency.”

**Force:** Correct.

**Defense:** Call it API wall-clock latency. It includes networking, OpenRouter routing, provider queueing, and model inference. Do not subtract an assumed network floor unless measured independently.

## Reviewer attack 8: “The cost is too cheap to be believable.”

**Force:** Low if raw `usage.cost` records are released.

**Defense:** Report exactly what the gateway returned: total US$0.120055 for 3,556 calls, 2,858,460 input tokens. Distinguish API price from hardware cost.

## Reviewer attack 9: “Official pass reconstruction is misleading because contraindicated choices are unknown.”

**Force:** High.

**Defense:** Never state “passed the JMLE.” State “published score thresholds were exceeded under conservative score reconstruction; formal pass status was indeterminate because prohibited-choice identities are not public.”

## Reviewer attack 10: “There is no direct GPT-4o/GPT-5/Claude baseline.”

**Force:** Moderate for a white paper, high for a comparative journal article.

**Defense:** Current paper is model characterization, not ranking. Prior papers provide context but are not head-to-head comparisons. Add a prespecified matched subset baseline if budget permits.

## Reviewer attack 11: “You ran the model once. How stable are probabilities?”

**Force:** Moderate.

**Defense:** Add repeatability on a stratified 300–500-item subset, 3–5 repetitions. Report exact agreement, probability SD, and threshold-crossing frequency.

## Reviewer attack 12: “Single author and AI-assisted writing undermine credibility.”

**Force:** Depends on venue.

**Defense:** Release code, hashes, item-level outputs where legally permissible, and a transparent AI-use statement. Reproducibility matters more than author count. For journal submission, recruit an independent clinician/statistician only if they make a genuine authorship-level contribution; do not add honorary authors.

## Claims allowed now

- Jev achieved 88.58% exact-set accuracy on the evaluated JMedQA option-choice set.
- Performance on `enough text` image-associated questions was similar to `none`.
- Performance was substantially lower when text was annotated as insufficient or the question required image interpretation.
- Returned Choice probabilities strongly discriminated correct from incorrect single-select answers.
- Retrospective confidence gating yielded high selective accuracy at reduced coverage.
- API wall-clock median latency was ~0.82 s and recorded cost was ~US$0.12 total.

## Claims not allowed now

- “Jev is clinically safe.”
- “Jev is better than GPT-4o/GPT-5.”
- “Jev passed the JMLE” without the contraindicated-choice caveat.
- “Removing images causes an 11.6-point drop.”
- “0.90 confidence guarantees 99% accuracy.”
- “Jev is well calibrated” without qualification.
- “Jev can perform clinical decision making autonomously.”
