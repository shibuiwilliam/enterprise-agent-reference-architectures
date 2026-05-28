---
title: "DC-6 ガードレール強度（誤検知 vs 見逃し）"
description: "ガードレールの閾値を誤検知率と見逃し率のバランスで調整する連続量パラメータ。"
status: done
---

# DC-6 ガードレール強度（誤検知 vs 見逃し）

## 概要

ガードレールを厳しくしすぎると、正当なメール送信まで「機密漏洩の疑い」でブロックされ、ユーザーはエージェントを使わなくなります。緩めすぎれば、本当に危険な出力を素通りさせてしまいます。このバランスを一律に決めることはできません。「社外向けメール送信」と「社内メモの要約」ではリスクがまるで異なるからです。[ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) の閾値を、経路のリスク特性ごとに調整する方法を示します。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-6
parameter: guardrail_strength
rules:
  - condition: "route_risk_level == 'low_risk' AND operation_type IN ['read', 'simple_qa']"
    threshold: lenient
    approach: lightweight_guardrail
    reason: "低リスク経路（参照のみ・社内下書き・既承認テンプレート）は軽量なガードレールで十分。FP（誤検知）による業務阻害を最小化する"
  - condition: "route_risk_level IN ['high_risk', 'critical'] AND operation_type IN ['send', 'publish', 'approve']"
    threshold: strict
    approach: minimize_fn
    reason: "高リスク経路（外部送信・機密データアクセス・副作用を伴う操作・顧客向け出力）は厳格な閾値を設定し、FN（見逃し）をゼロに近づける"
  - condition: "latency_critical == true"
    approach: async_or_sampling_inspection
    reason: "レイテンシがクリティカルな経路での検査は、同期ブロッキングではなく非同期・サンプリング方式を選択して影響を緩和する"
  - condition: "route_risk_level == 'low_risk' AND route_risk_level == 'critical'"
    action: differentiate_by_route
    reason: "全経路に同一の閾値を適用するのは過小・過大どちらかに必ず偏るアンチパターン。経路ごとにリスクを評価し閾値を個別に設定する"
  - condition: "eval_complete == true AND route_risk_level != 'low_risk'"
    action: rebalance_threshold_using_gv7
    reason: "FP率・FN率・インシデント件数をGV-7で定期計測し、ビジネス上どちらの害が大きいかを判断基準に閾値を調整する"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（緩すぎ） | 閾値が低く、危険な操作を多く通過させる | 機密情報漏洩・不正操作・外部公開など深刻なインシデントが発生します |
| 過大（厳しすぎ） | 閾値が高く、大半の操作を誤検知でブロック | 正当なタスクが連続して遮断され、業務が止まります。承認疲れと「ガードレール無効化」の誘因にもなります |

## 判断基準

経路のリスク特性に応じて閾値を分けることが基本方針です。

- **高リスク経路**（外部送信・機密データアクセス・副作用を伴う操作・顧客向け出力）は厳格な閾値を設定し、FN（見逃し）をゼロに近づけます。
- **低リスク経路**（参照のみ・社内下書き・既承認テンプレート）は軽量なガードレールで十分です。FP（誤検知）による業務阻害を最小化します。
- 閾値の設定根拠は「ビジネス許容点」に置きます。FP 率と FN 率をそれぞれ計測し、業務上どちらの害が大きいかで判断します。
- レイテンシがクリティカルな経路では、同期ブロッキングではなく非同期・サンプリング方式を選ぶことで影響を緩和できます。

[ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md) による認可決定と組み合わせると、ガードレールが拒否した操作の理由を監査証跡に残しやすくなります。

!!! warning "閾値の一律設定は避ける"
    全経路に同一の閾値を適用するのは過小・過大どちらかに必ず偏ります。経路ごとにリスクを評価し、閾値を個別に設定してください。

## 調整の仕組み

- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) で FP 率・FN 率・インシデント件数を定期計測し、閾値調整の根拠とします。
- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でガードレール発動件数・種別・経路を記録し、誤検知が多い経路を特定します。
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) の出力フィルタリングと連動させ、コンテンツ検査の粒度を揃えます。
- 閾値変更も変更管理の対象とし、変更前後の FP/FN 推移を比較して効果を確認します。

## 関連パターン

- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) — ガードレール実装の本体
- [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md) — 認可決定との連携
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — FP/FN 率の計測と調整
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — 出力フィルタリングとの整合

## 候補と推奨

| 状況／前提 | 推奨設定 | 必要パターン | トレードオフ |
|---|---|---|---|
| 社内参照・下書き作成 | 軽量ガードレール（FP最小化） | ID-7 | 見逃しリスク残存 |
| 外部送信・顧客向け出力 | 厳格ガードレール（FN最小化） | ID-7, ID-6, KM-6 | 誤検知による業務遅延 |
| レイテンシ重視の経路 | 非同期・サンプリング検査 | ID-7, OB-1 | リアルタイム防御の欠落 |

```yaml
decision:
  id: DC-6
  title: "ガードレール強度（誤検知 vs 見逃し）"
  options:
    - id: lenient
      name: "軽量ガードレール"
      patterns: [ID-7]
      pros: [業務阻害最小, 低レイテンシ]
      cons: [危険な出力の見逃しリスク]
      pick_when: ["低リスク経路", "社内参照のみ"]
    - id: strict
      name: "厳格ガードレール"
      patterns: [ID-7, ID-6, KM-6]
      pros: [見逃しゼロに近い安全性]
      cons: [誤検知による業務遅延, 承認疲れ]
      pick_when: ["外部送信", "機密データアクセス", "顧客向け出力"]
    - id: async_sampling
      name: "非同期・サンプリング検査"
      patterns: [ID-7, OB-1]
      pros: [レイテンシ影響なし]
      cons: [リアルタイム防御不可]
      pick_when: ["レイテンシクリティカル", "大量処理"]
  default_recommendation: "高リスク経路は厳格、低リスク経路は軽量とし、経路ごとに閾値を個別設定"
```
