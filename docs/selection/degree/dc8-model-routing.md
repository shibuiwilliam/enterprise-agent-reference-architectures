---
title: "DC-8 モデルの強さ・データ分類別ルーティング"
description: "タスク難易度とデータ機密度に基づくモデル選択とルーティング経路を設計する連続量パラメータ。"
status: done
---

# DC-8 モデルの強さ・データ分類別ルーティング

## 概要

「会議室の予約方法を教えて」に最大規模のモデルを使うのはコストの無駄だが、複雑な契約書レビューを軽量モデルに任せれば品質が足りない。さらに、顧客の個人情報を含むプロンプトを外部 API に送れば規制違反になりうる。タスクの難易度でモデルサイズを切り替え、データの機密度で推論経路（VPC 内か外部 API か）を分ける——この2軸のルーティングを [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md) でどう設計するかを扱う。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-8
parameter: model_routing
rules:
  - condition: "task_difficulty == 'simple' AND data_classification IN ['public', 'internal_general']"
    model_size: lightweight
    routing_path: external_api_or_internal
    reason: "会議室予約方法などの単純タスクに最大規模モデルを使うのはコストの無駄。軽量モデルで処理を試みる"
  - condition: "confidence_score < threshold AND verifier_rejects == true"
    model_size: escalate_to_stronger
    routing_path: same_as_original
    reason: "応答の信頼度が閾値を下回る、または検証エージェントが品質を否定した場合に、より強いモデルへエスカレーションする"
  - condition: "data_classification == 'top_secret'"
    routing_path: vpc_or_onprem_only
    external_api_allowed: false
    reason: "極秘データはVPC内またはオンプレミス推論経路のみを使用する。外部APIへの送信は禁止する"
  - condition: "data_classification IN ['public', 'internal_general'] AND latest_capability_required == true"
    routing_path: external_api_permitted
    prerequisite: dpa_confirmed
    reason: "一般データは外部APIを含む経路を使用可とし、コスト・性能バランスで選択する。ただしDPA・リージョン・データ保持の統制が必要"
  - condition: "routing_config_manual == true AND classification_auto_labeling == false"
    action: automate_routing_via_gv5
    reason: "極秘データのルーティング設定ミスは情報漏洩を引き起こす。分類別ルーティングはデータラベルに基づき自動適用し、手動設定に依存しない"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（弱いモデルに偏りすぎ） | すべてのタスクを軽量モデルで処理 | 複雑な推論・長文分析で品質が低下し、エラー修正コストが増える |
| 過大（強いモデルに偏りすぎ） | すべてのタスクを最大モデルで処理 | 単純なタスクでもコストが過大になり、レイテンシも不必要に高くなる |

機密分類を無視したルーティングは別の問題を引き起こす。極秘データを外部 API に送信すると、規制違反・情報漏洩のリスクに直結する。

## 判断基準

モデルルーティングは「難易度軸」と「機密分類軸」の2軸で設計する。

**難易度軸：カスケードエスカレーション**

- タスク受付時に難易度を推定し、軽量モデルから処理を試みる
- 応答の信頼度が閾値を下回る場合、または検証エージェントが品質を否定した場合に、より強いモデルへエスカレーションする
- エスカレーション率を [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) で継続計測し、閾値の適切さを評価する

**機密分類軸：経路の分離**

- 極秘データ（[KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) 対象）は VPC 内またはオンプレミス推論経路のみを使用する。外部 API への送信は禁止する
- 一般データは外部 API を含む経路を使用可とし、コスト・性能バランスで選択する
- 分類別ルーティング比率（VPC vs 外部）を定期確認し、分類エラーによる漏洩がないか検証する

[GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) でモデル別の品質スコアを比較し、エスカレーション閾値の調整に活用する。

!!! danger "機密分類ルーティングの誤設定"
    極秘データのルーティング設定ミスは、情報漏洩を引き起こす。機密分類ルーティングはデータラベル（[GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) の分類ポリシー）に基づき自動適用し、手動設定に依存しない仕組みにする。

## 調整の仕組み

- エスカレーション率を [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) で経路別・タスク種別に計測し、難易度推定モデルの精度を継続改善する
- VPC 経路と外部 API 経路それぞれのコスト・レイテンシ・品質スコアを [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) と連動して追跡する
- 機密分類別のルーティング比率を定期レビューし、データラベリングの精度を検証する

## 関連パターン

- [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md) — モデルルーティングの実装本体
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) — 極秘データの安全な処理経路
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — モデル別品質評価と閾値調整
