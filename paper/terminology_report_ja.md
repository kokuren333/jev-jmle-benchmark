# 用語レポート：Jev × 日本医師国家試験ベンチマーク

このレポートは、英語・日本語原稿に現れる技術用語を、日本語で「何を意味するか」「本研究ではどう使うか」「誤解しやすい点」の3点から整理したものです。

| 用語 | 日本語での意味 | 本研究での使い方・注意 |
|---|---|---|
| Structured probabilistic decision model | 構造化確率的意思決定モデル | 自由文を生成するのではなく、あらかじめ与えた選択肢に確率を付けて決定を返すモデル、という中立的な記述。Jevのベンダー用語「System One」をそのまま科学分類として採用しないための表現。 |
| System One model | System 1型モデル | TypeSafeがJevに用いる製品・概念上の呼称。KahnemanのSystem 1から借用しているが、独立した学術分類として確立したものではない。論文では引用・説明に留める。 |
| Choice | 選択プリミティブ | Jevに固定選択肢を与え、最も適切な選択肢と各選択肢確率を返させる質問形式。 |
| Choice probability | 選択肢確率 | Jevが各候補に返す確率。生成LLMのtoken log probabilityとは別物なので「内部確率」「token probability」と同一視しない。 |
| Confidence | 確信度 / 信頼度 | モデルが返すconfidenceフィールド。確率と関連するが、どのように算出されるかが完全公開されていない場合は「返却confidence」と表現する。 |
| Calibration | 確率校正 | 0.8と予測した事例が長期的に約80%正しい、というように予測確率と実際の頻度が一致する性質。高いaccuracyと同義ではない。 |
| Reliability diagram | 信頼度図 / 校正曲線 | confidence binsごとの平均予測確率と実測正答率を比較する図。対角線に近いほど校正が良い。 |
| ECE (Expected Calibration Error) | 期待校正誤差 | confidence binごとの予測確率と実測正答率のずれを、binの件数で重み付け平均したもの。小さいほど良い。binning依存なので単独で過大評価しない。 |
| MCE (Maximum Calibration Error) | 最大校正誤差 | 最もずれの大きいbinにおける校正誤差。ECEより局所的な最悪ケースを見る。 |
| NLL (Negative Log-Likelihood) | 負の対数尤度 | 正解選択肢にどれだけ確率を置いたかを評価するproper scoring rule。自信満々の誤答を強く罰する。小さいほど良い。 |
| Brier score | ブライアスコア | 予測確率分布と正解one-hot分布の二乗誤差。accuracyだけでなく確率の質も評価する。小さいほど良い。 |
| AUROC | ROC曲線下面積 | confidenceが「正解」と「不正解」をどれだけ区別できるかを0.5〜1で評価。0.5はランダム、1は完全識別。校正そのものではなくdiscriminationの指標。 |
| Discrimination | 識別能 | confidenceが正答と誤答の順位をうまく分ける能力。calibrationとは別概念。 |
| Selective prediction | 選択的予測 | 高confidenceの問題だけモデルが答え、低confidenceは人間や上位モデルに回す運用。 |
| Abstention | 回答保留 / 棄権 | confidence不足時に自動回答しないこと。selective predictionの実装概念。 |
| Coverage | カバレッジ | 全問題のうちモデルが「回答する」とした割合。thresholdを高くすると通常はcoverageが下がる。 |
| Selective accuracy | 選択的正答率 | 回答した問題だけに限定したaccuracy。coverageと必ずセットで示す。 |
| Risk–coverage curve | リスク・カバレッジ曲線 | confidence順に受け入れる問題を増やしたときの誤答率（risk）とcoverageのtrade-offを示す。 |
| Risk | リスク | 本稿のrisk–coverageでは「受理した回答の誤答率」。臨床的harmそのものを意味しない。 |
| Exact-set accuracy | 集合完全一致正答率 | 複数選択で予測集合がgold集合と完全に同じ場合だけ正解とする厳格な指標。 |
| Top-k | 上位k個選択 | 複数選択で確率上位k個を予測集合にする手法。本研究ではkは正答個数。Choiceは排他的分布のため、multilabel確率モデルとしては理論的制約がある。 |
| Multilabel classification | 多ラベル分類 | 複数の選択肢が同時に正しい分類問題。互いに排他的なmulticlass分類とは異なる。 |
| Multiclass | 多クラス分類 | 正解が1つだけの排他的選択問題。単一選択JMLE問題はこの形式に近い。 |
| Noul | Jevの二値判断プリミティブ | ある命題がtrueかfalseかを確率で返す形式。複数選択問題を各選択肢ごとに独立評価する感度分析に適する可能性がある。 |
| Image-withheld | 画像非提示 | 本来画像に関連する問題で、モデルには画像を与えずテキストだけを入力した条件。multimodal評価ではない。 |
| Image dependency | 画像依存度 | JMedQAのannotation。none / enough text / not enough text / image question / image only。視覚情報がどれだけ必要かを示す。 |
| Modality gap | モダリティ差 | text-onlyとtext+imageなど、入力モダリティの違いによる性能差。今回の研究は真のpaired modality gapではなく、主にimage-withheld条件の層別解析。 |
| Missing information | 情報欠損 | 解答に必要な画像等が入力に含まれないこと。accuracy低下が「医学知識不足」か「入力不足」かを区別する観点。 |
| JMLE / NMLE | 日本医師国家試験 | 英文ではJapanese Medical Licensing Examination (JMLE)が分かりやすい。NMLEはNational Medical Licensing Examinationの一般表現で他国と混同し得る。 |
| JMedQA | 日本医師国家試験由来QAデータセット | 2018–2026年のJMLEを構造化し、画像依存度や診療領域等を付与したbenchmark dataset。 |
| Benchmark | ベンチマーク | 一定条件でモデル性能を比較・測定する評価課題。実臨床能力そのものではない。 |
| Training-data contamination | 学習データ汚染 | 評価問題がモデル学習データに含まれていた可能性。公開国試では特に除外できず、高得点が純粋な推論能力だけとは限らない。 |
| External validity | 外的妥当性 | ベンチマーク結果が実臨床や別datasetへ一般化できる程度。国試MCQから臨床へ直接一般化するのは危険。 |
| Internal validity | 内的妥当性 | 実験条件内で測定が正しく行われている程度。dataset parsing、scoring、固定model build等が関係する。 |
| Causal effect | 因果効果 | 「画像を消したから何ポイント下がった」と言うには同一問題のpaired intervention等が必要。今回のbinary群は別問題集合なので因果推論ではない。 |
| Association | 関連 | 画像関連群の方がaccuracyが低い、という観察的差。原因を一意に断定しない表現。 |
| Wilson 95% CI | Wilson法95%信頼区間 | 二項割合（正答率）のCI。単純なnormal approximationより小標本や極端な割合で安定しやすい。 |
| Newcombe CI | Newcombe法信頼区間 | 2つの割合の差の信頼区間。画像条件間のpercentage-point差に使用。 |
| Percentage point (pp) | パーセンテージポイント | 91.8%と80.2%の差は11.6%。相対11.6%ではなく11.6 percentage points。 |
| Risk ratio | リスク比 | 2群の割合の比。本研究ではaccuracy比等として使えるが、因果的risk ratioと解釈しない。 |
| Odds ratio | オッズ比 | 正解oddsの群間比。割合差が大きいと直感とずれるため、主結果ではpercentage-point差を優先。 |
| Cohen's h | 割合差の効果量 | 2つの比率をarcsine変換して差を標準化する指標。補助的効果量。 |
| Chi-square test | カイ二乗検定 | 大きな分割表で正答/誤答の割合差を検定する。 |
| Fisher exact test | Fisherの正確確率検定 | 小標本でも使える2×2割合比較。image onlyのようなnが小さい層で適する。 |
| Mann–Whitney U test | Mann–WhitneyのU検定 | 分布形を強く仮定せず、2群のlatency分布を比較するrank-based test。 |
| Spearman correlation | Spearman順位相関 | 年度とaccuracyの単調関係を順位で評価。年数が9点しかないためpowerは限定的。 |
| Multiple comparisons | 多重比較 | 多数の診療科を個別検定すると偶然の有意差が増える問題。 |
| Benjamini–Hochberg FDR | BH法による偽発見率制御 | 多重比較で「発見」とした結果に含まれるfalse positive割合を制御する手法。 |
| Wall-clock latency | 実時間レイテンシ | API送信直前からresponse受信完了までの実測時間。モデル純粋推論時間だけでなくnetworkやgateway等を含む。 |
| p50 / median | 50パーセンタイル / 中央値 | 半数のrequestがこの時間以下。latency代表値としてmeanより外れ値の影響が少ない。 |
| p95 latency | 95パーセンタイルレイテンシ | 95%のrequestがこの値以下。tail latencyを見る指標。 |
| API cost | API利用料金 | このrunでgatewayが記録した課金額。ハードウェア計算コストそのものではない。 |
| Official-style reconstruction | 公式試験風再構成 | 公開されたJMLE配点・基準に近づけて得点を再計算したもの。公式合否そのものではない。 |
| Contraindicated choice / prohibited choice | 禁忌肢 | 選択数が一定以下であることがJMLE合格要件の一部。具体的な禁忌肢のidentityは公開されないためモデルの正式合否は確定できない。 |
| Conservative lower bound | 保守的下限 | 欠損・非評価問題をモデルに有利に仮定せず、最低限得られる点として計算した得点下限。 |
| Prospective validation | 前向き検証 | threshold等を決めた後、未使用の新しいdataで性能を確認すること。安全性主張には重要。 |
| Held-out calibration set | 独立校正用データ | confidence thresholdやcalibration mappingを決める専用subset。test setと分ける。 |
| Reproducibility | 再現可能性 | model ID、build、dataset hash、script、raw outputs、environment等を残し、同じ解析を再現できる性質。 |
| Stability / repeatability | 安定性 / 反復再現性 | 同じ入力を複数回投げたときに選択と確率がどの程度変わらないか。今回未測定で、追加実験候補。 |
| Closed model | 閉鎖モデル | weightsやtraining dataが公開されず、API経由でのみ利用するモデル。contamination監査やarchitecture検証に制約がある。 |
| Clinical competence | 臨床能力 | 実際の患者診療で必要な総合能力。MCQ正答率とは同義ではない。 |
| Clinical decision support | 臨床意思決定支援 | 医療従事者の診断・治療判断を支援する用途。本研究はこれを直接検証していない。 |
| Script Concordance Test (SCT) | スクリプト・コンコーダンス・テスト | 不確実な臨床状況で新情報が判断をどう変えるかを評価する試験形式。静的MCQより臨床推論の一面を測りやすい。 |
