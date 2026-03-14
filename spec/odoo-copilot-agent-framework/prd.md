# Odoo Copilot Agent Framework — Product Requirements Document

> Version: 2.0.0
> Last updated: 2026-03-15

## Problem

InsightPulseAI needs a governed AI assistant across multiple surfaces (landing page, Odoo ERP, M365) that can answer questions, navigate systems, and execute bounded write operations — all with audit trails, citations, and approval gates. The current single-agent model conflates read and write concerns, making it impossible to safely promote to production with write capabilities.

## Solution: 3 Agents + 1 Workflow

### Component Table

| Component | Form | Purpose | Runtime |
|-----------|------|---------|---------|
| ipai-odoo-copilot-advisory | Foundry Prompt Agent | User-facing, grounded, read-only | Foundry |
| ipai-odoo-copilot-ops | Agent Framework Agent | Internal diagnostics, read-only tools | Agent Framework |
| ipai-odoo-copilot-actions | Agent Framework Agent | Approved writes, bounded execution | Agent Framework |
| ipai-odoo-copilot-router | Agent Framework Workflow | Routing, approvals, checkpoints | Agent Framework |

### Foundry vs Agent Framework Split

| Concern | Foundry (Control Plane) | Agent Framework (Execution Plane) |
|---------|------------------------|-----------------------------------|
| Prompt agents | Yes | No |
| Datasets / eval sets | Yes | No |
| Evaluations | Yes | No |
| Tracing | Yes (collector) | Yes (emitter) |
| Project-scoped resources | Yes | No |
| Workflows / orchestration | No | Yes |
| Middleware / checkpointing | No | Yes |
| Approvals / handoffs | No | Yes |
| Tool execution | Via agent | Via middleware |

### Production Ingress

| Layer | Role |
|-------|------|
| APIM AI Gateway | Production front door — rate limiting, auth, routing |
| Playgrounds | Prototyping only — explicitly non-production |

## Users

| Persona | Surface | Agent |
|---------|---------|-------|
| External visitors | Landing page | Advisory |
| Internal staff | Odoo sidebar, Teams | Advisory → Router → Ops/Actions |
| Executives | M365 Copilot | Advisory |
| Platform operators | Internal tools | Ops |
| Automated workflows | n8n, CI/CD | Router → Actions |

## Functional Requirements

### FR-1: Informational Q&A (Advisory)
- Answer questions about BIR compliance, Odoo features, company capabilities
- Cite sources using 7 label types
- Grounded in Foundry knowledge base and Bing

### FR-2: Navigational Guidance (Advisory)
- Guide users to Odoo menu paths, records, dashboards
- Link to Superset dashboards, Supabase DMS

### FR-3: Operational Diagnostics (Ops)
- Read-only access to system status, logs, metrics
- No secrets in responses — hash or redact all sensitive values
- Diagnostics for Odoo, Databricks, infrastructure

### FR-4: Transactional Execution (Actions)
- Create/update Odoo records via OpenAPI bridge
- Every write requires router approval checkpoint
- Confirmation protocol with Adaptive Card display
- Bounded scope — only declared models, never raw SQL

### FR-5: Deterministic Routing (Router)
- Route requests to correct agent based on intent
- Enforce approval gates for write operations
- Handle escalation triggers deterministically
- Checkpoint state for resume-after-approval

## Non-Requirements

- Direct database access (all data through OpenAPI bridge)
- Bulk data export (max 100 records per query)
- Credential management (secrets stay in Key Vault)
- Fine-tuning (prompt engineering only)
- More than 3 agents + 1 workflow

## Capability Packs

| Pack | Contents | Agents |
|------|----------|--------|
| Databricks Intelligence Pack | Lakehouse queries, ML predictions, analytics marts | Advisory, Ops, Actions, Router |
| fal Creative Production Pack | Image generation, video, creative pipelines | Advisory, Ops, Actions, Router |
| Marketing Strategy & Insight Pack | Consumer intelligence, market analysis, evidence | Advisory, Ops |

## Success Metrics

| Metric | Target | Eval Set |
|--------|--------|----------|
| Groundedness score | > 0.8 | advisory, ops |
| Safety score | = 1.0 | all |
| Response time (advisory) | < 5s p95 | advisory |
| Response time (actions) | < 15s p95 | actions |
| Eval pass rate (smoke/safety) | 100% | all |
| Router accuracy | > 0.95 | router |
| Unauthorized write attempts blocked | 100% | actions, safety |

## Dependencies

| Dependency | Owner | Status |
|------------|-------|--------|
| Foundry Agent Service | Azure | Available |
| Microsoft Agent Framework | Azure | Available |
| APIM AI Gateway | infra | Not configured |
| Cosmos DB (session state) | infra | Implemented |
| Application Insights | infra | Implemented |
| OpenAPI Bridge | agents | Spec drafted |
| Azure AI Search | infra | Not started |
| Foundry KB files | agents | Drafted (6 files) |

## Acceptance Criteria

1. All 3 agents + 1 workflow defined in SSOT YAMLs
2. Every agent has eval datasets covering its scope
3. Safety evals pass at 100% before any production promotion
4. APIM is the only production ingress — playgrounds are non-production
5. Writes only flow through Actions agent with router approval
6. All traces visible in Application Insights
7. Capability packs are additive — no new top-level agents
