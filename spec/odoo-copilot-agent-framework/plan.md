# Execution Plan — IPAI Copilot Agent Framework

> Version: 1.0.0 | Last updated: 2026-03-15
> 5 phases from foundation to strategic capabilities

---

## Phase 1: Foundation (Q2 2026)

> Epic: E-FOUND-01 — Agent Foundation Layer

**Goal**: Establish the core agent infrastructure — persistence, observability, safety middleware, and tool contracts.

| Task | Status | Artifact |
|------|--------|----------|
| Cosmos DB session persistence | Done | `src/lib/cosmos.ts` |
| Application Insights telemetry wrapper | Done | `src/lib/telemetry.ts` |
| PII redaction middleware | Done | `src/middleware/pii-redact.ts` |
| Managed identity auth | Done | `server.ts` |
| Multi-turn conversations | Done | `server.ts` |
| Surface validation middleware | Done | `server.ts` |
| Foundry KB files drafted | Done | `docs/foundry-kb/` (6 files, 1302 lines) |
| Agent instructions v7 drafted | Done | `docs/foundry-kb/agent-instructions-v7-draft.md` |
| Upload KB files to Foundry portal | Pending | — |
| Replace agent instructions with v7 | Pending | — |
| Run first live eval against Foundry | Pending | — |
| Wire OpenAPI bridge as Foundry tool (read-only) | Pending | `apps/bridge-api/` |
| Enable Bing grounding in Foundry | Pending | — |
| Tool contract v1 (input/output schemas) | Pending | `contracts/tools/` |

**Exit criteria**: Landing page copilot live with Cosmos persistence, PII redaction, telemetry, KB-grounded responses, and smoke eval passing at 100%.

---

## Phase 2: Knowledge + Tools (Q3 2026)

> Epic: E-KAPA-01 — Citation-First Knowledge Copilot

**Goal**: Enable document-grounded answers with citations, connect OpenAPI bridge for read and write operations, establish agent registry.

| Task | Status | Artifact |
|------|--------|----------|
| Azure AI Search index creation | Not started | — |
| KB document indexing pipeline | Not started | — |
| Citation extraction middleware | Not started | — |
| Source label enforcement in eval | Not started | `eval/knowledge_copilot_eval.yaml` |
| OpenAPI bridge — read endpoints | Spec drafted | `apps/bridge-api/` |
| OpenAPI bridge — write endpoints (with confirmation) | Not started | — |
| Agent registry (multi-agent support) | Not started | — |
| Foundry Memory enablement | Not started | — |
| Groundedness eval passing > 0.8 | Not started | — |

**Exit criteria**: Groundedness score > 0.8 on eval, citation extraction working, OpenAPI bridge read endpoints live, agent registry operational.

**References**: E-KAPA-01 in `infra/ssot/roadmap/product_roadmap.yaml`

---

## Phase 3: Enterprise Copilot (Q4 2026)

> Epic: E-COP-01 — Enterprise Copilot Cross-Surface

**Goal**: Expand copilot to Odoo sidebar and M365 Teams, add expense management domain, OCR bridge, and full observability stack.

| Task | Status | Artifact |
|------|--------|----------|
| ipai_ai_copilot migration to Odoo 19 | Not started | `addons/ipai/ipai_ai_copilot/` |
| Odoo sidebar — chat panel integration | Not started | — |
| Odoo sidebar — deep link generation | Not started | — |
| M365 Teams bot registration | Not started | — |
| Teams — conversational interface | Not started | — |
| Expense management domain (CRUD) | Not started | — |
| OCR bridge (receipt → expense line) | Not started | — |
| Distributed tracing (correlation IDs) | Not started | — |
| Action eval passing at 100% | Not started | `eval/action_eval.yaml` |

**Exit criteria**: Odoo sidebar copilot functional with transactional capabilities, Teams bot responding to informational queries, action eval passing at 100%.

**References**: E-COP-01 in `infra/ssot/roadmap/product_roadmap.yaml`

---

## Phase 4: Marketing Intelligence (Q1 2027)

> Epic: E-MKTG-01 — Marketing Intelligence Agent

**Goal**: Add marketing-specific agent capabilities — evidence workspace, creative operations, and consumer intelligence.

| Task | Status | Artifact |
|------|--------|----------|
| Evidence workspace integration | Not started | — |
| Creative ops tools (brief generation, review) | Not started | — |
| Consumer intelligence queries | Not started | — |
| Campaign performance summarization | Not started | — |
| Marketing-specific KB documents | Not started | — |
| Marketing eval harness | Not started | — |

**Exit criteria**: Marketing team can query campaign performance, generate creative briefs, and access consumer insights via copilot.

**References**: E-MKTG-01 in `infra/ssot/roadmap/product_roadmap.yaml`

---

## Phase 5: Strategic (Q2 2027+)

> Epic: E-STRAT-01 — Strategic AI Capabilities

**Goal**: Long-horizon capabilities that extend the copilot into predictive, voice, and autonomous domains.

| Capability | Description | Prerequisite |
|-----------|-------------|--------------|
| Predictive analytics | Forecast revenue, cash flow, demand | Gold-tier data pipeline |
| Voice interface | Speech-to-text copilot interaction | Azure Speech Services |
| AI field generation | Auto-populate Odoo fields from context | OpenAPI bridge write + domain models |
| Coding agent | Generate ipai_* module scaffolds | Secure sandbox, code review gate |
| Autonomous scheduling | Auto-schedule compliance tasks | BIR calendar + Odoo calendar integration |

**Exit criteria**: At least 2 strategic capabilities in production pilot.

**References**: E-STRAT-01 in `infra/ssot/roadmap/product_roadmap.yaml`

---

## Cross-Phase Dependencies

```
Phase 1 (Foundation) ──→ Phase 2 (Knowledge + Tools) ──→ Phase 3 (Enterprise Copilot)
                                                     ──→ Phase 4 (Marketing Intelligence)
                                                                           │
                                                                           ▼
                                                                    Phase 5 (Strategic)
```

Phase 2 and Phase 4 can partially parallelize once Phase 1 exits. Phase 5 depends on mature data pipelines from Phase 3/4.
