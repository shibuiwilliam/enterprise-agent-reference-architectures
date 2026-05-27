---
title: "TO-10 Internal/On-premises Model vs. External API"
description: "Design guidance for automatically routing inference paths by data classification — using VPC/on-premises for confidential and regulated data, and external APIs for general or latest-capability cases."
status: done
---

# TO-10 Internal/On-premises Model vs. External API

## Overview

Sending prompts containing patients' medical information to an external API can constitute a regulatory violation. On the other hand, running expensive GPU infrastructure in-house to answer internal FAQs is not cost-effective. Neither "everything on-premises" nor "everything via external API" is realistic. The practical solution is a hybrid that automatically switches the inference path based on data sensitivity.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-10
decision_rules:
  - condition: "data_classification IN ['top_secret', 'personally_identifiable', 'competitive_intelligence']"
    recommendation: internal_onprem
    reason: "Top-secret and PII data must not leave internal infrastructure; regulatory/legal requirements may also mandate on-premise"
  - condition: "regulatory_requirement IN ['gdpr', 'financial', 'medical'] AND cross_border_transfer_prohibited == true"
    recommendation: internal_onprem
    reason: "Data regulated against cross-border transfer must remain in compliant infrastructure; DPA alone is insufficient"
  - condition: "data_classification == 'public' OR data_classification == 'general_internal' AND latest_model_required == true"
    recommendation: external_api
    reason: "General or public data with no regulatory restrictions can use external API, especially when latest model capability is required"
  - condition: "data_classification_mixed == true"
    recommendation: hybrid_data_classification_routing
    reason: "Central Model Gateway (GV-5) auto-routes by data classification label; eliminates per-developer routing decisions"
  - condition: "external_api_used == true AND dpa_not_confirmed == true"
    recommendation: internal_onprem
    reason: "Always confirm DPA, region, and data retention policy before using external APIs; default settings may cause unintended data usage"
```

## Comparison

| Perspective | Internal/On-premises Model | External API |
|---|---|---|
| Data Sovereignty | Completely in-house | Depends on vendor's processing and storage policy |
| Suitable For | Confidential data, regulated data, high-volume steady-state inference | General business, latest model performance needed, variable demand |
| Performance | Slow to adopt latest models | Latest models available immediately |
| Cost Structure | Fixed cost (infrastructure and maintenance) | Pay-per-use (follows demand but can become expensive) |
| Availability | Depends on in-house infrastructure reliability | SLA guaranteed by vendor |
| Setup | Complex (GPU, model management, MLOps) | Can start same day |

## Decision Criteria

Determine the inference path based on data sensitivity classification.

**Conditions requiring internal/on-premises model**:

- Prompts containing confidential data (internal secrets, personal information, competitive information, etc.)
- Data subject to restrictions on cross-border transfer under GDPR, financial regulations, healthcare regulations, etc.
- Cases with high-volume, steady-state inference needs where fixed costs are cheaper

**Conditions where external API is appropriate**:

- Inference involving publicly available information or internal policies requiring no authorization
- Use cases requiring the latest model performance (R&D support, etc.)
- Cases with variable demand where fixed infrastructure costs should be avoided
- Note: Always verify and control DPA (Data Processing Agreement), usage region, and data retention policy

[GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) automatically routes inference paths based on data classification, eliminating the need for developers to make individual judgments each time.

## Hybrid and Gradual Approach

Routing based on data classification within the same application is the standard design.

1. Set up a Central Model Gateway with [GV-5](../../patterns/gv-governance/gv5-central-model-gateway.md) and route all inference requests through it.
2. Establish a mechanism to attach data classification labels (confidentiality level, regulated data flag, etc.) to requests.
3. The Gateway automatically routes to internal model or external API based on the classification label.
4. When using external APIs, centrally manage DPA, region, and data retention control parameters in the Gateway.

!!! warning "Verify DPA Before Sending Data to External APIs"
    When using external APIs, always verify that a Data Processing Agreement has been established with the vendor, that the usage region meets requirements, and that input data will not be used for model training. Using external APIs with default settings creates risks of unintended data use and cross-border transfer.

## Related Patterns

- [GV-5 Central Model Gateway](../../patterns/gv-governance/gv5-central-model-gateway.md)
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)
