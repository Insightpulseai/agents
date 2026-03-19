# Odoo Copilot — Architecture Plan

> Four-plane architecture: Experience, Orchestration, Action, Knowledge.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      EXPERIENCE PLANE                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ M365     │  │ Teams    │  │ Odoo Web │  │ GitHub   │       │
│  │ Copilot  │  │ Bot      │  │ Widget   │  │ Copilot  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │              │              │              │             │
│  M365 Agents SDK     │         REST API    GitHub Copilot SDK   │
└───────┼──────────────┼──────────────┼──────────────┼────────────┘
        │              │              │              │
┌───────▼──────────────▼──────────────▼──────────────▼────────────┐
│                    ORCHESTRATION PLANE                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Microsoft Agent Framework                   │    │
│  │  ┌────────────┐                                         │    │
│  │  │ Router     │ ── classify intent ──► agent selection   │    │
│  │  │ Agent      │                                         │    │
│  │  └──┬───┬───┬─┘                                         │    │
│  │     │   │   │                                           │    │
│  │  ┌──▼┐ ┌▼──┐ ┌▼───────┐ ┌──────────┐                   │    │
│  │  │Biz│ │KB │ │Workflow│ │Developer │                   │    │
│  │  │   │ │   │ │        │ │          │                   │    │
│  │  └─┬─┘ └─┬─┘ └──┬─────┘ └────┬─────┘                   │    │
│  └────┼─────┼──────┼────────────┼──────────────────────────┘    │
│       │     │      │            │                               │
│  ┌────▼─────▼──────▼────────────▼──────────────────────────┐    │
│  │  Shared Services                                        │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐         │    │
│  │  │Prompt  │ │Memory  │ │Policy  │ │Tracing   │         │    │
│  │  │Assembly│ │/State  │ │Engine  │ │/Metrics  │         │    │
│  │  └────────┘ └────────┘ └────────┘ └──────────┘         │    │
│  └─────────────────────────────────────────────────────────┘    │
└───────┼─────┼──────┼────────────┼───────────────────────────────┘
        │     │      │            │
┌───────▼─────┼──────▼────────────▼───────────────────────────────┐
│                       ACTION PLANE                              │
│  ┌──────────────────┐  ┌──────────────┐  ┌────────────────┐    │
│  │ Odoo Agent       │  │ Microsoft    │  │ GitHub API     │    │
│  │ Gateway          │  │ Graph API    │  │                │    │
│  │                  │  │              │  │ - Repos        │    │
│  │ - Read tools     │  │ - Outlook    │  │ - PRs          │    │
│  │ - Write tools    │  │ - Calendar   │  │ - Issues       │    │
│  │ - Knowledge tools│  │ - OneDrive   │  │ - Actions      │    │
│  │ - Policy tools   │  │ - Teams msgs │  │ - Code search  │    │
│  └──────────────────┘  └──────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
        │
┌───────▼─────────────────────────────────────────────────────────┐
│                      KNOWLEDGE PLANE                            │
│  ┌──────────────────┐  ┌──────────────┐  ┌────────────────┐    │
│  │ Azure AI Search  │  │ Odoo Record  │  │ M365 Content   │    │
│  │                  │  │ Index        │  │ Index          │    │
│  │ - Hybrid search  │  │              │  │                │    │
│  │ - Vector index   │  │ - Partners   │  │ - SharePoint   │    │
│  │ - Semantic rank  │  │ - Invoices   │  │ - OneDrive     │    │
│  └──────────────────┘  │ - Projects   │  │ - Teams files  │    │
│                        └──────────────┘  └────────────────┘    │
│  ┌──────────────────┐  ┌──────────────┐                        │
│  │ Doc Corpus       │  │ Repo Docs    │                        │
│  │                  │  │              │                        │
│  │ - Odoo docs      │  │ - READMEs    │                        │
│  │ - SOPs           │  │ - Specs      │                        │
│  │ - Runbooks       │  │ - PRDs       │                        │
│  │ - Release notes  │  │ - ADRs       │                        │
│  └──────────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

## Channel Adapters

### Microsoft 365 Custom Engine Agent

- Deployed via Microsoft 365 Agents SDK
- Registered as a custom engine agent in M365 Copilot
- Handles authentication via Azure AD / Entra ID
- Routes requests to the Agent Framework orchestrator
- Returns adaptive cards, text responses, and deep links

### Teams Bot

- Bot Framework adapter within M365 Agents SDK
- Supports conversational and command-based interactions
- Proactive notifications for workflow completions
- Adaptive card rendering for structured data

### Odoo Web Widget

- REST API adapter hosted alongside agent runtime
- Authenticated via Odoo session tokens
- Context-aware: passes current module, view, record ID
- Returns structured responses with deep links

### GitHub Copilot Agent

- Built on GitHub Copilot SDK (technical preview)
- Registered as a Copilot extension
- Operates in IDE chat, CLI, and PR review contexts
- Scoped to Odoo addon development patterns

## Orchestration Runtime

### Microsoft Agent Framework

Core orchestration layer providing:

- **Agent registry**: router, business, knowledge, workflow, developer
- **Tool registry**: typed tool definitions with schemas
- **Memory/state**: per-user, per-session, per-project context
- **Policy engine**: permission checks, approval gates, scope enforcement
- **Prompt assembly**: context-aware prompt construction with grounding

### Agent Topology

| Agent | Responsibility | Tools |
|-------|---------------|-------|
| Router Agent | Intent classification, agent selection, fallback | All agents |
| Business Domain Agent | ERP/CRM/finance/project queries and actions | Odoo read/write tools |
| Knowledge Agent | Retrieval, citations, troubleshooting | Search, doc retrieval |
| Workflow Agent | Multi-step processes, approvals, cross-system | All action tools |
| Developer Agent | Code generation, review, migration | GitHub API, repo tools |

### Routing Logic

```
User message
  │
  ├─ Intent: query about Odoo data ──► Business Domain Agent
  ├─ Intent: documentation/help/how-to ──► Knowledge Agent
  ├─ Intent: multi-step process ──► Workflow Agent
  ├─ Intent: code/addon/PR question ──► Developer Agent
  └─ Intent: unclear ──► Clarification prompt
```

## Odoo Agent Gateway

### Design Principles

- **Facade pattern**: stable API contract independent of Odoo internals
- **Versioned**: `/api/v1/` prefix for all endpoints
- **Tenant-scoped**: company_id enforced on every request
- **Audit-logged**: every call recorded with trace context

### Transport

Primary: Dedicated Odoo HTTP controllers (preferred)
Fallback: JSON-RPC where legacy compatibility is needed

### Tool Categories

#### Read Tools
| Tool | Description |
|------|-------------|
| `odoo.search_partners` | Search customers/vendors by criteria |
| `odoo.get_invoices` | Fetch invoices with filters |
| `odoo.get_bills` | Fetch vendor bills with filters |
| `odoo.get_sales_orders` | Fetch sales orders |
| `odoo.get_purchase_orders` | Fetch purchase orders |
| `odoo.get_projects` | Fetch projects and tasks |
| `odoo.get_stock_moves` | Fetch inventory movements |
| `odoo.get_kpi_summary` | Fetch module-level KPI dashboard |
| `odoo.get_record_history` | Fetch chatter/log for a record |
| `odoo.get_user_context` | Fetch current user permissions and company |

#### Write Tools
| Tool | Description |
|------|-------------|
| `odoo.create_draft_invoice` | Create invoice in draft state |
| `odoo.create_draft_bill` | Create vendor bill in draft state |
| `odoo.create_task` | Create project task |
| `odoo.create_activity` | Schedule activity on any record |
| `odoo.post_message` | Post to record chatter |
| `odoo.create_followup` | Create follow-up action |
| `odoo.update_record` | Update safe fields on existing record |

#### Knowledge Tools
| Tool | Description |
|------|-------------|
| `odoo.search_docs` | Search module documentation |
| `odoo.get_model_help` | Get model/field descriptions |
| `odoo.search_sops` | Search SOPs and policies |
| `odoo.get_implementation_notes` | Get implementation-specific docs |

#### Policy Tools
| Tool | Description |
|------|-------------|
| `odoo.check_permission` | Verify user can perform action |
| `odoo.dry_run` | Preview action without executing |
| `odoo.get_approval_requirements` | Check if action needs approval |
| `odoo.log_audit_event` | Record action in audit trail |

## Knowledge Plane

### Indexing Pipeline

```
Sources                    Indexer              Search Index
┌────────────────┐    ┌──────────────┐    ┌──────────────────┐
│ Odoo records   │───►│              │───►│ Azure AI Search  │
│ Odoo docs      │    │  Incremental │    │                  │
│ SOPs/runbooks  │    │  indexer     │    │ - Vector index   │
│ M365 content   │    │  (scheduled) │    │ - Keyword index  │
│ Repo docs      │    │              │    │ - Semantic ranker │
│ Support tickets│    └──────────────┘    └──────────────────┘
└────────────────┘
```

### Retrieval Strategy

1. **Hybrid search**: combine vector similarity + keyword matching
2. **Semantic reranking**: Azure AI Search semantic ranker
3. **Source filtering**: scope to relevant document types
4. **Freshness weighting**: prefer recent documents
5. **Citation extraction**: return source + section + date

## Memory and State

### Session State
- Current conversation context
- Referenced entities (partners, invoices, etc.)
- Pending actions and confirmations

### User State
- Preferred company/entity
- Recent queries and entities
- Notification preferences

### Project State
- Active projects and their context
- Unresolved tasks and follow-ups
- Decision history

### Storage
- Azure Database for PostgreSQL (via Supabase)
- Session TTL: 24 hours
- User state TTL: 30 days
- Project state: persistent

## Observability

### Tracing
- Distributed trace ID on every request
- Spans for: channel adapter → router → agent → tool → response
- OpenTelemetry-compatible export

### Metrics
- Request latency (p50, p95, p99)
- Token usage per agent and tool
- Tool success/failure rates
- User satisfaction (thumbs up/down)

### Logging
- Structured JSON logs
- Audit trail for all write operations
- Error correlation via trace ID

### Platform
- Azure Application Insights
- Azure Monitor dashboards
- Alerting on error rate spikes and latency degradation

## Deployment Topology

### Azure Services

| Service | Purpose |
|---------|---------|
| Azure Container Apps | Agent runtime, gateway proxy |
| Azure AI Search | Hybrid/vector retrieval |
| Azure OpenAI | Model serving (GPT-4o, embeddings) |
| Azure Database for PostgreSQL | State, memory, audit |
| Azure Blob Storage | Document corpus, artifacts |
| Azure Service Bus | Async tool workflows |
| Azure Key Vault | Secrets management |
| Azure Application Insights | Observability |

### Odoo Deployment

- Odoo 18 CE on existing infrastructure
- Gateway addons installed as standard Odoo modules
- HTTP controller endpoints exposed via reverse proxy
- Authentication via API keys + Odoo session delegation

### Network

```
Internet
  │
  ├── Azure Front Door / App Gateway
  │     │
  │     ├── Agent Runtime (Container Apps)
  │     │     ├── Router Agent
  │     │     ├── Business Agent
  │     │     ├── Knowledge Agent
  │     │     ├── Workflow Agent
  │     │     └── Developer Agent
  │     │
  │     ├── Channel Adapters (Container Apps)
  │     │     ├── M365 Agent Adapter
  │     │     ├── Web API Adapter
  │     │     └── GitHub Adapter
  │     │
  │     └── Search Service (Azure AI Search)
  │
  ├── Odoo Instance (private network)
  │     └── Agent Gateway Controllers
  │
  └── GitHub (external)
        └── Copilot SDK webhook
```
