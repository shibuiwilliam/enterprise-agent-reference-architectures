---
title: "TO-8 中央集権プラットフォーム vs 部署フェデレーション"
description: "認証・監査・モデル統制は中央集権、ドメイン知識・ユースケース・エージェント内容は部署にフェデレートする二層統治の設計指針。"
status: done
---

# TO-8 中央集権プラットフォーム vs 部署フェデレーション

## 概要

中央の AI CoE がすべてのエージェントを作ろうとすれば現場のニーズに追いつけず、各部署が勝手に「野良エージェント」を立ち上げる結果になります。逆に各部署に完全に任せれば、セキュリティ設定がバラバラで監査もできません。どちらの極端も失敗します。認証・監査・コストは中央が統制し、業務ロジックやドメイン知識は部署が持つ——この二層統治が唯一の実用的な解です。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-8
decision_rules:
  - condition: "governance_concern IN ['authentication', 'audit', 'model_control', 'cost']"
    recommendation: two_layer_governance
    reason: "認証・認可基盤、監査ログ、モデル認定、コスト追跡、Policy-as-Codeは中央が担う（GV/ID面）"
  - condition: "governance_concern IN ['domain_knowledge', 'use_case', 'agent_content']"
    recommendation: two_layer_governance
    reason: "業務ドメインの知識・ユースケース定義・プロンプトは部署にフェデレート（GV-3テンプレートによる権限委譲）"
  - condition: "responsibility_spans_multiple_departments == false AND deployment_phase == 'initial'"
    recommendation: two_layer_governance
    reason: "「中央が全部作る」モデルは部署ニーズへの対応速度が出ず、野良エージェントが乱立するアンチパターン"
  - condition: "responsibility_spans_multiple_departments == true AND infrastructure_readiness == 'incomplete'"
    recommendation: two_layer_governance
    reason: "「各部署が野放し」モデルはセキュリティポリシーのばらつきにより情報漏洩・コンプライアンス違反が生じるアンチパターン"
  - condition: "deployment_phase == 'initial'"
    recommendation: two_layer_governance
    reason: "中央基盤（GV-1 Agent Control Plane）とPolicy-as-Code（ID-7）を先行整備し、その後GV-3テンプレートで部署展開する順序が正しい"
```

## 比較

| 観点 | 中央集権 | 部署フェデレーション |
|---|---|---|
| 責任領域 | 認証・認可・監査・モデル統制・コスト・憲法・評価 | ドメイン知識・ユースケース・エージェントコンテンツ |
| 主なパターン | [GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md)・[ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md) | [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) テンプレート |
| 失敗パターン | 中央が全ユースケースを把握しきれない・リリースが遅い | セキュリティ設定が各部署でバラバラ・監査ができない |
| 意思決定速度 | 遅い | 速い |
| 安全性 | 高い（統一ポリシー） | 低い（部署ごとのばらつき） |

## 判断基準

機能の性質で中央か部署かを決めます。

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

この分担を崩すと必ず失敗します。「中央が全部作る」モデルでは部署ニーズへの対応速度が出ず、現場に無視されて野良エージェントが乱立します。「各部署が野放し」モデルではセキュリティポリシーのばらつきから情報漏洩・コンプライアンス違反が生じます。

## ハイブリッド・段階的アプローチ

中央基盤を先行して整備し、部署はテンプレートを使ってその上でエージェントを作るのが正しい順序です。

1. [GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md) で Agent Control Plane を整備し、中央の認証・監査・コスト管理を確立します。
2. [ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md) で Policy-as-Code を定義し、全エージェントに一律適用します。
3. [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) で部署向け Agent Factory テンプレートを提供し、セルフサービスでエージェントを作れる環境を整えます。
4. 部署が作ったエージェントも、中央の監査・評価パイプラインに自動で組み込まれるようにします。

## 関連パターン

- [GV-1 Agent Control Plane](../../patterns/gv-governance/gv1-agent-control-plane.md)
- [GV-3 Department Agent Factory](../../patterns/gv-governance/gv3-department-agent-factory.md)
- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 認証・監査・モデル統制・コスト管理 | 中央集権（A） | GV-1, ID-7, GV-8 | 部署ニーズへの対応速度↓ |
| ドメイン知識・ユースケース・プロンプト | 部署フェデレーション（B） | GV-3, GV-7 | セキュリティ設定のばらつき |
| 中央基盤＋部署テンプレートの二層統治 | 二層統治（C） | GV-1, GV-3, ID-7, GV-8 | 設計・調整の初期工数↑ |

```yaml
decision:
  id: TO-8
  title: "中央集権プラットフォーム vs 部署フェデレーション"
  options:
    - id: A
      name: "Central Platform"
      patterns: [GV-1, ID-7, GV-8]
      pros: [統一ポリシー, 監査一元化, セキュリティ高]
      cons: [部署ニーズへの対応遅延, 野良エージェント乱立リスク]
      pick_when: ["セキュリティ最優先", "小規模組織"]
    - id: B
      name: "Department Federation"
      patterns: [GV-3, GV-7]
      pros: [俊敏性, ドメイン適合, 部署自律]
      cons: [セキュリティばらつき, 監査困難]
      pick_when: ["ドメイン知識が部署に閉じる", "ユースケース定義"]
    - id: C
      name: "Two-Layer Governance"
      patterns: [GV-1, GV-3, ID-7, GV-8]
      pros: [安全性と俊敏性の両立, 野良エージェント防止]
      cons: [初期設計・調整工数]
      pick_when: ["中〜大規模組織", "複数部署がエージェント利用"]
  default_recommendation: "C (Two-Layer Governance)が唯一の実用的な解。中央基盤を先行整備し部署テンプレートで展開"
```
