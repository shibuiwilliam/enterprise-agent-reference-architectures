---
title: "TO-1 OBO Delegation vs. Service Account"
description: "Decision criteria for choosing between User OBO, Service Account, Agent Identity, and Hybrid, based on three axes: permission fidelity, audit attribution, and implementation cost."
status: done
---

# TO-1 OBO Delegation vs. Service Account

## Overview

When an agent reads a Salesforce record, whether it reads as "Tanaka himself" or "as the system administrator account" completely changes both what data is visible and the meaning of the audit log. There are four methods — User OBO (delegation under the requester's own permissions), service account (shared technical account), Agent Identity (agent-specific ID), and a Hybrid combining these — and which to choose is determined by "whose authority it operates under and who is accountable."

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-1
decision_rules:
  - condition: "purpose == 'personal_assistance' AND saas_supports_token_exchange"
    recommendation: obo
    reason: "User-specific permissions are critical; SaaS native audit attribution is preserved via RFC 8693 token exchange"
  - condition: "purpose == 'department_representative' AND multiple_approvers == true"
    recommendation: agent_identity
    reason: "Multiple persons involved; attach department scope policy to agent identity for bounded authorization"
  - condition: "purpose == 'company_wide_batch' OR purpose == 'scheduled_job'"
    recommendation: service_account
    reason: "Batch/scheduled processing; compensate with strict audit and high-risk data classification controls"
  - condition: "operation_risk == 'high' AND irreversible == true"
    recommendation: hybrid
    reason: "High-risk irreversible operations require User OBO combined with human approval chain; agent executes under user permission ceiling"
  - condition: "existing_service_account == true AND migration_phase == 'early'"
    recommendation: service_account
    reason: "Incremental migration: first attach Workload Identity (SPIFFE/SVID) to existing SA, then switch to User OBO only for high-risk operations"
```

## Comparison

| Perspective | User OBO ([ID-2](../../patterns/id-identity/id2-identity-federation-obo.md)) | Service Account | Agent Identity ([ID-3](../../patterns/id-identity/id3-workload-agent-identity.md)) | Hybrid |
|---|---|---|---|---|
| Permission Fidelity | High (reduced to delegator's permission ceiling) | Low (judgment bug = permission leak) | Medium (controlled by agent-specific policy) | High (User as ceiling, Agent executes) |
| Coverage | OBO-compatible SaaS only | Any API | Autonomous jobs, batch | Wide |
| Audit Attribution | Clear to the individual | Tends to be ambiguous | Clear to Agent ID | Clear (records both User and Agent) |
| Implementation | Complex (Token Exchange / RFC 8693 required) | Simple | Medium | Complex |

## Decision Criteria

Recommended patterns differ by business type:

- **Personal work assistance**: Choose User OBO. The assigned person operates SaaS under their own permissions, guaranteeing faithful permission propagation and clear attribution.
- **Department representative tasks**: Choose Agent Identity + department policy. Even for tasks involving multiple people, attach a department scope to the Agent ID to control permissions.
- **Company-wide batch / regular processing**: Combine Service Account + strict audit + high-risk data classification. Service Accounts tend toward broad permissions, so separately strengthen operational scope and audit trails.
- **High-risk operations**: Combine User OBO + Human Approval Chain ([RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)). For irreversible operations and large transactions, execute only after the delegating party's confirmation.

The most practical architecture is the **Hybrid where "Agent is the executor and User is the permission ceiling."** The agent performs work on behalf of the user while the execution platform guarantees the constraint that the User's permission ceiling cannot be exceeded.

## Hybrid and Gradual Approach

A realistic migration path is to use existing tools running on Service Accounts as-is, and introduce User OBO only for high-risk operations. Since Hybrid adds implementation complexity, build it incrementally in the following order:

1. Assign SPIFFE/SVID-style Workload Identity ([ID-3](../../patterns/id-identity/id3-workload-agent-identity.md)) to existing Service Accounts to clarify audit attribution.
2. Switch only high-risk operations to User OBO via Token Exchange (RFC 8693).
3. Progress toward applying User OBO to all operations and retiring Service Accounts.

Relying solely on Service Accounts directly leads to the anti-pattern of "one omnipotent service account calling all SaaS." Once operations have settled, always aim for scope division or retirement.

## Related Patterns

- [ID-2 Identity Federation & On-Behalf-Of](../../patterns/id-identity/id2-identity-federation-obo.md)
- [ID-3 Workload / Agent Identity](../../patterns/id-identity/id3-workload-agent-identity.md)
- [ID-4 Permission Mirror / Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md)
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md)
