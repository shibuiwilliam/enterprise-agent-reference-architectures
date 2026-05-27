---
title: "DC-3 プロンプト/トレースのログ粒度（三層分離）"
description: "メタデータ・本文・集計の三層に分離し、ログの粒度と保存先を決める連続量パラメータ。"
status: done
---

# DC-3 プロンプト/トレースのログ粒度（三層分離）

## 概要

エージェントが何を考え、何を出力したかを後から追えなければ、障害調査も品質改善もできない。一方でプロンプトと応答をすべて平文で保存すれば、ログ基盤に PII や機密情報が拡散し、ストレージコストも急増する。「何をどこまで記録するか」の粒度を、メタデータ・本文・集計の三層（[OB-1](../../patterns/ob-observability/ob1-observability-lake.md)）に分けて設計する方法を扱う。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-3
parameter: log_granularity
rules:
  - condition: "data_classification == 'top_secret'"
    log_layer: metadata_only
    storage: trace_db
    body_retention: none
    reason: "極秘処理はメタデータのみ（リクエストID・タイムスタンプ・処理完了フラグ）。本文は一切保存しない"
  - condition: "data_classification IN ['internal_general', 'department_confidential'] AND audit_required == true"
    log_layer: three_layer_separated
    storage_metadata: trace_db
    storage_body: encrypted_object_storage
    storage_aggregate: dwh
    pii_masking: required_before_body_storage
    reason: "標準構成：メタはTrace DB、PIIマスキング済み本文は暗号化オブジェクトストレージ、集計はDWH"
  - condition: "cost_constraint == true"
    sampling_strategy: "error_events + high_risk_operations + random_N_percent"
    recommended_n_percent: 5
    reason: "全件保存が不要な場合はエラー時・高リスク操作時・ランダムN%のみフル保存するサンプリング方式でコストを制御する"
  - condition: "regulatory_requirement != 'none'"
    retention_policy: per_data_classification_per_regulation
    deletion_rule: required
    reason: "規制対象データはデータ分類別に保持ポリシーと削除ルールを設定する。再現性より法令遵守を優先する"
  - condition: "confidential_data_in_result == true AND defense_in_depth == false"
    log_layer: three_layer_separated
    action: remediate_immediately
    reason: "機密情報を含むプロンプトを平文で一般的なログ基盤に保存することはセキュリティインシデントの原因になるため即座に修正する"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（記録しなさすぎ） | メタデータのみ、本文なし | インシデント時の再現・原因究明ができない。品質改善のフィードバックループが回らない |
| 過大（記録しすぎ） | 全プロンプト・全応答を平文で全件保存 | ストレージコストが爆発し、PII・機密情報がログ基盤に拡散する |

## 判断基準

三層に分離し、それぞれの保存先と粒度を個別に決めることが基本だ。

| 層 | 内容 | 保存先 |
|---|---|---|
| メタデータ | モデル名・版・トークン数・レイテンシ・コスト・相関 ID・使用ツール・成否・risk_tier | Trace DB |
| 本文 | プロンプト・取得文脈・成果物（PII マスキング済み） | 暗号化オブジェクトストレージ |
| 集計 | 品質スコア・集計指標 | DWH |

- 極秘処理（[KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)）は本文をログに残さず、メタデータのみ保存する
- 全件保存が不要な場合は、エラー時・低評価時・ランダム N% のみフル保存するサンプリング方式を組み合わせるとコストを抑えられる

## 調整の仕組み

- サンプリング率は [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) の計測結果（エラー率・品質スコア分布）をもとに動的に調整する
- ストレージコストと保持期間は [GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) の予算に従属させる
- 規制要件（監査ログの保持義務）と機密要件（PII 最小化）のどちらを優先するか、データ分類ごとに保持ポリシーを定めておく

## 関連パターン

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) — 三層分離の設計本体
- [OB-2 Unified Audit & Lineage](../../patterns/ob-observability/ob2-unified-audit-lineage.md) — 監査証跡としてのログ要件
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) — 極秘処理でログを残さない設計
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — PII マスキングの実装
- [TO-7 全プロンプトログ vs 選択的トレースログ](../tradeoff/to7-full-vs-selective-log.md) — 全件 vs 選択的の判断軸
