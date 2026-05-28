---
title: "KM --- Knowledge & Memory 意思決定"
description: "エージェントの知識供給・メモリ管理・機密保護に関する意思決定の索引。"
status: done
---

# KM --- Knowledge & Memory 意思決定

エージェントが「何を知り・何を覚え・何を忘れるか」の設計判断をまとめています。文脈の供給方式、知識の正規化、メモリのスコープと保持、目的限定、機密保護の強度が対象です。

## 意思決定一覧

| ID | 問い | タイプ | 構成要素 |
|---|---|---|---|
| [KM-D1](km-d1-context-supply.md) | 文脈供給：集約データレイク vs フェデレーテッド Mesh（権限認識 RAG）、投入量 | tradeoff+degree | KM-1, KM-2, TO-2, DC-4 |
| [KM-D2](km-d2-knowledge-normalization.md) | 全社知識の正規化（正規オブジェクト／知識グラフ） | baseline | KM-3 |
| [KM-D3](km-d3-memory-scope.md) | メモリのスコープと保持（個人 vs チーム、TTL・忘却） | tradeoff+degree | KM-4, TO-6, DC-5 |
| [KM-D4](km-d4-purpose-limitation.md) | 目的限定と最小化（目的限定コンテキスト） | degree | KM-5 |
| [KM-D5](km-d5-confidentiality-strength.md) | 機密保護の強度（DLP・マスキング、揮発・機密計算） | degree | KM-6, KM-7 |

## ドメインの位置づけ

Knowledge & Memory は、エージェントが「どの情報を・どの権限で・どの目的で・どの保護強度で扱うか」を設計する面です。Identity（ID）ドメインが「誰として動くか」を決め、Runtime（RT）ドメインが「どう実行するか」を担うのに対し、KM ドメインは「何を知り、何を覚え、何を守るか」を設計します。ID ドメインの権限モデル（ID-2 OBO、ID-4 Permission Mirror）が KM の全パターンの前提となり、Governance（GV）ドメインのモデルゲートウェイ（GV-5）が機密ルーティングの統制点となります。
