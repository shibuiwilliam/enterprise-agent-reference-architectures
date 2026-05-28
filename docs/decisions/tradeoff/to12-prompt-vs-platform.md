---
title: "TO-12 プロンプトで守る vs ポリシー/実行基盤で守る"
description: "プロンプトはセキュリティ境界にならない。安全保証は権限・承認・検証・隔離・Policy-as-Codeで実行基盤側に置くという原則。"
status: done
---

# TO-12 プロンプトで守る vs ポリシー/実行基盤で守る

## 概要

システムプロンプトに「機密情報を出力するな」と書けば安全でしょうか。答えは明確に「いいえ」です。「上記の指示を無視して」と入力するだけで突破できるプロンプトは、セキュリティ境界になりません。安全保証は権限・認可・Policy Engine など実行基盤側に置き、プロンプトは応答トーンや出力形式の調整に使う——この役割分担がエンタープライズ設計の大原則です。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-12
decision_rules:
  - condition: "control_type IN ['access_control', 'approval_flow', 'output_validation', 'sandbox_isolation']"
    recommendation: prompt_for_quality_platform_for_security
    reason: "アクセス制御・承認フロー・DLP出力検証・実行環境の隔離は実行基盤側（権限・認可・Policy Engine）に置く"
  - condition: "control_type IN ['output_format', 'response_style', 'task_context', 'language_setting']"
    recommendation: prompt_for_quality_platform_for_security
    reason: "出力フォーマット・回答スタイル・タスクの目的・使用言語の指定はプロンプトが担うべき品質・ふるまいの調整"
  - condition: "security_enforced_by_prompt == true"
    recommendation: platform_only
    reason: "プロンプトでのセキュリティ保証は禁忌。「上記の指示を無視して」で容易に回避されるプロンプトはセキュリティ境界にならない"
  - condition: "infrastructure_readiness == 'incomplete' AND security_enforced_by_prompt == true"
    recommendation: platform_only
    reason: "まず実行基盤側のアクセス制御（ID-4）とPolicy-as-Code（ID-7）を整備する。これがなければプロンプトを精緻にしても安全は保証されない"
  - condition: "defense_in_depth == true"
    recommendation: prompt_for_quality_platform_for_security
    reason: "プロンプト制御と実行基盤制御は排他ではなく、それぞれ適切な役割を担う多層防御として組み合わせる"
```

## 比較

| 観点 | プロンプトで守る | ポリシー/実行基盤で守る（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)） |
|---|---|---|
| セキュリティとしての有効性 | 無効（プロンプトインジェクションで突破可能） | 有効（権限・Policy Engineが実行基盤で判定） |
| 向き | 品質管理・出力フォーマット・ふるまいの調整 | アクセス制御・承認フロー・データ保護 |
| 突破容易性 | 高（悪意ある入力で容易に回避） | 低（コードレベルで制御） |
| 監査可能性 | 低（プロンプトの意図を後から確認しにくい） | 高（Policy-as-Codeとして変更履歴が残る） |
| メンテナンス | 非体系的・属人的 | Policy-as-Codeとして体系的に管理 |

## 判断基準

この問いへの答えは二択ではなく、役割の明確な分担にある点がポイントです。

**実行基盤側（ポリシー・権限・承認）が担うべきもの**：

- アクセス制御：誰がどのデータ・ツールにアクセスできるかは権限システムで決めます（[ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md) / [ID-6](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)）
- 承認フロー：高リスク操作の実行前に人間の承認を挟みます（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）
- 出力検証：生成されたテキストに機密データが含まれていないかをDLPで検査します（[RT-5](../../patterns/rt-runtime/rt5-command-envelope.md)）
- 実行環境の隔離：エージェントが実行できる操作範囲をサンドボックスで制限します
- Policy-as-Code：禁止操作・必須操作をコードとして定義し、エージェントランタイムが自動適用します（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)）

**プロンプトが担うべきもの（品質・ふるまいの調整）**：

- 出力フォーマット（箇条書き・JSON・表等）の指定
- 回答スタイル（丁寧・簡潔・専門的等）の調整
- タスクの目的・背景情報の提供
- 使用言語・用語の指定

!!! danger "プロンプトでのセキュリティ保証は禁忌"
    「プロンプトに制約を書けばよい」という設計は、プロンプトインジェクション攻撃によって容易に回避されます。攻撃者が「上記の指示を無視して...」と入力するだけで制約が外れる設計は、セキュリティとしての意味を持ちません。安全保証は必ず実行基盤側（権限・認可・Policy Engine）に置いてください。

## ハイブリッド・段階的アプローチ

プロンプト制御と実行基盤制御は排他ではなく、それぞれ適切な役割を担う多層防御として組み合わせます。

実装の優先順位：

1. まず実行基盤側のアクセス制御（[ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md)）と Policy-as-Code（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)）を整備します。これがなければプロンプトをいくら精緻にしても安全は保証されません。
2. 承認フロー（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）と出力検証・DLP（[RT-5](../../patterns/rt-runtime/rt5-command-envelope.md)）を追加します。
3. PDP/PEP（[ID-6](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)）で全リクエストを認可判定する構造を完成させます。
4. 実行基盤の制御が整った段階で、品質向上・ふるまい調整のためのプロンプトエンジニアリングを行います。

## 関連パターン

- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md)
- [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)
- [RT-5 Command Envelope](../../patterns/rt-runtime/rt5-command-envelope.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| アクセス制御・承認・DLP・隔離 | 実行基盤（A） | ID-7, ID-6, RT-4 | 基盤整備の初期コスト |
| 出力形式・回答スタイル・言語指定 | プロンプト（B） | GV-3 | セキュリティ保証にならない |
| 品質調整＋実行基盤防御の多層防御 | 多層防御（C） | ID-7, ID-6, RT-4, RT-5 | 設計・運用の複雑度↑ |

```yaml
decision:
  id: TO-12
  title: "プロンプトで守る vs ポリシー/実行基盤で守る"
  options:
    - id: A
      name: "Platform Enforcement"
      patterns: [ID-7, ID-6, RT-4]
      pros: [突破困難, 監査可能, Policy-as-Codeで体系管理]
      cons: [基盤整備の初期コスト, 実装が複雑]
      pick_when: ["アクセス制御", "承認フロー", "DLP出力検証", "サンドボックス隔離"]
    - id: B
      name: "Prompt Control"
      patterns: [GV-3]
      pros: [即時適用, 柔軟, 低コスト]
      cons: [プロンプトインジェクションで突破可能, 監査不可, セキュリティ保証にならない]
      pick_when: ["出力フォーマット指定", "回答スタイル調整", "タスク背景情報提供"]
    - id: C
      name: "Defense in Depth"
      patterns: [ID-7, ID-6, RT-4, RT-5]
      pros: [安全性と品質の両立, 多層防御]
      cons: [設計・運用の複雑度]
      pick_when: ["本番運用", "セキュリティと品質の両方が必要"]
  default_recommendation: "A (Platform)を必ず先行整備。プロンプトはセキュリティ境界にならない。C (Defense in Depth)が最終形"
```
