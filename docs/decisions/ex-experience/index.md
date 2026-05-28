---
title: "EX — Experience & Gateway 意思決定"
description: "エージェントの入口設計・チャネル戦略・信頼UXに関する意思決定の索引。"
status: done
---

# EX — Experience & Gateway 意思決定

エージェントが従業員・顧客に届く「体験面」の設計判断をまとめています。統一入口（Gateway）の構成、チャネル配置、信頼と価値実感のUX設計が対象です。

## 意思決定一覧

| ID | 問い | タイプ | 構成要素 |
|---|---|---|---|
| [EX-D1](ex-d1-front-door-channel.md) | 統一フロントドアとチャネル戦略（埋め込み／独立ワークベンチ／両用） | baseline+tradeoff | EX-1, EX-2, EX-3 |
| [EX-D2](ex-d2-trust-value-ux.md) | 信頼・価値実感UXの強度（根拠提示・確信度・撤回可能性） | degree | EX-4 |

## ドメインの位置づけ

Experience & Gateway は、エージェントアーキテクチャの最前面に位置します。Identity（ID）ドメインが「誰として動くか」を決め、Runtime（RT）ドメインが「どう実行するか」を担うのに対し、EX ドメインは「どこから・どのように届けるか」を設計します。Gateway はすべてのチャネルからのリクエストを受ける単一統制点であり、ID・RT・OB 各ドメインの機能を呼び出す最初の接点となります。
