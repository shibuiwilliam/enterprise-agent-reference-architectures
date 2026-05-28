---
title: "DC-8 モデルの強さ・データ分類別ルーティング"
description: "タスク難易度とデータ機密度に基づくモデル選択とルーティング経路を設計する連続量パラメータ。"
status: done
---

# DC-8 モデルの強さ・データ分類別ルーティング

## 概要

「会議室の予約方法を教えて」に最大規模のモデルを使うのはコストの無駄です。一方、複雑な契約書レビューを軽量モデルに任せれば品質が足りません。さらに顧客の個人情報を含むプロンプトを外部 API に送れば規制違反になりえます。タスクの難易度でモデルサイズを切り替え、データの機密度で推論経路（VPC 内か外部 API か）を分ける——この2軸のルーティングを [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md) でどう設計するかを示します。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-8
parameter: model_routing
rules:
  - condition: "task_difficulty == 'simple' AND data_classification IN ['public', 'internal_general']"
    model_size: lightweight
    routing_path: external_api_or_internal
    reason: "会議室予約方法などの単純タスクに最大規模モデルを使うのはコストの無駄。軽量モデルで処理を試みる"
  - condition: "confidence_score_below_threshold == true"
    model_size: escalate_to_stronger
    routing_path: same_as_original
    reason: "応答の信頼度が閾値を下回る、または検証エージェントが品質を否定した場合に、より強いモデルへエスカレーションする"
  - condition: "data_classification == 'top_secret'"
    routing_path: vpc_or_onprem_only
    external_api_allowed: false
    reason: "極秘データはVPC内またはオンプレミス推論経路のみを使用する。外部APIへの送信は禁止する"
  - condition: "data_classification IN ['public', 'internal_general'] AND latest_model_required == true AND dpa_confirmed == true"
    routing_path: external_api_permitted
    prerequisite: dpa_confirmed
    reason: "一般データは外部APIを含む経路を使用可とし、コスト・性能バランスで選択する。ただしDPA・リージョン・データ保持の統制が必要"
  - condition: "routing_automated == false"
    action: automate_routing_via_gv5
    reason: "極秘データのルーティング設定ミスは情報漏洩を引き起こす。分類別ルーティングはデータラベルに基づき自動適用し、手動設定に依存しない"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（弱いモデルに偏りすぎ） | すべてのタスクを軽量モデルで処理 | 複雑な推論・長文分析で品質が低下し、エラー修正コストが増えます |
| 過大（強いモデルに偏りすぎ） | すべてのタスクを最大モデルで処理 | 単純なタスクでもコストが過大になり、レイテンシも不必要に高くなります |

機密分類を無視したルーティングは別の問題を引き起こします。極秘データを外部 API に送信すると、規制違反・情報漏洩のリスクに直結します。

## 判断基準

モデルルーティングは「難易度軸」と「機密分類軸」の2軸で設計します。

**難易度軸：カスケードエスカレーション**

- タスク受付時に難易度を推定し、まず軽量モデルで処理を試みます。
- 応答の信頼度が閾値を下回った場合、または検証エージェントが品質を否定した場合に、より強いモデルへエスカレーションします。
- エスカレーション率を [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) で継続計測し、閾値の妥当性を評価します。

**機密分類軸：経路の分離**

- 極秘データ（[KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) 対象）は VPC 内またはオンプレミス推論経路のみを使います。外部 API への送信は認めません。
- 一般データは外部 API を含む経路を使用可とし、コスト・性能バランスで選択します。
- 分類別ルーティング比率（VPC vs 外部）を定期確認し、分類エラーによる漏洩がないかを検証します。

[GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) でモデル別の品質スコアを比較し、エスカレーション閾値の調整に活用します。

!!! danger "機密分類ルーティングの誤設定"
    極秘データのルーティング設定ミスは、情報漏洩を引き起こします。機密分類ルーティングはデータラベル（[GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) の分類ポリシー）に基づき自動適用し、手動設定に依存しない仕組みにしてください。

## 調整の仕組み

- エスカレーション率を [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) で経路別・タスク種別に計測し、難易度推定の精度を継続的に改善します。
- VPC 経路と外部 API 経路それぞれのコスト・レイテンシ・品質スコアを [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) と連動して追跡します。
- 機密分類別のルーティング比率を定期レビューし、データラベリングの精度に問題がないか確認します。

## 関連パターン

- [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md) — モデルルーティングの実装本体
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) — 極秘データの安全な処理経路
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — モデル別品質評価と閾値調整

## 候補と推奨

| 状況／前提 | 推奨設定 | 必要パターン | トレードオフ |
|---|---|---|---|
| 単純Q&A・定型業務 | 軽量モデル・外部API可 | GV-5 | 複雑タスクで品質不足 |
| 複雑な分析・契約レビュー | 大規模モデル・カスケード | GV-5, GV-7 | コスト高・レイテンシ増 |
| 極秘データ処理 | VPC内／オンプレミス限定 | GV-5, KM-7 | モデル選択肢の制約 |

```yaml
decision:
  id: DC-8
  title: "モデルの強さ・データ分類別ルーティング"
  options:
    - id: lightweight_external
      name: "軽量モデル・外部API"
      patterns: [GV-5]
      pros: [低コスト, 高速応答]
      cons: [複雑推論で品質低下]
      pick_when: ["単純Q&A", "公開データ", "定型業務"]
    - id: cascade
      name: "カスケードエスカレーション"
      patterns: [GV-5, GV-7]
      pros: [コストと品質のバランス]
      cons: [エスカレーション時の遅延]
      pick_when: ["難易度不定", "複合タスク"]
    - id: vpc_strong
      name: "VPC内大規模モデル"
      patterns: [GV-5, KM-7]
      pros: [高品質, データ主権確保]
      cons: [インフラコスト高, モデル更新遅延]
      pick_when: ["極秘データ", "規制対応", "契約レビュー"]
  default_recommendation: "軽量モデルで開始しカスケードで品質担保、極秘データはVPC内経路に限定"
```
