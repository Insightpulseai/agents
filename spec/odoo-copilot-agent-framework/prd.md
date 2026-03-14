# Product Requirements Document — IPAI Copilot Agent Framework

> Version: 1.0.0 | Last updated: 2026-03-15
> Status: Active | Owner: InsightPulseAI Platform Team

---

## Problem Statement

InsightPulseAI requires an AI assistant that operates across 4 distinct surfaces (landing page, Odoo sidebar, M365 Teams, M365 Copilot) with governed tool use, citation-first knowledge delivery, and auditable transactional capabilities. Currently, the platform has no unified agent framework — each surface would require independent implementation without shared governance, evaluation, or tool contracts.

### Key Challenges

- **Fragmented user touchpoints**: External visitors need product info on the landing page; internal staff need Odoo operational assistance; executives need summarized insights via Teams/Copilot
- **Governance gap**: No standardized way to enforce citation requirements, PII redaction, escalation policies, or audit trails across surfaces
- **Tool safety**: Write operations against production Odoo must follow a confirmation protocol — silent writes are unacceptable
- **Compliance requirements**: BIR tax compliance, financial reporting, and audit trail requirements demand verifiable, source-cited responses

---

## Users and Surfaces

| Surface | Primary Users | Access Method | Auth |
|---------|--------------|---------------|------|
| **Landing Page** | External visitors, prospects, partners | Web chat widget | Managed identity (anonymous) |
| **Odoo Sidebar** | Internal staff (accounting, sales, ops) | Odoo 19 web client panel | Entra SSO via ipai_auth_oidc |
| **M365 Teams** | Executives, managers, field staff | Teams chat / channel bot | Entra SSO |
| **M365 Copilot** | Executives with M365 Copilot license | Copilot declarative agent | Entra SSO |

---

## Requirements

### Functional Requirements

#### FR-1: Informational Q&A
- Answer questions about IPAI platform capabilities, modules, and services
- Answer BIR tax compliance questions (filing calendar, form numbers, deadlines)
- Answer Odoo navigation questions (menu paths, feature locations)
- All answers must include source labels per constitution Rule 2

#### FR-2: Navigational Guidance
- Guide users to specific Odoo menu paths, records, and features
- Provide deep links where supported (Odoo sidebar surface)
- Surface-aware: landing page provides general guidance; Odoo sidebar provides actionable links

#### FR-3: Transactional with Confirmation
- Create, update, and mark records in Odoo via OpenAPI bridge
- Every write operation requires explicit user confirmation via Adaptive Card
- Confirmation card displays: action summary, affected records, reversibility status
- Only available on `odoo_sidebar` surface in `PROD-ACTION` environment mode

#### FR-4: Document-Grounded with Citations
- Retrieve answers from indexed documents via Azure AI Search
- Extract and display source citations with document name and section
- Groundedness score target: > 0.8 on eval harness

#### FR-5: Governed with Audit
- Enforce constitution rules (9 rules — see constitution.md)
- PII redaction on all inputs/outputs
- Escalation triggers for regulatory, high-value, bulk, credential, and admin operations
- Audit trail entry for every tool invocation

### Non-Functional Requirements

#### NFR-1: Response Time
- P95 response time < 5 seconds for informational queries
- P95 response time < 10 seconds for tool-augmented queries
- Streaming enabled where supported (landing page, Odoo sidebar)

#### NFR-2: Availability
- Landing page copilot: 99.5% uptime (graceful degradation to static FAQ)
- Odoo sidebar: availability tied to Odoo instance SLA
- M365 surfaces: availability tied to M365 service health

#### NFR-3: Observability
- Application Insights telemetry for all agent interactions
- Distributed tracing with correlation IDs across surfaces
- Eval metrics published to monitoring dashboard

---

## Non-Requirements (Explicitly Out of Scope)

| Item | Reason |
|------|--------|
| Direct database access | Agent communicates via OpenAPI bridge only, never direct SQL |
| Bulk data export | Security and performance risk; use Odoo export UI instead |
| Credential management | Agent never stores, retrieves, or displays secrets |
| Code generation | Agent is an operational copilot, not a development tool |
| Multi-tenant isolation | Single-tenant deployment (IPAI only) |
| Voice interface | Deferred to Phase 5 (strategic) |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Groundedness score | > 0.8 | Foundry eval API on groundedness eval set |
| Safety score | = 1.0 | Foundry eval API on safety eval set (zero tolerance) |
| Response time (P95) | < 5s informational, < 10s tool-augmented | Application Insights percentile |
| Eval pass rate (smoke) | 100% | CI-triggered eval harness |
| Eval pass rate (safety) | 100% | CI-triggered eval harness |
| Source label coverage | > 95% of grounded responses | Audit trail analysis |
| Escalation accuracy | > 90% true positive | Manual review of escalation logs |

---

## Dependencies

| Dependency | Status | Owner |
|------------|--------|-------|
| Azure AI Foundry Agent Service | Active | Azure platform |
| Cosmos DB (session persistence) | Implemented | IPAI infra |
| Application Insights | Implemented | IPAI infra |
| OpenAPI bridge (bridge-api) | Spec drafted | IPAI platform |
| Azure AI Search index | Not started | IPAI platform |
| Foundry KB files | Drafted (6 files, 1302 lines) | IPAI platform |
| Agent instructions v7 | Drafted (480 lines) | IPAI platform |
| Entra ID SSO | Active (landing page: managed identity) | IPAI auth |
| ipai_ai_copilot (Odoo 19 module) | Not migrated | IPAI Odoo |
| M365 Copilot license | Not procured | IPAI admin |
| Copilot Studio / Teams bot | Not started | IPAI platform |

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Foundry Agent Service API changes | High — breaks agent runtime | Pin API version, integration tests in CI |
| Hallucinated compliance answers | Critical — regulatory exposure | Safety eval with 1.0 pass rate, escalation triggers |
| OpenAPI bridge latency | Medium — degrades UX | Timeout + graceful fallback to advisory mode |
| KB staleness | Medium — outdated answers | KB version tracking, quarterly review cycle |
| M365 Copilot license cost | Low — delays Phase 3 | Landing page + Odoo sidebar cover primary use cases |
