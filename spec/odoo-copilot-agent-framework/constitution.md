# Odoo Copilot Agent Framework — Constitution

> Version: 2.0.0
> Last updated: 2026-03-15
> Governs: 3 agents + 1 workflow

## Architecture

| Component | Form | Runtime |
|-----------|------|---------|
| ipai-odoo-copilot-advisory | Foundry Prompt Agent | Foundry Control Plane |
| ipai-odoo-copilot-ops | Agent Framework Agent | Agent Framework Execution Plane |
| ipai-odoo-copilot-actions | Agent Framework Agent | Agent Framework Execution Plane |
| ipai-odoo-copilot-router | Agent Framework Workflow | Agent Framework Execution Plane |

## Rules

### 1. Advisory is the default surface

The advisory agent is the front-door copilot for all user-facing interactions. It is grounded, read-only, and never executes writes. All external traffic enters through the advisory agent.

### 2. Every grounded answer must cite its source

Responses use one of 7 source labels: `[IPAI-KB]`, `[BIR-CALENDAR]`, `[BING-LIVE]`, `[ODOO-LIVE]`, `[INFERRED]`, `[ADVISORY]`, `[UNVERIFIED]`. Uncitable claims must be labeled `[UNVERIFIED]` or refused.

### 3. Writes are isolated to the Actions agent

Only `ipai-odoo-copilot-actions` may execute write operations. Writes require explicit approval through the router workflow's checkpoint mechanism. The advisory and ops agents have no write tools.

### 4. Routing lives in the workflow, not in prompts

`ipai-odoo-copilot-router` is a deterministic Agent Framework workflow — not a chat agent. It handles routing, approvals, handoffs, and checkpoints. Routing logic must not be embedded in agent system prompts.

### 5. PII redaction is a cross-cutting control

PII redaction applies to all agent inputs and outputs across all surfaces. It is not a feature of any single agent — it is a guardrail enforced at the APIM/middleware layer.

### 6. Escalation triggers are deterministic

Escalation fires on: regulatory questions, amounts > PHP 500K, bulk operations (> 10 records), credential requests, system admin actions, ambiguous compliance interpretations. These rules live in the router workflow, not in agent prompts.

### 7. Environment mode constrains available capabilities

| Mode | Advisory | Ops | Actions | Router |
|------|----------|-----|---------|--------|
| BUILD | full | full | full | full |
| STAGING | full | full | full (with test data) | full |
| PROD-ADVISORY | full | read-only | disabled | routing only |
| PROD-ACTION | full | read-only | approval-gated | full |

### 8. All operations produce audit trail entries

Every tool invocation, routing decision, and approval checkpoint produces a trace entry with: timestamp, component, operation, input hash, result status, duration. Traces flow to Application Insights via the Foundry tracing integration.

### 9. Add capabilities, not agents

New functionality is added as capability packs attached to existing agents — not as new top-level agents. The 3+1 topology is fixed. Vendor-specific logic (Databricks, fal, marketing tools) lives inside capability packs.

## Capability Packs

| Pack | Purpose | Consumers |
|------|---------|-----------|
| Databricks Intelligence Pack | Lakehouse queries, analytics, ML predictions | Advisory, Ops, Actions, Router |
| fal Creative Production Pack | Image/video generation, creative asset pipeline | Advisory, Ops, Actions, Router |
| Marketing Strategy & Insight Pack | Consumer intelligence, market analysis, evidence synthesis | Advisory, Ops |

## Safety Caveat

System evaluations (groundedness, relevance, safety scores) are necessary but not sufficient. Safety requires:
- Human review of edge cases and adversarial inputs
- Policy tests for regulatory compliance (BIR, SEC, BSP)
- Red-team exercises before PROD-ACTION promotion
- Continuous monitoring of production traces for drift
