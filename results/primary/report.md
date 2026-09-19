# Jev medical licensing benchmark report

- Run: `20260919T092845Z_multi-year_both-derived`
- Dataset mode: `multi-year`
- Image mode: `both`
- Requested model: `typesafe/jev-1.13`
- Response model(s): `typesafe/jev-1.13-20260917`
- Dataset SHA-256: `fc19c416bda094040539746f3339fcac547a9a23cb3264712931d3ad0d1a041e`
- Protocol SHA-256: `56c901cb9330d299c75a1efbc1c34cc9d56ba7b0b52b800013c0f2840b7c4877`

## Results

- Exact-set accuracy: **88.583%** (3150/3556); Wilson 95% CI 87.496%–89.587%
- Single-select items: 3097
- Multi-select items (top-k): 459
- Median latency: **820.7 ms**
- p95 latency: **1061.0 ms**

- Single-select NLL: 0.3664
- Single-select multiclass Brier: 0.1568

## Interpretation

For multi-select questions, the model is given the original options once. The benchmark ranks the returned per-option probabilities and selects exactly k options (top-k), where k is the required answer count. Correctness requires exact set match.

For image-referenced questions, Jev receives no image. `image-only` therefore means an image-referenced, image-withheld text-only condition, not multimodal performance. Results are additionally stratified by JMedQA image_dependency.
