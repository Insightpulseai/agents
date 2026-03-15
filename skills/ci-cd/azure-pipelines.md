# Skill: Azure Pipelines — CI/CD for IPAI

source: https://learn.microsoft.com/en-us/azure/devops/pipelines/
extracted: 2026-03-15
applies-to: .github, infra, automations, agents

## What it is

Azure DevOps CI/CD service with YAML-based pipeline definitions, environment gates, and deep Azure integration. Supports multi-stage deployments, self-hosted agents, and Key Vault-backed secrets.

## Decision: Azure Pipelines vs GitHub Actions

- IPAI primary CI/CD = **GitHub Actions** (already in `.github/`)
- Azure Pipelines = use ONLY for workloads needing Azure DevOps integration or existing ADO org pipelines (e.g., TBWA\SMP if they use ADO)
- Do NOT duplicate pipeline definitions across both systems

## When to use

| Scenario | Azure Pipelines | GitHub Actions |
|----------|----------------|----------------|
| Standard CI/CD for IPAI repos | No | Yes (primary) |
| Client uses Azure DevOps | Yes | No |
| Needs ADO test plans integration | Yes | No |
| Needs ADO artifacts feed | Yes | Evaluate |
| Everything else | No | Yes |

## Key Concepts (for YAML Authoring)

| Concept | Description |
|---------|-------------|
| Stages | Top-level grouping (build → test → deploy) |
| Jobs | Run on an agent (parallel within a stage) |
| Steps | Individual tasks within a job |
| Environments | Named targets with approval gates (dev → staging → prod) |
| Service connections | Auth to Azure, ACR, AKS |
| Variable groups | Secret management (backed by Key Vault) |
| Templates | Reusable YAML fragments (equivalent to GHA reusable workflows) |
| Agents | Microsoft-hosted (ubuntu-latest) or self-hosted |

## IPAI-Specific Patterns

### ACA Deploy Stage (maps to infra/ Bicep)

```yaml
trigger:
  branches:
    include: [main]

stages:
  - stage: Build
    jobs:
      - job: BuildAndPush
        steps:
          - task: Docker@2
            inputs:
              containerRegistry: 'acr-ipai-dev'
              repository: 'ipai-app'
              command: 'buildAndPush'

  - stage: Deploy
    dependsOn: Build
    jobs:
      - deployment: DeployACA
        environment: 'ipai-dev'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureCLI@2
                  inputs:
                    scriptType: 'bash'
                    scriptLocation: 'inlineScript'
                    inlineScript: |
                      az containerapp update \
                        --name ipai-app \
                        --resource-group rg-ipai-dev \
                        --image acripaidev.azurecr.io/ipai-app:$(Build.BuildId)
```

### Secrets Pattern (SSOT-Compliant)

- Variable groups backed by Azure Key Vault
- Never commit secrets; reference `$(MY_SECRET)` syntax
- Key Vault = secrets plane; Supabase Vault = app secrets SSOT

### Self-Hosted Agent (If Needed)

- Deploy as ACA job in `rg-ipai-dev`
- Runs in SEA region, same VNet as `ipai-odoo-dev-pg`
- Use for workloads needing private network access to Odoo/Supabase

## Determinism Principle

From the MS SDLC article:

- CI/CD pipelines are **deterministic** — agents call them, not the reverse
- Pipeline NEVER makes agentic decisions (no LLM in deploy path)
- Agents produce artifacts → pipeline deploys them predictably

## SSOT/SOR Mapping

- Pipeline definitions → `.github/workflows/` (primary) or ADO YAML (client-specific)
- Pipeline run state → GitHub Actions / ADO native (not replicated to Supabase)
- Deploy artifacts → ACR image tags, ACA revision IDs
- Infrastructure config → `infra/` (Bicep/Terraform, version-controlled)

## Cross-References

- GitHub Actions workflows: `.github/workflows/`
- Infrastructure templates: `infra/`
- Agentic SDLC constitution: `agents/system/agentic-sdlc-constitution.md`
