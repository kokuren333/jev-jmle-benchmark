# Additional experiments to run

## A. Full-run repeatability (highest priority)
Run the same benchmark twice more with the same fixed model route. Keep each run separate. Desired outputs per item: chosen option(s), full probability distribution, latency, returned model build, provider, usage.

Primary repeatability outcomes:
- exact answer agreement across runs;
- probability mean absolute deviation / standard deviation per option;
- fraction of items whose correctness changes;
- agreement stratified by image dependency and confidence.

Because the completed full run cost about US$0.12, the financial cost of two additional full repeats is negligible; the main cost is sequential wall-clock time.

## B. Multi-answer Noul sensitivity
For all 459 multi-answer questions, ask an independent binary question for each original option (“Is this option one of the correct answers?”), obtain an independent probability for each option, and then choose the required k options by the highest positive probabilities. Compare:
- exact-set accuracy;
- item-level agreement with Choice-top-k;
- rank correlation;
- whether the sensitivity result changes conclusions about multi-answer performance.

Do not claim Noul probabilities are calibrated without a separate calibration analysis.

## C. Matched generative baseline
Lock a stratified subset before running the comparator. Recommended: >=450 items, 50 per year, stratified within year by image-dependency and answer cardinality where feasible. Use identical text input and no images. Report exact-set accuracy, latency, and cost.

A baseline is not needed to publish a technical report, but it will materially strengthen a journal submission by showing what the structured decision interface buys relative to a conventional generative model under matched conditions.
