---
title: "Department Examples"
description: "Practical guide for applying patterns in Sales, HR, CS, Engineering, and Executive departments."
status: done
---

# Department Examples

The **outcome KPIs** that enterprise AI agents drive differ significantly by department. Sales focuses on win rate and pipeline, HR on hiring lead time and attrition rate, customer support on CSAT and first-contact resolution, engineering on lead time and MTTR, and executives on decision speed and company-wide cost optimization — for each department's value use cases, there is a defined bundle of patterns to safely realize that value.

Each department page explains "how to move which outcome KPIs" (value use cases + outcome KPI mapping + value staircase) as the primary axis, with reasoning for the pattern applications that safely realize that value.

## Department List

| Department | Value Focus | Effective Outcome KPIs | Safety Foundation (Key Patterns) |
|---|---|---|---|
| [Sales Agent](sales.en.md) | Win rate improvement, deal cycle shortening, pipeline health | Win rate, deal cycle, pipeline value, deal size | ID-2, ID-4, IN-2, KM-5, RT-5, RT-4 |
| [HR Agent](hr.en.md) | Recruiting efficiency, attrition prevention, self-service inquiries | Hiring lead time, offer acceptance rate, attrition rate, self-resolution rate | KM-4, KM-6, RT-4, GV-4, RT-6 |
| [Customer Support Agent](customer-support.en.md) | Customer satisfaction improvement, handling efficiency, churn prevention | CSAT, AHT, first-contact resolution, churn rate, LTV | ID-1, RT-3, KM-1, RT-7, RT-9 |
| [Engineering Agent](engineering.en.md) | Development productivity improvement, incident response acceleration | Lead time (DORA), review time, MTTR, self-resolution rate | IN-1, ID-6, RT-8, OB-1, GV-9, ID-7 |
| [Executive Agent](executive.en.md) | Decision acceleration, company-wide optimization, early risk detection | Decision speed, judgment accuracy, cost optimization, loss prevention | KM-3, KM-2, KM-6, GV-8, GV-7, OB-2 |

## How to Select Patterns

When selecting the right pattern bundle for a department, the following six axes help organize the thinking.

### Value Axis (Which Outcome KPIs to Move)

**Business value type**: Whether the primary focus is revenue contribution (Sales), cost optimization (HR/CS/Engineering), or decision acceleration (Executive) determines use case selection. The "Value Use Cases" table and "Outcome KPI Mapping" diagram on each department page show specific causal paths.

**Value realization timeline**: The staged design of Quick Win (read-only, value felt in 1–4 weeks) → Analysis/Insights (1–3 months) → Automation (3–12 months) is common to all departments. The "Value Staircase" on each department page shows the functions and expected outcomes at each stage. For details, refer to the [Value Maturity Roadmap](../value-maturity-roadmap.md).

### Safety Axis (For Realizing Value Safely)

**Data sensitivity**: Departments handling high-risk data under personal information protection laws and corporate law — such as salary, evaluations, and executive information — require thicker DLP, scope separation, and audit patterns.

**Write risk**: When performing writes to CRM, ERP, and HR systems beyond read-only, use Command Envelope (RT-5) and SoR Write Boundary (RT-6) to structure operations, and insert Human Approval (RT-4) for confirmation.

**Customer-facing nature**: Agents that interact directly with customers (such as customer support) must completely separate ID, permissions, and logs from internal employee-facing agents (ID-1).

**Execution environment risk**: For engineering use cases involving code execution and production infrastructure operations, mandatory isolation through Zero-Trust PDP/PEP (ID-6) and sandboxing (equivalent to IN-1) is a prerequisite.
