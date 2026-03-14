# Azure-Native Platform Map — Odoo Copilot

> Canonical current-to-target placement for all Azure resources backing the
> InsightPulse AI Odoo Copilot platform.

## 1. Edge and Routing

```
Cloudflare (DNS authority)
  └─► Azure Front Door (ipai-fd-dev)
        ├─► WAF (ipaiDevWafPolicy)
        └─► Azure API Management (apim-ipai-dev)   ◄── NEW
              └─► Container App backends
```

| Layer                 | Current              | Target                    | Action |
|-----------------------|----------------------|---------------------------|--------|
| DNS authority         | Cloudflare           | Cloudflare                | Keep   |
| Public edge           | ipai-fd-dev          | ipai-fd-dev               | Keep   |
| WAF                   | ipaiDevWafPolicy     | ipaiDevWafPolicy          | Keep   |
| Unified API gateway   | **missing**          | Azure API Management      | **Add** |
| Public API hostname   | **missing**          | api.insightpulseai.com    | **Add DNS + Front Door route** |

## 2. Backend Services

All sit behind APIM — never exposed directly as the unified API.

| Service role      | Azure resource           | Public exposure                          |
|-------------------|--------------------------|------------------------------------------|
| Odoo app          | ipai-odoo-dev-web        | erp.insightpulseai.com + `/api/odoo/*`   |
| Odoo worker       | ipai-odoo-dev-worker     | internal only                            |
| Odoo cron         | ipai-odoo-dev-cron       | internal only                            |
| Odoo install job  | ipai-odoo-install        | internal only                            |
| Odoo wave job     | ipai-odoo-dev-wave1      | internal only                            |
| Auth service      | ipai-auth-dev            | auth.insightpulseai.com + `/api/auth/*`  |
| CRM service       | ipai-crm-dev             | crm.insightpulseai.com + `/api/crm/*`    |
| MCP / agent       | ipai-mcp-dev             | mcp.insightpulseai.com + `/api/agents/*` |
| OCR service       | ipai-ocr-dev             | ocr.insightpulseai.com + `/api/ocr/*`    |
| Plane             | ipai-plane-dev           | plane.insightpulseai.com (direct)        |
| Shelf             | ipai-shelf-dev           | shelf.insightpulseai.com                 |
| Superset          | ipai-superset-dev        | superset.insightpulseai.com              |
| Website           | ipai-website-dev         | www.insightpulseai.com / apex            |

## 3. Container Environments

| Resource             | Purpose                     | Action |
|----------------------|-----------------------------|--------|
| ipai-odoo-dev-env    | Odoo-focused Container Apps | Keep   |
| cae-ipai-dev         | Shared / non-Odoo services  | Keep   |
| capp-svc-lb          | Supporting load balancer     | Keep   |

## 4. AI and Knowledge Layer

| Capability            | Resource                    | Target use                            |
|-----------------------|-----------------------------|---------------------------------------|
| Foundry resource      | data-intel-ph-resource      | Canonical Foundry account/resource    |
| Foundry project       | data-intel-ph               | Project endpoint for agent/project APIs |
| AI hub                | aifoundry-ipai-dev          | Model/ops flow                        |
| Document Intelligence | docai-ipai-dev              | OCR/document extraction backend       |
| Language              | lang-ipai-dev               | Language AI service                   |
| Databricks            | dbw-ipai-dev                | Analytics/intelligence layer          |
| Search                | srch-ipai-dev               | Knowledge layer behind agent/OCR      |

### Canonical Foundry Endpoints

```
Foundry Resource:  https://data-intel-ph-resource.services.ai.azure.com/
Foundry Project:   https://data-intel-ph-resource.services.ai.azure.com/api/projects/data-intel-ph
Azure OpenAI:      https://data-intel-ph-resource.openai.azure.com/
```

## 5. Data, Secrets, and Identity

| Capability         | Resource(s)                | Target                          |
|--------------------|----------------------------|---------------------------------|
| Shared dev KV      | kv-ipai-dev                | Primary shared dev secret store |
| Odoo dev KV        | ipai-odoo-dev-kv           | Odoo-specific secrets           |
| Prod/staging KV    | kv-ipai-prod, kv-ipai-staging | Keep                         |
| Odoo MI            | mi-ipai-odoo-dev           | Canonical Odoo workload identity |
| Platform MI        | mi-ipai-platform-dev       | Gateway/platform identity       |
| ACA MI             | id-ipai-aca-dev            | Container Apps workload identity |
| Agent MI           | id-ipai-agents-dev         | Agent-runtime identity          |
| Lakehouse MI       | smi-ipai-lakehouse-*       | Analytics layer                 |

**Canonical rules:**
- Prefer Managed Identity over keys
- Use Key Vault for remaining secrets
- Never let app code depend on raw `.env` secrets in tracked files

## 6. Database Layer

| Resource            | Type                              | Target                    |
|---------------------|-----------------------------------|---------------------------|
| ipai-odoo-dev-pg    | Azure PostgreSQL Flexible Server  | Canonical Odoo dev DB     |

## 7. Registries and Build

| Resource                    | Target                                    |
|-----------------------------|-------------------------------------------|
| cripaidev                   | Shared ACR — keep for platform builds     |
| ipaiodoodevacr              | Odoo dev ACR — keep for repo separation   |
| ipai-build-pool             | Managed DevOps Pool — CI/CD capacity      |
| ipai-devcenter              | Azure Dev Center — dev infra standard     |
| ipai-devcenter-project      | Dev Center project                        |

## 8. Canonical Hostname Map

| Hostname                        | Target backend                         |
|---------------------------------|----------------------------------------|
| api.insightpulseai.com          | Front Door → APIM                      |
| erp.insightpulseai.com          | Front Door → ipai-odoo-dev-web         |
| auth.insightpulseai.com         | Front Door → ipai-auth-dev             |
| crm.insightpulseai.com          | Front Door → ipai-crm-dev              |
| mcp.insightpulseai.com          | Front Door → ipai-mcp-dev              |
| ocr.insightpulseai.com          | Front Door → ipai-ocr-dev              |
| plane.insightpulseai.com        | Front Door → ipai-plane-dev            |
| shelf.insightpulseai.com        | Front Door → ipai-shelf-dev            |
| superset.insightpulseai.com     | Front Door → ipai-superset-dev         |
| www.insightpulseai.com          | Front Door → ipai-website-dev          |

## 9. Canonical API Path Map (behind APIM)

| Path             | Backend              |
|------------------|----------------------|
| `/api/odoo/*`    | ipai-odoo-dev-web    |
| `/api/auth/*`    | ipai-auth-dev        |
| `/api/crm/*`     | ipai-crm-dev         |
| `/api/agents/*`  | ipai-mcp-dev         |
| `/api/ocr/*`     | ipai-ocr-dev         |

**Future paths:**

| Path                | Backend                             |
|---------------------|-------------------------------------|
| `/api/automation/*` | Automation service / n8n gateway    |
| `/api/search/*`     | Search/query service façade         |
| `/api/analytics/*`  | Curated analytics façade            |

## 10. DNS Drift — Stale Entries to Clean Up

| Hostname | Current                                      | Problem                  | Target                          |
|----------|----------------------------------------------|--------------------------|---------------------------------|
| ops      | CNAME → vercel-dns.com                       | Stale Vercel dependency  | Move to Front Door or retire    |
| agent    | CNAME → wr2azp5dsl6mu6xvxtpglk5v.agents.do-ai.run | Stale DO dependency | Move to Azure or retire         |
| mail     | A → 178.128.112.214                          | Legacy / non-Azure       | Keep only if intentional        |

## 11. Build Order

1. Add APIM (`az deployment group create` with `infra/bicep/main.bicep`)
2. Add `api.insightpulseai.com` DNS → Front Door CNAME
3. Wire APIM backends: Odoo, Auth, CRM, MCP, OCR
4. Clean stale DNS: ops, agent
5. Document canonical surface in `infra` + `ops-platform` repos

## 12. Repo Placement

| Concern                            | Repo           |
|------------------------------------|----------------|
| Front Door / APIM / DNS / IaC      | infra          |
| API contract catalog / conventions  | ops-platform   |
| Odoo controllers/adapters          | odoo           |
| MCP / agent route contracts         | agents         |
| Public docs / developer docs        | web            |
