---
title: "DC-8 Model Strength and Data-Classification-Based Routing"
description: "A continuous parameter for designing model selection and routing paths based on task difficulty and data sensitivity."
status: done
---

# DC-8 Model Strength and Data-Classification-Based Routing

## Overview

Using the largest model for "tell me how to book a meeting room" wastes cost, but assigning complex contract review to a lightweight model produces insufficient quality. Furthermore, sending prompts containing customer PII to an external API may violate regulations. This covers how to design two-axis routing in [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md): switching model size by task difficulty, and separating inference paths (within VPC vs. external API) by data sensitivity.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-8
parameter: model_routing
rules:
  - condition: "task_difficulty == 'simple' AND data_classification IN ['public', 'internal_general']"
    model_size: lightweight
    routing_path: external_api_or_internal
    reason: "Simple tasks with non-sensitive data can use lightweight models via any path; minimize cost and latency"
  - condition: "confidence_score_below_threshold == true"
    model_size: escalate_to_stronger
    routing_path: same_as_original
    reason: "Cascade escalation: when lightweight model confidence falls below threshold or verifier rejects, escalate to stronger model"
  - condition: "data_classification == 'top_secret'"
    routing_path: vpc_or_onprem_only
    external_api_allowed: false
    reason: "Top-secret data must route exclusively to VPC-internal or on-premise inference; external API send is prohibited"
  - condition: "data_classification IN ['public', 'internal_general'] AND latest_model_required == true AND dpa_confirmed == true"
    routing_path: external_api_permitted
    prerequisite: dpa_confirmed
    reason: "Non-sensitive data may use external API paths; confirm DPA and regional compliance before routing"
  - condition: "routing_automated == false"
    action: automate_routing_via_gv5
    reason: "Anti-pattern: manual routing depends on developer judgment and is error-prone; automate via GV-5 Central Model Gateway with data labels"
```

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (biased toward weak models) | All tasks processed by lightweight model | Quality degrades for complex reasoning and long-text analysis; error correction costs increase |
| Too much (biased toward strong models) | All tasks processed by the largest model | Cost becomes excessive even for simple tasks; latency is unnecessarily high |

Ignoring sensitivity classification causes different problems. Sending top-secret data to an external API creates a regulatory violation and information leakage risk.

## Decision Criteria

Model routing is designed along two axes: "difficulty axis" and "sensitivity classification axis."

**Difficulty Axis: Cascade Escalation**

- Estimate task difficulty at intake and begin processing with a lightweight model
- Escalate to a more capable model when response confidence falls below a threshold, or when a verification agent negates quality
- Continuously measure escalation rate with [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) by path and task type to evaluate threshold appropriateness

**Sensitivity Classification Axis: Path Separation**

- Top-secret data (subject to [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)) must use only VPC-internal or on-premises inference paths. Sending to external APIs is prohibited
- General data may use paths including external APIs; select based on cost/performance balance
- Periodically review the routing ratio per classification (VPC vs. external) and verify there are no leaks from classification errors

Compare quality scores by model using [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) and apply to escalation threshold tuning.

!!! danger "Misconfigured Sensitivity-Based Routing"
    A routing configuration error for top-secret data causes information leakage. Sensitivity-based routing must be automatically applied based on data labels ([GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) classification policy) without depending on manual settings.

## Adjustment Mechanism

- Measure escalation rate per path and task type with [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) and continuously improve the accuracy of difficulty estimation models
- Track cost, latency, and quality scores for both VPC paths and external API paths in conjunction with [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)
- Periodically review the routing ratio per sensitivity classification and verify data labeling accuracy

## Related Patterns

- [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md) — the core model routing implementation
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) — safe processing paths for top-secret data
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — per-model quality evaluation and threshold adjustment
