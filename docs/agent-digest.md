---
title: "コーディングエージェント向けダイジェスト"
description: "全46パターン・選定基準・依存グラフ・インターフェイスを1ファイルに集約したダイジェスト。"
---

# コーディングエージェント向けダイジェスト

> このファイルはコーディングエージェント（Claude Code、Cursor、GitHub Copilot Workspace 等）が最初に読み込むことを想定している。全体像を把握したうえで、詳細が必要なパターンの個別ページに進んでほしい。

## 使い方

1. 下の一覧テーブルで候補パターンを特定する
2. `requires` 列で依存関係を確認する
3. `applies_when` 列でシナリオとの適合を確認する
4. 個別パターンページの `## Interfaces` セクションでインターフェイス定義を取得する
5. 構造化データが必要なら `patterns-index.yaml` と `selection-rules.yaml` を読み込む

## 全パターン一覧

| ID | 名称（日本語） | 面 | 前提パターン | 適用条件（代表） | 主要インターフェイス |
|---|---|---|---|---|---|
| EX-1 | Enterprise Agent Gateway（統一フロントドア） | experience | ID-1, ID-2, ID-6 | enterprise_scale, multi_channel, audit_required | Authentication & Risk Classification, Rate Control, Audit Entry Point |
| EX-2 | 業務埋め込み＋独立ワークベンチ（チャネル配置） | experience | EX-1, EX-3 | multi_channel, enterprise_scale, long_running | Embedded UI, Standalone Workbench, Channel Adapter |
| EX-3 | チャネル非依存フロントドア | experience | EX-1, ID-2 | multi_channel, audit_required, enterprise_scale | Channel Adapter, Unified Session Store, Unified Audit Logger |
| EX-4 | 信頼と価値実感のUX（定着を支える体験設計） | experience | EX-1, KM-1, RT-3 | enterprise_scale, adoption_challenge, prod_deployment | Citation & Confidence Layer, Progressive Confirmation UI, Value Feedback Dashboard |
| GV-1 | Enterprise Agent Control Plane（レジストリ／ライフサイクル） | governance | ID-7 | multi_department, enterprise_scale, audit_required | Agent Registry, Lifecycle Review Gate, Execution Enforcement |
| GV-2 | Agent Catalog & Marketplace（社内カタログ） | governance | GV-1 | multi_department, enterprise_scale, prod_deployment | Catalog UI/API, Access Request Workflow, Usage Analytics & Quality Score |
| GV-3 | Department Agent Factory（役割テンプレート工場） | governance | GV-1, GV-2, ID-4, GV-4 | multi_department, enterprise_scale, frequent_perm_chg | Role-Based Template Store, Low-Code Builder, IdP Role Change Listener |
| GV-4 | Industry Policy Pack（業界ポリシーパック） | governance | ID-6, ID-7 | regulated_industry, multi_department, enterprise_scale | Policy Pack Definition, Policy Engine Deployment, Evaluation Rubric |
| GV-5 | Central Model Gateway（モデル・ベンダー統制） | governance | GV-1 | enterprise_scale, confidential_data, external_llm_api | Model Approval Check, Data Classification Router, Token & Cost Meter |
| GV-6 | Version Registry（版管理） | governance | OB-1 | continuous_updates, prod_deployment, audit_required | Version Tag per Execution, PR-Gated Change Flow, Canary + Auto-Rollback |
| GV-7 | Evaluation & Governance Pipeline（評価CI/CD） | governance | OB-1 | prod_deployment, continuous_updates, regulated_industry | Offline Evaluation Gate, Security Evaluation, Production Drift Monitor |
| GV-8 | Cost Quota & Chargeback（コスト配賦） | governance | GV-1, GV-5 | enterprise_scale, cost_mgmt_needed, multi_agent | cost_center Tag Attribution, Budget Alert & Degradation, ROI Dashboard |
| GV-9 | Incident Response & Kill Switch（事故対応・停止） | governance | OB-1, OB-2, GV-1, GV-5 | prod_deployment, enterprise_scale | Granular Kill Switch, Trace Preservation, Incident Response Runbook |
| GV-10 | Three-Layer Value Measurement（採用定着×生産性×経営KPI） | governance | GV-8, OB-1 | enterprise_scale, roi_justification, multi_agent | Layer 0 Adoption Metrics, Layer 1 & 2 Business KPI Joiner, ROI Dashboard |
| ID-1 | Workforce/Customer 二面分離 | identity | — | customer_facing, confidential_data, enterprise_scale | Dual IdP Boundary, Explicit Cross-Boundary Gate, Tenant Isolation |
| ID-2 | Identity Federation & On-Behalf-Of（OBO委譲） | identity | — | cross_saas, audit_required, write_operations | Token Broker, SaaS Native Authorization, Audit Delegation Chain |
| ID-3 | Workload / Agent Identity（エージェント自身のID） | identity | ID-5, ID-6 | autonomous_exec, audit_required, kubernetes_cloud | Workload Certificate Issuer, Dual Representation Audit Record, Least-Privilege Workload Scope |
| ID-4 | Permission Mirror & Least-of Faithful Access（権限忠実アクセス） | identity | — | cross_saas_search, frequent_perm_chg, legacy_saas_mix | ACL Sync Pipeline, Effective Permission Calculator, Stale-Access Monitor |
| ID-5 | JIT Scoped Credentials（最小・短命・用途限定） | identity | ID-6 | cross_saas, high_risk_ops, vault_sts_infra | Credential Broker, PDP Pre-Issuance Check, Credential Audit Trail |
| ID-6 | Zero-Trust Runtime + 中央PDP/分散PEP（ABAC/ReBAC） | identity | — | confidential_data, cross_saas, regulated_industry | Central PDP, Distributed PEP, Org Graph Attribute Feed |
| ID-7 | Policy-as-Code Guardrail（決定論的行動可否） | identity | ID-6 | regulated_industry, enterprise_scale, multi_agent | Structured Policy Input, Policy Engine, Policy Version & Test Gate |
| ID-8 | Consent & Access Transparency（同意・透明化） | identity | ID-2, ID-4, ID-5 | personal_data, privacy_regulation, adoption_challenge | Consent Screen, Consent Registry, Revocation & Instant Token Invalidation |
| RT-1 | 組織階層型ハブ＆スポーク（意図ルーティング＋ドメインスポーク） | runtime | ID-4 | multi_department, enterprise_scale, multi_agent | Hub Agent, Domain Spoke Agent, Capability Registry |
| RT-2 | RACI型マルチエージェント・オーケストレーション | runtime | OB-2 | multi_department, high_risk_ops, hitl_approval | Orchestrator, Decision Log, Approval Gate |
| RT-3 | リスク段階型自律度（自律度の階層） | runtime | ID-7 | write_operations, high_risk_ops, enterprise_scale | Risk Scoring Engine, Policy Engine, Approval Workflow |
| RT-4 | 組織解決型承認チェーン | runtime | RT-8, ID-7 | high_risk_ops, hitl_approval, org_chart_maintained | Approver Resolution Engine, Workflow Tool Notification, Decision Log |
| RT-5 | 構造化コマンド封筒（意図→エンタープライズコマンド変換） | runtime | — | cross_saas, write_operations, audit_required | Intent Parser + Entity Extractor, Policy Engine, SaaS Adapter |
| RT-6 | 基幹システム書き込み境界 | runtime | RT-5 | sor_writes, sox_internal_ctrl, multi_agent | Domain Service, SoE Draft Store, Audit Trail |
| RT-7 | エンタープライズSagaエージェント（補償トランザクション） | runtime | RT-8 | multi_saas_saga, cross_saas, write_operations | Saga Orchestrator, Idempotency Key Manager, Compensation Action Library |
| RT-8 | 永続エンタープライズエージェントワークフロー | runtime | OB-1 | long_running, hitl_approval, audit_required | Workflow Definition, Activity Function, Budget / Step Limit Guard |
| RT-9 | エンタープライズ業務キュー参加エージェント | runtime | — | itsm_queue, enterprise_scale, async_processing | Queue Consumer, Escalation Handler, SLA Monitor |
| RT-10 | イベント駆動エンタープライズオーケストレーター | runtime | RT-7, RT-8 | event_driven, async_processing, cross_saas | Event Gateway, Debounce / Rate Limiter, Durable Workflow Engine |
| RT-11 | プロジェクト・デジタルツインエージェント | runtime | KM-1, KM-4, ID-4 | project_team, cross_saas_search, persistent_memory | Project Workspace Provisioner, GraphRAG Memory, Decision Log Store |
| KM-1 | 権限認識RAG（アクセス制御型エンタープライズRAG） | knowledge | ID-2, ID-4 | cross_saas_search, frequent_perm_chg, confidential_data | Ingest Pipeline with ACL Embedding, Permission Filter, Hybrid Search + Reranker |
| KM-2 | フェデレーテッド文脈メッシュ（アクセス制御型コンテキストメッシュ） | knowledge | ID-2 | confidential_data, data_residency, cross_saas | Context Router, Context Provider, Context Package Builder |
| KM-3 | 正規オブジェクト／知識グラフ | knowledge | — | multi_department, cross_saas, enterprise_scale | Entity Resolution Engine, Knowledge Graph, Graph Traversal API |
| KM-4 | スコープ記憶階層 | knowledge | — | persistent_memory, multi_department, personal_data | Memory Scope Partitioner, Lifecycle Event Handler, Memory Review UI |
| KM-5 | 目的限定コンテキストパッケージ | knowledge | — | multi_purpose_agent, confidential_data, privacy_regulation | Purpose Policy Store, Context Builder, DLP / Classification Filter |
| KM-6 | DLP・マスキング境界 | knowledge | — | personal_data, external_llm_api, privacy_regulation | Input DLP Gate, Output DLP Gate, Log Filter |
| KM-7 | 揮発・機密計算コンテキストバス | knowledge | — | top_secret_data, privacy_regulation, regulated_industry | DLP Proxy, Isolated Inference Environment, Sealed Audit Metadata Sink |
| IN-1 | エンタープライズツール／MCPゲートウェイ | integration | ID-6 | multi_agent, cross_saas, audit_required | Tool Catalog, Auth / Authz Layer, Audit Recorder |
| IN-2 | SaaSコネクタアダプタ（腐敗防止層） | integration | — | cross_saas, multi_agent, enterprise_scale | Canonical Tool Interface, SaaS-Specific Adapter, Error Normalizer |
| IN-3 | レート／クォータ調停ブローカー | integration | — | high_api_volume, enterprise_scale, async_processing | Token Bucket per SaaS, Priority Queue, Centralized Retry Handler |
| IN-4 | 既存iPaaS資産再利用 | integration | IN-1 | existing_ipaas, cross_saas, enterprise_scale | MCP Adapter, iPaaS Flow, Contract Test Suite |
| OB-1 | エンタープライズエージェント観測基盤（Observability Lake） | observability | — | prod_deployment, enterprise_scale | OTel Instrumentation Layer, Three-Layer Storage, Replay Tool |
| OB-2 | 統一監査台帳・系統追跡（三者帰責） | observability | GV-1, RT-8 | prod_deployment, audit_required, regulated_industry | Three-Party Audit Record, Correlation ID Stitcher, SIEM Integration |

## 選定クイックリファレンス（トレードオフ）

| 問い | 回答 | 参照 |
|---|---|---|
| エージェントは下流SaaSにどう認証すべきか？ | 個人支援=OBO（ID-2）、自律バッチ=Agent ID（ID-3）、高リスク不可逆=Hybrid（OBO＋HitL） | TO-1 |
| 知識基盤を中央DBかフェデレーテッドMeshか？ | 公開データ=中央レイク（KM-1 ACL同梱）、機密SaaS=フェデレーテッドMesh（KM-2）、混在=Hybrid | TO-2 |
| 単一エージェントかRACIマルチエージェントか？ | まず単一エージェント。複数部門の独立承認がある場合のみマルチ化（RT-2） | TO-3 |
| エージェントに付与する書き込み権限レベルは？ | 初期はRead-only。低リスク可逆操作はeval後に自動Write昇格。不可逆はHitL必須 | TO-4 |
| Copilot（業務支援）かAutopilot（業務代行）か？ | まず全操作をCopilotで開始。eval・カナリア・kill switchが整ってから段階的にAutopilot化 | TO-5 |
| エージェントの記憶を個人スコープかチーム共有か？ | 個人設定・機密=個人Enclave、共有ナレッジ=プロジェクトWorkspace、混在=物理分離必須 | TO-6 |
| 全プロンプトをログに残すか選択的トレースか？ | 標準=三層分離（メタ→Trace DB、本文→暗号化ストレージ、集計→DWH）。極秘=メタのみ | TO-7 |
| AIガバナンスを中央集権か部署フェデレートか？ | 認証・監査・モデル管理=中央。業務ドメイン・ユースケース=部署に委譲（二層ガバナンス） | TO-8 |
| 統合コネクタを自前構築か既存iPaaS再利用か？ | 既存iPaaSは認可粒度・監査証跡を検証後に再利用。新規統合はMCP化（IN-1）を標準に | TO-9 |
| 推論を内部/オンプレモデルか外部APIか？ | 極秘・規制対象=内部/オンプレ必須。一般データ=外部API可（DPA確認後）。混在=GV-5で自動ルーティング | TO-10 |
| エージェントの処理を同期か非同期か？ | 数秒以内Q&A=同期。10秒超・承認待ち・複数API=非同期（RT-8）。複数SaaSトランザクション=Saga（RT-7） | TO-11 |
| 安全制御はプロンプトか、ポリシー/実行基盤か？ | アクセス制御・承認・DLP・サンドボックスは実行基盤側必須。プロンプトは品質・ふるまい調整のみ | TO-12 |

## 選定クイックリファレンス（程度）

| パラメータ | 出発点 | 調整基準 | 参照 |
|---|---|---|---|
| 自律度ティア境界 | 書き込みは全て承認要求、読み取りは自動実行 | 不可逆性×影響範囲×データ機密度×役職。金融・契約・外部送信は複数承認 | DC-1 |
| タイムアウト・リトライ・予算 | Q&A: TTFT=5s, 合計=30s, リトライ=2回。長文分析: 合計=300s | 人間承認待ちは全体タイムアウト外し、非冪等操作はリトライ=0 | DC-2 |
| ログ粒度・保存先 | 標準=三層分離（メタ/本文暗号化/集計）。規制対象は分類別保持ポリシー必須 | 極秘=メタのみ。コスト制約=エラー+高リスク+ランダムN%サンプリング | DC-3 |
| コンテキスト投入量（top-k・トークン予算） | Q&A: top-k=3, 予算25%。多ソース分析: top-k=10, 予算50%+リランカー | 機密データはKM-6でマスキング後に投入。全件投入はアンチパターン | DC-4 |
| 記憶保持TTL | セッション=終了時破棄。個人（高頻度）=90日ローリング | 退職・異動・プロジェクト終了で即時失効必須。本人の削除権を設計に含める | DC-5 |
| ガードレール閾値 | 低リスク経路=軽量ガードレール。高リスク経路=厳格（FN最小化） | FP率・FN率をGV-7で定期計測し、ビジネス上の害が大きい方を優先して調整 | DC-6 |
| キャッシュ積極度・JIT TTL | 安定・非パーソナライズ・低リスク=積極キャッシュ（TTL=時間単位） | パーソナライズ・機密・副作用操作=キャッシュ無効化。権限変更で強制失効 | DC-7 |
| モデルルーティング | 単純タスク+非機密=軽量モデル。信頼度低下=強いモデルへエスカレーション | 極秘データ=VPC/オンプレ経路のみ。手動ルーティングはGV-5で自動化 | DC-8 |
| カナリア段階設計・イベント頻度制限 | 1%→5%→25%→100%多段階ロールアウト | 品質/エラー/コスト閾値超過でGV-6自動ロールバック。イベントストームにはデバウンス+レート制限+予算上限 | DC-9 |

## 依存グラフ（隣接リスト）

```yaml
EX-1: [ID-1, ID-2, ID-6]
EX-2: [EX-1, EX-3]
EX-3: [EX-1, ID-2]
EX-4: [EX-1, KM-1, RT-3]
GV-1: [ID-7]
GV-2: [GV-1]
GV-3: [GV-1, GV-2, ID-4, GV-4]
GV-4: [ID-6, ID-7]
GV-5: [GV-1]
GV-6: [OB-1]
GV-7: [OB-1]
GV-8: [GV-1, GV-5]
GV-9: [OB-1, OB-2, GV-1, GV-5]
GV-10: [GV-8, OB-1]
ID-1: []
ID-2: []
ID-3: [ID-5, ID-6]
ID-4: []
ID-5: [ID-6]
ID-6: []
ID-7: [ID-6]
ID-8: [ID-2, ID-4, ID-5]
RT-1: [ID-4]
RT-2: [OB-2]
RT-3: [ID-7]
RT-4: [RT-8, ID-7]
RT-5: []
RT-6: [RT-5]
RT-7: [RT-8]
RT-8: [OB-1]
RT-9: []
RT-10: [RT-7, RT-8]
RT-11: [KM-1, KM-4, ID-4]
KM-1: [ID-2, ID-4]
KM-2: [ID-2]
KM-3: []
KM-4: []
KM-5: []
KM-6: []
KM-7: []
IN-1: [ID-6]
IN-2: []
IN-3: []
IN-4: [IN-1]
OB-1: []
OB-2: [GV-1, RT-8]
```

## 部門別パターンバンドル

| 部門 | 主要パターン | 価値の焦点 |
|---|---|---|
| Sales Agent | ID-2, ID-4, IN-2, KM-5, RT-5, RT-4 | 受注率向上・商談サイクル短縮・パイプライン健全化 |
| HR Agent | KM-4, KM-6, RT-4, GV-4, RT-6 | 採用効率化・離職予防・問い合わせ自己解決 |
| Customer Support Agent | ID-1, RT-3, KM-1, RT-7, RT-9 | 顧客満足度向上・対応効率化・解約予防 |
| Engineering Agent | IN-1, ID-6, RT-8, OB-1, GV-9, ID-7 | 開発生産性向上・インシデント対応高速化 |
| Executive Agent | KM-3, KM-2, KM-6, GV-8, GV-7, OB-2 | 経営判断加速・全社最適化・リスク早期察知 |

## 基盤層パターン（優先度高）

以下のパターンは他の多くのパターンが依存しているため、最初に整備する。後から入れると既存パターンの改修コストが大きくなる。

| パターン | 依存される主なパターン |
|---|---|
| OB-1 Observability Lake | GV-7, GV-9, GV-6, RT-8, GV-10 |
| OB-2 Unified Audit | GV-9 |
| ID-2 OBO | KM-1, KM-2, EX-1, EX-3 |
| ID-4 Permission Mirror | KM-1, RT-1, RT-11, GV-3, ID-8 |
| ID-6 Zero-Trust PDP/PEP | GV-4, ID-7, ID-5, IN-1, ID-3 |
| ID-7 Policy-as-Code | RT-3, RT-4, GV-4, GV-1 |
| GV-1 Control Plane | GV-2, GV-8, OB-2, GV-9 |
| RT-8 Durable Workflow | RT-4, RT-7, OB-2, RT-10 |

## 最小統制セット（MVP）

Read-only の低リスク・高頻度ユースケース（ナレッジ検索・議事録要約）を30日以内に現場に出す場合の最小構成。

```
ID-2 (OBO読み取り版) + KM-1 (権限フィルタ) + OB-1 (ログ)
```

この3パターンで「誰が何を見たか」の監査証跡を持ちながら安全にRead-onlyエージェントを稼働させられる。基盤と統治は並行整備する。
