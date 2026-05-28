---
title: "TO-7 全プロンプトログ vs 選択的トレースログ"
description: "メタはTrace DB、本文は暗号化ストレージ、集計はDWHの三層分離で、コスト・機密・再現性を両立する設計指針。"
status: done
---

# TO-7 全プロンプトログ vs 選択的トレースログ

## 概要

障害が起きたとき「あのとき何を入力して何が返ってきたか」が再現できなければ、原因調査は行き詰まります。しかし全プロンプトを平文でログ基盤に流し込めば、顧客の個人情報や機密情報がログストレージに拡散し、それ自体がセキュリティインシデントの火種になりかねません。「全部記録したい」と「機密を拡散したくない」のあいだの実務的な落としどころとして、三層分離をどう設計するかを示します。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-7
decision_rules:
  - condition: "data_classification == 'top_secret' OR defense_in_depth == false"
    recommendation: metadata_only
    reason: "極秘処理は本文を一切ログに残さず、メタデータ（リクエストID・タイムスタンプ・処理完了フラグ）のみ保存する"
  - condition: "data_classification IN ['internal_general', 'department_confidential'] AND audit_required == true"
    recommendation: three_layer_separated
    reason: "標準構成は三層分離：メタはTrace DB、本文は暗号化ストレージ、集計はDWH"
  - condition: "confidential_data_in_result == true AND defense_in_depth == false"
    recommendation: three_layer_separated
    reason: "機密情報を含むプロンプトを平文で一般的なログ基盤に保存することは禁忌。本文保存は暗号化ストレージに限定する"
  - condition: "cost_constraint == true"
    recommendation: selective_with_encrypted_body
    reason: "全件保存が不要な場合はエラー時・高リスク操作時・ランダムN%のみフル保存するサンプリング方式を併用する"
  - condition: "regulatory_requirement IN ['gdpr', 'personal_information_protection']"
    recommendation: three_layer_separated
    reason: "規制対象データはGDPR・個人情報保護法等の要件に応じて保存期間と削除ルールを設定する"
```

## 比較

| ログ種別 | 保存先 | 含む情報 | 目的 |
|---|---|---|---|
| トレースメタ | Trace DB（[OB-1](../../patterns/ob-observability/ob1-observability-lake.md)） | リクエストID・モデル・レイテンシ・ツール呼び出し名・エラーコード | 監視・アラート・コスト追跡 |
| プロンプト本文 | 暗号化ストレージ（[DC-3](../degree/dc3-log-granularity.md)） | 実際のプロンプトとレスポンステキスト | 再現・デバッグ・監査 |
| 集計・分析 | DWH | 匿名化・集計後のトークン数・精度指標等 | 改善・レポーティング |

## 判断基準

三層分離（[DC-3](../degree/dc3-log-granularity.md) / [OB-1](../../patterns/ob-observability/ob1-observability-lake.md)）を標準構成とします。

ログ設計の判断軸：

- **再現性**：バグ調査や監査に必要な最小限の情報を本文ストレージに保存します。全件ではなく、エラー発生時・高リスク操作時・ランダムサンプリング分に絞るとコストを抑えられます。
- **機密性**：本文ストレージは暗号化し、アクセスを監査対応者・セキュリティチームに限定します。平文でのメタデータ DB への保存は禁止します。
- **コスト**：トークン数の多いプロンプト本文を全件保存するとストレージコストが急増します。保存対象の絞り込みルールは設計段階で決めておきます。

特殊ケースの扱い：

- **極秘処理（[KM-7](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)）**：本文は保存せず、メタ（リクエスト ID・タイムスタンプ・処理完了フラグ）のみ保存します。内容の再現より「実行した事実」の証明を優先します。
- **規制対象データ**：GDPR・個人情報保護法等の要件に応じて保存期間と削除ルールを設定します。再現性より法令遵守を優先します。

!!! warning "平文での全プロンプト保存は禁忌"
    機密情報を含むプロンプトを平文で一般的なログ基盤に保存することは、セキュリティインシデントの原因になります。本文保存は暗号化ストレージに限定し、アクセス権を最小化してください。

## ハイブリッド・段階的アプローチ

まずメタのみ保存する最小構成で運用を開始し、必要性が確認された範囲で本文保存を追加します。

1. トレースメタ（[OB-1](../../patterns/ob-observability/ob1-observability-lake.md)）のみで監視・アラートを構築します。
2. デバッグ・監査の需要が生じた時点で、暗号化ストレージへの本文保存を追加します。
3. 保存対象の選定ルール（エラー時・高リスク操作時・N% サンプリング）を整備します。
4. DWH 集計レイヤーを追加し、匿名化データで品質改善のループを回します。

## 関連パターン

- [OB-1 Enterprise Agent Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md)
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)
- [DC-3 ログ粒度](../degree/dc3-log-granularity.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 監視・アラート・コスト追跡のみ | メタデータのみ（A） | OB-1, DC-3 | 再現性・デバッグ不可 |
| デバッグ・監査・再現性が必要 | 三層分離（B） | OB-1, DC-3, KM-7 | ストレージコスト・運用複雑度↑ |
| 極秘処理・規制対象データ | メタ＋暗号化本文（C） | OB-1, KM-7, DC-3 | アクセス制限による調査遅延 |

```yaml
decision:
  id: TO-7
  title: "全プロンプトログ vs 選択的トレースログ"
  options:
    - id: A
      name: "Metadata Only"
      patterns: [OB-1, DC-3]
      pros: [低コスト, 機密拡散なし, 即時導入可]
      cons: [再現性なし, デバッグ困難]
      pick_when: ["初期導入", "極秘処理", "コスト制約が厳しい"]
    - id: B
      name: "Three-Layer Separated"
      patterns: [OB-1, DC-3, KM-7]
      pros: [再現性確保, 監査対応, 品質改善ループ]
      cons: [ストレージコスト, 暗号化運用の複雑度]
      pick_when: ["標準構成", "監査要件あり", "デバッグ需要"]
    - id: C
      name: "Selective Encrypted Body"
      patterns: [OB-1, KM-7, DC-3]
      pros: [コストと再現性のバランス, 規制対応]
      cons: [サンプリング漏れ, アクセス制限による調査遅延]
      pick_when: ["規制対象データ", "コスト最適化", "エラー時のみフル保存"]
  default_recommendation: "B (Three-Layer Separated)を標準構成とし、極秘処理はA、コスト制約時はCを併用"
```
