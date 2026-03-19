# Odoo Copilot — Task Sequence

> Phased delivery plan from MVP to full platform.

## Phase 1 — Finance Copilot MVP

Target: Narrow, high-value, de-risking first delivery.

### 1.1 Odoo Agent Gateway Foundation

- [ ] Create `ipai_agent_gateway` Odoo addon with base controller structure
- [ ] Implement authentication middleware (API key + session delegation)
- [ ] Implement company/tenant scoping on all endpoints
- [ ] Implement audit logging for all gateway operations
- [ ] Create base tool response schema (data, metadata, citations)
- [ ] Write gateway integration tests

### 1.2 Finance Read Tools

- [ ] `odoo.search_partners` — search customers/vendors
- [ ] `odoo.get_invoices` — fetch invoices with filters (status, date, amount, customer)
- [ ] `odoo.get_bills` — fetch vendor bills with filters
- [ ] `odoo.get_overdue_summary` — overdue analysis by customer/vendor
- [ ] `odoo.get_payment_status` — payment status for invoices/bills
- [ ] `odoo.get_record_history` — chatter/log retrieval
- [ ] `odoo.get_user_context` — user permissions and company context
- [ ] Write tool-level unit tests for each read tool

### 1.3 Agent Runtime Bootstrap

- [ ] Set up Agent Framework project structure
- [ ] Implement Router Agent with intent classification
- [ ] Implement Business Domain Agent (finance scope)
- [ ] Implement prompt assembly with user/company context
- [ ] Implement session state management
- [ ] Implement tool registry with Odoo gateway tools
- [ ] Write agent integration tests

### 1.4 Teams Channel MVP

- [ ] Set up M365 Agents SDK project
- [ ] Implement Teams bot adapter
- [ ] Implement Azure AD authentication flow
- [ ] Implement adaptive card rendering for invoice/bill data
- [ ] Implement deep-link generation to Odoo records
- [ ] Deploy to Azure Container Apps (staging)
- [ ] Write end-to-end tests

### 1.5 Finance Write Tools (Gated)

- [ ] `odoo.create_draft_invoice` — create invoice in draft state
- [ ] `odoo.create_activity` — schedule follow-up activity
- [ ] `odoo.post_message` — post to record chatter
- [ ] `odoo.create_followup` — create follow-up action
- [ ] Implement dry-run preview for all write tools
- [ ] Implement permission check before write execution
- [ ] Write write-tool integration tests with rollback

---

## Phase 2 — Knowledge Layer (Kapa-like)

Target: Grounded retrieval with citations.

### 2.1 Indexing Pipeline

- [ ] Set up Azure AI Search instance with hybrid index
- [ ] Build Odoo docs indexer (module help, field descriptions)
- [ ] Build SOP/runbook indexer (markdown/HTML sources)
- [ ] Build implementation notes indexer
- [ ] Build helpdesk resolution indexer
- [ ] Implement incremental indexing scheduler
- [ ] Implement freshness metadata on all indexed documents

### 2.2 Knowledge Agent

- [ ] Implement Knowledge Agent in Agent Framework
- [ ] Implement hybrid search (vector + keyword) retrieval
- [ ] Implement semantic reranking
- [ ] Implement citation extraction and formatting
- [ ] Implement confidence scoring (high/medium/low)
- [ ] Implement escalation routing for low-confidence answers
- [ ] Write retrieval quality evaluation tests

### 2.3 Knowledge Tools

- [ ] `odoo.search_docs` — search module documentation
- [ ] `odoo.get_model_help` — model/field descriptions
- [ ] `odoo.search_sops` — search SOPs and policies
- [ ] `odoo.get_implementation_notes` — implementation-specific docs
- [ ] Implement source citation in all knowledge tool responses

### 2.4 Troubleshooting Capability

- [ ] Implement traceback analysis tool
- [ ] Implement workflow failure diagnosis
- [ ] Implement module/field/view identification
- [ ] Implement resolution suggestion with evidence
- [ ] Write troubleshooting accuracy tests

---

## Phase 3 — Workflow Layer (Joule-like)

Target: Cross-system multi-step workflows.

### 3.1 Workflow Agent

- [ ] Implement Workflow Agent in Agent Framework
- [ ] Implement multi-step workflow engine
- [ ] Implement approval gate integration
- [ ] Implement workflow state persistence
- [ ] Implement workflow resume after approval

### 3.2 Microsoft Graph Integration

- [ ] Implement Outlook email draft creation
- [ ] Implement Teams notification sending
- [ ] Implement Calendar event creation
- [ ] Implement OneDrive/SharePoint document access
- [ ] Write Graph API integration tests

### 3.3 Cross-System Workflows

- [ ] Invoice follow-up workflow (detect → summarize → email → task → notify)
- [ ] Vendor onboarding workflow (create → verify → notify → task)
- [ ] Expense approval workflow (submit → route → approve → notify)
- [ ] Project status rollup workflow (gather → summarize → distribute)
- [ ] Write workflow end-to-end tests

### 3.4 M365 Copilot Integration

- [ ] Register as M365 Copilot custom engine agent
- [ ] Implement connector for enterprise search grounding
- [ ] Implement declarative agent shell for simple queries
- [ ] Write M365 Copilot integration tests

### 3.5 Expanded Domain Coverage

- [ ] CRM tools (opportunities, pipeline, activities)
- [ ] Project tools (tasks, timesheets, milestones)
- [ ] Inventory tools (stock levels, moves, transfers)
- [ ] HR tools (leaves, headcount, policies) — if applicable

---

## Phase 4 — Developer Copilot

Target: Repo-aware Odoo development assistant.

### 4.1 Developer Agent

- [ ] Implement Developer Agent in Agent Framework
- [ ] Implement addon-aware repo reasoning (manifest, models, views, security)
- [ ] Implement ORM/domain pattern library
- [ ] Implement XML/QWeb view generation
- [ ] Implement access rule generation
- [ ] Write codegen quality tests

### 4.2 GitHub Copilot SDK Integration

- [ ] Set up GitHub Copilot SDK project
- [ ] Register as Copilot extension
- [ ] Implement IDE chat integration
- [ ] Implement CLI command integration
- [ ] Write SDK integration tests

### 4.3 PR Review Capabilities

- [ ] Implement PR summarization
- [ ] Implement risky delta detection (models, views, security, data)
- [ ] Implement migration script proposals
- [ ] Implement manifest/dependency validation
- [ ] Implement upgrade-safe pattern enforcement
- [ ] Write review accuracy tests

### 4.4 Migration Assistance

- [ ] Implement version migration helper
- [ ] Implement deprecated API detector
- [ ] Implement view architecture modernizer (list/tree)
- [ ] Implement test generation from model definitions
- [ ] Write migration correctness tests

---

## Phase 5 — Hardening and Scale

Target: Production-grade reliability and governance.

### 5.1 Observability

- [ ] Implement OpenTelemetry tracing across all agents
- [ ] Implement Azure Application Insights integration
- [ ] Build monitoring dashboards (latency, errors, usage)
- [ ] Implement alerting (error rates, latency, tool failures)
- [ ] Implement user satisfaction tracking

### 5.2 Security Hardening

- [ ] Implement API rate limiting
- [ ] Implement input sanitization on all tools
- [ ] Security audit of gateway endpoints
- [ ] Penetration testing of agent runtime
- [ ] Implement secret rotation automation

### 5.3 Performance

- [ ] Implement response caching for frequent queries
- [ ] Optimize search index for latency
- [ ] Implement connection pooling for Odoo gateway
- [ ] Load testing at target scale
- [ ] Implement graceful degradation under load

### 5.4 Multi-Company Support

- [ ] Validate tenant isolation across all tools
- [ ] Implement company switching in session
- [ ] Test cross-company permission boundaries
- [ ] Implement per-company policy configuration
