---
title: "DC-1 Autonomy Tier Boundary (How to Draw Risk-Tier Lines)"
description: "A continuous parameter for determining the boundary between autonomous agent execution and human approval, based on irreversibility of impact, amount, sensitivity, and job responsibility."
status: done
---

# DC-1 Autonomy Tier Boundary (How to Draw Risk-Tier Lines)

## Overview

Treating "searching internal FAQs" and "approving a ¥1 million purchase order" with the same level of autonomy is unacceptable. The boundary between what the agent does automatically and where human approval is required — how that line is drawn affects both business value and risk. This covers how to practically divide the Tier 0–5 framework from [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md).

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-1
parameter: autonomy_tier_boundary
rules:
  - condition: "operation_type == 'read' AND data_classification <= 'internal_general'"
    tier: 0
    autonomy: auto_execute
    reason: "Read-only operations on non-confidential data carry negligible risk; full automation is appropriate"
  - condition: "irreversibility == 'reversible' AND impact_scope IN ['personal', 'team'] AND data_classification <= 'department_confidential'"
    tier: 1
    autonomy: auto_execute_with_audit
    reason: "Reversible, low-scope operations on non-secret data can be auto-executed; maintain audit trail for quality review"
  - condition: "irreversibility == 'partially_reversible' OR impact_scope IN ['department', 'company_wide'] OR data_classification == 'department_confidential'"
    tier: 2
    autonomy: require_approval
    reason: "Partially reversible operations or broader impact scope require human approval; risk of cascading errors justifies oversight"
  - condition: "irreversibility == 'irreversible' AND impact_type IN ['financial', 'contractual', 'external_publish', 'permission_escalation']"
    tier: 3
    autonomy: require_approval_with_dual_sign
    reason: "Irreversible operations with financial, contractual, or external impact require multi-approver sign-off and human-in-the-loop"
  - condition: "deployment_phase == 'initial' OR eval_complete == false"
    tier: 2
    autonomy: require_approval
    reason: "Initial deployment: set broadly conservative (require-approval) and expand automation range incrementally as GV-7 eval confirms safety"
```

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (too strict) | Every operation requires approval | Approvers become bottlenecks, eliminating the value of agent adoption. Approval fatigue also causes the process to become a formality |
| Too much (too permissive) | Most operations are automatically executed | Risk of irreversible incorrect execution (money transfers, contract changes, permission escalation, external publication) becomes real |

## Decision Criteria

Tier boundaries are determined by combining four axes:

- **Irreversibility of impact**: Reversible operations (draft creation, read access) lean toward automatic; irreversible operations (wire transfers, contract signing, external transmission) lean toward approval
- **Impact amount / scope**: Stage by whether impact is confined to an individual or extends to a team, department, company, or externally
- **Data sensitivity**: Escalate strictness according to classification: public → general internal → department confidential → top secret
- **Requester's job responsibility**: Make the autonomy range variable based on the requester's job title and permission level. The threshold may differ between management and non-management for the same operation

Read operations (retrieval) default to automatic; write operations (money, contracts, HR, permission changes, external publication) lean toward approval.

!!! tip "Principle for Initial Deployment"
    During initial deployment, set a broad approval-required range, and gradually expand the automatic range while confirming safety with the [GV-7 Evaluation Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md). Starting with loose settings from the beginning is irreversible.

## Adjustment Mechanism

- Measure approval rates, success rates of automated execution, and incident rates using [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md)
- Regularly verify the quality of automatically executed operations with the [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)
- Tiers with persistently high approval rates are automation candidates; tiers with incidents should have their approval scope expanded
- Subject changes to tier boundaries to change management ([GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md)) and retain audit trails

## Related Patterns

- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md) — the core tier definition
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md) — approval flow design when leaning toward approval
- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) — the means to implement tier boundaries in policy code
- [DC-6 Guardrail Strength](dc6-guardrail-strength.md) — complementary relationship with guardrail threshold tuning
