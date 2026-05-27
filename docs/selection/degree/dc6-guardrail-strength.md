---
title: "DC-6 ガードレール強度（誤検知 vs 見逃し）"
description: "ガードレールの閾値を誤検知率と見逃し率のバランスで調整する連続量パラメータ。"
status: done
---

# DC-6 ガードレール強度（誤検知 vs 見逃し）

## 概要

ガードレールを厳しくしすぎると、正当なメール送信まで「機密漏洩の疑い」で毎回ブロックされ、ユーザーはエージェントを使わなくなる。緩めすぎれば本当に危険な出力を素通りさせてしまう。このバランスは一律に決められるものではない。「社外向けメール送信」と「社内メモの要約」では当然リスクが異なるからだ。[ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) の閾値を経路のリスク特性ごとに調整する方法を扱う。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-6
parameter: guardrail_strength
rules:
  - condition: "route_risk_level == 'low_risk' AND operation IN ['internal_draft', 'read_only', 'pre_approved_template']"
    threshold: lenient
    approach: lightweight_guardrail
    reason: "低リスク経路（参照のみ・社内下書き・既承認テンプレート）は軽量なガードレールで十分。FP（誤検知）による業務阻害を最小化する"
  - condition: "route_risk_level IN ['high_risk', 'critical'] AND operation IN ['external_send', 'confidential_access', 'side_effect']"
    threshold: strict
    approach: minimize_fn
    reason: "高リスク経路（外部送信・機密データアクセス・副作用を伴う操作・顧客向け出力）は厳格な閾値を設定し、FN（見逃し）をゼロに近づける"
  - condition: "latency_critical == true AND synchronous_blocking_inspection == true"
    approach: async_or_sampling_inspection
    reason: "レイテンシがクリティカルな経路での検査は、同期ブロッキングではなく非同期・サンプリング方式を選択して影響を緩和する"
  - condition: "uniform_threshold_all_routes == true"
    action: differentiate_by_route
    reason: "全経路に同一の閾値を適用するのは過小・過大どちらかに必ず偏るアンチパターン。経路ごとにリスクを評価し閾値を個別に設定する"
  - condition: "fp_rate_high OR fn_rate_high"
    action: rebalance_threshold_using_gv7
    reason: "FP率・FN率・インシデント件数をGV-7で定期計測し、ビジネス上どちらの害が大きいかを判断基準に閾値を調整する"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（緩すぎ） | 閾値が低く、危険な操作を多く通過させる | 機密情報漏洩・不正操作・外部公開など深刻なインシデントが発生する |
| 過大（厳しすぎ） | 閾値が高く、大半の操作を誤検知でブロック | 正当なタスクが連続して遮断され、業務が止まる。承認疲れと「ガードレール無効化」の誘因にもなる |

## 判断基準

経路のリスク特性に応じて閾値を分けることが基本方針だ。

- **高リスク経路**（外部送信・機密データアクセス・副作用を伴う操作・顧客向け出力）は厳格な閾値を設定し、FN（見逃し）をゼロに近づける
- **低リスク経路**（参照のみ・社内下書き・既承認テンプレート）は軽量なガードレールで十分とし、FP（誤検知）による業務阻害を最小化する
- 閾値の設定根拠は「ビジネス許容点」に置く。FP 率と FN 率をそれぞれ計測し、業務上どちらの害が大きいかを判断基準にする
- レイテンシがクリティカルな経路では、同期ブロッキングではなく非同期・サンプリング方式を選択することで影響を緩和できる

[ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md) による認可決定と組み合わせると、ガードレールが拒否した操作の理由を監査証跡に残しやすくなる。

!!! warning "閾値の一律設定は避ける"
    全経路に同一の閾値を適用するのは過小・過大どちらかに必ず偏る。経路ごとにリスクを評価し、閾値を個別に設定する。

## 調整の仕組み

- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) で FP 率・FN 率・インシデント件数を定期計測し、閾値調整の判断材料とする
- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でガードレール発動件数・種別・経路を記録し、誤検知が多い経路を特定する
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) の出力フィルタリングと連動させ、コンテンツ検査の粒度を揃える
- 閾値変更自体を変更管理の対象とし、変更前後の FP/FN 推移を比較する

## 関連パターン

- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) — ガードレール実装の本体
- [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md) — 認可決定との連携
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — FP/FN 率の計測と調整
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — 出力フィルタリングとの整合
