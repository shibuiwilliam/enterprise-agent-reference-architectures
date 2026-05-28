---
title: "DC-3 プロンプト/トレースのログ粒度（三層分離）"
description: "メタデータ・本文・集計の三層に分離し、ログの粒度と保存先を決める連続量パラメータ。"
status: done
---

# DC-3 プロンプト/トレースのログ粒度（三層分離）

## 概要

エージェントが何を考え、何を出力したかを後から追えなければ、障害調査も品質改善もできません。しかしプロンプトと応答をすべて平文で保存すれば、ログ基盤に PII や機密情報が拡散し、ストレージコストも急増します。「何をどこまで記録するか」の粒度を、メタデータ・本文・集計の三層（[OB-1](../../patterns/ob-observability/ob1-observability-lake.md)）に分けて設計する方法を示します。

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
| 過小（記録しなさすぎ） | メタデータのみ、本文なし | インシデント時の再現・原因究明ができません。品質改善のフィードバックループが回りません |
| 過大（記録しすぎ） | 全プロンプト・全応答を平文で全件保存 | ストレージコストが爆発し、PII・機密情報がログ基盤に拡散します |

## 判断基準

三層に分けて、それぞれの保存先と粒度を個別に決めるのが基本方針です。

| 層 | 内容 | 保存先 |
|---|---|---|
| メタデータ | モデル名・版・トークン数・レイテンシ・コスト・相関 ID・使用ツール・成否・risk_tier | Trace DB |
| 本文 | プロンプト・取得文脈・成果物（PII マスキング済み） | 暗号化オブジェクトストレージ |
| 集計 | 品質スコア・集計指標 | DWH |

- 極秘処理（[KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)）は本文をログに残さず、メタデータのみ保存します
- 全件保存が不要な場合は、エラー時・低評価時・ランダム N% のみフル保存するサンプリング方式を組み合わせるとコストを抑えられます

## 調整の仕組み

- サンプリング率は [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) の計測結果（エラー率・品質スコア分布）をもとに動的に調整します。
- ストレージコストと保持期間は [GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) の予算に従属させます。
- 規制要件（監査ログの保持義務）と機密要件（PII 最小化）のどちらを優先するかは、データ分類ごとに保持ポリシーを定めておくことで解決します。

## 関連パターン

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) — 三層分離の設計本体
- [OB-2 Unified Audit & Lineage](../../patterns/ob-observability/ob2-unified-audit-lineage.md) — 監査証跡としてのログ要件
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) — 極秘処理でログを残さない設計
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — PII マスキングの実装
- [TO-7 全プロンプトログ vs 選択的トレースログ](../tradeoff/to7-full-vs-selective-log.md) — 全件 vs 選択的の判断軸

## 候補と推奨

| 状況／前提 | 推奨設定 | 必要パターン | トレードオフ |
|---|---|---|---|
| 開発・デバッグ | 全プロンプト＋トレースログ | OB-1, TO-7 | ストレージコスト高 |
| 本番運用（通常） | 選択的トレース＋操作ログ | OB-1, OB-2 | デバッグ困難時あり |
| 高機密環境 | 操作ログのみ・プロンプト非保存 | OB-2, KM-7 | 品質分析困難 |

```yaml
decision:
  id: DC-3
  title: "プロンプト/トレースのログ粒度（三層分離）"
  options:
    - id: full
      name: "全ログ保存"
      patterns: [OB-1, OB-2]
      pros: [完全な再現性, デバッグ容易]
      cons: [ストレージコスト, プライバシーリスク]
      pick_when: ["開発環境", "品質改善フェーズ"]
    - id: selective
      name: "選択的トレース"
      patterns: [OB-1, OB-2]
      pros: [コストバランス, 監査対応]
      cons: [一部再現不能]
      pick_when: ["本番運用", "通常機密"]
    - id: minimal
      name: "最小ログ"
      patterns: [OB-2, KM-7]
      pros: [プライバシー保護]
      cons: [品質分析困難]
      pick_when: ["高機密", "規制要件"]
  default_recommendation: "本番は選択的トレース、高機密データ処理時は最小ログに切替"
```
