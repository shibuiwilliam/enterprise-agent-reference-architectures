---
title: "TO-8 中央集権プラットフォーム vs 部署フェデレーション"
description: "認証・監査・モデル統制は中央集権、ドメイン知識・ユースケース・エージェント内容は部署にフェデレートする二層統治の設計指針。"
status: done
---

# TO-8 中央集権プラットフォーム vs 部署フェデレーション

## 概要

中央の AI CoE がすべてのエージェントを作ろうとすれば、現場のニーズに追いつけず、結局は各部署が勝手に「野良エージェント」を立ち上げる。逆に各部署に完全に任せれば、セキュリティ設定がバラバラで監査もできない。どちらの極端も失敗する。認証・監査・コストは中央が統制し、業務ロジックやドメイン知識は部署が持つ二層統治が唯一の実用的な解である。

## 比較

| 観点 | 中央集権 | 部署フェデレーション |
|---|---|---|
| 責任領域 | 認証・認可・監査・モデル統制・コスト・憲法・評価 | ドメイン知識・ユースケース・エージェントコンテンツ |
| 主なパターン | [GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md)・[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md) | [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) テンプレート |
| 失敗パターン | 中央が全ユースケースを把握しきれない・リリースが遅い | セキュリティ設定が各部署でバラバラ・監査ができない |
| 意思決定速度 | 遅い | 速い |
| 安全性 | 高い（統一ポリシー） | 低い（部署ごとのばらつき） |

## 判断基準

機能の性質で中央か部署かを決める。

**中央集権が担うもの（GV/ID 面）**：

- 認証・認可基盤（IdP連携・Token発行）
- 監査ログ・トレースの収集と保管
- 利用可能なモデルの認定と更新管理
- コスト追跡・クォータ割り当て（[GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)）
- 安全方針（Policy-as-Code）の制定と施行（[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)）
- エージェントの評価基準・品質ゲート（[GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）

**部署にフェデレートするもの（[GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) テンプレートによる権限委譲）**：

- 業務ドメインの知識・FAQ・ルール
- 部署固有のユースケース定義とプロンプト
- エージェントの外観・チャンネル設定
- 部署内の承認フロー（中央が定めた枠内で）

この分担を守らないと失敗する。「中央が全部作る」モデルは部署ニーズへの対応速度が出ず、現場に無視されて野良エージェントが乱立する。「各部署が野放し」モデルはセキュリティポリシーのばらつきから情報漏洩・コンプライアンス違反が生じる。

## ハイブリッド・段階的アプローチ

中央基盤を先行して整備し、部署はテンプレートを使ってその上でエージェントを作る順序が正しい。

1. [GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md) でAgent Control Planeを整備し、中央の認証・監査・コスト管理を確立する。
2. [ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md) でPolicy-as-Codeを定義し、全エージェントに一律適用する。
3. [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) で部署向けAgent Factoryテンプレートを提供し、セルフサービスでエージェントを作れる環境を整える。
4. 部署が作ったエージェントも中央の監査・評価パイプラインに自動で組み込まれるようにする。

## 関連パターン

- [GV-1 Agent Control Plane](../../patterns/gv-governance/gv1-agent-control-plane.md)
- [GV-3 Department Agent Factory](../../patterns/gv-governance/gv3-department-agent-factory.md)
- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md)
