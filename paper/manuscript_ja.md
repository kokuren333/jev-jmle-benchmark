**日本医師国家試験9年分を用いた構造化確率的意思決定モデルの評価  
- 情報充足度と選択的予測に着目した解析 -**

**Ren Matsushita, MD**

独立研究者

プレプリント原稿 - 2026年9月

# **要旨**

**背景：**医師国家試験の正答率だけでは、最新の医療AIの特性を十分に区別しにくくなっている。実運用を考えるうえでは、必要情報が欠けたときに性能がどう変わるか、返却確率が誤答の識別に使えるか、不確実な例だけを上位系へ回せるかが重要である。

**目的：**構造化確率的意思決定インターフェースを持つJevを、日本医師国家試験由来9年分の問題で評価し、とくに情報充足度、選択的予測、正答率、レイテンシ、APIコストを明らかにする。

**方法：**2018-2026年のJMedQA
3,581問から数値回答25問を除外し、選択式3,556問をtypesafe/jev-1.13で評価した。JMedQAが付与したimage_dependency（none、enough
text、not enough text、image question、image
only）を情報充足度の層別に用いた。画像は入力せず、テキスト評価用questionフィールドを使用した。確率解析は単一選択3,097問に限定し、5-fold
held-out感度解析を含む選択的予測を評価した。

**結果：**全体の完全一致正答率は88.58%（3,150/3,556、95% CI
87.50-89.59%）であった。画像依存なしは91.75%、画像参照があっても本文のみで解答可能と注釈されたenough
textは92.09%であった。一方、本文だけでは情報不足のnot enough
textは59.30%、画像所見を直接問うimage
questionは49.19%まで低下した。単一選択ではtop-choice
probabilityによる正誤識別AUROCは0.918で、5-fold
held-out感度解析では67.6%を受理し99.00%が正解であった。API wall-clock
latency中央値は820.7
ms、3,556回の記録上のAPI総コストはUS\$0.120であった。

**結論：**最も重要な結果は「国試に合格した」ことではなく、性能が入力情報の充足度と整合して変化したことである。固定選択肢の限定タスクでは、必要情報が本文に含まれる例を低コストに処理し、確率を用いて不確実例を上位モデルや人間へ回す一次判断層として研究価値がある。ただし臨床能力や自律運用の安全性を示すものではない。

キーワード：日本医師国家試験、JMedQA、医療AI、不確実性、選択的予測、情報充足度、確率校正

# **1. はじめに**

医師国家試験は医療AIの標準的ベンチマークとして広く用いられている。GPT-4やGPT-4oはすでに日本医師国家試験で合格水準または高い正答率を示しており\[1,2\]、「AIが国試に受かるか」という問いだけでは、現在の高性能モデルの違いを十分に表現しにくい。

実運用に近い評価では、入力に必要情報がそろっているかを識別できること、不確実性が誤答の発見に役立つこと、容易で自信の高い例だけを安価に処理して難しい例を人間や高性能モデルへ回せることが重要になる。MedHELMやHealthBenchも、単純な試験正答率だけでは臨床タスクの多様性を捉えられないことを強調している\[6,7\]。

Jevは一般的な生成LLMとは運用上のインターフェースが異なり、固定された選択肢に対して選択結果と各選択肢の確率を返すChoice機能を持つ\[11,12\]。本稿では、この入出力形式を表す記述的名称として「構造化確率的意思決定モデル」と呼ぶ。これは非公開の内部アーキテクチャに関する主張ではない。

本研究で重要なのがJMedQAのimage_dependencyアノテーションである。JMedQAは単に「画像が付いているか」だけでなく、画像依存なし、画像参照はあるが本文だけで解答可能、本文だけでは情報不足、画像所見・画像診断を直接問う、ほぼ画像参照のみ、という層別を提供している\[3\]。したがって、画像問題一般の難しさではなく、「テキスト入力に解答に必要な情報が残っているか」というより具体的な問いを検討できる。

そこで本研究では、(1)
9年分のJMLE由来選択式問題における正答率と運用指標、(2)
JMedQAが定義した情報充足度と性能の関係、(3) native
probabilityが誤答識別と選択的予測に使えるか、(4)
年度別安定性と公式得点基準の保守的再構成、を評価した。

# **2. 方法**

## **2.1 研究デザインと解析対象**

厚生労働省が公開する日本医師国家試験資料をもとに構築されたJMedQAを用いた後ろ向きベンチマーク研究である。対象リリースには第112-120回（2018-2026年）の3,581問が含まれた。Jev
Choiceは定義済み選択肢を必要とするため、数値回答25問を除外し、選択式3,556問を解析した。内訳は単一選択3,097問、複数選択459問であった\[3\]。

## **2.2 JMedQAの画像依存度アノテーションとテキスト入力**

本研究の中心となる情報充足度解析には、JMedQAがデータセット側で付与したimage_dependencyを用いた。これらのラベルをJevの回答から後付けで推定したわけではない。JMedQAの定義では、noneは画像依存なし、enough
textは画像参照があるが本文テキストのみで解答可能、not enough
textは画像参照があり本文だけでは情報不足、image
questionは画像所見・画像診断・視覚的解釈などを直接問う問題、image
onlyは問題文の大部分が画像参照でテキスト情報がほとんどない問題を意味する\[3\]。

JMedQAには、明示的な画像参照表現を残したquestion_rawと、テキストのみの評価用に画像参照表現を削除したquestionが用意されている。image_dependencyがnone以外では、question_rawから画像参照句を削除するdeletion-only
policyでquestionが作成されている\[3\]。本研究ではquestionフィールドを入力し、画像は一切提示しなかった。したがって本解析は、同一問題から画像を取り除いたpairedな因果実験ではなく、JMedQAが事前に付与した「本文だけで情報が足りるか」という分類ごとのテキスト-only性能比較である。

<img src="/mnt/data/_pandoc_ja/media/image1.png"
style="width:6.2in;height:3.97942in" />

図1．研究フローとJMedQAのimage_dependency層別。ラベルはJMedQAが付与したものであり、本研究のモデル出力から生成したものではない。推論時に画像は入力していない。

## **2.3 モデルと推論**

OpenRouter Decisions API経由で固定route
typesafe/jev-1.13を使用し、返却されたserving
buildはtypesafe/jev-1.13-20260917であった。role
prompting、chain-of-thought要求、few-shot例、検索、外部医学資料は用いなかった。選択結果、各選択肢確率、モデル情報、token使用量、記録上のコスト、wall-clock
latencyを保存した。

## **2.4 採点と確率解析**

単一選択は最大確率の選択肢で採点した。複数選択は正答数kに応じてChoice確率の上位k個を選び、正答集合との完全一致を正解とした。ただしChoiceの確率分布は排他的選択肢を想定しており、複数正答のmultilabel確率ではない。このため確率品質・校正・選択的予測の解析は単一選択に限定した。

単一選択ではnegative log loss、multiclass Brier score、10-bin expected
calibration error（ECE）、top-choice
probabilityによる正誤識別AUROC、risk-coverage曲線を算出した。同一データで閾値を選ぶことによる楽観を減らすため、5-fold感度解析を行った。各foldで残り4
foldから受理群正答率99%以上となる最低閾値を選び、held-out
foldに適用した。これは内部感度解析であり外部検証ではない。

## **2.5 統計解析と公式試験風再構成**

正答率の95%信頼区間はWilson法を用いた。別問題群間の差はNewcombe区間とchi-squareまたはFisher
exact test、latencyはMann-Whitney U
testを用いた。年度別の単調trendは年度集計値に対するSpearman順位相関で探索した。厚生労働省の各年度の公開得点基準を用いて保守的な公式試験風得点再構成を行ったが、禁忌肢の具体的選択肢が非公開であるため正式合否は判定しなかった。

## **2.6 倫理・透明性・再現性**

公開試験由来の資料のみを用い、患者情報・研究参加者データを含まないため、倫理審査委員会への申請は行わなかった。コード、派生結果、統計解析スクリプト、環境情報、原稿資料はプロジェクトリポジトリで公開する。試験問題本文および画像は再配布しない。

# **3. 結果**

## **3.1 全体性能と運用指標**

選択式3,556問中3,150問が正解で、完全一致正答率は88.58%（95% CI
87.50-89.59%）であった。API wall-clock latency中央値は820.7
ms、p95は1,061.0 msであった。記録されたinput
tokenは2,858,460、3,556回のAPI総コストはUS\$0.120であった。これらはgatewayを含む実測値であり、モデル単体の計算時間や内部計算コストを表すものではない。

**表1．主要ベンチマーク結果**

| **条件**                 | **n** | **正解** | **正答率（95% CI）**  | **中央値** |
|--------------------------|-------|----------|-----------------------|------------|
| 全選択式                 | 3,556 | 3,150    | 88.58%（87.50-89.59） | 820.7 ms   |
| 画像参照なし             | 2,582 | 2,369    | 91.75%（90.63-92.75） | 820.3 ms   |
| 画像参照あり・画像非提示 | 974   | 781      | 80.18%（77.57-82.57） | 822.6 ms   |

なお、二値の画像メタデータ有無による分類と、アノテーションに基づく
`image_dependency` 分類は同一ではない。1問（2023C074）は、補助画像メタデータが存在するため
メタデータベースのヘルパーでは画像参照ありに分類されたが、JMedQA の
`image_dependency` ラベルは `none` であった。そのため、二値の画像参照なし群は2,582問、
アノテーションベースの `none` 層は2,583問となる。この差は全体の分母および
アノテーション別の結果には影響しない。

## **3.2 本質的な差は「画像があるか」ではなく「本文だけで必要情報が足りるか」だった**

画像参照あり群は画像参照なし群より11.57 percentage points低かった（95%
CI -14.28 to
-8.85、P\<.001）。しかし両群は別問題集合であり、この差を「画像を取り除いたことの因果効果」と解釈することはできない。より直接的に解釈できるのがJMedQAのimage_dependency別解析である。none
91.75%とenough text 92.09%はほぼ同等であった（差 +0.34 percentage
points、95% CI -2.16 to +2.47）。一方、not enough textは59.30%、image
questionは49.19%まで低下した。image
onlyは7問すべて誤答であったが、n=7と少数であり推定は不安定である。

ここで重要なのは、enough textやnot enough
textが本研究の結果を見て後付けした分類ではない点である。JMedQA側が「画像参照はあるが本文だけで解答可能」「本文だけでは情報不足」と事前に付与した注釈である\[3\]。したがって今回観察された勾配は、Jevが「画像付き問題一般」に弱いというより、モデルへ与えたテキストに解答へ必要な証拠が含まれているかどうかと性能が整合して変化した、と解釈するのが最も慎重かつ一貫している。

<img src="/mnt/data/_pandoc_ja/media/image2.png"
style="width:6.2in;height:3.30739in" />

図2．JMedQA image_dependency別の完全一致正答率。誤差棒はWilson
95%信頼区間。noneとenough
textがほぼ同等である一方、本文だけでは情報不足と注釈された群で大きく低下している。

**表2．JMedQA image_dependencyの定義と観察された性能**

| **JMedQAラベル** | **データセット上の定義**           | **n** | **正答率** |
|------------------|------------------------------------|-------|------------|
| none             | 画像依存なし                       | 2,583 | 91.75%     |
| enough text      | 画像参照はあるが本文だけで解答可能 | 670   | 92.09%     |
| not enough text  | 画像参照があり本文だけでは情報不足 | 172   | 59.30%     |
| image question   | 画像所見・視覚的解釈を直接問う     | 124   | 49.19%     |
| image only       | 問題文の大部分が画像参照           | 7     | 0.00%      |

## 3.3 返却確率は不確実例を振り分ける信号になり得た

単一選択3,097問の正答率は88.89%であった。top-choice
probabilityによる正誤識別AUROCは0.918、10-bin ECEは0.014、negative log
lossは0.366、multiclass Brier
scoreは0.157であった。ECE単独を「良好な校正」の証明とは解釈しなかった。

事後的にはtop-choice probability 0.90以上を受理するとcoverage
68.5%、受理群正答率99.01%であった。5-fold
held-out感度解析では、calibration側で選ばれた0.90または0.92の閾値をheld-out
foldへ適用し、合計2,093/3,097問（67.6%）を受理、2,072問が正解で99.00%であった。これは単純なin-sample閾値より楽観を減らすが、臨床的に有効な安全閾値を証明するものではない。

<img src="/mnt/data/_pandoc_ja/media/image3.png"
style="width:6.2in;height:3.37899in" />

図3．単一選択問題のrisk-coverage関係。Confidence閾値を上げるほど自動受理する割合は低下する一方、受理群の正答率は上昇した。菱形は5-fold
held-out感度解析の集計点。

## **3.4 年度別性能は概ね安定していた**

年度別完全一致正答率は第115回の85.68%から第118回の90.91%の範囲であった。9年度の集計値に単調trendは明確でなかった（Spearman
rho=0.533、P=.139）。ただしJevはclosed
modelであり、国試過去問は公開情報であるため、この結果から学習データ汚染を否定することはできない。

<img src="/mnt/data/_pandoc_ja/media/image4.png"
style="width:6.2in;height:3.32016in" />

図4．第112-120回の年度別完全一致正答率とWilson
95%信頼区間。破線は9年全体の正答率。

## **3.5 公式試験風得点再構成**

第112-120回の各年度で、必修および一般・臨床の保守的得点下限はその年度の公開得点基準を上回った。これは「公開得点基準を再構成上は上回った」という限定的事実を支持する。しかし禁忌肢の具体的選択肢は非公開であり、数値回答や公式採点調整を受験者と完全同一条件で再現できないため、「Jevが医師国家試験に正式合格した」とは表現しない。

# **4. 考察**

## **4.1 中心的な結果は国試の点数ではなく「情報充足度」である**

本研究で最も解釈価値が高いのは、88.6%という全体正答率そのものではない。画像参照がある問題でも、JMedQAが本文だけで解答可能と注釈したenough
text群は、画像依存なし群とほぼ同じ正答率を維持した。一方、本文だけでは情報不足とされた群や画像所見の直接解釈を要する群では性能が急落した。したがって、「画像問題だから難しい」という粗い説明よりも、「モデルへ与えた入力にその判断へ必要な証拠が含まれているか」が性能境界として現れた、と読む方が結果全体をよく説明する。

ただし、この結果を「画像を消すと何ポイント性能が落ちる」という因果効果として扱うべきではない。各image_dependency群は別問題集合であり、問題難易度や診療領域も異なり得る。本研究で言えるのは、JMedQA作成者が独立に付与したテキスト充足度の分類に沿って、テキスト-onlyの性能が期待される方向に層別化された、ということである。これはJevの能力全般を証明するものではないが、入力情報の十分性がこのインターフェースの実用上の境界条件である可能性を示す。

## 4.2 返却確率の価値は「正しさの保証」ではなく「振り分け」である

もう一つの重要な結果は、Jevが返すChoice
probabilityが単一選択問題の正誤をかなり強く順位づけできたことである。confidenceが高い例だけを受理すると、処理できる問題数は減る代わりに、受理群の誤答率は大きく低下した。5-fold
held-out感度解析でも同様の傾向が残ったため、単一の事後的閾値だけによる見かけの結果ではない可能性が高い。

この性質から想定されるのは、Jev単独による自律的臨床判断ではなく、固定候補が既に定義されている限定タスクの一次ルータである。情報が十分でconfidenceが高い例は低コストに処理し、低confidence例や画像・追加情報を必要とする例を大規模生成モデル、multimodal
model、あるいは人間へ回す。しかし本研究はそのend-to-end
systemを直接比較しておらず、これは今回のベンチマークから生じた設計仮説である。

## **4.3 既存のJMLE・医療LLM研究との位置づけ**

GPT-4やGPT-4oがJMLEで合格水準または高い性能を示すことは既報である\[1,2\]。本研究はそれらとJevの優劣を決める比較ではない。年度、prompt、画像入力条件、モデルクラスが異なるため直接順位づけは不適切である。本研究の新規性は、9年分を通した評価、JMedQAが定義した情報充足度、native
probability、選択的予測、API-levelのレイテンシとコストを同一研究内で評価した点にある。

## **4.4 国試正答率は臨床能力ではない**

国家試験は静的なclosed-ended
taskである。実臨床では、情報収集、鑑別診断の生成・更新、治療計画、患者説明、文書化、時間経過に伴う状態変化への対応が必要になる\[6,7\]。したがって88.6%という国試形式の正答率を「臨床判断を88.6%正しく行える」と読み替えることはできない。選択的予測の結果も臨床運用の安全閾値を意味しない。

## **4.5 敵対的に見た場合の主要な弱点**

**学習データ汚染：**国試問題は公開されており、Jevの学習データは非公開である。記憶を排除できない。最近の年度で性能低下がみられないことも、汚染がない証拠にはならない。

**複数選択の意味論：**排他的Choice分布をtop-kして複数正答問題に用いるのはmultilabel確率モデルとして厳密ではない。このため確率解析は単一選択に限定した。各選択肢の独立binary判定による感度解析が望ましい。

**matched
baselineなし：**同一問題・同一条件で生成LLMを比較していないため、Jevが相対的に速い、安い、高精度とは断定できない。

**closed
APIの再現性：**単一build・限られた回数の評価であり、将来のAPI挙動が同一とは限らない。回答一致率やprobability変動を再実行で確認する必要がある。

**選択的予測の内部検証：**5-fold解析は単純なin-sample閾値より強いが、外部・前向き検証ではない。未公開問題で事前固定した閾値を評価する必要がある。

## **4.6 次に行うべき決定的な実験**

次に価値が高いのは、過去問をさらに増やすことではなく、新規作成または未公開の問題でroutingを前向きに検証することである。別calibration
setでconfidence閾値を事前固定し、低confidence例・画像依存例を大規模multimodal
modelや医師へ送る。そして、全件を最初から大規模モデルへ送る方式と、end-to-end
accuracy、残存誤答、latency、costを比較する。この実験が、今回示唆された一次判断層という役割を直接検証する。

# **5. 限界**

本研究には、closed model 1
build・1時点の評価、学習データ不明、公開国試によるtraining
contaminationの可能性、image_dependency群がpairedでないこと、画像自体を入力していないこと、JMedQAの抽出・注釈に残存誤差があり得ること、複数選択top-kの意味論的限界、同一条件の生成LLM
baselineがないこと、repeatability評価が限定的であること、selective
predictionが内部検証にとどまること、禁忌肢非公開のため正式合否を判定できないこと、という限界がある。

# **6. 結論**

Jevは日本医師国家試験由来9年分の選択式問題で高いベンチマーク正答率を示し、API
wall-clock
latency中央値は1秒未満、記録上のAPIコストは極めて低かった。しかし本研究のより重要な知見は、その性能境界である。画像参照の有無そのものではなく、本文に解答へ必要な情報が十分含まれる場合には性能が維持され、必要な視覚情報が欠ける場合には大きく低下した。またnative
probabilityは単一選択問題の不確実例を振り分ける信号になり得た。これらは、Jevを自律的な臨床判断主体としてではなく、より大きな意思決定システム内の低コストな構造化一次判断層として検討する根拠を与える。

# **開示**

研究費：本研究は外部研究費を受けていない。

利益相反：著者はTypeSafe、OpenRouter、JMedQA開発者その他本研究に関連する開示すべき利益相反を有しない。

データ・コード：コード、派生結果、統計解析スクリプト、環境情報、原稿資料を
https://github.com/kokuren333/jev-jmle-benchmark
で公開する。試験問題本文・画像は再配布せず、JMedQAは原配布元から取得し適用される利用条件に従う。

生成AI利用：生成AIをコード開発、統計解析設計、文献探索、言語編集、図の再設計、原稿作成補助に使用した。著者が解析、数値、参考文献、解釈、最終原稿を確認し、本研究の内容に責任を負う。

著者貢献：Ren Matsushita：Conceptualization, Methodology, Software,
Formal Analysis, Investigation, Visualization, Writing - Original Draft,
Writing - Review & Editing.

# **参考文献**

1\. Tanaka Y, Nakata T, Aiga K, et al. Performance of Generative
Pretrained Transformer on the National Medical Licensing Examination in
Japan. PLOS Digital Health. 2024;3(1):e0000433.
doi:10.1371/journal.pdig.0000433.

2\. Miyazaki Y, Hata M, Omori H, et al. Performance of ChatGPT-4o on the
Japanese Medical Licensing Examination: Evaluation of Accuracy in
Text-Only and Image-Based Questions. JMIR Medical Education.
2024;10:e63129. doi:10.2196/63129.

3\. Yamagishi Y, Kobayashi K, Shibaki R, Aizawa A, Kurohashi S. JMedQA:
Benchmarking Large Language Models and Vision-Language Models on the
Japanese Medical Licensing Examination. Hugging Face dataset. 2026.
https://huggingface.co/datasets/SIP-med-LLM/JMedQA. Accessed June 25,
2026.

4\. Singhal K, Azizi S, Tu T, et al. Large language models encode
clinical knowledge. Nature. 2023;620:172-180.
doi:10.1038/s41586-023-06291-2.

5\. Bentegeac R, Le Guellec B, Kuchcinski G, Amouyel P, Hamroun A. Token
Probabilities to Mitigate Large Language Models Overconfidence in
Answering Medical Questions: Quantitative Study. J Med Internet Res.
2025;27:e64348. doi:10.2196/64348.

6\. Bedi S, Cui H, Fuentes M, et al. Holistic evaluation of large
language models for medical tasks with MedHELM. Nature Medicine.
2026;32:943-951. doi:10.1038/s41591-025-04151-2.

7\. OpenAI. HealthBench: An evaluation for AI systems and human health.
2025.

8\. McCoy LG, Swamy R, Sagar N, et al. Do Language Models Think Like
Doctors? medRxiv. 2025. doi:10.1101/2025.02.11.25321822.

9\. Large language model uncertainty proxies: discrimination and
calibration for medical diagnosis and treatment. 2024. PMCID:
PMC11648734.

10\. Ministry of Health, Labour and Welfare, Japan. Official passing
criteria and answer keys for the 112th-120th Japanese Medical Licensing
Examinations, 2018-2026.

11\. TypeSafe / Jev API documentation. Jev Choice API. Accessed
September 2026.

12\. OpenRouter. TypeSafe: Jev 1.13 model page. Accessed September 2026.
