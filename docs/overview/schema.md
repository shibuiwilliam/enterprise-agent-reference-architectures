---
title: "項目設計と面（カテゴリ）分類"
description: "各パターンの共通記述スキーマ（6項目）と7面の分類設計を定義する。"
status: done
---

# 項目設計と面（カテゴリ）分類

## 共通記述スキーマ

各パターンを以下の項目で統一記述する。エンタープライズでは「落とし穴（アンチパターン）」が事故に直結するため、明示項目として独立させている。

| # | 項目 | 記述内容 |
|---|---|---|
| 1 | **概要** | 何であるかの一文要約 |
| 2 | **解決する企業課題** | どういう課題を解決するために、どのエンタープライズ固有の力（漏洩・サイロ・動的文脈・監査・コスト）に応えるか |
| 3 | **解決策と設計** | 課題の解決策と、それを実現する設計としての構造・データフロー・状態遷移・実装上の要点 |
| 4 | **向き／不向き** | 採用が効く条件と、害・過剰になる条件 |
| 5 | **要素技術・既存システム連携** | 代表技術・標準・対象SaaS |
| 6 | **落とし穴／選定の勘所** | 典型的な失敗と回避の指針 |
| 7 | **関連パターン** | 類似・補完・対比される他のパターンへのリンク |

!!! note "解決策と設計節の図"
    構造・データフロー・状態遷移・認可シーケンスは mermaid で記述する。特に [ID-2 OBO委譲](../patterns/id-identity/id2-identity-federation-obo.md)、[ID-6 PDP/PEP](../patterns/id-identity/id6-zero-trust-pdp-pep.md)、[RT-7 Saga](../patterns/rt-runtime/rt7-enterprise-saga.md)、[RT-10 イベント駆動](../patterns/rt-runtime/rt10-event-driven-orchestrator.md) はシーケンス/フロー図を推奨する。

## 面（カテゴリ）設計

パターンは「どの設計圧力に応えるか」で7面に分類する。これは責務境界とも一致し、[リファレンスアーキテクチャ](../integration/architecture/index.md)の層構造に対応する。

| 面 | テーマ | 主眼 | パターン数 |
|---|---|---|---|
| [面1 体験・ゲートウェイ (EX)](../patterns/ex-experience/index.md) | 入口と提供面 | 仕事のある場所に届け、入口で統制する | 3 |
| [面2 制御・ガバナンス (GV)](../patterns/gv-governance/index.md) | 統治・統制 | 一元レジストリ・モデル統制・評価・コスト・事故対応 | 10 |
| [面3 アイデンティティ・信頼 (ID)](../patterns/id-identity/index.md) | 権限の忠実な伝播 ★最難関 | 誰の権限で動くかを保証する | 8 |
| [面4 実行・オーケストレーション (RT)](../patterns/rt-runtime/index.md) | 分業・実行・自動化 | 責任分担・自律度・副作用・長尺・イベント | 11 |
| [面5 知識・メモリ・コンテキスト (KM)](../patterns/km-knowledge/index.md) | 漏らさず活かす | 権限を保ったまま横断文脈を供給 | 7 |
| [面6 統合・ツール (IN)](../patterns/in-integration/index.md) | 既存システム連携 | 作らず束ね、固有差を吸収 | 4 |
| [面7 観測・評価・監査 (OB)](../patterns/ob-observability/index.md) | 説明責任 | 三者帰責で全行為を再構成可能に | 2 |

### 面の読み方

面1〜2が「入口と統治」、面3が「最難関の権限」、面4〜6が「実行と知識と連携」、面7が「説明責任」である。これらを積み上げる依存関係は[依存関係と依存チェーン](../integration/dependency-chain.md)で示す。

### エンタープライズ固有の設計圧力

ここで言う設計圧力は、一般的なソフトウェア設計とは異なるエンタープライズ固有の力である。

| 設計圧力 | 具体例 |
|---|---|
| **漏洩** | 顧客データの社外流出、部門間の不正アクセス、PII の外部LLM送信 |
| **サイロ** | SaaS間のデータ分断、部門間の語彙差、横断文脈の統合不能 |
| **動的文脈** | 人事異動・プロジェクト終了による権限変更、リアルタイムな組織構造の反映 |
| **監査** | 規制対応の証跡、インシデント原因究明、説明責任の確保 |
| **コスト** | LLMトークンの部門按分、マルチエージェントの推論爆発、SaaS APIレート消費 |

### 横断軸

7面に加えて、以下の2つが全面を貫く横断軸として機能する。

- **組織グラフ**：全面がスコープ・委譲・承認を組織構造から一貫して導く土台。[ID-4](../patterns/id-identity/id4-permission-mirror-least-of.md)・[RT-1](../patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md)・[RT-4](../patterns/rt-runtime/rt4-human-approval-chain.md)・[KM-4](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) の根拠となる。
- **ゼロトラスト／監査**：全呼び出しを「人＋エージェント＋システム」の三者で認可・記録する。[ID-6](../patterns/id-identity/id6-zero-trust-pdp-pep.md)・[OB-2](../patterns/ob-observability/ob2-unified-audit-lineage.md) が中核を担う。
