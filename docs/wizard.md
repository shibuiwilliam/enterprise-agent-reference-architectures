---
title: "パターン選定ウィザード"
description: "6〜8問の質問に答えるだけで、あなたのシナリオに必要な最小パターンセットが分かる。"
status: done
---

# パターン選定ウィザード

以下の質問に順番に答えると、あなたのシナリオに必要なパターンの最小セットが明らかになる。

## Q1: エージェントは外部顧客と直接やり取りするか？

- **はい** → [ID-1 二面分離](patterns/id-identity/id1-workforce-customer-split.md) が必須。Q2へ進む。
- **いいえ** → Q2へ進む。

## Q2: 接続する SaaS の数は？

- **0（社内システムのみ）** → Q3へ進む。
- **1つ** → [IN-2 SaaS Adapter](patterns/in-integration/in2-saas-connector-adapter.md) を推奨。Q3へ進む。
- **2つ以上** → [EX-1 Gateway](patterns/ex-experience/ex1-enterprise-agent-gateway.md) + [IN-1 Tool Gateway](patterns/in-integration/in1-tool-mcp-gateway.md) + [IN-2 SaaS Adapter](patterns/in-integration/in2-saas-connector-adapter.md) + [ID-2 OBO](patterns/id-identity/id2-identity-federation-obo.md) が必須。Q3へ進む。

## Q3: SoR（基幹システム）への書き込みはあるか？

- **いいえ（参照のみ）** → [KM-1 権限認識RAG](patterns/km-knowledge/km1-access-controlled-rag.md) を推奨。Q5へ進む。
- **はい** → [RT-5 Command Envelope](patterns/rt-runtime/rt5-command-envelope.md) + [RT-6 SoR Write Boundary](patterns/rt-runtime/rt6-sor-write-boundary.md) が必須。Q4へ進む。

## Q4: 複数システムにまたがる多段処理があるか？

- **はい** → [RT-7 Saga](patterns/rt-runtime/rt7-enterprise-saga.md) + [RT-8 Durable Workflow](patterns/rt-runtime/rt8-durable-workflow.md) を追加。Q5へ進む。
- **いいえ** → Q5へ進む。

## Q5: データの機密レベルは？

- **公開情報のみ** → 最小限のアイデンティティパターンで十分。Q6へ進む。
- **社内一般〜機密** → [ID-4 Permission Mirror](patterns/id-identity/id4-permission-mirror-least-of.md) + [KM-6 DLP](patterns/km-knowledge/km6-dlp-redaction-boundary.md) を追加。Q6へ進む。
- **極秘（人事評価・M&A等）** → 上記に加え [KM-7 揮発セキュアバス](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) を追加。Q6へ進む。

## Q6: エージェントの起動方式は？

- **ユーザーが呼び出す** → [ID-2 OBO](patterns/id-identity/id2-identity-federation-obo.md)（Q2で未追加なら追加）。Q7へ進む。
- **イベント駆動（Webhook等）** → [RT-10 イベント駆動](patterns/rt-runtime/rt10-event-driven-orchestrator.md) + [ID-3 Workload Identity](patterns/id-identity/id3-workload-agent-identity.md) を追加。Q7へ進む。
- **定時バッチ** → [ID-3 Workload Identity](patterns/id-identity/id3-workload-agent-identity.md) を追加。Q7へ進む。

## Q7: 高リスク操作（金銭・契約・人事）を含むか？

- **はい** → [RT-3 Risk-Tiered Autonomy](patterns/rt-runtime/rt3-risk-tiered-autonomy.md) + [RT-4 Human Approval](patterns/rt-runtime/rt4-human-approval-chain.md) + [ID-7 Policy-as-Code](patterns/id-identity/id7-policy-as-code-guardrail.md) を追加。
- **いいえ** → スキップ。

## 常に必須のパターン

どの回答であっても、以下は本番環境で常に必須となる:

- [GV-1 Control Plane](patterns/gv-governance/gv1-agent-control-plane.md) — エージェント登録
- [OB-2 Unified Audit](patterns/ob-observability/ob2-unified-audit-lineage.md) — 監査証跡
- [ID-6 Zero-Trust PDP/PEP](patterns/id-identity/id6-zero-trust-pdp-pep.md) — ゼロトラスト認可

## コーディングエージェント向け：YAML 判定木

以下の YAML をプログラム的に評価することで、質問への回答からパターンセットを自動導出できる。

```yaml
wizard:
  always_required:
    patterns: [GV-1, OB-2, ID-6]
    reason: "Agent registry, audit trail, and zero-trust authorization are mandatory for production."
    reason_ja: "エージェントレジストリ・監査証跡・ゼロトラスト認可は本番環境で常に必須。"

  questions:
    - id: q1_customer_facing
      question: "Does the agent interact with external customers?"
      question_ja: "エージェントは外部顧客と直接やり取りするか？"
      type: boolean
      if_true: { add_patterns: [ID-1] }
      if_false: { add_patterns: [] }

    - id: q2_saas_count
      question: "How many SaaS systems does the agent connect to?"
      question_ja: "接続するSaaSの数は？"
      type: enum
      values:
        - value: "0"
          label: "None (internal only)"
          label_ja: "なし（社内のみ）"
          add_patterns: []
        - value: "1"
          label: "One"
          label_ja: "1つ"
          add_patterns: [IN-2]
        - value: "2+"
          label: "Two or more"
          label_ja: "2つ以上"
          add_patterns: [EX-1, IN-1, IN-2, ID-2]

    - id: q3_write_operations
      question: "Does the agent write to System of Record?"
      question_ja: "SoRへの書き込みはあるか？"
      type: boolean
      if_true: { add_patterns: [RT-5, RT-6] }
      if_false: { add_patterns: [KM-1] }

    - id: q4_multi_step
      question: "Multi-step workflows spanning multiple systems?"
      question_ja: "複数システムにまたがる多段処理があるか？"
      type: boolean
      depends_on: { q3_write_operations: true }
      if_true: { add_patterns: [RT-7, RT-8] }
      if_false: { add_patterns: [] }

    - id: q5_data_sensitivity
      question: "Data sensitivity level?"
      question_ja: "データの機密レベルは？"
      type: enum
      values:
        - value: public
          label: "Public only"
          label_ja: "公開情報のみ"
          add_patterns: []
        - value: confidential
          label: "Internal/Confidential"
          label_ja: "社内一般〜機密"
          add_patterns: [ID-4, KM-6]
        - value: top_secret
          label: "Top Secret (HR eval, M&A)"
          label_ja: "極秘（人事評価・M&A等）"
          add_patterns: [ID-4, KM-6, KM-7]

    - id: q6_trigger_type
      question: "How is the agent triggered?"
      question_ja: "エージェントの起動方式は？"
      type: enum
      values:
        - value: user_request
          label: "User request"
          label_ja: "ユーザーが呼び出す"
          add_patterns: [ID-2]
        - value: event_driven
          label: "Event-driven (webhooks)"
          label_ja: "イベント駆動"
          add_patterns: [RT-10, ID-3]
        - value: scheduled_batch
          label: "Scheduled batch"
          label_ja: "定時バッチ"
          add_patterns: [ID-3]

    - id: q7_high_risk
      question: "Includes high-risk operations (financial, contract, HR)?"
      question_ja: "高リスク操作（金銭・契約・人事）を含むか？"
      type: boolean
      if_true: { add_patterns: [RT-3, RT-4, ID-7] }
      if_false: { add_patterns: [] }
```
