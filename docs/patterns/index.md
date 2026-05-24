---
title: "パターンカタログ"
description: "12カテゴリ・約50のAIエージェント・アーキテクチャパターンの一覧。"
---

# パターンカタログ

パターンは「どの設計圧力（force）に応えるか」で12カテゴリに分類している。これは責務境界とも一致し、[リファレンスアーキテクチャ](../integration/reference-architecture.md)の層構造に対応する。

各パターンは共通スキーマ（**概要 / 設計 / 解決する課題 / ユースケース / 向き / 不向き / 要素技術 / 関連パターン**）で記述する。スキーマの定義は[項目設計](../overview/schema.md)を参照。

## カテゴリ一覧

| カテゴリ | テーマ | 主眼 |
|---|---|---|
| [A](a-execution/index.md) | 実行・セッション・オーケストレーション | 長く・止まり・再開し・暴走しうる実行を骨格化 |
| [B](b-composition/index.md) | エージェント構成・分担 | 何を決定論に残し、どこをどう分業するか |
| [C](c-io-contract/index.md) | 入出力・契約化 | 曖昧な自然言語を安全な契約へ変換 |
| [D](d-tools-mcp/index.md) | ツール・MCP・外部接続 | 副作用の最重要リスク境界の統制 |
| [E](e-memory/index.md) | メモリ・コンテキスト管理 | 記憶を保存・忘却・権限付きのデータ機能に |
| [F](f-reliability/index.md) | 信頼性・検証・ガードレール | 確率的出力を品質保証された出力へ |
| [G](g-security/index.md) | セキュリティ・マルチテナント | 騙されても被害が小さい設計 |
| [H](h-cost-performance/index.md) | コスト・性能・可用性 | 高コスト・可変・不安定の資源管理 |
| [I](i-observability/index.md) | 観測性・評価・変更管理（LLMOps） | 測定・再現・安全な継続変更 |
| [J](j-abstraction/index.md) | デプロイ・ベンダー抽象化 | モデル/SDKロックインの構造的隔離 |
| [K](k-human/index.md) | 人間協調・UI/UX | 制御された自律性と協働点の設計 |
| [L](l-adoption/index.md) | 導入・移行・統治 | 後付け統合と段階的な信頼獲得 |

!!! tip "読み方"
    A〜Bは「骨格」、C〜Gは「安全と品質の境界層」、H〜Jは「資源と運用」、K〜Lは「人とプロセス」。これらを積み上げる依存関係は[統合](../integration/dependencies.md)を参照。
