---
id: P03
slug: AI-GATEWAY
title: "P03 · AI-GATEWAY — AIエージェント・ゲートウェイ"
category: 統合
audience: both
maturity: 基盤
related: [P08, P09, P23, P24, P25, P27]
status: done
---

# P03 · AI-GATEWAY — AIエージェント・ゲートウェイ

!!! abstract "一言で"
    全エージェントの呼び出しが通る中央コントロールプレーンです。認証・レート制限・コスト計上・モデルルーティング・ロギング・ガードレール・PIIマスキングを一箇所に集約し、組織全体のAI利用を可視化・統制します。モデルプロバイダの抽象化により、ロックインを回避しつつ統一的なポリシー適用を可能にします。

## 解決する問題

- **シャドーAI**: 各チームが独自にAPIキーを取得し、管理外のモデル利用が拡散します。
- **コスト不可視**: 部署・プロジェクト単位のコスト把握ができず、暴走を検知できません。
- **モデルロックイン**: 特定プロバイダに直結し、切替・比較が困難になります。
- **監査不能**: 誰が何を問い合わせたか追跡できず、コンプライアンス要件を満たせません。
- **ガードレール重複**: 各アプリが個別に安全対策を実装し、品質がばらつきます。

## 選定条件

**採用する場合（When to use）**

- 全社的にAI利用を解禁する／複数モデルを使い分ける／シャドーAI・コスト不可視を防ぎたい。
- 中〜大規模組織でガバナンス重視、複数モデル・複数チームがAIを利用する環境。

**採用しない場合（When NOT）**

- 小規模PoCで統制より速度優先の段階、超低レイテンシが最優先で中間層を許容できない用途。

## 構造

- **北向き（統一エンドポイント）**: 全エージェント・アプリケーションからのリクエストを受け付ける単一のAPIエンドポイントです。
- **南向き（マルチプロバイダ）**: 複数LLMプロバイダ（OpenAI / Anthropic / Bedrock / Azure OpenAI 等）への抽象化ルーティングです。モデル選択・フォールバックを透過的に処理します。
- **横断機能**: トークン交換（[P08](../identity/p08-token-exchange-obo.md)）・PDP呼び出し（[P09](../identity/p09-dynamic-authz-pdp.md)）・セマンティックキャッシュ（[P24](../reliability/p24-semantic-cache.md)）・トレース送出（[P25](../reliability/p25-observability-tracing.md)）・メータリング・入出力ガードレールを集約します。
- テナント/部署別クォータを強制し、コスト按分（[P27](../reliability/p27-cost-governance.md)）の基盤とします。

## ユースケース

- 全社AI解禁の初期基盤として、Slack・Salesforce・ServiceNow 等の各業務アプリからのAI呼び出しを単一ゲートウェイに集約し、部署別コスト可視化・PII自動マスキング・モデル切替を一元管理します。
- 規制業種（金融・医療）で、全推論リクエストの監査ログを確実に取得し、入出力ガードレール（機密情報フィルタ・トピック制限）を統一適用します。

## 実装メモ

LiteLLM、Portkey、Kong AI Gateway、Cloudflare AI Gateway、Amazon Bedrock、OPA/Cedar（ポリシー評価）、OpenTelemetry GenAI semantic conventions、Redis（レート制限・キャッシュ）。

## 関連パターン

**カテゴリ**: 統合 ／ **対象**: 両方 ／ **成熟度**: 基盤

- [P08 トークン交換](../identity/p08-token-exchange-obo.md)
- [P09 動的認可PDP](../identity/p09-dynamic-authz-pdp.md)
- [P23 サーキットブレーカ/フォールバック](../reliability/p23-circuit-breaker-fallback.md)
- [P24 セマンティックキャッシュ](../reliability/p24-semantic-cache.md)
- [P25 オブザーバビリティ/トレーシング](../reliability/p25-observability-tracing.md)
- [P27 コストガバナンス](../reliability/p27-cost-governance.md)
