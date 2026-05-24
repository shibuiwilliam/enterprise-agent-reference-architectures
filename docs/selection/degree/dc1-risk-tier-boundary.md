---
title: "DC-1 自律度のティア境界（Risk-Tier の引き方）"
description: "影響の不可逆性・額・機密度・職責を軸に、エージェントの自律実行と人間承認の境界を決める連続量パラメータ。"
status: done
---

# DC-1 自律度のティア境界（Risk-Tier の引き方）

## 概要

エージェントが自律的に実行できる範囲と、人間の承認を求める範囲の境界線をどこに引くかを決める連続量パラメータである。[RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md) で定義するティア（Tier 0–5）の境界の引き方を扱う。

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（厳しすぎ） | すべての操作に承認を要求 | 承認者がボトルネック化し、エージェント導入の価値が消える。承認疲れにより形骸化も起こる |
| 過大（緩すぎ） | 大半の操作を自動実行 | 不可逆な誤実行（金銭移動・契約変更・権限昇格・外部公開）のリスクが現実化する |

## 判断基準

ティア境界は以下の4軸の掛け合わせで決定する。

- **影響の不可逆性**：取り消し可能な操作（ドラフト作成・参照）は自動寄り、取り消し不能な操作（送金・契約締結・外部送信）は承認寄り
- **影響額／影響範囲**：影響が個人に閉じるか、チーム・部門・全社・社外に及ぶかで段階を分ける
- **データ機密度**：公開情報 → 社内一般 → 部門機密 → 極秘の分類に応じて厳格度を上げる
- **本人の職責**：依頼者の役職・権限レベルに応じて自律範囲を可変にする。同じ操作でも管理職と一般職で閾値が異なりうる

参照系（読み取り）は原則自動、更新系（金銭・契約・人事・権限変更・外部公開）は承認寄りに倒す。

!!! tip "導入初期の原則"
    導入初期は広めに要承認に設定し、[GV-7 評価パイプライン](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)で安全性を確認しながら自動範囲を段階的に拡大する。最初から緩い設定で始めるのは取り返しがつかない。

## 調整の仕組み

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) で承認率・自動実行の成功率・インシデント発生率を計測する
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) の定期 eval で、自動実行された操作の品質を検証する
- 承認率が高止まりしている Tier は自動化候補、インシデントが発生した Tier は承認範囲を拡大する
- Tier 境界の変更自体を変更管理（[GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md)）の対象にし、監査証跡を残す

## 関連パターン

- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md) — ティア定義の本体
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md) — 承認寄りに倒した場合の承認フロー設計
- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) — ティア境界をポリシーコードで実装する手段
- [DC-6 ガードレール強度](dc6-guardrail-strength.md) — ガードレールの閾値調整と補完関係にある
