---
title: "TO-9 Custom Connector vs. Existing iPaaS Reuse"
description: "Design guidance for verifying authorization granularity in existing integration assets meets permission-faithful requirements, and MCP-ifying only the insufficient parts."
status: done
---

# TO-9 Custom Connector vs. Existing iPaaS Reuse

## Overview

If you've already built a Salesforce integration with MuleSoft or Workato, rewriting it from scratch is wasteful. However, be cautious about whether existing connectors are designed to "hit all APIs with a single admin-privileged service account." If per-user permission isolation is not possible, data beyond the user's permissions can be accessed through the agent. The decision to reuse existing assets can only be made after verifying authorization granularity.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-9
decision_rules:
  - condition: "existing_ipaas_connector == true AND authorization_granularity_verified == true AND audit_trail_linkable == true"
    recommendation: ipaas_reuse
    reason: "Reuse existing iPaaS assets where authorization granularity and audit trail requirements are verified as met"
  - condition: "existing_ipaas_connector == true AND uses_admin_service_account == true"
    recommendation: custom_build
    reason: "iPaaS connectors embedding admin-level service accounts cannot enforce user-level permission fidelity; reuse is disqualified"
  - condition: "new_integration_point == true"
    recommendation: mcp_gateway
    reason: "New integration points should be MCP-standardized (IN-1) to enable future swap and extension with unified tool definitions"
  - condition: "ipaas_obo_support == false AND obo_required == true"
    recommendation: hybrid_validated_ipaas
    reason: "If iPaaS lacks User OBO (RFC 8693) support, restrict reuse scope and add MCP Gateway for permission-controlled operations"
  - condition: "authorization_granularity_not_verified == true"
    recommendation: hybrid_validated_ipaas
    reason: "Never skip authorization granularity verification; unverified adoption preserves admin service account anti-pattern"
```

## Comparison

| Perspective | Custom Connector | Existing iPaaS Reuse ([IN-4](../../patterns/in-integration/in4-existing-ipaas-reuse.md)) |
|---|---|---|
| Development Cost | High | Low (leverages existing connection configuration) |
| Authorization Granularity Control | Can be designed freely | Depends on iPaaS implementation |
| Maintenance Burden | Owned by the company | Owned by iPaaS vendor (updates and incident response) |
| Ecosystem | Built from zero | Existing flows can be reused |
| MCP Compatibility | Standardized via [IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md) | Depends on iPaaS-side MCP support |

## Decision Criteria

**Prioritize reuse ([IN-4](../../patterns/in-integration/in4-existing-ipaas-reuse.md)) in areas where existing integration assets exist.** However, perform the following verification before reusing.

Decision axes for reusability:

- **Authorization granularity**: Verify that the iPaaS's existing connector meets the permission-faithful ([ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md)) requirements. Connectors where "a service account with administrator privileges to the entire SaaS is embedded" cannot reduce user permissions and are judged as not reusable.
- **Audit trail**: Verify that operations via iPaaS can be linked to audit logs on the agent side. If the operator, operation content, and timestamp cannot be traced, custom implementation may be required.
- **User OBO support**: Verify whether Token Exchange per [ID-2](../../patterns/id-identity/id2-identity-federation-obo.md) is supported. If not, limit the scope of reuse.

For new and unique integration points, MCP-ification ([IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md)) is the standard. MCP standardizes tool definitions, making future replacement and extension straightforward.

!!! warning "Authorization Granularity Verification Must Not Be Skipped"
    If existing iPaaS connectors are adopted without verification "because they're convenient," designs using admin-privileged service accounts are preserved, leading to permission leakage. Always perform authorization granularity verification before reuse.

## Hybrid and Gradual Approach

A practical combination is to reuse existing iPaaS where authorization granularity is satisfied, and implement custom or MCP-based solutions only where it is not.

1. Enumerate existing iPaaS connectors and score them from the perspective of authorization granularity and audit trail.
2. Connectors that meet requirements are reused as-is and registered as agent tools.
3. For connectors that do not meet requirements, add permission controls via MCP Gateway ([IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md)) or switch to custom implementation.
4. Design new integration points with MCP as the standard, unifying iPaaS connections through MCP Adapters as well.

## Related Patterns

- [IN-1 Enterprise Tool / MCP Gateway](../../patterns/in-integration/in1-tool-mcp-gateway.md)
- [IN-4 Existing iPaaS Reuse](../../patterns/in-integration/in4-existing-ipaas-reuse.md)
- [ID-4 Permission Mirror / Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md)
