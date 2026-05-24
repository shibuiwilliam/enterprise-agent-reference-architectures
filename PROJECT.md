# PROJECT.md — プロジェクト仕様・計画

本書はプロジェクトの**仕様と計画（何を・なぜ・どの順で作るか）**を定義する。日々の作業手順・コマンド・執筆規約は `CLAUDE.md` を参照すること。

---

## 1. 概要

- **プロジェクト名**：AIエージェント本番組み込み アーキテクチャ・リファレンス
- **成果物**：MkDocs（Material テーマ）で生成し、GitHub Pages で公開する技術ドキュメントサイト。
- **目的**：AIエージェントを本番システムへ安全・堅牢・スケーラブルに組み込むための再利用可能なアーキテクチャパターンを、横並び比較・選定可能な形で提供する。
- **想定読者**：本番にAIエージェントを組み込むソフトウェアアーキテクト、バックエンド/プラットフォームエンジニア、テックリード、SRE。
- **執筆主体**：Claude Code。本書（PROJECT.md）と `CLAUDE.md` を契約として、各ページを段階的に執筆する。

## 2. 一次ソース（source of truth）

- すべての内容の出典は **`reference/source-unified-reference.md`**（統合済みリファレンス）である。
- 各ページは「該当節を Web ドキュメントとして読みやすい粒度に再構成する」作業であり、内容を勝手に創作・水増ししない。
- 事実・固有名（プロダクト名・標準名）はソースの範囲に従う。ソース外の最新情報を足す場合は出典を明記し、過度な断定を避ける。

## 3. 情報設計（IA）とディレクトリ構成

公開対象は `docs/` 配下のみ。`reference/` は執筆用の素材で公開しない。

```text
.
├── PROJECT.md                  # 本書（仕様・計画）
├── CLAUDE.md                   # Claude Code 向け作業マニュアル
├── README.md                   # 人間向けクイックスタート
├── mkdocs.yml                  # サイト設定・ナビゲーション
├── requirements.txt            # mkdocs-material, pymdown-extensions
├── .github/workflows/deploy.yml# GitHub Pages 自動デプロイ
├── scripts/build_nav.sh        # nav を docs ツリーから再生成
├── reference/
│   └── source-unified-reference.md   # 一次ソース（非公開）
└── docs/
    ├── index.md                # ホーム
    ├── overview/
    │   ├── agenda.md           # ステップ1：到達目標とエージェント特性
    │   └── schema.md           # ステップ2：項目設計とカテゴリ分類
    ├── patterns/
    │   ├── index.md            # カテゴリ一覧
    │   ├── a-execution/        # カテゴリA（index.md + A-1..A-6）
    │   ├── b-composition/      # カテゴリB（B-1..B-5）
    │   ├── c-io-contract/      # カテゴリC（C-1..C-4）
    │   ├── d-tools-mcp/        # カテゴリD（D-1..D-5）
    │   ├── e-memory/           # カテゴリE（E-1..E-4）
    │   ├── f-reliability/      # カテゴリF（F-1..F-5）
    │   ├── g-security/         # カテゴリG（G-1..G-3）
    │   ├── h-cost-performance/ # カテゴリH（H-1..H-5）
    │   ├── i-observability/    # カテゴリI（I-1..I-4）
    │   ├── j-abstraction/      # カテゴリJ（J-1..J-3）
    │   ├── k-human/            # カテゴリK（K-1..K-3）
    │   └── l-adoption/         # カテゴリL（L-1..L-3）
    ├── selection/
    │   ├── degree-criteria.md  # ステップ4：「程度」の選定基準
    │   └── tradeoffs.md        # ステップ5：「相反する仕組み」の選定基準
    ├── integration/
    │   ├── dependencies.md     # ステップ6.1：依存関係
    │   ├── roadmap.md          # ステップ6.2：成熟度ロードマップ
    │   ├── selection-guide.md  # ステップ6.3：選定ガイド
    │   ├── reference-architecture.md # ステップ6.4：標準構成図
    │   └── principles.md       # ステップ6.5/6.6：写像表・設計原則
    └── assets/                 # 画像等（必要時）
```

## 4. ページ仕様

### 4.1 パターンページ共通スキーマ（必須・順序固定）

各パターンページは以下の見出しをこの順序で持つ。空節を残さない。

1. `## 概要` — 一文要約。
2. `## 設計` — 構造・データフロー・状態遷移・実装上の要点。図は mermaid。
3. `## 解決する課題` — どのエージェント特性（force）に応えるか。
4. `## ユースケース` — 典型的な適用場面。
5. `## 向き` — 採用が効くシステム条件。
6. `## 不向き` — 採用が害・過剰になる条件。
7. `## 要素技術` — 代表的な実装技術・プロダクト・標準。
8. `## 関連パターン` — 依存・併用するパターンへの相対リンク。

フロントマター：`title`（`"<ID> <名称>"`）、`description`（1文）、`status`（`draft`→`done`）。

### 4.2 パターン一覧（全50・執筆対象）

| ID | 名称 | ファイル |
|---|---|---|
| A-1 | Request-to-Job Gateway | patterns/a-execution/a1-request-to-job-gateway.md |
| A-2 | Durable Agent Session | patterns/a-execution/a2-durable-session.md |
| A-3 | Streaming Progress | patterns/a-execution/a3-streaming-progress.md |
| A-4 | Interruptible Agent | patterns/a-execution/a4-interruptible-agent.md |
| A-5 | Time-Budgeted Agent Loop | patterns/a-execution/a5-time-budgeted-loop.md |
| A-6 | Agent Saga | patterns/a-execution/a6-agent-saga.md |
| B-1 | Deterministic Backbone, Probabilistic Edge | patterns/b-composition/b1-deterministic-backbone.md |
| B-2 | Planner–Executor–Reviewer | patterns/b-composition/b2-planner-executor-reviewer.md |
| B-3 | Supervisor & Specialist | patterns/b-composition/b3-supervisor-specialist.md |
| B-4 | Agent Ensemble & Debate | patterns/b-composition/b4-ensemble-debate.md |
| B-5 | Blackboard Coordination | patterns/b-composition/b5-blackboard.md |
| C-1 | Natural Language Boundary Adapter | patterns/c-io-contract/c1-nl-boundary-adapter.md |
| C-2 | Structured Output Contract & Self-Correction | patterns/c-io-contract/c2-structured-output-contract.md |
| C-3 | Inverted Structured Output | patterns/c-io-contract/c3-inverted-structured-output.md |
| C-4 | Ambiguity Negotiation | patterns/c-io-contract/c4-ambiguity-negotiation.md |
| D-1 | Tool Gateway | patterns/d-tools-mcp/d1-tool-gateway.md |
| D-2 | Least-Privilege Tool Binding | patterns/d-tools-mcp/d2-least-privilege-binding.md |
| D-3 | Dry-Run First Execution | patterns/d-tools-mcp/d3-dry-run-execution.md |
| D-4 | Sandboxed Tool Runtime | patterns/d-tools-mcp/d4-sandboxed-runtime.md |
| D-5 | MCP Adapter Isolation | patterns/d-tools-mcp/d5-mcp-adapter-isolation.md |
| E-1 | Layered Memory | patterns/e-memory/e1-layered-memory.md |
| E-2 | Context Pack | patterns/e-memory/e2-context-pack.md |
| E-3 | Memory Write Gate | patterns/e-memory/e3-memory-write-gate.md |
| E-4 | Forgetting & Expiration | patterns/e-memory/e4-forgetting-expiration.md |
| F-1 | Evidence-First Answer | patterns/f-reliability/f1-evidence-first.md |
| F-2 | Guardrail Sidecar | patterns/f-reliability/f2-guardrail-sidecar.md |
| F-3 | Verifier Agent | patterns/f-reliability/f3-verifier-agent.md |
| F-4 | Policy-as-Code Guardrail | patterns/f-reliability/f4-policy-as-code.md |
| F-5 | Human Approval Checkpoint | patterns/f-reliability/f5-human-approval.md |
| G-1 | Confused-Deputy Damage Limitation | patterns/g-security/g1-confused-deputy-limitation.md |
| G-2 | Data Boundary Firewall | patterns/g-security/g2-data-boundary-firewall.md |
| G-3 | Tenant-Isolated Runtime | patterns/g-security/g3-tenant-isolated-runtime.md |
| H-1 | Cost-Aware Model Router | patterns/h-cost-performance/h1-cost-aware-router.md |
| H-2 | Semantic Result Cache | patterns/h-cost-performance/h2-semantic-cache.md |
| H-3 | Prompt-Cache Optimized Context | patterns/h-cost-performance/h3-prompt-cache-context.md |
| H-4 | Graceful Degradation & Fallback | patterns/h-cost-performance/h4-graceful-degradation.md |
| H-5 | Speculative / Hedged Execution | patterns/h-cost-performance/h5-speculative-hedged.md |
| I-1 | Agent Trace & Observability | patterns/i-observability/i1-trace-observability.md |
| I-2 | Evaluation CI/CD | patterns/i-observability/i2-evaluation-cicd.md |
| I-3 | Production Replay | patterns/i-observability/i3-production-replay.md |
| I-4 | Version Pinning & Change Management | patterns/i-observability/i4-version-pinning.md |
| J-1 | Agent Runtime Abstraction | patterns/j-abstraction/j1-runtime-abstraction.md |
| J-2 | Model Behavior Compatibility Layer | patterns/j-abstraction/j2-model-compatibility-layer.md |
| J-3 | Agent Capability Registry | patterns/j-abstraction/j3-capability-registry.md |
| K-1 | Agent Workbench | patterns/k-human/k1-agent-workbench.md |
| K-2 | Editable Plan | patterns/k-human/k2-editable-plan.md |
| K-3 | Agent-to-Human Escalation | patterns/k-human/k3-human-escalation.md |
| L-1 | Shadow Mode & Progressive Autonomy | patterns/l-adoption/l1-shadow-progressive-autonomy.md |
| L-2 | Anti-Corruption Layer | patterns/l-adoption/l2-anti-corruption-layer.md |
| L-3 | Agent Constitution | patterns/l-adoption/l3-agent-constitution.md |

### 4.3 非パターンページ

| ページ | 対応ステップ | ソース節 |
|---|---|---|
| overview/agenda.md | ステップ1 | ステップ1・0章特性表 |
| overview/schema.md | ステップ2 | ステップ2 |
| selection/degree-criteria.md | ステップ4 | ステップ4（全13項目） |
| selection/tradeoffs.md | ステップ5 | ステップ5（全16軸） |
| integration/dependencies.md | ステップ6.1 | 6.1 |
| integration/roadmap.md | ステップ6.2 | 6.2 |
| integration/selection-guide.md | ステップ6.3 | 6.3 |
| integration/reference-architecture.md | ステップ6.4 | 6.4（mermaidで作図） |
| integration/principles.md | ステップ6.5/6.6 | 6.5写像表・6.6設計原則 |

## 5. 執筆計画（フェーズと優先順位）

ソースの「成熟度ロードマップ」に沿い、本番で最初に効くパターンから着手する。

- **Phase 0：足場確認** — `mkdocs serve` で全スタブが表示・ビルド（`--strict`）が通ることを確認。
- **Phase 1：導入の骨格** — overview 2ページ ＋ A-1, B-1, C-2, H-4, A-5, I-1。
- **Phase 2：副作用と統制** — A-2, A-6, D-1, D-2, D-3, F-5。
- **Phase 3：信頼性と品質** — F-1, F-3, B-4, I-2, I-4 ＋ selection 2ページ。
- **Phase 4：規模と統治** — E系・G系・H-1〜3・J系・L系 ＋ 残りの A/B/C/K。
- **Phase 5：統合章の仕上げ** — integration 5ページ（全パターンへの相互リンクを張る）。

## 6. 完了の定義（Definition of Done）

各ページは以下をすべて満たして `status: done`。

- 共通スキーマの全節が、空・TODO なしで埋まっている（パターンページ）。
- フロントマター `title` が nav と一致、`description` が1文で記入済み。
- 内部リンクが有効（`mkdocs build --strict` が警告なしで通る）。
- 図が必要な箇所は mermaid で描かれている。
- 一次ソースの該当節の主旨を逸脱していない。

## 7. 非目標（やらないこと）

- ソースに無い新パターンの追加（提案は Issue として別途）。
- 実装コードの完全な提供（要素技術名と最小擬似コードに留める）。
- 特定ベンダー製品の宣伝・優劣の断定。
