# Odoo Copilot Agent Framework — Execution Plan

> Version: 2.0.0
> Last updated: 2026-03-15

## Phased Rollout

### Phase 1 — Foundation (Q2 2026)

**Epics**: E-FND-01, E-FND-02

| Deliverable | Status |
|-------------|--------|
| Cosmos DB session persistence | Done |
| Application Insights telemetry | Done |
| PII redaction middleware | Done |
| Foundry KB files (6 files, 1302 lines) | Drafted |
| Agent instructions v7 | Drafted |
| Upload KB to Foundry portal | Pending |
| Replace instructions with v7 | Pending |
| First live eval against Foundry | Pending |
| Tool Contract v1 template | Done |
| Eval harness: smoke + safety | Done |

**Gate**: `tool_spec_contract_gate` — every tool has a spec before connection.

**Agent topology**: Single advisory agent (current `ipai-odoo-copilot-azure`).

### Phase 2 — Knowledge + Tools + Agent Split (Q3 2026)

**Epics**: E-KAPA-01, E-BRIDGE-01, E-AGT-01, E-NLQ-01

| Deliverable | Status |
|-------------|--------|
| Azure AI Search index | Not started |
| Citation extraction pipeline | Not started |
| OpenAPI bridge (read-only endpoints) | Spec drafted |
| OpenAPI bridge (write endpoints with confirmation) | Not started |
| Agent registry + scoped permissions | Not started |
| NL-to-SQL pipeline for Odoo data | Not started |
| **Split single agent into 3 agents + 1 workflow** | Not started |
| APIM AI Gateway configuration | Not started |
| Databricks Intelligence Pack (v1) | Not started |

**Gate**: `knowledge_eval` — groundedness > 0.8 on knowledge eval set.

**Agent topology**: Advisory + Ops + Actions + Router deployed, APIM routing live.

### Phase 3 — Enterprise Copilot (Q4 2026)

**Epics**: E-COP-01, E-EXP-01, E-OCR-01, E-OBS-01

| Deliverable | Status |
|-------------|--------|
| M365 Teams channel (via Copilot Studio or bot) | Not started |
| Odoo sidebar copilot (ipai_ai_copilot 19.0) | Not started |
| Unified conversation state across surfaces | Not started |
| Expense + cash advance domain | Not started |
| Receipt OCR via Document Intelligence | Not started |
| Distributed tracing for all agents | Not started |
| CI-triggered eval runs | Not started |
| fal Creative Production Pack (v1) | Not started |

**Gate**: `action_eval` — 100% safety, approval checkpoint compliance.

### Phase 4 — Marketing Intelligence (Q1 2027)

**Epics**: E-LIO-01, E-SMT-01, E-QLT-01, E-DI-01

| Deliverable | Status |
|-------------|--------|
| Evidence workspace (Lions-like) | Not started |
| Creative ops (Smartly-like) | Not started |
| Consumer intelligence (Quilt-like) | Not started |
| Data Intelligence Philippines lakehouse | Not started |
| Marketing Strategy & Insight Pack | Not started |

### Phase 5 — Strategic (Q2 2027+)

| Deliverable | Priority |
|-------------|----------|
| Predictive analytics (cash flow, demand, churn) | P2 |
| Voice transcription | P2 |
| AI field generation | P2 |
| Coding agent (issue → PR) | P1 |
| Multi-provider routing | P1 |
| Proactive insight engine | P1 |

## Component Lifecycle

```
Phase 1: [advisory (single agent)]
Phase 2: [advisory] [ops] [actions] [router] ← agent split happens here
Phase 3: [advisory] [ops] [actions] [router] + cross-surface
Phase 4: [advisory] [ops] [actions] [router] + capability packs
Phase 5: [advisory] [ops] [actions] [router] + strategic capabilities
```

## Rule

Add capabilities to existing agents via packs. Do not add top-level agents beyond the 3+1 topology.
