# 構造化確率的意思決定モデルの日本医師国家試験9年分における評価：正答率、視覚情報欠損、確率校正、選択的予測、レイテンシ、コスト

**Ren Matsushita, MD**  
独立研究者（Independent Researcher）

**原稿状態：** v0.2 完全稿ドラフト。主要ベンチマークは完了済みだが、査読前であり、感度分析の追加余地がある。

## 要旨

### 背景
大規模言語モデル（LLM）は、米国および日本の医師国家試験で合格水準に到達している。しかし、国家試験正答率のみでは、不確実性、情報欠損時の挙動、実運用レイテンシ、コストを十分に評価できない。Jevは自由文を生成せず、あらかじめ与えられた選択肢に対して選択結果と各選択肢の確率を返す、テキスト入力型の構造化意思決定モデルである。

### 目的
2018〜2026年の日本医師国家試験由来問題を用い、Jevの正答率、視覚情報欠損への感受性、返却確率の有用性、選択的予測、レイテンシ、APIコスト、および公式得点基準の保守的再現を評価する。

### 方法
JMedQA 3,581問のうち、数値入力25問を除外し、選択式3,556問を対象とした。`typesafe/jev-1.13`（実返却build `typesafe/jev-1.13-20260917`）をOpenRouter Decisions API経由で評価した。単一選択はtop-1、複数選択は正答数kに応じたtop-kを用い、集合完全一致で採点した。画像なし相当2,582問と、画像参照・画像非提示974問を別々に実行し、重複推論せず統合した。正答率にはWilson 95%信頼区間を付与した。JMedQAの`image_dependency`（none / enough text / not enough text / image question / image only）を用いて画像依存度別に解析した。確率校正はChoice確率の意味が明確な単一選択3,097問に限定し、NLL、multiclass Brier score、ECE、正誤判別AUROC、risk–coverage曲線を評価した。API wall-clock latency、token usage、実測costも保存した。第112〜120回について厚生労働省の公開得点基準を用い、禁忌肢が非公開であることを明示したうえで公式試験風再構成を行った。

### 結果
全3,556問中3,150問に正解し、正答率は**88.58%**（Wilson 95% CI 87.50–89.59%）であった。画像なし相当は91.75%（2,369/2,582）、画像参照・画像非提示群は80.18%（781/974）で、差は−11.57 percentage points（95% CI −14.28〜−8.85）であった。ただし両群は同一設問のpaired比較ではない。画像依存度別では、`none` 91.75%（2,370/2,583）、`enough text` 92.09%（617/670）、`not enough text` 59.30%（102/172）、`image question` 49.19%（61/124）、`image only` 0%（0/7）であった。`enough text` は`none`とほぼ同等（差+0.34 pp、95% CI −2.16〜+2.47）であった。単一選択では、top-choice probabilityによる正誤判別AUROCは0.918、10-bin ECEは0.014であった。確率0.90以上のみ回答する事後的ルールではcoverage 68.5%、selective accuracy 99.01%（2,121件中21誤答）であった。全体median latencyは820.7 ms、p95は1,061.0 msで、全3,556問の記録上のAPIコストは約US$0.120であった。第112〜120回の全年度で、保守的下限得点は公開された必修および一般・臨床得点基準を上回ったが、禁忌肢の具体的内容が非公開のため正式な合否は判定不能とした。

### 結論
Jevは、日本医師国家試験9年分の選択式問題に対して高いベンチマーク正答率を示し、テキスト情報が十分な画像関連問題では性能が維持された一方、視覚情報が必要な設問では大きく低下した。返却されたChoice確率は単一選択問題の正誤を強く識別し、選択的予測に利用可能な可能性を示した。ただし、これは国家試験形式の制約されたQA性能であり、臨床能力や自律的安全性を示すものではない。

**キーワード：** 日本医師国家試験、医療QA、不確実性、確率校正、選択的予測、意思決定モデル、医療AI

## 1. Introduction / 序論

医師国家試験は、LLMの医学知識を評価する代表的ベンチマークとして広く用いられてきた。日本ではTanakaらがGPT-4を第116・117回医師国家試験で評価し、prompt optimization後に合格水準の得点を報告した[1]。MiyazakiらはGPT-4oを第118回全400問で評価し、画像を実際に提示した条件で全体93.2%の正答率を報告している[2]。

しかし、最先端モデルが国家試験で高得点を得る現在、「合格できるか」だけでは医療AIの性質を十分に区別できない。MedHELMは国家試験が実臨床の多様な業務を反映しないことを明示し[6]、HealthBenchも現実的な医療対話や専門家基準へ評価軸を広げている[7]。また、医療QAではモデルのconfidenceが実際の正答率と一致するかが安全性上重要であり、生成LLMでは自己申告confidenceよりtoken probabilityの方が正誤識別に優れるとの報告がある[5]。

Jevは従来の生成LLMとは異なり、自由文を生成せず、固定選択肢に対する選択結果・各選択肢確率・confidenceを構造化出力する[11]。TypeSafeはこれを「System One model」と呼ぶが、本稿ではベンダー独自の分類を科学的事実として採用せず、**structured probabilistic decision model（構造化確率的意思決定モデル）**と呼ぶ。

JMedQAは2018〜2026年の日本医師国家試験を構造化し、画像依存性を`none`、`enough text`、`not enough text`、`image only`、`image question`に分類している[3]。これにより、「画像が付いているか」ではなく、「画像情報がなくても本文だけで回答可能か」という情報欠損の程度に沿ってモデル挙動を解析できる。

### Research Questions

**RQ1：** Jevは2018〜2026年の日本医師国家試験選択式問題に対し、どの程度の正答率・レイテンシ・APIコストを示すか。

**RQ2：** 画像を与えないtext-only条件で、画像依存度が高まるにつれて正答率はどのように変化するか。また`enough text`では性能が維持されるか。

**RQ3：** Jevが返す各選択肢確率は正誤を識別し、校正された不確実性指標またはselective predictionの基礎として利用できるか。

**RQ4：** 年度、診療領域、回答数kで性能はどの程度変動し、第112〜120回の公開得点基準を保守的再構成した場合にどのような結果となるか。

本研究の新規性は「AIが国試に合格した」という点ではなく、**非生成型の構造化decision modelを、9年分・画像依存度・native probability・selective prediction・latency/costを統合して評価すること**にある。

## 2. Methods / 方法

### 2.1 Study design and dataset

公開データを用いたretrospective benchmark studyとした。JMedQAは第112〜120回（2018〜2026年）の3,581問を含む[3]。数値入力25問を除外し、選択式3,556問を解析した。現行データでは選択式はいずれも5択であった。正答数は1個3,097問、2個368問、3個90問、4個1問である。計算問題でも選択式なら除外しなかった。

### 2.2 Model and inference

`typesafe/jev-1.13`をOpenRouter Decisions API経由で使用した。レスポンスに記録されたbuildは`typesafe/jev-1.13-20260917`、providerはTypeSafeであった。各設問では問題文と元の選択肢を提示し、Choiceの返却確率を保存した。医師役割prompt、CoT、few-shot、RAG、検索は用いなかった。

### 2.3 Scoring

単一選択はtop-1、複数選択は正答個数kに応じたtop-kとし、予測集合とgold集合の完全一致を正解とした。ただしChoiceはmutually exclusiveな分布であるため、複数選択問題をmultilabel probabilityとして解釈することは理論的に不適切である。このためprobability calibrationは単一選択に限定した。

### 2.4 Image conditions

Jevはtext-onlyであり、画像そのものは一切入力していない。画像なし相当2,582問と画像関連・画像非提示974問を別runで評価し、後処理で統合した。主要な視覚情報欠損解析ではJMedQAの`image_dependency`を直接使用した。1問（2023C074）はbinary helper上で画像関連とされた一方`image_dependency=none`であり、metadata discordanceとして記録した。

### 2.5 Statistical analysis

正答率にはWilson 95% CIを使用。binary image conditionの差はNewcombe CIおよびχ²検定、画像依存度別の小標本比較にはFisher exact test、latency比較にはMann–Whitney U、年度trendにはSpearman相関を用いた。診療領域の探索的比較にはBenjamini–Hochberg FDR補正を行った。

単一選択のみについてNLL、multiclass Brier score、10-bin ECE、top-choice probabilityによるcorrectness AUROC、reliability curve、risk–coverage curveを算出した。confidence thresholdによる選択的予測は同一dataset内の事後解析であり、prospective safety guaranteeとはみなさない。

### 2.6 Official-style reconstruction

厚生労働省が公開した第112〜120回の年度別合格基準を用いた。非選択式問題および年度ごとの採点除外は得点区間として保守的に扱った。禁忌肢の具体的選択肢が公開されないため、正式合否はすべて判定不能とした。

## 3. Results / 結果

### 3.1 Overall accuracy

3,556問中3,150問正解、88.58%（95% CI 87.50–89.59%）。単一選択は88.89%、2個選択は86.41%、3個選択は86.67%であった。年度別は85.68〜90.91%で、年度とaccuracyの単調trendは明確でなかった（Spearman rho=0.533, P=.139）。

### 3.2 Missing visual information

画像なし相当91.75%、画像関連・画像非提示80.18%。binary差は−11.57 ppであった。しかしより重要なのはimage_dependency別であり、`none` 91.75%、`enough text` 92.09%、`not enough text` 59.30%、`image question` 49.19%、`image only` 0%であった。`enough text`と`none`の差は+0.34 pp（95% CI −2.16〜+2.47）で、実質的に同程度であった。

### 3.3 Probability quality and selective prediction

単一選択3,097問では、top-choice probabilityによる正誤判別AUROCは0.918、10-bin ECEは0.014であった。threshold 0.90ではcoverage 68.5%、selective accuracy 99.01%（21誤答）、0.95ではcoverage 59.9%、accuracy 99.57%（8誤答）、0.99ではcoverage 43.3%、accuracy 99.85%（2誤答）であった。これは同一データ上の事後的結果であり、外部検証なしに臨床運用thresholdとして用いるべきではない。

### 3.4 Latency and cost

全体median 820.7 ms、p95 1,061.0 ms。画像なしと画像関連群のmedianは820.3 vs 822.6 msで差は明確でなかった（P=.297）。全3,556問でinput tokenは2,858,460、記録上のAPI costは約US$0.120、1,000問あたり約US$0.0338であった。

### 3.5 Official-style reconstruction

第112〜120回の全年度で、必修および一般・臨床の保守的下限得点が各年度の公開得点基準を上回った。ただし禁忌肢の具体的内容は非公開であり、正式合否は判定不能である。

## 4. Discussion / 考察

### 4.1 Principal interpretation

本研究の主結果は、Jevが88.6%という高い国試ベンチマーク正答率を示したこと自体ではない。既存のGPT-4/GPT-4o研究ですでに国試合格水準は示されている[1,2]。より重要なのは、Jevの性能が**入力情報の充足度に応じて規則的に変化し、native probabilityが正誤識別とselective predictionに利用できた**点である。

画像関連問題でも本文のみで十分とannotateされた問題は92.1%で、画像依存なし91.8%とほぼ同じだった。一方、本文のみでは不足する問題では59.3%、画像所見を直接問う問題では49.2%に低下した。この結果は、「画像問題一般が難しい」という説明よりも、「必要情報が入力に含まれないと性能が低下する」という情報可用性の説明と整合する。ただし同一問題を画像あり/なしでpaired評価していないため、画像除去の因果効果とは言えない。

### 4.2 Uncertainty as a potential routing signal

医療LLM研究では、自己申告confidenceよりtoken-level probabilityの方が正誤識別に有用との報告がある[5]。Jevでは確率が生成tokenの副産物ではなく、Choice primitiveの直接出力である。単一選択におけるAUROC 0.918とrisk–coverage曲線は、低confidence例をより大きなLLMまたは人間へ送るrouting signalとして研究価値があることを示す。ただしthreshold 0.90で99%だったという結果は、同じデータでthresholdを観察したpost hoc結果であり、安全性保証にはならない。held-out calibration setを用いたprospective validationが必要である。

### 4.3 Why examination performance is not clinical competence

MedHELMやHealthBenchが強調する通り、医療実務には情報収集、鑑別、治療計画、患者とのコミュニケーション、文書化、状況変化への対応などが含まれる[6,7]。Script Concordance Test系の研究も、不確実な状況で新情報によって判断を更新する能力を評価する[8]。したがって本研究から「Jevが臨床判断を88.6%正しく行える」と解釈することはできない。

### 4.4 Adversarial review of our own claims

最も強い反論は、「公開済み国試問題を閉鎖モデルに解かせただけであり、training contaminationを除外できない」というものである。これは正しい。2018〜2026で新しい年度ほど明確に低下するtrendは認めなかったが、それは汚染がない証拠ではない。training dataが非公開である以上、prospective/embargoed itemsが必要である。

第二の反論はmultiple-answer top-kである。Choiceの確率は排他的選択肢分布であり、「2つ正しい」というmultilabel taskに直接対応しない。したがって複数選択のexact-set accuracyは順位情報としては意味がある一方、確率校正を論じるべきではない。投稿前に各選択肢を独立Noulで判定するsensitivity analysisを追加したい。

第三に、同一条件のLLM baselineがない。GPT-4o等の既報とはdataset、年度、prompt、画像入力条件が異なるため、Jevがより優れている/劣っているとは言えない。新規性はaccuracy rankingではなく、structured decision + probability + operational characteristicsに置くべきである。

### 4.5 Limitations

closed modelでtraining data不明、単一build・単一時点、repeated inferenceなし、直接baselineなし、multimodal入力なし、binary image groupsがnonpaired、JMedQA annotationに小規模な誤差の可能性、1件のmetadata discordance、thresholdがin-sample、multi-answer確率解釈の制約、禁忌肢非公開による正式合否不能、という限界がある。

## 5. Conclusion / 結論

Jevは日本医師国家試験9年分の選択式問題で高い正答率を示し、本文情報が十分な場合は画像関連問題でも性能を維持したが、必要な視覚情報が欠けると大幅に低下した。単一選択では返却Choice probabilityが正誤を強く識別し、選択的予測の研究対象として有望であった。ただし本結果は国試形式のclosed-ended QA性能であり、臨床能力や自律的運用の安全性を意味しない。

## データ・コード公開方針

GitHubに解析コード・manifest・再現手順を公開し、versioned releaseをZenodoに保存してDOIを付与することを推奨する。モデルレスポンスの再配布可否とJMedQA/厚生労働省資料の利用条件は公開前に再確認する。

## Funding
外部研究費なし。

## Competing interests
TypeSafe、OpenRouter、JMedQA開発者等との利益相反がない場合：「著者は開示すべき利益相反を有しない。」

## Author contributions
Ren Matsushita: Conceptualization, Methodology, Software, Formal Analysis, Investigation, Visualization, Writing – Original Draft, Writing – Review & Editing.

## 生成AI利用の開示（暫定）
生成AIをコード開発、統計解析案、文献探索、原稿言語編集の補助として使用した。著者が解析と出典を確認し、最終原稿の責任を負う。投稿先の最新ポリシーに合わせて最終文言を調整する。

## 参考文献
`references.md`参照。
