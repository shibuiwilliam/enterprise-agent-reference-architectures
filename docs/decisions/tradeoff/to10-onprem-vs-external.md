---
title: "TO-10 内部/オンプレモデル vs 外部 API"
description: "データ分類で推論経路を自動ルーティングし、極秘・規制データはVPC/オンプレ、一般・最新性能が必要なケースは外部APIを使い分ける設計指針。"
status: done
---

# TO-10 内部/オンプレモデル vs 外部 API

## 概要

顧客の医療情報を含むプロンプトを外部 API に送信すれば規制違反になりえます。一方、社内 FAQ の回答のために高価な GPU インフラを自前で運用するのはコストが見合いません。「全部オンプレ」も「全部外部 API」もどちらも現実的ではありません。データの機密度に応じて推論経路を自動的に切り替えるハイブリッドが実務解です。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-10
decision_rules:
  - condition: "data_classification IN ['top_secret', 'department_confidential'] AND cross_border_transfer_prohibited == true"
    recommendation: internal_onprem
    reason: "極秘データ（社内秘・個人情報・競争情報等）を含むプロンプトは内部/オンプレモデルが必須"
  - condition: "regulatory_requirement IN ['gdpr', 'financial', 'medical'] AND cross_border_transfer_prohibited == true"
    recommendation: internal_onprem
    reason: "GDPR・金融規制・医療規制等で国外への持ち出しが規制されるデータは内部推論経路のみを使用する"
  - condition: "data_classification IN ['public', 'internal_general'] AND latest_model_required == true"
    recommendation: external_api
    reason: "一般公開情報や権限不要の社内規程を扱う推論、最新モデル性能を必要とするユースケースは外部APIが適切"
  - condition: "data_classification == 'department_confidential' AND data_classification == 'public'"
    recommendation: hybrid_data_classification_routing
    reason: "GV-5のCentral Model Gatewayがデータ分類に応じて推論経路を自動ルーティングするため、開発者が都度判断する手間を排除できる"
  - condition: "dpa_confirmed == false AND data_classification IN ['public', 'internal_general']"
    recommendation: internal_onprem
    reason: "外部APIを使う際はDPA・利用リージョン・データ保持ポリシーを必ず確認する。デフォルト設定のまま利用すると意図しないデータ利用や越境転送のリスクがある"
```

## 比較

| 観点 | 内部/オンプレモデル | 外部API |
|---|---|---|
| データ主権 | 完全に自社内 | ベンダーの処理・保存ポリシーに依存 |
| 向き | 極秘データ・規制対象データ・大量定常推論 | 一般的な業務・最新モデル性能が必要・変動需要 |
| 性能 | 最新モデルへの追従が遅い | 最新モデルを即時利用可能 |
| コスト構造 | 固定コスト（インフラ・保守） | 従量制（需要に追随するが高コストになりやすい） |
| 可用性 | 自社インフラの信頼性に依存 | SLAをベンダーが保証 |
| セットアップ | 複雑（GPU・モデル管理・MLOps） | 即日開始可能 |

## 判断基準

データの機密性分類で推論経路を決めます。

**内部/オンプレモデルが必須の条件**：

- 極秘データ（社内秘・個人情報・競争情報等）を含むプロンプト
- GDPR・金融規制・医療規制等で国外への持ち出しが規制されるデータ
- 大量かつ定常的な推論ニーズがあり、固定コストの方が安くなるケース

**外部APIが適切な条件**：

- 一般公開情報や権限不要の社内規程を扱う推論
- 最新のモデル性能を必要とするユースケース（R&D支援等）
- 需要が変動し、固定インフラコストを避けたいケース
- ただし、DPA（Data Processing Agreement）・利用リージョン・データ保持ポリシーを必ず確認・統制する

[GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) がデータ分類に応じて推論経路を自動ルーティングすることで、開発者が都度判断する手間を省けます。

## ハイブリッド・段階的アプローチ

同一アプリケーション内でデータ分類に応じた経路分岐を行うのが標準設計です。

1. [GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) の Central Model Gateway を設置し、全推論リクエストを経由させます。
2. データ分類ラベル（機密性・規制対象フラグ等）をリクエストに付与する仕組みを整備します。
3. Gateway が分類ラベルに基づき、内部モデル／外部 API へ自動振り分けします。
4. 外部 API 利用時は DPA・リージョン・データ保持の統制パラメータを Gateway で一元管理します。

!!! warning "外部APIへのデータ送信前にDPAを確認する"
    外部APIを使う際、ベンダーとのData Processing Agreementが締結されているか、利用リージョンが要件を満たすか、入力データがモデル学習に使われないかを必ず確認してください。デフォルト設定のまま外部 API を利用すると、意図しないデータ利用や越境転送のリスクがあります。

## 関連パターン

- [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md)
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 極秘・規制対象データの推論 | 内部/オンプレ（A） | GV-5, KM-7 | 最新モデル追従遅延・固定コスト |
| 一般情報・最新性能・変動需要 | 外部API（B） | GV-5, GV-8 | データ主権リスク・DPA確認必須 |
| データ分類で推論経路を自動分岐 | ハイブリッド（C） | GV-5, KM-7, GV-8 | Gateway設計・運用の複雑度↑ |

```yaml
decision:
  id: TO-10
  title: "内部/オンプレモデル vs 外部 API"
  options:
    - id: A
      name: "Internal/On-Prem"
      patterns: [GV-5, KM-7]
      pros: [データ主権完全, 規制準拠, 大量定常推論でコスト有利]
      cons: [最新モデル追従遅延, GPU運用コスト, セットアップ複雑]
      pick_when: ["極秘データ", "規制対象データ", "大量定常推論"]
    - id: B
      name: "External API"
      patterns: [GV-5, GV-8]
      pros: [最新モデル即時利用, 従量制, 即日開始]
      cons: [データ主権リスク, DPA確認必須, 高コストになりやすい]
      pick_when: ["一般公開情報", "最新性能が必要", "変動需要"]
    - id: C
      name: "Hybrid Data-Classification Routing"
      patterns: [GV-5, KM-7, GV-8]
      pros: [データ分類に応じた最適経路, 開発者の判断負荷排除]
      cons: [Gateway設計・運用の複雑度]
      pick_when: ["機密と一般が混在", "Central Model Gateway導入済み"]
  default_recommendation: "C (Hybrid)でGV-5 Central Model Gatewayによるデータ分類ルーティングを標準構成とする"
```
