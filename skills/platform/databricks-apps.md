# Skill: Databricks Apps (Lakehouse Apps)

source: databricks.com/product/databricks-apps
extracted: 2026-03-15
applies-to: lakehouse, web, ops-platform

## What it is

Deploy web apps (Streamlit, Gradio, Flask, custom) inside a Databricks workspace. SSO via Databricks identity, Unity Catalog permissions inherited automatically, data never leaves workspace.

## When to Use (Decision Matrix)

| Use Case | Use Databricks Apps | Use IPAI web repo |
|----------|--------------------|--------------------|
| Internal analyst tool (CKVC, RIM dashboards) | Yes — data stays in lakehouse | No |
| Executive report viewer | Yes — SSO + Unity Catalog | No |
| External client portal | No — use web repo | Yes |
| ops-console (control plane) | No — needs Supabase RLS | Yes |

## Deployment

```bash
databricks apps deploy my_app --source-code-path ./app
```

## Integration with Lakehouse

- Read directly from Unity Catalog tables via Python/SQL
- Lakebase connection: `postgresql://lakebase-host/db` (if Lakebase enabled)
- MLflow Model Serving: call registered models via REST

## Relevant for IPAI

Finance dashboards for TBWA\SMP team: deploy as Databricks App
- CKVC/RIM/BOM get SSO access, data never leaves workspace
- Replaces Superset for internal finance analytics use case

Evaluation criteria: Databricks Apps vs. AI/BI Genie vs. Superset
- Decision tracked in: `lakehouse/decisions/adr-001-bi-tool-selection.md`

## SSOT/SOR Mapping

- Databricks Apps = presentation layer only
- Data stays in Unity Catalog (governed)
- No operational state in Databricks Apps — stateless renderers
- User auth via Databricks identity (not Supabase Auth)

## Gaps / Watch

- Not suitable for external-facing apps (no custom domain, no public auth)
- SSO is Databricks-native only (no SAML/OIDC federation to external IdPs)
- Any language/framework supported — not a proprietary runtime
