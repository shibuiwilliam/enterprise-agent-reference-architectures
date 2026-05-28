---
title: "意思決定カタログ"
description: "エンタープライズAIエージェントのアーキテクチャ設計で決めるべき31の意思決定を7ドメインに分類した一覧。"
status: done
---

# 意思決定カタログ

本カタログは、エンタープライズにAIエージェントを組み込む際に**決めるべき問い（意思決定）**を網羅しています。各意思決定は「問い→選択肢→判断軸→推奨→必要な構成要素→効く価値→落とし穴→機械可読サマリ」の統一スキーマで記述されています。

## 意思決定の3類型

| 類型 | 記号 | 意味 |
|---|---|---|
| **基盤** | baseline | 必須の構成要素を導入するか・どう形作るかを決めます |
| **相反** | tradeoff | 競合する仕組みのどちらを選ぶかを決めます |
| **程度** | degree | どこまで／どの強さで調整するかを決めます |

## 7つの意思決定ドメイン

| ドメイン | 意思決定数 | 概要 |
|---|---|---|
| [体験・ゲートウェイ（D-EX）](ex-experience/index.md) | 2 | 統一フロントドア・チャネル戦略・信頼UX |
| [ガバナンス・統制（D-GV）](gv-governance/index.md) | 7 | 統制プレーン・モデル統制・評価・コスト・事故対応・規制・価値計測 |
| [アイデンティティ・信頼（D-ID）](id-identity/index.md) | 6 | 二面分離・委譲方式・権限縮退・資格情報・認可・同意 |
| [実行・オーケストレーション（D-RT）](rt-runtime/index.md) | 6 | 分業・自律度・副作用・長尺処理・起動契機・デジタルツイン |
| [知識・メモリ（D-KM）](km-knowledge/index.md) | 5 | 文脈供給・知識正規化・メモリスコープ・目的限定・機密保護 |
| [統合・ツール（D-IN）](in-integration/index.md) | 3 | ツールゲートウェイ・構築vs再利用・レート調停 |
| [観測・監査（D-OB）](ob-observability/index.md) | 2 | 観測範囲・監査帰責 |

合計 **31 の意思決定** があります。

## 全意思決定一覧

| ID | 意思決定 | 類型 | 構成要素（旧パターンID） |
|---|---|---|---|
| [EX-D1](ex-experience/ex-d1-front-door-channel.md) | 統一フロントドアとチャネル戦略 | 基盤＋相反 | EX-1, EX-2, EX-3 |
| [EX-D2](ex-experience/ex-d2-trust-value-ux.md) | 信頼・価値実感UXの強度 | 程度 | EX-4 |
| [GV-D1](gv-governance/gv-d1-control-plane-scope.md) | 統制プレーンの導入と範囲 | 基盤＋相反 | GV-1, GV-2, GV-3, TO-8 |
| [GV-D2](gv-governance/gv-d2-model-vendor-routing.md) | モデル・ベンダー・データ経路の統制 | 相反＋程度 | GV-5, TO-10, DC-8 |
| [GV-D3](gv-governance/gv-d3-change-eval-rigor.md) | 変更管理と評価の厳格度 | 程度 | GV-6, GV-7, DC-9 |
| [GV-D4](gv-governance/gv-d4-cost-visibility.md) | コストの可視化と配賦 | 程度 | GV-8, DC-2 |
| [GV-D5](gv-governance/gv-d5-incident-kill-switch.md) | 事故対応と停止粒度 | 基盤 | GV-9 |
| [GV-D6](gv-governance/gv-d6-industry-regulation.md) | 業界規制の組み込み | 基盤 | GV-4 |
| [GV-D7](gv-governance/gv-d7-value-measurement.md) | 価値計測の設計 | 基盤 | GV-10 |
| [ID-D1](id-identity/id-d1-workforce-customer-split.md) | 従業員面／顧客面の分離 | 基盤 | ID-1 |
| [ID-D2](id-identity/id-d2-delegation-method.md) | 実行主体と権限の委譲方式 | 相反 | ID-2, ID-3, TO-1 |
| [ID-D3](id-identity/id-d3-permission-reduction.md) | 権限の忠実な縮退 | 基盤 | ID-4 |
| [ID-D4](id-identity/id-d4-credential-minimization.md) | 資格情報の最小・短命化 | 程度 | ID-5, DC-7 |
| [ID-D5](id-identity/id-d5-authorization-method.md) | 認可の決定方式 | 基盤＋相反＋程度 | ID-6, ID-7, TO-12, DC-6 |
| [ID-D6](id-identity/id-d6-consent-transparency.md) | 同意と透明化の範囲 | 程度 | ID-8 |
| [RT-D1](rt-runtime/rt-d1-single-vs-multi-agent.md) | 単一 vs マルチエージェントと分業 | 相反 | RT-1, RT-2, TO-3 |
| [RT-D2](rt-runtime/rt-d2-autonomy-design.md) | 自律度の設計 | 相反＋程度 | RT-3, RT-4, TO-4, TO-5, DC-1 |
| [RT-D3](rt-runtime/rt-d3-side-effect-safety.md) | 副作用の安全な実行 | 基盤 | RT-5, RT-6 |
| [RT-D4](rt-runtime/rt-d4-long-running-reliability.md) | 長尺・分散処理の信頼性 | 基盤＋相反＋程度 | RT-7, RT-8, TO-11, DC-2 |
| [RT-D5](rt-runtime/rt-d5-trigger-mechanism.md) | 起動契機 | 基盤＋程度 | RT-9, RT-10, DC-9 |
| [RT-D6](rt-runtime/rt-d6-project-digital-twin.md) | プロジェクト・デジタルツイン | 基盤 | RT-11 |
| [KM-D1](km-knowledge/km-d1-context-supply.md) | 文脈供給の方式と投入量 | 相反＋程度 | KM-1, KM-2, TO-2, DC-4 |
| [KM-D2](km-knowledge/km-d2-knowledge-normalization.md) | 全社知識の正規化 | 基盤 | KM-3 |
| [KM-D3](km-knowledge/km-d3-memory-scope.md) | メモリのスコープと保持 | 相反＋程度 | KM-4, TO-6, DC-5 |
| [KM-D4](km-knowledge/km-d4-purpose-limitation.md) | 目的限定と最小化 | 程度 | KM-5 |
| [KM-D5](km-knowledge/km-d5-confidentiality-strength.md) | 機密保護の強度 | 程度 | KM-6, KM-7 |
| [IN-D1](in-integration/in-d1-tool-gateway.md) | ツール接続の統制 | 基盤 | IN-1 |
| [IN-D2](in-integration/in-d2-build-vs-reuse.md) | 自前構築 vs 既存資産 | 相反 | IN-2, IN-4, TO-9 |
| [IN-D3](in-integration/in-d3-rate-capacity.md) | レート・容量の調停 | 程度 | IN-3 |
| [OB-D1](ob-observability/ob-d1-observability-scope.md) | 観測の範囲とログ粒度 | 程度＋相反 | OB-1, DC-3, TO-7 |
| [OB-D2](ob-observability/ob-d2-audit-attribution.md) | 監査と帰責 | 基盤 | OB-2 |
