---
title: "DC-3 Prompt/Trace Log Granularity (Three-Layer Separation)"
description: "A continuous parameter for separating metadata, body, and aggregate into three layers and deciding log granularity and storage destinations."
status: done
---

# DC-3 Prompt/Trace Log Granularity (Three-Layer Separation)

## Overview

Without being able to trace what an agent thought and what it output, incident investigation and quality improvement are impossible. But storing all prompts and responses in plain text spreads PII and confidential information across the logging infrastructure and causes storage costs to skyrocket. This covers how to design the granularity of "what to record and to what extent" using three-layer separation ([OB-1](../../patterns/ob-observability/ob1-observability-lake.md)): metadata, body, and aggregate.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-3
parameter: log_granularity
rules:
  - condition: "data_classification == 'top_secret'"
    log_layer: metadata_only
    storage: trace_db
    body_retention: none
    reason: "Top-secret or ephemeral: store only request ID, timestamp, and completion flag; never persist prompt body"
  - condition: "data_classification IN ['internal_general', 'department_confidential'] AND audit_required == true"
    log_layer: three_layer_separated
    storage_metadata: trace_db
    storage_body: encrypted_object_storage
    storage_aggregate: dwh
    pii_masking: required_before_body_storage
    reason: "Standard: metadata to Trace DB, PII-masked body to encrypted object storage, anonymized metrics to DWH"
  - condition: "cost_constraint == true"
    sampling_strategy: "error_events + high_risk_operations + random_N_percent"
    recommended_n_percent: 5
    reason: "Sample-based full body storage (errors + high-risk + N%) controls storage cost while preserving debugging capability"
  - condition: "regulatory_requirement != 'none'"
    retention_policy: per_data_classification_per_regulation
    deletion_rule: required
    reason: "Regulated data: define per-classification retention and deletion rules; compliance takes precedence over reproducibility"
  - condition: "confidential_data_in_result == true AND defense_in_depth == false"
    log_layer: three_layer_separated
    action: remediate_immediately
    reason: "Anti-pattern: plaintext prompt storage in general log infrastructure must be remediated; it is a security incident source"
```

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (not recording enough) | Metadata only, no body | Incidents cannot be reproduced or root-cause investigated. Quality improvement feedback loop cannot run |
| Too much (recording too much) | All prompts and responses stored in plain text, all records | Storage costs explode; PII and confidential information spreads across log infrastructure |

## Decision Criteria

Separate into three layers and decide storage destination and granularity for each.

| Layer | Content | Storage Destination |
|---|---|---|
| Metadata | Model name, version, token count, latency, cost, correlation ID, tools used, success/failure, risk_tier | Trace DB |
| Body | Prompts, retrieved context, outputs (with PII masking applied) | Encrypted object storage |
| Aggregate | Quality scores, aggregated metrics | DWH |

- For top-secret processing ([KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)), leave no body in logs at all — metadata only
- When full retention is not required, combine with sampling (only errors, only low-score sessions, or random N%) for full storage

## Adjustment Mechanism

- Dynamically adjust sampling rate based on [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) measurement results (error rate, quality score distribution)
- Subordinate storage costs and retention periods to the budget in [GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)
- Define retention policies per data classification, balancing regulatory requirements (audit log retention obligations) and confidentiality requirements (PII minimization)

## Related Patterns

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) — the core three-layer separation design
- [OB-2 Unified Audit & Lineage](../../patterns/ob-observability/ob2-unified-audit-lineage.md) — log requirements as audit trails
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) — design for top-secret processing that leaves no logs
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — PII masking implementation
- [TO-7 Full Prompt Log vs. Selective Trace Log](../tradeoff/to7-full-vs-selective-log.md) — decision axis between full vs. selective
