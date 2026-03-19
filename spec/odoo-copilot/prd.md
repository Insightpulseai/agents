# Odoo Copilot — Product Requirements Document

> Three-surface copilot system: Business + Knowledge + Developer.

## Overview

Odoo Copilot is an enterprise AI assistant platform that connects Odoo 18 CE with Microsoft 365 and GitHub through a unified agent runtime. It delivers three distinct product experiences under one platform.

## User Surfaces

### 1. Microsoft 365 Copilot / Teams

- Primary channel for business users
- Custom engine agent for Odoo action-taking
- Connector/search layer for retrieval grounding
- Declarative agent shell where appropriate

### 2. Odoo Web Portal

- Embedded assistant in Odoo backoffice
- Context-aware (current module, view, record)
- Inline action suggestions and navigation

### 3. GitHub / IDE / CLI

- Developer-facing copilot for Odoo addons
- PR review, codegen, migration assistance
- Integrated through GitHub Copilot SDK

## Personas

| Persona | Surface | Key Tasks |
|---------|---------|-----------|
| Finance User | M365 + Odoo | Invoice lookup, overdue analysis, vendor follow-ups, payment status |
| HR Manager | M365 + Odoo | Leave summaries, headcount queries, policy questions |
| CRM User | M365 + Odoo | Pipeline status, opportunity summaries, customer history |
| Project Manager | M365 + Odoo | Task status, resource allocation, timeline queries |
| Executive | M365 | Cross-module KPI dashboards, trend summaries, decision support |
| Support Agent | M365 + Knowledge | Troubleshooting, SOP lookup, escalation guidance |
| Implementer | Knowledge + Dev | Module docs, configuration help, migration guidance |
| Developer | GitHub + IDE | Addon codegen, XML fixes, test generation, PR review |

## Capability Split

### Business Copilot (SAP Joule-like)

**Read capabilities:**
- Search partners, customers, vendors
- Fetch invoices, bills, sales orders, purchase orders
- Fetch project tasks, stock moves, inventory levels
- Retrieve KPI dashboards and summaries
- Access chatter/history for any record

**Write capabilities (gated):**
- Create draft invoices, bills, tasks, activities
- Post messages to chatter
- Generate draft emails via Outlook
- Create follow-up tasks
- Submit approval requests
- Trigger predefined server-side workflows

**Navigation capabilities:**
- Deep-link to specific Odoo records/views
- Suggest next-best-action based on context
- Open related records across modules

### Knowledge Copilot (Kapa-like)

**Retrieval capabilities:**
- Odoo module documentation
- Implementation notes and runbooks
- SOPs and policy documents
- Helpdesk resolution history
- Release notes and changelogs
- Customer/project-specific docs

**Answer requirements:**
- Every answer cites source document and section
- Freshness metadata on all citations
- Confidence signal (high/medium/low)
- Escalation path when confidence is low

**Troubleshooting capabilities:**
- Explain Odoo tracebacks and errors
- Diagnose workflow failures
- Identify responsible module/field/view
- Propose resolution steps with evidence

### Developer Copilot (GitHub Copilot-like)

**Code capabilities:**
- Addon scaffolding (`__manifest__.py`, models, views, security, data)
- XML view generation and fixes (list, form, kanban, search)
- ORM domain expression assistance
- Computed field and onchange patterns
- Access rule and record rule generation
- Test scaffolding and generation

**Review capabilities:**
- PR summarization
- Risky model/view/security delta detection
- Migration script proposals
- Manifest dependency validation
- Upgrade-safe pattern enforcement

**Migration capabilities:**
- Version migration assistance (field renames, API changes)
- View architecture migration (list/tree modernization)
- Deprecated API detection and replacement

## Guardrails

### Permission Model
- All operations scoped to authenticated user's Odoo permissions
- Company/entity isolation enforced at gateway level
- Sensitive operations require explicit approval

### Audit Trail
- Every tool invocation logged with: user, timestamp, tool, input, output, trace ID
- Write operations include before/after state
- Logs are immutable and queryable

### Content Safety
- No PII in logs beyond what Odoo already stores
- No training on customer data
- Model outputs filtered for harmful content

### Scope Boundaries
- Agent cannot modify Odoo system configuration
- Agent cannot create/modify users or access rights
- Agent cannot execute arbitrary Python/SQL on Odoo
- Agent cannot access modules outside user's permission scope

## Non-Goals (v1)

- Mobile-native app (use Teams mobile instead)
- Voice interface
- Autonomous multi-step workflows without confirmation
- Cross-tenant or multi-instance Odoo support
- Real-time streaming of Odoo events to agent
- Custom model fine-tuning on customer data
