# Terms / licensing / limitations checklist (2026-09-19確認用)

これは法的助言ではありません。公開前に現行規約を再確認してください。

## OpenRouter
- OpenRouter Terms (2026-08-31版) は利用者に適用Model Termsの遵守を要求。
- 無断red teaming、サービスのscraping/copying、競合API開発等は禁止。
- 本パッケージは通常のAPI推論による性能評価のみを行い、jailbreak/red-team、reverse engineering、蒸留・模倣用データ生成を目的としない。
- API keyをリポジトリ/結果に保存しない。

## TypeSafe / Jev
- TypeSafe公開Terms (2026-09-14版) は少なくとも同社Siteについての利用条件。今回確認できた公開文面だけから、第三者API経由のベンチマーク結果公開について包括的な権利保証までは断定しない。
- OpenRouter上のJev model pageはJevをrouting/classification等のstructured decisions用途として案内している。
- ホワイトペーパー公開直前にOpenRouterのModel TermsリンクとTypeSafeの最新規約を再確認し、必要ならTypeSafeに書面確認するのが最も堅い。

## Dataset
- JMLE2026-Bench: code MIT, dataset CC BY 4.0、原典は厚労省公開資料由来とリポジトリが説明。
- JMedQA: dataset cardはlicenseを `other` とし、厚労省の適用利用条件に従うよう明記。ここでは補助metadata用途に限定。
- 問題文そのものをホワイトペーパー本文へ大量転載せず、集計値とquestion ID中心にする。

## Medical interpretation
研究ベンチマークであり、臨床診断性能・患者安全性・医師資格を示すものではありません。

## 規約上の結論（実務的）
2026-09-19時点で確認した公開文面には、通常のAPIを使った非敵対的な精度・速度ベンチマークを名指しで禁止する条項は見当たりません。TypeSafe Termsの自動取得禁止や新製品開発禁止は文言上 `Site` を対象としており、本スクリプトはTypeSafe Siteをスクレイピングせず、OpenRouterが提供する正規APIだけを利用します。ただしOpenRouterはModel Termsへの遵守を利用者責任としているため、論文・ホワイトペーパー公開時には最新版を再確認してください。結果公開まで含めて完全な法的確実性が必要なら、TypeSafe/OpenRouterへの書面確認が最も安全です。
