---
title: "EX-1 Enterprise Agent Gateway (Unified Front Door)"
description: "A pattern that applies authentication, classification, risk scoring, rate control, and audit entry creation centrally at a single entry point through which every agent request passes."
status: done
pattern_id: EX-1
facet: experience
requires: ["ID-1", "ID-2", "ID-6"]
required_by: []
applies_when: [enterprise_scale, multi_channel, audit_required, customer_facing]
not_applicable_when: [poc_phase, single_team]
risk_tiers: [1, 2, 3, 4]
key_technologies: [Kong, Apigee, AWS API Gateway, OIDC, SAML 2.0, Risk Scoring, OpenTelemetry Trace ID, Token Bucket]
---

# EX-1 Enterprise Agent Gateway (Unified Front Door)

## Overview

Whether an employee talks to an agent via Slack, uses a web portal, or invokes it from within a Salesforce screen, all requests pass through a single entry point. Because identity verification, risk scoring, rate control, and audit log creation are all handled at this one point, security and governance quality do not degrade as channels multiply. This gateway also absorbs the burst traffic of tens of thousands of employees all starting work at the same time during morning peak hours.

## Business Problem

As enterprise AI is called from multiple channels (Slack, web, SaaS embedded, API), entry points become fragmented and governance, auditing, and capacity management break down. When each channel uses a different authentication method, completeness of permission checks cannot be guaranteed, and audit logs become fragmented, hindering post-incident investigations. When individual agents try to absorb burst traffic from tens of thousands of users during business hours, back-end systems become overloaded. Furthermore, implementing separate governance logic per channel causes maintenance costs to multiply and creates governance gaps. A single entry point structurally addresses all of these problems at once.

!!! tip "Minimum Viable Implementation"
    Accept all channel requests through a single reverse proxy and implement three things: OIDC authentication, correlation ID attachment, and audit log output. Risk classification and rate control can be added in later phases.

## Value Hypothesis

Establishing a company-wide unified entry point reduces the cost for employees to reach agents to near zero, increasing utilization and retention rates. Higher utilization directly speeds value realization across all use cases and also reduces security costs by eliminating shadow AI.

## Solution and Design

Position the Gateway as the "sole passage to the execution plane" and perform all governance controls there in one place. Individual agents do not need to implement authentication, risk scoring, or audit entry creation — they simply receive the guaranteed user identity and correlation ID from the Gateway. Adding a new agent or channel requires no re-implementation of governance logic.

Absorb channels (Slack, web, SaaS-embedded) and propagate user identity and correlation ID downstream. The Gateway is a control point and serves as the first PEP ([ID-6](../id-identity/id6-zero-trust-pdp-pep.md)) that executes authentication, classification, risk scoring, rate control, and audit.

```mermaid
flowchart TB
    subgraph Channels["Channels"]
        SL[Slack]
        WEB[Web]
        SF[Salesforce Embedded]
        API[API]
    end

    subgraph GW["Enterprise Agent Gateway"]
        AUTH[Authentication<br/>OIDC / SAML]
        CLS[Request Classification<br/>Intent Detection]
        RISK[Risk Classification]
        RATE[Rate Control<br/>Burst Absorption]
        AUD[Audit Entry<br/>Correlation ID Assignment]
    end

    subgraph Backend["Execution Plane"]
        RT[Runtime / Orchestrator]
    end

    Channels --> AUTH
    AUTH --> CLS --> RISK --> RATE --> AUD
    AUD -->|User Identity + Correlation ID| RT
```

## Applicability

| Good Fit | Poor Fit |
|---|---|
| Multiple channels with large-scale organization-wide deployment | Single-channel PoC |
| Environments with governance and audit requirements | Fully isolated experimental environments |
| Need to separate workforce and customer channels | Small-scale deployments with only one channel |
| — | Deterministic RPA or form-processing fixed workflows (AI agent adoption itself is unnecessary) |

## Technology and Integration

- **API Gateway**: Kong, Apigee, AWS API Gateway
- **Authentication**: OIDC, SAML 2.0
- **Risk classification**: Risk Scoring, intent classifier
- **Correlation ID**: OpenTelemetry Trace ID
- **Rate control**: Token Bucket, burst absorption

## Pitfalls and Selection Criteria

!!! warning "Passthrough Proxy Anti-Pattern"
    Making the Gateway a passthrough proxy that delegates authorization and auditing to downstream components is the greatest pitfall. The entry point is a control point — authentication, risk classification, and audit entry creation must be executed here, reliably.

- Separate workforce and customer channels with a trust boundary, following [ID-1 Dual-Plane Separation](../id-identity/id1-workforce-customer-split.md).
- Execute Token Exchange ([ID-2 OBO](../id-identity/id2-identity-federation-obo.md)) at the Gateway and pass OBO tokens to downstream components.
- Integrate rate control with [IN-3 Rate/Quota Broker](../in-integration/in3-rate-quota-broker.md) and account for SaaS-side rate limits as well.

## Interfaces

The following are the key interfaces for implementing this pattern. Coding agents can generate stub code from these definitions.

```yaml
interfaces:
  - name: Authentication & Risk Classification
    description: "Validates OIDC/SAML identity tokens, classifies request intent and risk tier, and assigns a correlation ID before forwarding to the backend runtime."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Error occurred during Authentication & Risk Classification processing"
    protocol: "REST / gRPC"
    implementation_hints:
      - "See the Solution and Design section for details"
    code_examples:
      typescript: |
        interface AuthenticationRiskClassificationRequest {
          idToken: string;
          channel: string;
          requestPayload: object;
        }
        interface AuthenticationRiskClassificationResponse {
          principalId: string;
          correlationId: string;
          riskTier: number;
          intent: string;
        }
        interface AuthenticationRiskClassification {
          authenticationRiskClassification(req: AuthenticationRiskClassificationRequest): Promise<AuthenticationRiskClassificationResponse>;
        }
      python: |
        @dataclass
        class AuthenticationRiskClassificationRequest:
            id_token: str
            channel: str
            request_payload: dict
        
        @dataclass
        class AuthenticationRiskClassificationResponse:
            principal_id: str
            correlation_id: str
            risk_tier: int
            intent: str
        
        class AuthenticationRiskClassification(Protocol):
            async def authentication_risk_classification(self, req: AuthenticationRiskClassificationRequest) -> AuthenticationRiskClassificationResponse: ...
  - name: Rate Control & Burst Absorption
    description: "Token-bucket rate limiter that absorbs enterprise-wide peak bursts and coordinates with IN-3 Rate/Quota Broker for SaaS-side quota limits."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Error occurred during Rate Control & Burst Absorption processing"
    protocol: "REST / gRPC"
    implementation_hints:
      - "See the Solution and Design section for details"
    code_examples:
      typescript: |
        interface RateControlBurstAbsorptionRequest {
          agentId: string;
          saasTarget: string;
          requestCount: number;
        }
        interface RateControlBurstAbsorptionResponse {
          allowed: boolean;
          remainingQuota: number;
          retryAfterMs: number;
        }
        interface RateControlBurstAbsorption {
          rateControlBurstAbsorption(req: RateControlBurstAbsorptionRequest): Promise<RateControlBurstAbsorptionResponse>;
        }
      python: |
        @dataclass
        class RateControlBurstAbsorptionRequest:
            agent_id: str
            saas_target: str
            request_count: int
        
        @dataclass
        class RateControlBurstAbsorptionResponse:
            allowed: bool
            remaining_quota: int
            retry_after_ms: int
        
        class RateControlBurstAbsorption(Protocol):
            async def rate_control_burst_absorption(self, req: RateControlBurstAbsorptionRequest) -> RateControlBurstAbsorptionResponse: ...
  - name: Audit Entry Point
    description: "Emits a structured audit record per request (actor ID, channel, intent, risk tier, correlation ID) to OB-1 Observability Lake."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Error occurred during Audit Entry Point processing"
    protocol: "REST / gRPC"
    implementation_hints:
      - "See the Solution and Design section for details"
    code_examples:
      typescript: |
        interface AuditEntryPointRequest {
          actorId: string;
          agentId: string;
          correlationId: string;
          action: string;
          resource: string;
        }
        interface AuditEntryPointResponse {
          auditId: string;
          recordedAt: Date;
        }
        interface AuditEntryPoint {
          auditEntryPoint(req: AuditEntryPointRequest): Promise<AuditEntryPointResponse>;
        }
      python: |
        @dataclass
        class AuditEntryPointRequest:
            actor_id: str
            agent_id: str
            correlation_id: str
            action: str
            resource: str
        
        @dataclass
        class AuditEntryPointResponse:
            audit_id: str
            recorded_at: datetime
        
        class AuditEntryPoint(Protocol):
            async def audit_entry_point(self, req: AuditEntryPointRequest) -> AuditEntryPointResponse: ...
```

## Related Patterns

- [EX-2 Business-Embedded + Independent Workbench (Channel Placement)](ex2-embedded-vs-portal.md) — Complementary: determines the UI delivery form under the Gateway
- [EX-3 Channel-Agnostic Front Door](ex3-channel-agnostic-frontdoor.md) — Complementary: handles channel-difference absorption before reaching the Gateway
- [ID-1 Workforce/Customer Dual-Plane Separation](../id-identity/id1-workforce-customer-split.md) — Complementary: prerequisite for separating trust boundaries at the entry point
- [ID-2 Identity Federation & OBO](../id-identity/id2-identity-federation-obo.md) — Complementary: implementation of Token Exchange at the Gateway
- [ID-6 Zero-Trust PDP/PEP](../id-identity/id6-zero-trust-pdp-pep.md) — Similar: the Gateway functions as the first PEP
- [OB-1 Observability Lake](../ob-observability/ob1-observability-lake.md) — Complementary: destination for audit entry submissions
