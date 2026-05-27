---
title: "TO-4 Read-only vs. Write-capable (Gradual Expansion)"
description: "Design guidance for clearly separating read and write operations and gradually expanding permissions from Read-only to High-risk Controlled Write."
status: done
---

# TO-4 Read-only vs. Write-capable (Gradual Expansion)

## Overview

The damage from "retrieving a record" and "updating a record" are completely different when things go wrong. A retrieval mistake can be retried, but issuing an invoice with the wrong amount may be unrecoverable. The golden rule is to gradually expand write permissions: Read-only → Draft-only → Approved Write → Automatic Write.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-4
decision_rules:
  - condition: "operation_type == 'read' AND human_review_before_use == true"
    recommendation: read_only
    reason: "Information retrieval, reporting, and analysis are safe for autopilot; humans review output before acting on it"
  - condition: "operation_type == 'write' AND irreversible == false AND operation_frequency == 'high' AND eval_complete == true"
    recommendation: auto_write_low_risk
    reason: "Low-risk, high-frequency, reversible write operations can be automated once eval and canary validation are complete"
  - condition: "operation_type == 'write' AND irreversible == true AND approval_workflow_available == true"
    recommendation: approved_write
    reason: "Irreversible write operations require human approval; use SoR write boundary with approval chain"
  - condition: "system_of_record == 'erp_crm_hr' OR financial_impact == true"
    recommendation: high_risk_controlled_write
    reason: "Core business systems (ERP/CRM/HR) and financial operations require SoR + HitL; must not be fully automated"
  - condition: "deployment_phase == 'initial'"
    recommendation: read_only
    reason: "Start all operations in read-only mode; observe agent behavior via production traces before expanding write permissions"
```

## Comparison

| Stage | Description | Applicable Conditions |
|---|---|---|
| Read-only | Read/view only. No write access | Initial deployment, before risk assessment |
| Draft-only | Draft generation only. Human makes the final save | Document creation support, email drafts |
| Approved Write | Writes executed after human approval | Medium-risk operations, approval flow established |
| Low-risk Automatic Write | Only predefined low-risk operations executed automatically | Eval, canary, and audit in place |
| High-risk Controlled Write | High-risk operations executed via SoR + HitL | Full audit infrastructure and incident response capability in place |

## Decision Criteria

The principle is to clearly separate read and write operations.

- **Read operations (Read-only) = Autopilot**: Information search, report generation, and analysis can be executed autonomously. Incorrect results are confirmed by humans before use, so irreversible damage is unlikely.
- **Write operations (Write-capable) = SoR-mediated ([RT-6](../../patterns/rt-runtime/rt6-sor-write-boundary.md)) + HitL ([RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)) Copilot**: Data changes and writes to external systems must go through the System of Record to leave a change log, and include human confirmation.

Decision axes for gradual expansion:

- Is the operation irreversible? (Irreversible = maintain a more cautious stage)
- What is the scope of impact of the operation? (Broader = requires a higher stage)
- Has behavioral verification via eval and canary been completed?
- Is the audit trail sufficiently established?

## Hybrid and Gradual Approach

Do not apply the same stage to all business operations; assign stages per operation type.

1. Begin with all operations in Read-only mode and observe agent behavior with production traces.
2. Promote low-risk, high-frequency repetitive operations (standard form entry, etc.) from Draft-only to Approved Write.
3. Only promote to Automatic Write operations whose safety has been confirmed via eval ([GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)) and canary release.
4. Maintain the SoR + HitL combination for high-risk operations, excluding them from automation or leaving them at the final stage.

## Related Patterns

- [RT-6 SoR Write Boundary](../../patterns/rt-runtime/rt6-sor-write-boundary.md)
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md)
- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)
