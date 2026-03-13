# Odoo Copilot — Architecture Document

> Reference architecture for the three-surface Odoo Copilot platform.

## System Context

Odoo Copilot connects three ecosystems through a unified agent runtime:

| Ecosystem | Role | Integration |
|-----------|------|-------------|
| **Odoo 18 CE** | System of record, system of action | Agent Gateway (HTTP controllers) |
| **Microsoft 365** | User experience surface | M365 Agents SDK, Microsoft Graph |
| **GitHub** | Developer experience surface | GitHub Copilot SDK |

## Four-Plane Architecture

### A. Experience Plane

Where users interact with the copilot.

| Adapter | SDK | Auth | Capabilities |
|---------|-----|------|-------------|
| M365 Copilot | Microsoft 365 Agents SDK | Azure AD / Entra ID | Custom engine agent, connectors |
| Teams Bot | M365 Agents SDK (Bot Framework) | Azure AD | Conversational, adaptive cards |
| Odoo Web Widget | REST API | Odoo session token | Context-aware, inline actions |
| GitHub Copilot | GitHub Copilot SDK | GitHub OAuth | IDE chat, CLI, PR review |

### B. Orchestration Plane

Where reasoning, routing, and tool execution happen.

**Runtime:** Microsoft Agent Framework (.NET / Python)

**Agent Topology:**

```
                    ┌──────────────┐
                    │ Router Agent │
                    └──────┬───────┘
              ┌────────┬───┴───┬──────────┐
         ┌────▼───┐ ┌──▼──┐ ┌─▼──────┐ ┌─▼────────┐
         │Business│ │Know-│ │Workflow│ │Developer │
         │Domain  │ │ledge│ │        │ │          │
         └────────┘ └─────┘ └────────┘ └──────────┘
```

**Shared Services:**
- **Prompt Assembly**: User context, company context, tool results, conversation history
- **Memory/State**: Session, user, and project-level persistence (PostgreSQL)
- **Policy Engine**: Permission checks, approval gates, scope enforcement
- **Tracing**: Distributed traces via OpenTelemetry → Application Insights

### C. Action Plane

Where real work happens through typed tools.

| System | Transport | Tools |
|--------|-----------|-------|
| Odoo 18 CE | HTTP controllers (gateway) | Read, write, knowledge, policy |
| Microsoft Graph | REST API | Outlook, Calendar, OneDrive, Teams |
| GitHub | REST/GraphQL API | Repos, PRs, Issues, Actions, Code Search |

### D. Knowledge Plane

Where retrieval and grounding happen.

| Source | Index | Strategy |
|--------|-------|----------|
| Odoo records | Azure AI Search | Structured projections |
| Odoo docs | Azure AI Search | Vector + keyword hybrid |
| SOPs/runbooks | Azure AI Search | Vector + keyword hybrid |
| M365 content | Microsoft Graph + Search | Connector-based |
| Repo docs | Azure AI Search | Vector + keyword hybrid |

## Service Contracts

### Agent Runtime ↔ Odoo Gateway

```
Protocol: HTTPS (TLS 1.3)
Auth: API key (X-Agent-Api-Key header) + user context (X-Odoo-User-Id, X-Odoo-Company-Id)
Format: JSON
Base URL: https://{odoo-host}/api/agent/v1/
Rate limit: 100 req/s per agent instance
Timeout: 30s default, 60s for write operations
```

### Agent Runtime ↔ Microsoft Graph

```
Protocol: HTTPS
Auth: OAuth 2.0 (on-behalf-of flow via Azure AD)
Format: JSON
Base URL: https://graph.microsoft.com/v1.0/
Scopes: Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite, Chat.ReadWrite
```

### Agent Runtime ↔ Azure AI Search

```
Protocol: HTTPS
Auth: API key (api-key header)
Format: JSON
Base URL: https://{search-service}.search.windows.net/
Indexes: odoo-records, odoo-docs, sops-runbooks, support-resolutions
```

### Channel Adapters ↔ Agent Runtime

```
Protocol: gRPC (internal) or HTTPS (external)
Auth: mTLS (internal) or Azure AD token (external)
Format: Protobuf (gRPC) or JSON (HTTPS)
```

## Data Flow: Finance Query Example

```
1. User in Teams: "Show overdue invoices for top 10 customers"
2. Teams Bot adapter receives message
3. Router Agent classifies intent → Business Domain Agent
4. Business Domain Agent assembles prompt with user context
5. Agent calls odoo.get_user_context → verifies finance read permission
6. Agent calls odoo.get_overdue_summary(limit=10, group_by=customer)
7. Gateway queries Odoo account.move with domain filters
8. Gateway returns structured result with metadata
9. Agent formats response with adaptive card
10. Teams Bot adapter renders card with deep links to Odoo
11. Audit trail recorded: user, query, tools used, response time
```

## Data Flow: Cross-System Workflow Example

```
1. User in Teams: "Follow up on invoice INV-2024-0142"
2. Router Agent → Workflow Agent (multi-step intent)
3. Workflow Agent executes:
   a. odoo.get_invoices(number="INV-2024-0142") → fetch invoice details
   b. odoo.get_record_history(model="account.move", id=142) → fetch history
   c. odoo.search_partners(id=invoice.partner_id) → fetch customer details
   d. Assemble follow-up email draft
   e. graph.create_draft_email(to=customer.email, subject=..., body=...)
   f. odoo.create_activity(model="account.move", id=142, type="email", note="Follow-up sent")
   g. graph.send_teams_notification(user=invoice.user_id, message="Follow-up drafted for INV-2024-0142")
4. Each step: permission check → dry-run preview → execute → audit log
5. User confirms email send → Workflow Agent completes
```

## Security Model

### Authentication Chain

```
User → Azure AD → Channel Adapter → Agent Runtime → Gateway → Odoo
         │                                    │
         └── OAuth token ────────────────────►│
                                              └── Odoo user mapping
```

### Authorization Layers

| Layer | Enforcement |
|-------|-------------|
| Channel | Azure AD roles/groups |
| Agent Runtime | Policy engine (tool-level permissions) |
| Gateway | Odoo RBAC (user permissions, record rules) |
| Odoo | Native access controls and record rules |

### Data Protection

- No PII stored in agent runtime beyond session scope
- All gateway requests over TLS
- API keys rotated via Azure Key Vault
- Audit logs encrypted at rest
- No customer data used for model training
