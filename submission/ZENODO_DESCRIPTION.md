# Jev x Japanese Medical Licensing Examination Benchmark

Research code and reproducibility artifacts for:

**Information Sufficiency and Selective Prediction in a Structured Probabilistic Decision Model: Nine Years of the Japanese Medical Licensing Examination**

This archive contains author-generated source code, derived benchmark results, statistical-analysis outputs, figures, tables, manuscript sources, the Japanese companion translation, and the Japanese terminology guide. It does not redistribute JMedQA question text, examination images, raw provider responses, or API credentials. Users should obtain JMedQA from its upstream source and follow the applicable dataset and Ministry of Health, Labour and Welfare terms.

The primary run evaluated 3,556 option-choice JMedQA items from 2018-2026 after excluding 25 numeric-response items. Exact-set accuracy was 88.58% (3,150/3,556). No images were supplied during inference.

The binary image-presence grouping and the annotation-based `image_dependency` grouping are not identical. One item (2023C074) had auxiliary image metadata and was therefore classified as image-referenced by the metadata-based helper, although its JMedQA `image_dependency` label was `none`. Consequently, the binary no-image group contains 2,582 items, while the annotation-based `none` stratum contains 2,583 items. This does not alter the overall denominator or the annotation-stratified results.

## Software and typesetting

The benchmark and statistical workflow used Python 3.12.10 with the frozen environment in `environment/requirements-lock.txt`, including NumPy 2.5.3, pandas 2.3.3, SciPy 1.18.1, Matplotlib 3.11.2, requests 2.34.2, and datasets 4.8.5. Source control and release preparation used Git and GitHub.

The English and Japanese manuscripts were prepared with python-docx and converted to PDF using LibreOffice Writer 25.2.3.2 (x86_64). The English PDF uses embedded Liberation Serif and Liberation Sans fonts. The Japanese PDF uses embedded Noto Serif CJK JP and Noto Sans CJK JP fonts, with limited fallback glyph coverage from Carlito and Noto Sans CJK HK. The terminology guide uses Noto Serif CJK JP and Noto Sans CJK JP.

The English and Japanese manuscripts are US Letter PDFs of 9 and 10 pages, respectively. The terminology guide is a three-page landscape A4 PDF. The PDFs are PDF 1.7, tagged, and contain embedded font subsets. Figures were produced or revised with Matplotlib-based tooling; the repository visualization script uses 180 dpi PNG output, but the final redesigned figures are not asserted to be byte-identical to a single run of that script, and no explicit Matplotlib font family is claimed for those final figures.

Generative AI tools were used as disclosed in the manuscript for code development, statistical workflow design, literature discovery, language editing, figure redesign, and manuscript drafting. The author reviewed the analyses, numerical results, references, interpretations, and final manuscript and assumes responsibility for the work.

## Licenses

Author-generated code is released under the MIT License. Author-generated manuscript text and figures are released under CC BY 4.0. Third-party datasets, examination content, model outputs, and provider materials are not relicensed by this archive; see `THIRD_PARTY_NOTICES.md`.
