# Skill: Databricks Data Intelligence Platform — IPAI Reference

source: databricks.com/product/*
extracted: 2026-03-15
applies-to: lakehouse, agents, ops-platform

## What it is

Unified analytics platform combining data lake, data warehouse, and AI capabilities on a single governance layer (Unity Catalog). Built on Delta Lake with ACID transactions, time travel, and schema enforcement on object storage.

## IPAI Platform Layer Map

```
stipaidevlake (ADLS)           ← raw storage (Bronze)
  ↓ Delta Live Tables
dbw-ipai-dev Unity Catalog     ← Silver + Gold tables (SSOT for analytics)
  ↓ AI/BI Dashboards / DBSQL
ops-console (web repo)         ← surfaces to users
  ↓
Supabase (ops-platform)        ← SSOT for orchestration + control plane
  ↓
Odoo (odoo repo)               ← SOR for ERP/accounting
```

## Capability Matrix (dbw-ipai-dev)

| Capability | Status | Notes |
|-----------|--------|-------|
| Delta Lake + Spark | GA | Core compute |
| Unity Catalog | Partial | Needs full activation |
| Delta Live Tables (DLT) | Ready | Medallion pipelines |
| AI/BI Dashboards | Evaluating | vs. Superset retirement |
| Lakebase (Postgres OLTP) | Evaluating | Neon-acquired, Azure preview |
| Databricks Apps | Evaluating | Internal app hosting |
| MLflow 3.0 | Ready | Agent eval + LLMOps |
| Model Serving (GPU) | On demand | Cost-gated |
| Vector Search | Ready | RAG pipelines |

## 2025-2026 Platform Shifts (Strategic Signals)

1. **Lakebase** (Postgres OLTP, Neon-acquired): OLTP + OLAP unified. Evaluate as Supabase complement for pure-analytics apps that don't need RLS/Auth complexity.
2. **Databricks Apps**: Deploy Streamlit/Gradio/custom apps inside the workspace with SSO + Unity Catalog auth. Use for internal analyst tools, not external portals.
3. **Agent Bricks**: First-class multi-agent runtime on the lakehouse. Native alternative to MS Agent Framework for Databricks-native agent workflows.
4. **AI/BI Genie**: Conversational analytics ("ask your data a question"). Evaluate as Superset replacement → natural language → SQL → chart.
5. **Lakeflow Connect**: Managed connectors (SharePoint, Salesforce, etc.). Reduces custom ETL code for standard SaaS sources.

## SSOT/SOR Mapping

- Databricks IS NOT SSOT or SOR for any operational domain
- Databricks = analytics/intelligence layer ONLY
- Canonical path: Odoo SOR → Supabase SSOT → Databricks (read-only replica for analytics)
- Never write back from Databricks to Odoo or Supabase except via explicit Edge Function / queue workflow with audit trail

## Governance Contract

- All Databricks tables must be registered in Unity Catalog
- Schema: `ipai_bronze` / `ipai_silver` / `ipai_gold` / `ipai_ai`
- External access: Delta Sharing only (no direct JDBC from external apps)
- Lineage: auto-captured by Unity Catalog — do not bypass

## Cross-references

- Data engineering: `skills/platform/data-engineering.md`
- Databricks Apps: `skills/platform/databricks-apps.md`
- Financial services: `skills/industries/financial-services.md`
- Marketing/retail/media: `skills/industries/marketing-retail-media.md`
