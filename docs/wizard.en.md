---
title: "Pattern Selection Wizard"
description: "Answer 6–8 questions to identify the minimum set of patterns required for your scenario."
status: done
---

# Pattern Selection Wizard

Answer the following questions in order to identify the minimum set of patterns required for your scenario.

## Q1: Does the agent interact directly with external customers?

- **Yes** → [ID-1 Workforce/Customer Split](patterns/id-identity/id1-workforce-customer-split.md) is mandatory. Proceed to Q2.
- **No** → Proceed to Q2.

## Q2: How many SaaS systems does the agent connect to?

- **0 (internal systems only)** → Proceed to Q3.
- **1** → [IN-2 SaaS Adapter](patterns/in-integration/in2-saas-connector-adapter.md) recommended. Proceed to Q3.
- **2 or more** → [EX-1 Gateway](patterns/ex-experience/ex1-enterprise-agent-gateway.md) + [IN-1 Tool Gateway](patterns/in-integration/in1-tool-mcp-gateway.md) + [IN-2 SaaS Adapter](patterns/in-integration/in2-saas-connector-adapter.md) + [ID-2 OBO](patterns/id-identity/id2-identity-federation-obo.md) are mandatory. Proceed to Q3.

## Q3: Does the agent write to Systems of Record (SoR)?

- **No (read-only)** → [KM-1 Access-Controlled RAG](patterns/km-knowledge/km1-access-controlled-rag.md) recommended. Proceed to Q5.
- **Yes** → [RT-5 Command Envelope](patterns/rt-runtime/rt5-command-envelope.md) + [RT-6 SoR Write Boundary](patterns/rt-runtime/rt6-sor-write-boundary.md) are mandatory. Proceed to Q4.

## Q4: Are there multi-step workflows spanning multiple systems?

- **Yes** → Add [RT-7 Saga](patterns/rt-runtime/rt7-enterprise-saga.md) + [RT-8 Durable Workflow](patterns/rt-runtime/rt8-durable-workflow.md). Proceed to Q5.
- **No** → Proceed to Q5.

## Q5: What is the data sensitivity level?

- **Public information only** → Minimal identity patterns are sufficient. Proceed to Q6.
- **Internal/Confidential** → Add [ID-4 Permission Mirror](patterns/id-identity/id4-permission-mirror-least-of.md) + [KM-6 DLP](patterns/km-knowledge/km6-dlp-redaction-boundary.md). Proceed to Q6.
- **Top Secret (HR evaluations, M&A, etc.)** → Add the above plus [KM-7 Ephemeral Secure Bus](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md). Proceed to Q6.

## Q6: How is the agent triggered?

- **User request** → [ID-2 OBO](patterns/id-identity/id2-identity-federation-obo.md) (add if not already added in Q2). Proceed to Q7.
- **Event-driven (webhooks, etc.)** → Add [RT-10 Event-Driven Orchestrator](patterns/rt-runtime/rt10-event-driven-orchestrator.md) + [ID-3 Workload Identity](patterns/id-identity/id3-workload-agent-identity.md). Proceed to Q7.
- **Scheduled batch** → Add [ID-3 Workload Identity](patterns/id-identity/id3-workload-agent-identity.md). Proceed to Q7.

## Q7: Does the scenario include high-risk operations (financial, contract, HR)?

- **Yes** → Add [RT-3 Risk-Tiered Autonomy](patterns/rt-runtime/rt3-risk-tiered-autonomy.md) + [RT-4 Human Approval](patterns/rt-runtime/rt4-human-approval-chain.md) + [ID-7 Policy-as-Code](patterns/id-identity/id7-policy-as-code-guardrail.md).
- **No** → Skip.

## Always-Required Patterns

Regardless of your answers, the following are always mandatory in production:

- [GV-1 Control Plane](patterns/gv-governance/gv1-agent-control-plane.md) — Agent registry
- [OB-2 Unified Audit](patterns/ob-observability/ob2-unified-audit-lineage.md) — Audit trail
- [ID-6 Zero-Trust PDP/PEP](patterns/id-identity/id6-zero-trust-pdp-pep.md) — Zero-trust authorization

## For Coding Agents: YAML Decision Tree

The following YAML can be evaluated programmatically to automatically derive a pattern set from question answers.

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
