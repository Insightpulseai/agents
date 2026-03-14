# Odoo Copilot Agent Framework — Sprint Tasks

> Last updated: 2026-03-15
> Current phase: Phase 1 (Foundation)

## Phase 1 — Foundation

### Done
- [x] Cosmos DB session persistence (2026-03-14)
- [x] Application Insights telemetry wrapper (2026-03-14)
- [x] PII redaction middleware (2026-03-14)
- [x] Foundry KB files drafted — 6 files, 1302 lines (2026-03-14)
- [x] Agent instructions v7 drafted — 480 lines (2026-03-14)
- [x] Tool spec template + contract gate (2026-03-15)
- [x] Eval harnesses: knowledge + action (2026-03-15)
- [x] Singleton artifact migration: infra + agents (2026-03-15)
- [x] 3-agent + 1-workflow target state defined (2026-03-15)
- [x] Agent capability matrix created (2026-03-15)
- [x] Agent ingress matrix created (2026-03-15)
- [x] Eval datasets: advisory, ops, actions, router (2026-03-15)

### Pending — Pre-eval
- [ ] Upload KB files to Foundry portal
- [ ] Replace agent instructions with v7 in Foundry
- [ ] Run first live eval against Foundry endpoint
- [ ] Validate groundedness score > 0.8 on advisory eval set
- [ ] Validate safety score = 1.0 on safety eval set

### Pending — Post-eval
- [ ] Wire OpenAPI bridge as Foundry custom tool (read-only)
- [ ] Enable Bing grounding in Foundry
- [ ] Enable Memory in Foundry
- [ ] Fix model name mismatch (ipai_tax_compliance_* → ipai_bir_tax_compliance)
- [ ] Configure APIM AI Gateway for production ingress

## Phase 2 — Agent Split (blocked on Phase 1 eval)

- [ ] Deploy advisory agent as standalone Foundry prompt agent
- [ ] Deploy ops agent on Agent Framework
- [ ] Deploy actions agent on Agent Framework
- [ ] Deploy router workflow on Agent Framework
- [ ] Connect OpenAPI bridge write endpoints to actions agent
- [ ] Configure APIM routing rules for 3+1 topology
- [ ] Databricks Intelligence Pack v1

## Blocked

| Item | Blocker |
|------|---------|
| Odoo sidebar copilot | ipai_ai_copilot not migrated to 19.0 |
| M365 Teams channel | Requires Copilot Studio or Teams bot setup |
| M365 Copilot declarative agent | Requires M365 Copilot license |
| fal Creative Production Pack | fal.ai integration not started |
