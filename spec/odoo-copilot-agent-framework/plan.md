# Plan — Odoo Copilot Agent Framework

## Architecture

```
Users / APIs / Channels
        │
   APIM AI Gateway (production front door)
        │
   ┌────┴────┐
   │Advisory │ ← Foundry Prompt Agent (user-facing)
   └────┬────┘
        │
   ┌────┴────┐
   │ Router  │ ← Agent Framework Workflow (deterministic)
   └──┬───┬──┘
      │   │
  ┌───┴┐ ┌┴────┐
  │Ops │ │Act. │ ← Agent Framework Agents
  └──┬─┘ └─┬───┘
     │      │
  ┌──┴──────┴──┐
  │ Capability │
  │   Packs    │
  └────────────┘
```

## Ingress Matrix

| Ingress path | Use it for | Backing endpoint / client | Who should use it | Governance layer |
|---|---|---|---|---|
| Foundry Project Client | project config, connections, tracing, Foundry-native ops | `AIProjectClient` on `https://<resource>.services.ai.azure.com/api/projects/<project>` | internal control-plane services | Foundry RBAC + project scope |
| OpenAI-compatible client from project | agents, evaluations, responses, model calls in project context | `project.get_openai_client(...)` / `/openai` route | advisory, ops, actions runtime calls | Foundry project scope + model deployment policy |
| Direct REST | adapters, n8n/webhooks, lightweight bridges | `/openai/v1` or compatible route | automation bridges, service adapters | APIM or service auth in front |
| API Management AI gateway | enterprise front door for models, agents, tools, MCP/A2A APIs | APIM AI gateway | all production ingress | auth, quotas, throttling, routing, observability |
| Foundry Playgrounds | rapid prototyping and validation | model / agents playground | builders and operators only | non-production sandbox |

## Ingress Ownership by Component

| Component | Primary ingress | Secondary ingress | Notes |
|---|---|---|---|
| Advisory | APIM → Foundry/OpenAI-compatible client | Playground during prototyping | main enterprise chat/API surface |
| Ops | internal APIM route → Agent Framework runtime | project client for setup/tracing | internal-only |
| Actions | internal APIM route → Agent Framework runtime | none | approval-gated only |
| Router | internal service ingress only | none | not user-facing |

## Evaluation Model

### System evaluations
- Task Completion
- Task Adherence
- Intent Resolution
- Relevance / Groundedness where applicable

### Process evaluations
- Tool Selection
- Tool Call Success
- Tool Output Utilization
- Tool Input Accuracy
- Task Navigation Efficiency for workflow paths with ground truth

**Important**: Several tool-centric evaluators have limited support when conversations include Azure AI Search. First wave should rely more on system evals, retrieval quality checks, business-scenario pass/fail tests, and trace review.

### Safety evaluations
- Advisory: content risk + jailbreak screening + sampled human review
- Ops: leakage/refusal + internal red-team scenarios
- Actions: policy tests, approval-path tests, human review before production enablement
- Router: approval compliance and routing correctness

## Safety Caveat

Foundry safety evaluations are helpful but not sufficient alone; they are not comprehensive, can produce false positives/negatives, and should be combined with human review and domain-specific policy tests before production release.

## Phased Rollout

### Phase 1 — Stabilize Advisory
- Keep current `ipai-odoo-copilot-azure` as front door
- Attach custom guardrail correctly
- Clean up knowledge indexing
- Create advisory eval datasets
- Enable tracing + App Insights

### Phase 2 — Add Ops
- Create Ops agent
- Connect read-only Odoo + Databricks diagnostics
- Add process evals for read-only tool use

### Phase 3 — Add Router
- Create Router workflow in Agent Framework
- Implement deterministic routing and approval pauses
- Add routing and workflow evals

### Phase 4 — Add Actions
- Build Action agent with smallest safe write scope
- Add strict approval/evidence/rollback requirements
- Add process + safety evals

### Phase 5 — Layer Capability Packs
- Databricks Intelligence Pack
- fal Creative Production Pack
- Marketing Strategy & Insight Pack
- BIR Compliance Pack
- Document Intake & Extraction Pack

### Phase 6 — Production Ingress
- Move to APIM-governed production
- Project client + OpenAI-compatible client behind APIM
- Direct REST only for adapters/automation bridges

## Odoo-Native Workflow Integration

Use Odoo Project/Service primitives for operational workflow:

| Odoo primitive | Tax/compliance use |
|---|---|
| Stages | Draft → Computed → Validated → Approved → Filed → Confirmed |
| Activities | reminders, approvals, missing-data follow-ups |
| Reporting | overdue filings, blocked filings, upcoming deadlines |
| Project task templates | recurring BIR/month-end tasks |
| Milestones | compute, validate, export, pay, confirm |
| Task Dependencies | prerequisite chains |

PLM-style approval semantics for tax tasks:
- **Required approver** — must approve before stage transition
- **Optional approver** — can approve but not blocking
- **Comments only** — observer, no gate

## Not In Scope

- Teams/BizChat publishing (future, depends on M365 Agents SDK maturity)
- Hosted agent deployment (Action agent may migrate later when action logic grows)
- Fine-tuning (deferred until datasets and evaluations are stable)
