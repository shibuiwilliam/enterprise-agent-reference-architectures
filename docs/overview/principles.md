---
title: "設計原則"
description: "エンタープライズAIエージェント・アーキテクチャの12箇条の設計原則。"
status: done
---

# 設計原則

> **価値を生むために動かし、壊さないために統べる。** 目的は企業価値の創出であり、統制（権限・組織・監査）はその価値を持続的に生み続けるための土台です。この二重命題がすべての設計原則の根底にあります。

エンタープライズAIエージェント・アーキテクチャを貫く12箇条の設計原則を示します。

## 原則一覧

### 1. エージェントは本人の権限を超えない

実効権限は「能力 ∩ 本人権限 ∩ ポリシー」の最小です。便利さのための全権化を禁じます。

エージェントが万能サービスアカウントで動く設計は危険です。侵害が起きた瞬間、全ユーザー・全 SaaS のデータが一度に危険にさらされます。OBO 委譲で依頼者本人の権限に縮退したトークンを SaaS ごとに取得し、SaaS 側のネイティブ認可で実データアクセスを制約する二段構えが基本形となります。委譲非対応の系では Permission Mirror で権限を近似できますが、あくまでキャッシュであり権威ソースではない点を常に意識してください。

参照：[ID-4 Permission Mirror](../patterns/id-identity/id4-permission-mirror-least-of.md) / [ID-2 OBO](../patterns/id-identity/id2-identity-federation-obo.md)

### 2. 従業員面と顧客面を物理的に分ける

最重大の事故クラス——顧客向けが社内データに到達する（逆も）——を構造的に排除します。

従業員向けと顧客向けが同一の IdP・データストア・ネットワークセグメントを共有すると、一方の脆弱性が他方の面に波及します。IdP とデータストアの物理分離、面間のネットワーク到達性ゼロは初日から確立してください。そうすることで、設計レビューやペネトレーションテストで「面をまたぐ経路が存在しない」ことを証明できるようになります。

参照：[ID-1 二面分離](../patterns/id-identity/id1-workforce-customer-split.md)

### 3. 作らず、寄り添う

SoR を置き換えず、読み、正規手続きで書きます。既存統合資産を再利用します。

Salesforce・Workday・ServiceNow などの SoR は企業の業務データの真実を保持しています。エージェントがこれらを迂回して独自にデータを持つと、整合性の崩壊と二重管理が生じます。エージェントは SoR の API を正規手続きで呼び出し、書き込みは検証済みのドメインサービス経由に限定します。既存の iPaaS フロー（MuleSoft・Workato 等）がある場合は、コネクタを自作せず MCP アダプターでラップして再利用するのが基本方針です。

参照：[RT-6 SoR Write Boundary](../patterns/rt-runtime/rt6-sor-write-boundary.md) / [IN-4 iPaaS Reuse](../patterns/in-integration/in4-existing-ipaas-reuse.md)

### 4. データはコピーする前に疑う

no-copy・JIT・ACL 同梱を既定にし、集約は目的が明確なときだけにします。

全社文書を1つのベクトル DB にコピーして索引化すると、コピーした瞬間に元の ACL が切り離され、権限変更の反映遅延が漏洩に直結します。既定は「コピーしない」（JIT 取得・フェデレーション）とし、コピーが必要な場合は ACL メタデータを同梱して検索時に本人権限でフィルタします。データの集約にはモザイク効果（単体では非機密なデータが組み合わさることで機密情報が推測可能になるリスク）もあります。目的と範囲を絞ることが重要です。

参照：[KM-2 Context Mesh](../patterns/km-knowledge/km2-context-mesh.md) / [KM-1 Access-Controlled RAG](../patterns/km-knowledge/km1-access-controlled-rag.md)

### 5. 組織グラフを唯一の権威に

スコープ・共有・承認・委譲を組織構造から一貫して導きます。

「このエージェントが動かせる範囲はどこか」「誰が承認者か」「メモリのスコープはどこまでか」——これらの問いに一貫した答えを出すには、Workday・Okta・プロジェクト管理ツール等から名寄せした単一の組織マスターが欠かせません。組織グラフを唯一の権威とすることで、異動・昇格・退職といったライフサイクルイベントが、エージェントの権限スコープ・承認チェーン・メモリ階層に自動で反映される仕組みができあがります。

参照：[KM-3 Canonical Object & KG](../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) / [KM-4 Scoped Memory](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)

### 6. プロンプトでなく、アイデンティティとポリシーで守る

安全保証は実行基盤側に置きます。プロンプトはセキュリティ境界になりません。

「機密情報を出力するな」とプロンプトに書いても、プロンプトインジェクションで容易に突破されます。安全の保証は LLM の外側——PDP/PEP によるゼロトラスト認可・OPA/Cedar 等のポリシーコード・DLP によるマスキング——に置きます。ポリシーをコードとして管理すれば、変更履歴・テスト・CI/CD による自動検証が可能になり、組織全体でのポリシー一貫性も担保できるようになります。

参照：[ID-7 Policy-as-Code](../patterns/id-identity/id7-policy-as-code-guardrail.md) / [ID-6 Zero-Trust](../patterns/id-identity/id6-zero-trust-pdp-pep.md)

### 7. すべての行為を三者で帰責する

人＋エージェント＋システムを相関 ID で貫き企業横断で監査します。

エージェントの操作が「サービスアカウントが実行した」としか記録されなければ、インシデント調査で誰が依頼し何が起きたかを追跡できません。すべての行為に「依頼者（人間）・実行主体（エージェント/ワークロード）・対象システム」の三者を相関 ID で紐付けて記録します。三者帰責の監査証跡はコンプライアンス監査・インシデント対応・責任追跡の基盤となります。後付けでの導入は極めて困難なため、初日から設計に組み込んでください。

参照：[OB-2 Unified Audit](../patterns/ob-observability/ob2-unified-audit-lineage.md) / [OB-1 Observability Lake](../patterns/ob-observability/ob1-observability-lake.md)

### 8. 中央はガードレールと舗装路を、部署は業務ロジックを

集権と分権の二層統治です。中央がインフラ・認可・監査・評価を、部署がドメイン知識・ユースケースを持ちます。

中央プラットフォームチームが Gateway・IdP 連携・モデル Gateway・監査基盤・評価パイプラインを整備し、部署はその上にドメイン固有のエージェントテンプレート・業務ロジック・ユースケースを構築します。中央が全業務ロジックを抱えると部署の機動性が失われ、逆に部署が独自にインフラを立てるとガバナンスが崩壊します。テンプレート工場パターンを活用すれば、中央が安全なひな形を提供し、部署がパラメータを埋める形の分業が成り立ちます。

参照：[GV-3 Department Factory](../patterns/gv-governance/gv3-department-agent-factory.md) / [GV-1 Control Plane](../patterns/gv-governance/gv1-agent-control-plane.md)

### 9. 自然言語はUIであり内部プロトコルではない

作用は必ず構造化コマンドへ変換します。自然言語のまま API に渡しません。

LLM が生成した自然言語をそのまま下流システムに渡すと、意図の曖昧さ・インジェクション・再現不能という三重の問題が生じます。ユーザーの自然言語入力は Gateway で受け取り、LLM が意図を解釈した後、actor・target_system・action・params を持つ構造化コマンド（Command Envelope）に変換します。構造化されたコマンドはポリシー評価・監査記録・冪等性保証の対象にできるため、企業システムとの統合に必要な決定論性が確保できます。

参照：[RT-5 Command Envelope](../patterns/rt-runtime/rt5-command-envelope.md) / [IN-2 SaaS Adapter](../patterns/in-integration/in2-saas-connector-adapter.md)

### 10. エージェントは「業務キューを処理する管理されたデジタル業務主体」

チャットボットではなく、登録・監査・権限制御・評価され続ける実行主体として設計します。

エージェントは agent_id・owner_department・risk_tier・allowed_tools・cost_budget 等の属性を持つ、企業内の一級オブジェクトです。コントロールプレーンに登録されていないエージェントは実行を許可されません。登録済みのエージェントは継続的に評価・監査・コスト管理の対象となります。この設計によってエージェントの増殖を統制し、「誰が・いつ・どのエージェントを・どの権限で動かしたか」を企業横断で把握できるようになります。

参照：[RT-9 Work Queue](../patterns/rt-runtime/rt9-work-queue-agent.md) / [GV-1 Control Plane](../patterns/gv-governance/gv1-agent-control-plane.md)

### 11. AIを賢くするより、企業の境界内で安全に働けるようにする

知能は前提、勝負は権限・統合・統治です。

LLM の能力向上はモデルベンダーが担います。エンタープライズアーキテクトが設計すべきは、その知能を企業の ID・権限・監査・組織構造の中にどう閉じ込めるかです。Gateway による統一入口、ゼロトラスト認可による都度検証、ポリシーコードによる決定論的な行動制御——これらの「檻」が整って初めて、確率的な知能を数万人規模の本番に投入できる段階に達します。

参照：[EX-1 Gateway](../patterns/ex-experience/ex1-enterprise-agent-gateway.md) / [ID-6 Zero-Trust](../patterns/id-identity/id6-zero-trust-pdp-pep.md)

### 12. やるか/やらないかでなく、どの程度かを設計する

自律度・ログ・予算・キャッシュ等の連続量を、トレースと eval で継続調整します。

エージェントの導入は「全自動か手動か」の二択ではありません。自律度のティア境界、ログの三層分離（メタ/本文/集計）、コスト予算、キャッシュ TTL、ガードレール強度——いずれも連続量であり、業務リスク・データ機密度・組織の成熟度に応じて段階的に調整します。この調整はリリース時に一度決めて終わりでなく、Observability Lake のトレースと評価パイプラインの出力を継続的にフィードバックしながら更新し続けるものといえます。

参照：[「程度」の選定基準](../decisions/degree/index.md) / [GV-7 Eval Pipeline](../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)

---

> 最も凝縮すると——**AIエージェントを企業に導入するとは、LLMを業務システムにつなぐことではなく、企業のID・権限・責任・データ・プロセス・監査・組織構造の中に新しい実行主体を安全に参加させることです。** 確率的な知能を決定論的な権限・組織・監査の檻の中に閉じ込めたとき、初めて数万人規模の本番に耐えるエンタープライズAIエージェントが成立します。
