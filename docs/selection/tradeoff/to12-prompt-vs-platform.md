---
title: "TO-12 プロンプトで守る vs ポリシー/実行基盤で守る"
description: "プロンプトはセキュリティ境界にならない。安全保証は権限・承認・検証・隔離・Policy-as-Codeで実行基盤側に置くという原則。"
status: done
---

# TO-12 プロンプトで守る vs ポリシー/実行基盤で守る

## 概要

「プロンプトに『機密情報を出力するな』と書けば安全」という設計思想は、エンタープライズAIエージェントにおいて禁忌である。プロンプトは品質・ふるまいの調整手段であり、セキュリティ境界にはなり得ない。この問いに対する答えは明確である。

## 比較

| 観点 | プロンプトで守る | ポリシー/実行基盤で守る（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)） |
|---|---|---|
| セキュリティとしての有効性 | 無効（プロンプトインジェクションで突破可能） | 有効（権限・Policy Engineが実行基盤で判定） |
| 向き | 品質管理・出力フォーマット・ふるまいの調整 | アクセス制御・承認フロー・データ保護 |
| 突破容易性 | 高（悪意ある入力で容易に回避） | 低（コードレベルで制御） |
| 監査可能性 | 低（プロンプトの意図を後から確認しにくい） | 高（Policy-as-Codeとして変更履歴が残る） |
| メンテナンス | 非体系的・属人的 | Policy-as-Codeとして体系的に管理 |

## 判断基準

この問いに対する答えは二択ではなく、役割の明確な分担である。

**実行基盤側（ポリシー・権限・承認）が担うべきもの**：

- アクセス制御：誰がどのデータ・ツールにアクセスできるかは権限システムで決める（[ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md) / [ID-6](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)）
- 承認フロー：高リスク操作の実行前に人間の承認を挟む（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）
- 出力検証：生成されたテキストに機密データが含まれていないかをDLPで検査（[RT-5](../../patterns/rt-runtime/rt5-command-envelope.md)）
- 実行環境の隔離：エージェントが実行できる操作範囲をサンドボックスで制限
- Policy-as-Code：禁止操作・必須操作をコードとして定義し、エージェントランタイムが自動適用（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)）

**プロンプトが担うべきもの（品質・ふるまいの調整）**：

- 出力フォーマット（箇条書き・JSON・表等）の指定
- 回答スタイル（丁寧・簡潔・専門的等）の調整
- タスクの目的・背景情報の提供
- 使用言語・用語の指定

!!! danger "プロンプトでのセキュリティ保証は禁忌"
    「プロンプトに制約を書けばよい」という設計は、プロンプトインジェクション攻撃によって容易に回避される。攻撃者が「上記の指示を無視して...」と入力するだけで制約が外れる設計は、セキュリティとしての意味を持たない。安全保証は必ず実行基盤側（権限・認可・Policy Engine）に置く。

## ハイブリッド・段階的アプローチ

プロンプト制御と実行基盤制御は排他ではなく、それぞれ適切な役割を担う多層防御として組み合わせる。

実装の優先順位：

1. まず実行基盤側のアクセス制御（[ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md)）と Policy-as-Code（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)）を整備する。これがなければいくらプロンプトを精緻にしても安全は保証されない。
2. 承認フロー（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）と出力検証・DLP（[RT-5](../../patterns/rt-runtime/rt5-command-envelope.md)）を追加する。
3. PDP/PEP（[ID-6](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)）で全リクエストを認可判定する構造を完成させる。
4. 実行基盤の制御が整った後に、品質向上・ふるまい調整のためのプロンプトエンジニアリングを行う。

## 関連パターン

- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md)
- [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)
- [RT-5 Command Envelope](../../patterns/rt-runtime/rt5-command-envelope.md)
