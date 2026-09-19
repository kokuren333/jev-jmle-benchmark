# Extended Statistical Analysis (v0.2)

## Dataset

The derived combined dataset contains **3,556 option-choice questions**, of which **3,150 were answered correctly (88.58%)**. The Wilson 95% CI is 87.50%–89.59%.

## Binary image-condition comparison

The operational no-image-reference subset contained 2,582 items with 91.75% accuracy; the image-referenced/image-withheld subset contained 974 items with 80.18% accuracy. The difference was -11.57 percentage points (Newcombe 95% CI -14.37 to -8.93; chi-square P=7.09e-22). Because these are different item sets rather than paired versions of the same items, this is an association, not a causal estimate of image removal.

## Image-dependency gradient

Using the JMedQA image-dependency annotation directly, accuracy was 91.75% for `none` (n=2,583), 92.09% for `enough text` (n=670), 59.30% for `not enough text` (n=172), 49.19% for `image question` (n=124), and 0% for `image only` (n=7). Compared with `none`, the `enough text` difference was +0.34 pp (95% CI −2.16 to +2.47), whereas `not enough text` was −32.45 pp (95% CI −39.99 to −25.30) and `image question` was −42.56 pp (95% CI −51.26 to −33.80).

One item (2023C074) was operationally classified as image-referenced by the benchmark helper while carrying `image_dependency=none`. This metadata discordance explains the n=2,582 vs n=2,583 difference between the binary no-image subset and the annotation-based `none` stratum.

## Probability quality and selective prediction

Calibration analyses were restricted to the **3,097 single-select items**, because Jev Choice returns a mutually exclusive probability distribution; using that distribution as calibrated probabilities for multi-select top-k items is not formally justified. Single-select accuracy was 88.89%. The returned top-choice probability discriminated correct from incorrect answers with AUROC **0.918**. Ten-bin equal-width ECE was **0.014**.

At a returned-choice-probability threshold of 0.90, coverage was 68.5% (2,121/3,097) and selective accuracy was 99.01% (21 errors). At 0.95, coverage was 59.9% and selective accuracy was 99.57%. These are descriptive, in-sample thresholds and **must not be presented as prospective safety guarantees**.

## Latency and cost

Median wall-clock latency was 820.7 ms overall. Median latency did not materially differ between the two binary image conditions (820.3 vs 822.6 ms; Mann–Whitney U P=0.297). Across all 3,556 calls, the recorded OpenRouter API cost was **US$0.1201**, corresponding to approximately **US$0.0338 per 1,000 questions**, with 2,858,460 input tokens recorded.

## Year and domain heterogeneity

Across the 112th–120th examinations, annual exact-set accuracy ranged from 85.68% to 90.91%. Spearman correlation between year and annual accuracy was rho=0.533, P=0.139; this nine-point analysis does not demonstrate a monotonic temporal trend. Accuracy varied across the 31 clinical-area labels (chi-square=69.68, df=30, P=5.35e-05). Domain-specific significance tests are exploratory; Benjamini–Hochberg q values are provided in Table 7.

## Official-style reconstruction

For each examination year, the conservative lower bound of the reconstructed required-section and general/clinical scores exceeded the corresponding published score threshold. Formal pass/fail nevertheless remains indeterminate because the identities of contraindicated choices are not public and because this benchmark excludes numeric-response items.
