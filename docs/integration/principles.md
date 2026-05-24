---
title: "設計原則と組み合わせ方"
description: "「程度」と「相反」の設計判断をパターンへ写像する対応表と、全体を貫く11の設計原則。"
status: done
---

# 設計原則と組み合わせ方

## 概要

[「程度」の選定基準](../selection/degree-criteria.md)と[「相反する仕組み」の選定基準](../selection/tradeoffs.md)で定めた設計判断は、抽象論ではなく具体的なパターンの設定値として現れる。本ページでは、設計判断からパターンへの写像表と、全体を貫く設計原則を示す。

## 「程度」と「相反」をパターンへ写像する

| 設計判断 | 主に効くパターン | 設定の勘所 |
|---|---|---|
| タイムアウト / リトライ | [A-5 Time-Budget](../patterns/a-execution/a5-time-budgeted-loop.md)、[H-4 Fallback](../patterns/h-cost-performance/h4-graceful-degradation.md) | セッション予算に従属させ、副作用は冪等＋Saga |
| ループ予算 | [A-5 Time-Budget](../patterns/a-execution/a5-time-budgeted-loop.md) | 上限到達を分岐点（部分結果 / 承認 / 縮退）に |
| ログ粒度 | [I-1 Trace](../patterns/i-observability/i1-trace-observability.md) | メタはトレース、本文はストレージ退避＋サンプリング |
| コンテキスト量 | [E-2 Context Pack](../patterns/e-memory/e2-context-pack.md)、[F-1 Evidence-First](../patterns/f-reliability/f1-evidence-first.md) | トークン予算内にランキング圧縮 |
| 温度 / 決定性 | [C-2 Structured Output](../patterns/c-io-contract/c2-structured-output-contract.md)、[B-4 Ensemble](../patterns/b-composition/b4-ensemble-debate.md) | 連携は低温＋検証、合議は高温で多様性 |
| ガードレール強度 | [F-2 Guardrail Sidecar](../patterns/f-reliability/f2-guardrail-sidecar.md)、[G-2 Data Boundary](../patterns/g-security/g2-data-boundary-firewall.md) | 経路リスク別に閾値、FP/FNを計測 |
| 承認範囲 | [F-5 Human Approval](../patterns/f-reliability/f5-human-approval.md)、[L-1 Shadow Mode](../patterns/l-adoption/l1-shadow-progressive-autonomy.md) | リスク分類器で自動可 / 要承認 / 禁止 |
| 同期 / 非同期 | [A-1 Request-to-Job](../patterns/a-execution/a1-request-to-job-gateway.md)、[A-3 Streaming](../patterns/a-execution/a3-streaming-progress.md) | 部分ストリーム＋非同期のハイブリッド |
| 単一 / 複数エージェント | [B-2 Planner](../patterns/b-composition/b2-planner-executor-reviewer.md)、[B-3 Supervisor](../patterns/b-composition/b3-supervisor-specialist.md)、[B-5 Blackboard](../patterns/b-composition/b5-blackboard.md) | 既定は単一、肥大 / 並列利得で複数化 |
| 抽象化 / 固有最適化 | [J-1 Runtime Abstraction](../patterns/j-abstraction/j1-runtime-abstraction.md)、[J-2 Model Compatibility](../patterns/j-abstraction/j2-model-compatibility-layer.md)、[H-3 Prompt Cache](../patterns/h-cost-performance/h3-prompt-cache-context.md) | 抽象を基本、ホットパスのみ固有機能 |
| プロンプト / 基盤で守る | [F-4 Policy-as-Code](../patterns/f-reliability/f4-policy-as-code.md)、[D-2 Least-Privilege](../patterns/d-tools-mcp/d2-least-privilege-binding.md)、[G-1 Confused-Deputy](../patterns/g-security/g1-confused-deputy-limitation.md) | 安全保証は必ず実行基盤側に |

## 設計原則

以下の11原則が、全パターンを貫く設計思想である。

### 原則1：同期リクエストでなく、長時間セッションとして扱う

Session / Job / Workflow / Checkpoint を一級概念にする。[A-1 Request-to-Job Gateway](../patterns/a-execution/a1-request-to-job-gateway.md)・[A-2 Durable Session](../patterns/a-execution/a2-durable-session.md) がこの原則を体現する。

### 原則2：LLMを業務ロジックの中心に置きすぎない

中核の状態遷移・権限・金額計算・DB更新は決定論コードに残す。[B-1 Deterministic Backbone](../patterns/b-composition/b1-deterministic-backbone.md) がこの原則を体現する。

### 原則3：自然言語をそのまま実行しない

Intent → Plan → Action → Evidence → Approval へ構造化する。[C-1 NL Boundary Adapter](../patterns/c-io-contract/c1-nl-boundary-adapter.md)・[C-2 Structured Output](../patterns/c-io-contract/c2-structured-output-contract.md)・[B-2 Planner–Executor–Reviewer](../patterns/b-composition/b2-planner-executor-reviewer.md) がこのパイプラインを形成する。

### 原則4：ツール実行を最重要リスク境界として設計する

Gateway・最小権限・Dry-Run・Sandbox・監査を必須にする。[D-1](../patterns/d-tools-mcp/d1-tool-gateway.md)〜[D-5](../patterns/d-tools-mcp/d5-mcp-adapter-isolation.md) のカテゴリD全体がこの原則を担う。

### 原則5：メモリはデータ管理機能として扱う

保存・忘却・権限・鮮度・根拠・テナント分離を設計する。[E-1](../patterns/e-memory/e1-layered-memory.md)〜[E-4](../patterns/e-memory/e4-forgetting-expiration.md) のカテゴリE全体がこの原則を担う。

### 原則6：プロンプトでなく、ポリシーと実行基盤で守る

権限・承認・検証・隔離で守る。プロンプトは攻撃者が操作可能であり、安全保証の最終手段にしない。[F-4 Policy-as-Code](../patterns/f-reliability/f4-policy-as-code.md)・[D-2 Least-Privilege](../patterns/d-tools-mcp/d2-least-privilege-binding.md)・[G-1 Confused-Deputy](../patterns/g-security/g1-confused-deputy-limitation.md) がこの原則を体現する。

### 原則7：評価をCI/CDに組み込む

モデル・プロンプト・ツール・RAGの変更は eval なしに本番反映しない。[I-2 Evaluation CI/CD](../patterns/i-observability/i2-evaluation-cicd.md)・[I-4 Version Pinning](../patterns/i-observability/i4-version-pinning.md) がこの原則を担う。

### 原則8：観測性を通常システム以上に重視する

なぜその判断か・何を見たか・どのツールを呼んだか・いくらかかったか。[I-1 Agent Trace](../patterns/i-observability/i1-trace-observability.md) がこの原則の基盤となる。

### 原則9：コストを設計対象にする

ルーティング・キャッシュ・予算・早期停止・フォールバック。[A-5 Time-Budget](../patterns/a-execution/a5-time-budgeted-loop.md) と [H-1](../patterns/h-cost-performance/h1-cost-aware-router.md)〜[H-5](../patterns/h-cost-performance/h5-speculative-hedged.md) がコスト設計のパターン群である。

### 原則10：「やるか」でなく「どの程度か」を設計する

極端を避け、トレースと eval で継続調整する。[「程度」の選定基準](../selection/degree-criteria.md)がこの原則の実践ガイドとなる。

### 原則11：完全自律でなく、制御された自律性を目指す

[F-5 Human Approval](../patterns/f-reliability/f5-human-approval.md)・[K-2 Editable Plan](../patterns/k-human/k2-editable-plan.md)・[K-3 Escalation](../patterns/k-human/k3-human-escalation.md)・[L-1 Shadow Mode](../patterns/l-adoption/l1-shadow-progressive-autonomy.md) が、自律と制御のバランスを実現する。

## まとめ

> AIエージェントの本番化とは、賢いが信用しきれない・遅く・高コストで・騙されうる実行主体を、決定論的な殻・契約・権限・検証・予算・観測・統治の中に安全に閉じ込め、その周囲に従来のソフトウェア工学（状態管理・トランザクション・監査・テスト・デプロイ・可観測性）を配置し、各設計判断を「程度」と「相反軸」の明示的なトレードオフとして決める工学である。

!!! tip "関連ページ"
    - [「程度」の選定基準](../selection/degree-criteria.md) — 連続量パラメータの決め方
    - [「相反する仕組み」の選定基準](../selection/tradeoffs.md) — 二者択一の判断軸
    - [パターン間の依存関係](dependencies.md) — パターンの前提と依存先
    - [成熟度別ロードマップ](roadmap.md) — 段階的な導入順序
    - [リファレンスアーキテクチャ](reference-architecture.md) — 全パターンの標準構成図
