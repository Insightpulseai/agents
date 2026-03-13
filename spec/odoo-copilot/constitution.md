# Odoo Copilot — Constitution

> Governing principles for the Odoo Copilot platform.

## Identity

Odoo Copilot is a three-surface enterprise assistant platform that delivers business intelligence, knowledge retrieval, and developer tooling across Microsoft 365, Odoo, and GitHub.

## Governing Principles

### 1. Odoo-First, Azure-Hosted

Odoo is the system of record and system of action. Azure is the compute and AI platform. The agent runtime never bypasses Odoo's business logic or security model.

### 2. Tool-Based Architecture

All agent interactions with external systems happen through typed, schema-defined tools. No raw LLM calls to production systems. No arbitrary model access.

### 3. Policy-Safe by Default

Every write action requires:

- Permission verification against Odoo RBAC
- Dry-run preview before execution
- Optional approval gate for sensitive operations
- Immutable audit trail

### 4. Grounded Answers Only

The knowledge layer must cite sources. Every factual answer includes:

- Source document or record reference
- Section or field-level citation
- Freshness metadata (last indexed date)
- Confidence signal

### 5. Separation of Surfaces

| Surface | Purpose | SDK |
|---------|---------|-----|
| Business Copilot | ERP/CRM/finance ops for business users | Microsoft 365 Agents SDK |
| Knowledge Copilot | Docs, SOPs, troubleshooting, citations | Microsoft 365 Agents SDK |
| Developer Copilot | Addon codegen, PR review, migrations | GitHub Copilot SDK |

Each surface has its own persona, tools, and guardrails. They share the orchestration runtime and Odoo gateway.

### 6. Gateway as Sole Action Layer

The Odoo Agent Gateway is the only interface between the agent runtime and Odoo. Direct XML-RPC/JSON-RPC calls from agent code are prohibited. The gateway provides:

- Versioned tool contracts
- Input validation and sanitization
- Rate limiting and tenant scoping
- Audit logging for every operation

### 7. 80/15/5 Module Rule

Following the existing Odoo strategy:

- 80% native Odoo 18 CE functionality
- 15% OCA community modules
- 5% custom `ipai_*` modules

Agent gateway addons follow this same discipline.

### 8. Minimal Custom Surface Area

Do not build what Odoo or Microsoft already provides. Extend only where the gap between systems creates user friction.

### 9. Progressive Capability Expansion

Ship capabilities in this order:

1. Read-only queries and retrieval
2. Draft creation with human confirmation
3. Gated write operations
4. Multi-step cross-system workflows
5. Autonomous workflow execution (with guardrails)

### 10. Observable and Debuggable

Every agent interaction produces:

- Trace ID linking request to tool calls to responses
- Latency and token usage metrics
- Tool success/failure rates
- User satisfaction signals

## Non-Goals

- Replacing Odoo's native UI for standard operations
- Autonomous writes without human confirmation (Phase 1)
- Supporting Odoo versions other than 18.0 CE
- Building a general-purpose chatbot unrelated to Odoo/M365 workflows
- Exposing raw database access through the agent layer

## Compliance

- All PH-specific tax, BIR, and statutory compliance remains in Odoo modules
- Agent actions respect company/entity scoping
- PII handling follows data residency requirements
- Audit logs are immutable and retained per policy
