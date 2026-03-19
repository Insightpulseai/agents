# Microsoft Foundry — Deep Research (March 2026)

> **Formerly:** Azure AI Studio → Azure AI Foundry → Microsoft Foundry
> **Current Portal:** [foundry.ai.azure.com](https://foundry.ai.azure.com)
> **Azure Resource Provider:** `Microsoft.CognitiveServices/accounts`

---

## 1. What Is Microsoft Foundry?

Microsoft Foundry is Azure's unified platform-as-a-service for building, deploying, and operating enterprise AI applications and agents. It consolidates model hosting, agent orchestration, evaluation, observability, and governance into a single control plane.

### Branding Timeline

| Date | Name | Portal |
|------|------|--------|
| Nov 2023 | Azure AI Studio (Public Preview) | ai.azure.com |
| Nov 2024 (Ignite) | Azure AI Foundry | ai.azure.com |
| Nov 2025 (Ignite) | **Microsoft Foundry** | foundry.ai.azure.com |

The rebrand is not cosmetic — each iteration added new resource types, SDK surfaces, and agent capabilities.

---

## 2. Architecture

### 2.1 Three-Tier Resource Hierarchy

```
┌──────────────────────────────────────────────┐
│  Foundry Resource  (Microsoft.CognitiveServices/accounts)  │
│  ├── Governance: networking, RBAC, policies  │
│  ├── Model deployments (shared across projects) │
│  │                                              │
│  ├── Project A                                  │
│  │   └── Agents, evaluations, files, indexes   │
│  ├── Project B                                  │
│  │   └── ...                                    │
│  └── Project C                                  │
└──────────────────────────────────────────────┘
```

1. **Foundry Resource** — Top-level Azure resource. Governance boundary for networking, security, model deployments, and policy.
2. **Project** — Development boundary. Teams build and evaluate use cases within projects.
3. **Project Assets** — Files, agents, evaluations, search indexes, and artifacts scoped to a project.

### 2.2 Shared Provider Namespace

Foundry resources share the `Microsoft.CognitiveServices` provider namespace with Azure OpenAI, Azure Speech, Azure Vision, and Azure Language. This unifies management APIs, access control, networking, and policy behavior.

### 2.3 Old vs. New Resource Types

| Attribute | Classic (Hub-based) | New (Foundry) |
|-----------|-------------------|---------------|
| Resource Provider | `Microsoft.MachineLearningServices/workspaces` | `Microsoft.CognitiveServices/accounts` |
| Structure | Hub → Hub-based Projects | Foundry Resource → Foundry Projects |
| Investment focus | Legacy / maintenance | Active development |
| Agent Service | Limited | Full GA support |

Going forward, new capabilities for Agents and Models are focused on the new Foundry Projects.

---

## 3. Foundry Agent Service (GA — March 2026)

### 3.1 Overview

Foundry Agent Service enables developers to build, deploy, and scale AI agents natively in Foundry. Agents reason, plan, and act across tools, data, and workflows with enterprise-grade identity, observability, governance, and autoscaling.

### 3.2 Key Capabilities

- **Multi-agent orchestration** — Build collaborative agent workflows using SDKs for Python, C#, JS/TS, and Java.
- **Tool Catalog** — 1,400+ tools through public and private catalogs.
- **Memory** (Public Preview) — Managed long-term memory store with automatic extraction, consolidation, and retrieval across sessions.
- **Voice Live** — Real-time voice interaction for agents.
- **Hosted Agents** — Deploy custom-code agents (Microsoft Agent Framework, LangGraph, CrewAI, open-source) into a fully managed runtime — no containers, K8s, or deployment pipelines required.

### 3.3 Open Protocol Support

#### MCP (Model Context Protocol)
- Agents can call MCP-compatible tools directly.
- Cloud-hosted MCP server at `mcp.ai.azure.com` (live since Dec 2025).
- Auth methods: Key-based, Entra Agent Identity, Managed Identity, OAuth Identity Passthrough.
- Logic Apps supports MCP — existing workflows/connectors work inside Foundry agents.
- Each tool requires a unique `server_label` and `server_url`.

#### A2A (Agent-to-Agent Protocol)
- Standardized agent-to-agent communication across runtimes and ecosystems.
- **A2A Tool**: Agent A calls Agent B → B's answer returns to A → A summarizes for user. A keeps control.
- **Multi-agent workflow**: Agent A delegates to Agent B → B takes full responsibility.
- Implemented through Semantic Kernel.
- Available via Python, C#, TypeScript, and REST API.

#### MCP vs. A2A

| Protocol | Purpose | Analogy |
|----------|---------|---------|
| MCP | Agent-to-tool access | "What tools can I use?" |
| A2A | Agent-to-agent coordination | "Let me ask another agent" |

They are complementary, not competing.

---

## 4. Foundry Models

### 4.1 Model Catalog

Over **11,000 pre-trained models** spanning:
- Language understanding & generation
- Image generation
- Code completion
- Embeddings
- Speech processing
- Reasoning
- Multimodal
- Industry / domain-specific

Both proprietary and open-source options available.

### 4.2 Notable Models (as of March 2026)

| Model | Provider | Status | Notes |
|-------|----------|--------|-------|
| GPT-5.2 | OpenAI | GA | Multi-step reasoning, agentic tool-calling |
| GPT-5-Codex | OpenAI | GA | Multimodal code reasoning, repo awareness |
| Claude Opus 4.6 | Anthropic | GA | 1M-token context (beta), adaptive thinking |
| Claude Sonnet 4.6 | Anthropic | GA | 1M-token context (beta) |
| Grok 4.0 | xAI | GA | Reasoning model |
| Grok 4.1 Fast | xAI | Preview | $0.20/M input tokens |
| DeepSeek V3.2 | DeepSeek | Preview | 128K context window |
| Mistral Large 3 | Mistral | Preview | 41B active / 675B total (MoE) |
| Llama (various) | Meta | GA | Multiple sizes |
| FLUX | Black Forest Labs | GA | Image generation |

### 4.3 Deployment Options

- **Pay-as-you-go** — Per-token billing, no commitment.
- **Provisioned Throughput** — Reserved capacity with guaranteed throughput. Can flex capacity across multiple models.
- **Serverless API** — Models-as-a-Service with no infrastructure to manage.

---

## 5. SDKs & APIs

### 5.1 REST API (GA)

Core GA endpoints:
- Chat completions
- Responses
- Embeddings
- Files
- Fine-tuning
- Models
- Vector stores

GA SLAs apply.

### 5.2 SDK Consolidation

All development is consolidating into a single `azure-ai-projects` package per language.

| Language | Package | Latest Version (Mar 2026) |
|----------|---------|--------------------------|
| Python | `azure-ai-projects` | 2.0.0b4 |
| .NET | `Azure.AI.Projects` | 2.0.0-beta.1 |
| JS/TS | `@azure/ai-projects` | 2.0.0-beta.4 |
| Java | `azure-ai-projects` | 2.0.0-beta.1 |

Agents, inference, evaluations, and memory operations that previously lived in separate packages are being unified. SDK GA announcements are imminent.

### 5.3 Breaking Changes in 2.0

- Tool class renames
- Credential updates
- Preview feature opt-in flags
- Built on top of the GA REST surface

---

## 6. Observability (GA — March 2026)

### 6.1 Three Pillars

1. **Evaluations** — Out-of-the-box evaluators for coherence, relevance, groundedness, retrieval quality, safety. Custom evaluators (LLM-as-a-judge, code-based) in preview.
2. **Tracing** — Distributed tracing capturing LLM calls, tool invocations, agent decisions, inter-service dependencies. Built on OpenTelemetry, integrated with Application Insights.
3. **Monitoring** — Continuous evaluation samples live traffic, runs evaluator suites, surfaces results in dashboards. Azure Monitor alerts for quality/safety threshold breaches.

### 6.2 Framework Auto-Instrumentation

- Semantic Kernel
- LangChain
- LangGraph
- OpenAI Agents SDK

### 6.3 Azure Monitor Integration

- Cross-stack correlation (AI quality + infrastructure telemetry in one workspace)
- Unified alerting (PagerDuty, Teams, automated runbooks)
- Governance (RBAC, retention policies, diagnostic settings, audit logging)
- Agent Monitoring Dashboard in Foundry portal
- Can onboard external agents (non-Foundry) via AI Gateway

### 6.4 OpenTelemetry Semantic Conventions

Microsoft is contributing new multi-agent observability semantic conventions to OpenTelemetry (with Outshift/Cisco), standardizing tracing for multi-agent systems.

---

## 7. Security & Governance

### 7.1 Authentication

| Method | Use Case | Features |
|--------|----------|----------|
| Microsoft Entra ID | Production | Conditional access, managed identities, granular RBAC |
| API Keys | Prototyping | Simple but no per-user traceability |

### 7.2 RBAC Model

Control plane and data plane operations are separated:

- **Control plane**: Creating deployments, projects, resource management
- **Data plane**: Building agents, running evaluations, uploading files

Key built-in roles:

| Role | Scope | Permissions |
|------|-------|-------------|
| Azure AI Owner | Resource + Project | Full control (control + data plane) |
| Azure AI Account Owner | Resource | Control plane management |
| Azure AI User | Resource/Project | Data plane operations |

RBAC assignments can be scoped at both the top-level resource and individual project level.

### 7.3 Network Isolation

- **Private Link** — PaaS resources (storage, Key Vault, container registry, monitoring) isolated via Private Link.
- **VNet Injection** — Agent client injected into customer-managed VNet subnet. All traffic stays within customer network.
- **Public Network Access (PNA)** flag — Options: disabled, enabled, enabled from selected IPs.
- **Dedicated Agent Subnet** — Each Foundry resource requires its own subnet (recommended /24). Delegated to `Microsoft.App/environments`.
- **BYO VNet** — Standard Setup with private networking, no public egress.

### 7.4 Customer-Managed Keys (CMK)

- System-assigned or user-assigned managed identity required.
- Key Vault Crypto User role assigned to managed identity.
- Encryption at rest with customer-controlled keys.

### 7.5 Regional Requirements

All Foundry workspace resources (Cosmos DB, Storage, AI Search, OpenAI, etc.) must be deployed in the same region as the VNet.

---

## 8. Pricing

### 8.1 Platform Access

The Foundry platform itself is **free to use and explore**. No Azure account needed for exploration. Azure subscription required to build agents.

### 8.2 Agent Service Pricing

- **No additional charge** for creating or running Foundry-native agents using prompts and workflows.
- Charges incurred for:
  - Model token consumption (Foundry Models)
  - Foundry Tools and Foundry IQ connections
  - Azure Logic Apps connectors
  - Microsoft Fabric
  - SharePoint
  - Grounding with Bing Search
  - Licensed data sources

### 8.3 Pre-Purchase Plan

**Agent Commit Units (ACUs)** — 1-year metered plan:
- Discounted tiers for upfront commitment
- Flexible usage across included Microsoft services (Foundry + Copilot Credit)

### 8.4 Pricing Pages

- [Microsoft Foundry Pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-foundry/)
- [Foundry Agent Service Pricing](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/)
- [Foundry Models Pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry-models/microsoft/)
- [Foundry Tools Pricing](https://azure.microsoft.com/en-us/pricing/details/foundry-tools/)

---

## 9. Integration Ecosystem

### 9.1 Connected Azure Services

- Azure OpenAI Service
- Azure AI Search
- Azure Cosmos DB
- Azure Blob Storage
- Azure Key Vault
- Azure Container Registry
- Azure Monitor / Application Insights
- Azure Logic Apps
- Microsoft Fabric
- SharePoint

### 9.2 Enterprise Connectors

Thousands of connectors into SaaS and enterprise systems:
- Dynamics 365
- ServiceNow
- Custom APIs
- Microsoft 365 / SharePoint

### 9.3 Cross-Cloud Support

Open interoperability standards (MCP, A2A) enable agents to collaborate across Azure, AWS, Google Cloud, and on-premises environments.

### 9.4 Framework Support

Agents can be built with:
- Microsoft Agent Framework
- Semantic Kernel
- LangGraph
- LangChain
- CrewAI
- OpenAI Agents SDK
- Custom open-source frameworks

---

## 10. Migration Notes

### 10.1 Azure ML SDK v1 End of Life

- **End of support:** June 30, 2026
- CLI v1 already sunset September 2025
- Migrate to SDK v2 / Foundry SDK immediately

### 10.2 Classic → New Resource Migration

Hub-based projects (classic) remain accessible for GenAI capabilities not yet supported by new resource type, but all new investment targets Foundry Projects.

---

## 11. Recent & Upcoming Developments

| Date | Milestone |
|------|-----------|
| Dec 2025 | Foundry MCP Server live at mcp.ai.azure.com |
| Jan 2026 | SDK 2.0.0b3 ships; Memory preview launches |
| Feb 2026 | Claude Opus/Sonnet 4.6, Grok 4.0 GA in Foundry |
| Mar 2026 | Agent Service GA; Observability GA; Private networking GA |
| Mar 2026 | NVIDIA GTC: Nemotron models, Vera Rubin NVL72 on Azure |
| Jun 2026 | Azure ML SDK v1 end of support |

---

## 12. Key References

- [What is Microsoft Foundry?](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)
- [Microsoft Foundry Architecture](https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture)
- [RBAC for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)
- [Authentication & Authorization](https://learn.microsoft.com/en-us/azure/foundry/concepts/authentication-authorization-foundry)
- [Network Isolation](https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link)
- [Agent Service Private Networking](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/virtual-networks)
- [MCP Server Connection](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [A2A Tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/agent-to-agent?view=foundry)
- [Agent Tools Overview](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/tool-catalog)
- [Observability GA Announcement](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/generally-available-evaluations-monitoring-and-tracing-in-microsoft-foundry/4502760)
- [Agent Service GA Blog](https://devblogs.microsoft.com/foundry/foundry-agent-service-ga/)
- [What's New — Dec 2025 / Jan 2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/)
- [What's New — Feb 2026](https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-feb-2026/)
- [NVIDIA GTC Mar 2026 Announcements](https://blogs.microsoft.com/blog/2026/03/16/microsoft-at-nvidia-gtc-new-solutions-for-microsoft-foundry-azure-ai-infrastructure-and-physical-ai/)
- [Agent Factory — MCP & A2A Blog](https://azure.microsoft.com/en-us/blog/agent-factory-connecting-agents-apps-and-data-with-new-open-standards-like-mcp-and-a2a/)
