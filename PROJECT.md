# PROJECT.md — プロジェクト仕様・計画

本書はプロジェクトの**仕様と計画（何を・なぜ・どの順で作るか）**を定義する。日々の作業手順・コマンド・執筆規約は `CLAUDE.md` を参照すること。

---

## 1. 概要

- **プロジェクト名**：エンタープライズAIエージェント・アーキテクチャ・リファレンス
- **成果物**：MkDocs（Material テーマ）で生成し、GitHub Pages で公開する技術ドキュメントサイト。
- **目的**：数万人規模・多様な既存SaaS・厳格な権限管理・階層的組織を前提に、AIエージェントをエンタープライズへ安全に組み込むための再利用可能なアーキテクチャパターンを、横並び比較・選定可能な形で提供する。
- **中心命題**：AIを賢くすることではなく、企業のID・権限・責任・業務プロセス・監査・データ境界・組織構造の中に、新しい実行主体を安全に参加させること。
- **想定読者**：エンタープライズアーキテクト、プラットフォーム/基盤エンジニア、セキュリティ/IAM担当、AI CoE、テックリード、SRE。
- **執筆主体**：Claude Code。本書と `CLAUDE.md` を契約として各ページを段階的に執筆する。

## 2. 一次ソース（source of truth）

- すべての内容の出典は **`reference/source-unified-enterprise.md`**（3レポートの統合済みリファレンス、7面・45パターン）。
- 各ページは「該当節を Web ドキュメントとして読みやすい粒度に再構成する」作業。内容を勝手に創作・水増ししない。
- 標準・固有名（NIST AI RMF / OWASP LLM Top 10 / OIDC / SCIM / RFC 8693 / NIST SP 800-207 / OPA / Cedar / MCP / CloudEvents / OpenTelemetry、および Salesforce / Workday / Okta 等のSaaS）はソースの範囲に従う。ソース外の最新情報を足す場合は出典を明記し過度な断定を避ける。

## 3. 情報設計（IA）とディレクトリ構成

公開対象は `docs/` 配下のみ。`reference/` は執筆用素材で公開しない。

```text
.
├── PROJECT.md                  # 本書（仕様・計画）
├── CLAUDE.md                   # Claude Code 向け作業マニュアル
├── README.md                   # 人間向けクイックスタート
├── mkdocs.yml                  # サイト設定・ナビゲーション
├── pyproject.toml              # uv で管理する依存関係（mkdocs-material, pymdown-extensions）
├── uv.lock                     # uv のロックファイル
├── .github/workflows/deploy.yml# GitHub Pages 自動デプロイ
├── scripts/build_nav.sh        # nav を docs ツリーから再生成
├── reference/
│   └── source-unified-enterprise.md   # 一次ソース（非公開）
└── docs/
    ├── index.md                # ホーム
    ├── overview/
    │   ├── agenda.md           # ステップ1：中心命題・分類学・組織グラフ・7面
    │   └── schema.md           # ステップ2：項目設計と面分類
    ├── patterns/
    │   ├── index.md            # 7面一覧
    │   ├── ex-experience/      # 面1（index.md + EX-1..EX-3）
    │   ├── gv-governance/      # 面2（GV-1..GV-10）
    │   ├── id-identity/        # 面3（ID-1..ID-8）★最難関
    │   ├── rt-runtime/         # 面4（RT-1..RT-11）
    │   ├── km-knowledge/       # 面5（KM-1..KM-7）
    │   ├── in-integration/     # 面6（IN-1..IN-4）
    │   └── ob-observability/   # 面7（OB-1..OB-2）
    ├── selection/
    │   ├── degree/             # ステップ4：「程度」の選定基準（index.md + DC-1..DC-9）
    │   └── tradeoff/           # ステップ5：「相反する仕組み」の選定基準（index.md + TO-1..TO-12）
    ├── integration/
    │   ├── dependencies.md     # ステップ6.1/6.2：依存関係・組み合わせレシピ
    │   ├── department-examples.md # ステップ6.3：部門別適用例
    │   ├── roadmap.md          # ステップ6.4：成熟度ロードマップ
    │   ├── reference-architecture.md # ステップ6.5：標準構成図
    │   └── principles.md       # ステップ6.6：設計原則
    └── assets/                 # 画像等（必要時）
```

## 4. ページ仕様

### 4.1 パターンページ共通スキーマ（必須・順序固定）

各パターンページは以下の見出しをこの順序で持つ。空節を残さない。

1. `## 概要` — 何であ���かの一文要約。
2. `## 解決する企業課題` — ど���いう課題を解決するために、どのエンタープライズ固有の力（漏洩・サイロ・動的文脈・監査・コスト）に応えるか。
3. `## 価値仮説` — このパターンがどの企業価値KPI（売上・利益／業務自動化／プロジェクト生産性／従業員効率／経営判断速度）に、どの経路で効くか。1〜3行で記載。
4. `## 解決策と設計` — 課題の解決策と、それを実現する設計としての構造・データフロー・状態遷移・実装上の要点。図は mermaid。
5. `## 向き／不向き` — 採用が効く条件と、害・過剰になる条件を対で。
6. `## 要素技術・既��システム連携` — 代表技術・標準・対象SaaS。
7. `## 落とし穴／選定の勘所` — 典型的な失敗と回避の指針。
8. `## 関連パターン` — 類似・補完・対比される他のパターンへの相対リンク。

フロントマター：`title`（`"<ID> <名称>"`）、`description`（1文）、`status`（`draft`→`done`）。

### 4.2 パターン一覧（全45・執筆対象）

| ID | 名称 | ファイル |
|---|---|---|
| EX-1 | Enterprise Agent Gateway | patterns/ex-experience/ex1-enterprise-agent-gateway.md |
| EX-2 | 業務埋め込み vs 独立ポータル | patterns/ex-experience/ex2-embedded-vs-portal.md |
| EX-3 | チャネル非依存フロントドア | patterns/ex-experience/ex3-channel-agnostic-frontdoor.md |
| EX-4 | 信頼と価値実感のUX（定着を支える体験設計） | patterns/ex-experience/ex4-trust-value-ux.md |
| GV-1 | Enterprise Agent Control Plane | patterns/gv-governance/gv1-agent-control-plane.md |
| GV-2 | Agent Catalog & Marketplace | patterns/gv-governance/gv2-agent-catalog-marketplace.md |
| GV-3 | Department Agent Factory | patterns/gv-governance/gv3-department-agent-factory.md |
| GV-4 | Industry Policy Pack | patterns/gv-governance/gv4-industry-policy-pack.md |
| GV-5 | Central Model Gateway | patterns/gv-governance/gv5-central-model-gateway.md |
| GV-6 | Version Registry | patterns/gv-governance/gv6-version-registry.md |
| GV-7 | Evaluation & Governance Pipeline | patterns/gv-governance/gv7-evaluation-governance-pipeline.md |
| GV-8 | Cost Quota & Chargeback | patterns/gv-governance/gv8-cost-quota-chargeback.md |
| GV-9 | Incident Response & Kill Switch | patterns/gv-governance/gv9-incident-response-kill-switch.md |
| GV-10 | Two-Layer Value Measurement | patterns/gv-governance/gv10-two-layer-value-measurement.md |
| ID-1 | Workforce/Customer 二面分離 | patterns/id-identity/id1-workforce-customer-split.md |
| ID-2 | Identity Federation & OBO | patterns/id-identity/id2-identity-federation-obo.md |
| ID-3 | Workload / Agent Identity | patterns/id-identity/id3-workload-agent-identity.md |
| ID-4 | Permission Mirror & Least-of | patterns/id-identity/id4-permission-mirror-least-of.md |
| ID-5 | JIT Scoped Credentials | patterns/id-identity/id5-jit-scoped-credentials.md |
| ID-6 | Zero-Trust Runtime + PDP/PEP | patterns/id-identity/id6-zero-trust-pdp-pep.md |
| ID-7 | Policy-as-Code Guardrail | patterns/id-identity/id7-policy-as-code-guardrail.md |
| ID-8 | Consent & Access Transparency | patterns/id-identity/id8-consent-access-transparency.md |
| RT-1 | Org-Hierarchical Hub & Spoke | patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md |
| RT-2 | RACI-based Multi-Agent | patterns/rt-runtime/rt2-raci-multi-agent.md |
| RT-3 | Risk-Tiered Autonomy | patterns/rt-runtime/rt3-risk-tiered-autonomy.md |
| RT-4 | Human Approval Chain | patterns/rt-runtime/rt4-human-approval-chain.md |
| RT-5 | Command Envelope | patterns/rt-runtime/rt5-command-envelope.md |
| RT-6 | SoR Write Boundary | patterns/rt-runtime/rt6-sor-write-boundary.md |
| RT-7 | Enterprise Saga Agent | patterns/rt-runtime/rt7-enterprise-saga.md |
| RT-8 | Durable Workflow | patterns/rt-runtime/rt8-durable-workflow.md |
| RT-9 | Work Queue Agent | patterns/rt-runtime/rt9-work-queue-agent.md |
| RT-10 | Event-Driven Orchestrator | patterns/rt-runtime/rt10-event-driven-orchestrator.md |
| RT-11 | Project Digital Twin | patterns/rt-runtime/rt11-project-digital-twin.md |
| KM-1 | Access-Controlled RAG | patterns/km-knowledge/km1-access-controlled-rag.md |
| KM-2 | Context Mesh | patterns/km-knowledge/km2-context-mesh.md |
| KM-3 | Canonical Object & Knowledge Graph | patterns/km-knowledge/km3-canonical-object-knowledge-graph.md |
| KM-4 | Scoped Memory Hierarchy | patterns/km-knowledge/km4-scoped-memory-hierarchy.md |
| KM-5 | Purpose-Bound Context | patterns/km-knowledge/km5-purpose-bound-context.md |
| KM-6 | DLP & Redaction Boundary | patterns/km-knowledge/km6-dlp-redaction-boundary.md |
| KM-7 | Ephemeral Secure Context Bus | patterns/km-knowledge/km7-ephemeral-secure-context-bus.md |
| IN-1 | Enterprise Tool / MCP Gateway | patterns/in-integration/in1-tool-mcp-gateway.md |
| IN-2 | SaaS Connector Adapter | patterns/in-integration/in2-saas-connector-adapter.md |
| IN-3 | Rate / Quota Broker | patterns/in-integration/in3-rate-quota-broker.md |
| IN-4 | Existing iPaaS Reuse | patterns/in-integration/in4-existing-ipaas-reuse.md |
| OB-1 | Observability Lake | patterns/ob-observability/ob1-observability-lake.md |
| OB-2 | Unified Audit & Lineage | patterns/ob-observability/ob2-unified-audit-lineage.md |

### 4.3 選定基準ページ共通スキーマ

#### 「程度」の選定基準（DC-*）ページスキーマ（必須・順序固定）

1. `## 概要` — この連続量パラメータが何を制御するかの一文要約。
2. `## 過小・過大の害` — 両極端が引き起こす具体的な害。表形式で対比。
3. `## 判断基準` — どの入力変数（影響度・機密度・職責等）でどう決めるか。
4. `## 調整の仕組み` — 本番でどう計測・調整するか（OB-1/GV-7 との連携）。
5. `## 関連パターン` — 対応するパターンへの相対リンク。

フロントマター：`title`（`"DC-<N> <名称>"`）、`description`（1文）、`status`（`draft`→`done`）。

#### 「相反する仕組み」の選定基準（TO-*）ページスキーマ（必須・順序固定）

1. `## 概要` — 何と何が対立するか、なぜ二者択一に見えるか。
2. `## 比較` — 観点別の比較表。
3. `## 判断基準` — どの条件でどちらを選ぶか（線引きの軸）。
4. `## ハイブリッド・段階的アプローチ` — 実務的な併用・段階戦略（該当する場合）。
5. `## 関連パターン` — 対応するパターンへの相対リンク。

フロントマター：`title`（`"TO-<N> <名称>"`）、`description`（1文）、`status`（`draft`→`done`）。

### 4.4 選定基準ページ一覧

#### 「程度」の選定基準（DC-1〜DC-9）

| ID | 名称 | ファイル |
|---|---|---|
| DC-1 | 自律度のティア境界（Risk-Tier の引き方） | selection/degree/dc1-risk-tier-boundary.md |
| DC-2 | タイムアウト・リトライ・予算（コスト上限） | selection/degree/dc2-timeout-retry-budget.md |
| DC-3 | プロンプト/トレースのログ粒度（三層分離） | selection/degree/dc3-log-granularity.md |
| DC-4 | コンテキスト投入量（top-k・トークン予算） | selection/degree/dc4-context-volume.md |
| DC-5 | メモリ保持・忘却（TTL・スコープ） | selection/degree/dc5-memory-retention.md |
| DC-6 | ガードレール強度（誤検知 vs 見逃し） | selection/degree/dc6-guardrail-strength.md |
| DC-7 | キャッシュ積極度・JIT 資格情報 TTL | selection/degree/dc7-cache-jit-ttl.md |
| DC-8 | モデルの強さ・データ分類別ルーティング | selection/degree/dc8-model-routing.md |
| DC-9 | カナリア段階・イベント駆動の頻度制限 | selection/degree/dc9-canary-event-throttle.md |

#### 「相反する仕組み」の選定基準（TO-1〜TO-12）

| ID | 名称 | ファイル |
|---|---|---|
| TO-1 | OBO委譲 vs サービスアカウント | selection/tradeoff/to1-obo-vs-service-account.md |
| TO-2 | 中央集権データレイク vs フェデレーテッド Context Mesh | selection/tradeoff/to2-lake-vs-mesh.md |
| TO-3 | 単一エージェント vs RACI マルチエージェント | selection/tradeoff/to3-single-vs-multi-agent.md |
| TO-4 | Read-only vs Write-capable（段階的拡張） | selection/tradeoff/to4-readonly-vs-write.md |
| TO-5 | Copilot vs Autopilot | selection/tradeoff/to5-copilot-vs-autopilot.md |
| TO-6 | 個人の記憶 vs プロジェクト/チームの記憶 | selection/tradeoff/to6-personal-vs-team-memory.md |
| TO-7 | 全プロンプトログ vs 選択的トレースログ | selection/tradeoff/to7-full-vs-selective-log.md |
| TO-8 | 中央集権プラットフォーム vs 部署フェデレーション | selection/tradeoff/to8-central-vs-federation.md |
| TO-9 | コネクタ自前構築 vs 既存 iPaaS 再利用 | selection/tradeoff/to9-custom-vs-ipaas.md |
| TO-10 | 内部/オンプレモデル vs 外部 API | selection/tradeoff/to10-onprem-vs-external.md |
| TO-11 | 同期 vs 非同期 | selection/tradeoff/to11-sync-vs-async.md |
| TO-12 | プロンプトで守る vs ポリシー/実行基盤で守る | selection/tradeoff/to12-prompt-vs-platform.md |

### 4.5 非パターン・非選定基準ページ

| ページ | 対応ステップ | ソース節 |
|---|---|---|
| overview/agenda.md | ステップ1 | ステップ1 全体（命題・分類学・組織グラフ・7面・標準整合） |
| overview/schema.md | ステップ2 | ステップ2 |
| integration/dependencies.md | ステップ6.1/6.2 | 6.1 依存関係・6.2 組み合わせレシピ |
| integration/department-examples.md | ステップ6.3 | 6.3 部門別適用例 |
| integration/roadmap.md | ステップ6.4 | 6.4 成熟度ロードマップ |
| integration/reference-architecture.md | ステップ6.5 | 6.5（mermaidで作図） |
| integration/principles.md | ステップ6.6 | 6.6 設計原則 |
| integration/adoption.md | 定着・アダプション | レビュー指摘2-1に基づく新設（チェンジマネジメント・信頼獲得UX・定着指標） |
| integration/portfolio.md | AI投資ポートフォリオ管理 | レビュー指摘4-2に基づく新設（価値×コスト×リスクの投資配分） |

## 5. 執筆計画（フェーズと優先順位）

ソースの成熟度ロードマップに沿い、本番で最初に効く面から着手する。**面3（アイデンティティ）が最難関かつ最重要のため、骨格を早期に固める。**

- **Phase 0：足場確認** — `mkdocs serve` で全スタブ表示・`mkdocs build --strict` 通過を確認。
- **Phase 1：セキュリティ基盤** — overview 2ページ ＋ ID-2, ID-4, ID-1, ID-6, ID-7（権限の忠実な伝播を先に固める）＋ KM-7。
- **Phase 2：統治の骨格** — GV-1, GV-5, OB-1, OB-2, GV-9, EX-1。
- **Phase 3：知識と連携** — KM-1, KM-2, KM-3, KM-4, IN-1, IN-2 ＋ selection（DC-1〜DC-9, TO-1〜TO-12）。
- **Phase 4：実行と自動化** — RT-1〜RT-11、残りの GV/EX/KM/IN/ID。
- **Phase 5：統合章の仕上げ** — integration 5ページ（全パターンへの相互リンクを張る）。

## 6. 完了の定義（Definition of Done）

各ページは以下をすべて満たして `status: done`。

- 共通スキーマの全節が、空・TODO なしで埋まっている（パターンページ）。
- フロントマター `title` が nav と一致、`description` が1文で記入済み。
- 内部リンクが有効（`mkdocs build --strict` が警告なしで通る）。
- 図が必要な箇所は mermaid で描かれている（特に ID-2 OBO、RT-7 Saga、RT-10 イベント駆動はシーケンス/フロー図を推奨）。
- 一次ソースの該当節の主旨を逸脱していない。

## 7. 非目標（やらないこと）

- ソースに無い新パターンの追加（提案は Issue として別途）。
- 実装コードの完全提供（要素技術名と最小擬似コード／設定例に留める）。
- 特定ベンダー製品の宣伝・優劣の断定。
- 顧客面と従業員面の境界をまたぐ設計例の安易な提示（ID-1 の原則に反する）。
