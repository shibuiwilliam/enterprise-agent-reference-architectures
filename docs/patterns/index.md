---
title: "パターンカタログ"
description: "7面・45のエンタープライズAIエージェント・アーキテクチャパターンの一覧。"
---

# パターンカタログ

パターンは「どの設計圧力（漏洩・サイロ・動的文脈・監査・コスト）に応えるか」で7面に分類している。この分類は責務境界とも一致し、[リファレンスアーキテクチャ](../integration/architecture/index.md)の層構造に対応する。

各パターンは共通スキーマ（**概要 / 設計 / 解決する企業課題 / 向き・不向き / 要素技術・既存システム連携 / 落とし穴・選定の勘所 / 関連パターン**）で記述する。スキーマの定義は[項目設計](../overview/schema.md)を参照。

## 面（カテゴリ）一覧

| 面 | テーマ | 主眼 | 数 |
|---|---|---|---|
| [面1 体験・ゲートウェイ (EX)](ex-experience/index.md) | 入口と提供面 | 仕事のある場所に届け、入口で統制 | 3 |
| [面2 制御・ガバナンス (GV)](gv-governance/index.md) | 統治・統制 | レジストリ・モデル統制・評価・コスト・事故対応 | 10 |
| [面3 アイデンティティ・信頼 (ID)](id-identity/index.md) | 権限の忠実な伝播 | 誰の権限で動くかを保証（設計難度が最も高い） | 8 |
| [面4 実行・オーケストレーション (RT)](rt-runtime/index.md) | 分業・実行・自動化 | 責任分担・自律度・副作用・長尺・イベント | 11 |
| [面5 知識・メモリ・コンテキスト (KM)](km-knowledge/index.md) | 漏らさず活かす | 権限を保ったまま横断文脈を供給 | 7 |
| [面6 統合・ツール (IN)](in-integration/index.md) | 既存システム連携 | 作らず束ね、固有差を吸収 | 4 |
| [面7 観測・評価・監査 (OB)](ob-observability/index.md) | 説明責任 | 三者帰責で全行為を再構成可能に | 2 |

!!! tip "読み方"
    面1〜2が「入口と統治」、面3が「権限の忠実な伝播（設計難度が高い）」、面4〜6が「実行と知識と連携」、面7が「説明責任」。積み上げる依存関係は[依存関係と依存チェーン](../integration/dependency-chain.md)を参照。

!!! info "最小安全セット：まずここから始める"
    45パターンを一度に導入する必要はない。以下の6パターンが「最小安全セット」であり、これだけで参照系エージェントを安全に稼働させ、段階的に拡張できる。

    1. **[GV-1 Agent Control Plane](gv-governance/gv1-agent-control-plane.md)** — エージェントの登録・ライフサイクル管理
    2. **[ID-2 Identity Federation & OBO](id-identity/id2-identity-federation-obo.md)** — 依頼者本人の権限で SaaS を操作
    3. **[ID-4 Permission Mirror & Least-of](id-identity/id4-permission-mirror-least-of.md)** — 最小権限の合成
    4. **[RT-6 SoR Write Boundary](rt-runtime/rt6-sor-write-boundary.md)** — 書き込み操作の境界制御
    5. **[KM-1 Access-Controlled RAG](km-knowledge/km1-access-controlled-rag.md)** — 権限認識の知識検索
    6. **[OB-2 Unified Audit & Lineage](ob-observability/ob2-unified-audit-lineage.md)** — 三者帰責の監査証跡

    この最小セットで開始し、業務要件の成熟に応じてガバナンス（GV-5/GV-7）→ 実行高度化（RT-3/RT-4/RT-7）→ 知識拡充（KM-2/KM-4）の順で拡張するのが推奨ルートだ。詳細は[成熟度ロードマップ](../integration/architecture/index.md)を参照。
