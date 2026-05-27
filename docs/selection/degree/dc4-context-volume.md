---
title: "DC-4 コンテキスト投入量（top-k・トークン予算）"
description: "RAG等で取得したコンテキストをどれだけプロンプトに投入するか、目的限定で最小化する連続量パラメータ。"
status: done
---

# DC-4 コンテキスト投入量（top-k・トークン予算）

## 概要

RAG で社内文書を 50 件取得できたとして、すべてをプロンプトに詰め込めば精度が上がるわけではない。トークンの大量消費とレイテンシ悪化が生じるだけでなく、中盤の情報が無視される「lost in the middle」現象で回答品質がむしろ下がることもある。「使えるデータ」ではなく「このタスクに必要な最小のデータ」に絞る（[KM-5 Purpose-Bound Context](../../patterns/km-knowledge/km5-purpose-bound-context.md)）ために、top-k やトークン予算をどう設定するかを扱う。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-4
parameter: context_volume
rules:
  - condition: "task_type == 'qa' AND data_type == 'public_knowledge'"
    recommended_top_k: 3
    token_budget_fraction: 0.25
    reason: "事実確認Q&Aは上位3件程度で十分。全件投入は「lost in the middle」現象で回答品質が下がることがある"
  - condition: "task_type == 'analysis' AND multiple_source_comparison == true"
    recommended_top_k: 10
    token_budget_fraction: 0.5
    reranking: required
    reason: "多ソース比較分析は広いコンテキストが有効。リランカーで件数をさらに絞り、トークン予算内に圧縮する"
  - condition: "data_classification IN ['department_confidential', 'top_secret'] AND context_contains_sensitive_fields == true"
    action: dlp_mask_before_inject
    reason: "機密度の高い情報はKM-6 DLP & Redaction Boundaryでマスキング後に投入する。生の機密データをそのまま投入しない"
  - condition: "cost_constraint == true AND data_classification == 'public'"
    action: reduce_to_purpose_bound_minimum
    reason: "「使えるデータ」を全件投入するのは過剰。KM-5の目的限定原則に従い、タスクに不要な属性・フィールドは投入しない"
  - condition: "eval_complete == false"
    action: ab_test_top_k_values
    reason: "top-kやトークン予算の値を段階的に変えたA/Bテストで最適点を探り、GV-7でコスト対品質比を追跡する"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（少なすぎ） | top-k が小さすぎ、関連文脈が欠落 | 回答品質が低下し、幻覚が増加する |
| 過大（多すぎ） | 取得可能なデータを全件投入 | 精度低下（lost in the middle 現象）、コスト増、レイテンシ悪化、不要な機密情報の拡散 |

## 判断基準

- 関連度ランキングで上位のみを選択し、リランカーでさらに件数を絞る
- タスクの種類（Q&A・要約・分析）によって必要な量は異なる。目的別にトークン予算を設定し、その範囲内に収めるようにする
- [KM-5](../../patterns/km-knowledge/km5-purpose-bound-context.md) の目的限定原則に従い、タスクに不要な属性・フィールドは投入しない
- 機密度の高い情報は [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) でマスキングしてから投入する

## 調整の仕組み

- [GV-7 Evaluation Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) で回答品質と投入量の相関を計測する
- top-k やトークン予算を段階的に変えた A/B テストで最適点を探る
- [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) でトークン消費量と品質スコアの推移を監視し、コスト対品質比を継続追跡する

## 関連パターン

- [KM-5 Purpose-Bound Context](../../patterns/km-knowledge/km5-purpose-bound-context.md) — 目的限定の原則
- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — 権限認識 RAG でのコンテキスト取得
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — フェデレーテッド取得でのコンテキスト量制御
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — 投入前のマスキング
