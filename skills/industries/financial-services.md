# Skill: Databricks — Financial Services Use Cases

source: databricks.com/solutions/industries/financial-services
extracted: 2026-03-15
applies-to: lakehouse, agents

## What it is

Databricks financial services patterns mapped to TBWA\SMP Finance team needs. Covers fraud detection, compliance reporting, risk management, and financial analytics on the lakehouse architecture.

## Use Case Mapping (Databricks FS → IPAI/TBWA\SMP)

| Databricks FS Use Case | IPAI/TBWA\SMP Equivalent |
|------------------------|--------------------------|
| Real-time fraud detection | AP/AR anomaly detection |
| AI model risk management | Budget variance alerts |
| Card transaction analytics | Expense categorization (Concur replacement) |
| Regulatory compliance reporting | BIR tax compliance automation |
| Risk-weighted asset computation | Financial period close analytics |
| Customer 360 for banking | Client/project profitability dashboards |

## Solution Accelerators (Pre-Built Notebooks)

Available via Databricks Marketplace — adapt to IPAI use case:
- AI model risk management
- Card transaction analytics
- Cybersecurity at scale

## TBWA\SMP Finance Team Mapping

| Person | Role | Databricks Surface |
|--------|------|-------------------|
| CKVC | Finance Director | Executive dashboards (Gold layer, AI/BI Genie) |
| RIM | Senior Finance Manager | Operational reports (Silver layer, DBSQL) |
| BOM | Finance Supervisor | Pipeline monitoring, data quality alerts |
| Accountants | Staff | Self-serve SQL via AI/BI Genie (no notebook required) |

## BIR Compliance Pattern on Databricks

```
Bronze: raw Odoo journal entries (replicated via Supabase)
Silver: validated + enriched (BIR field mapping, tax code normalization)
Gold: BIR-ready summaries (2307, SLSP, SAWT reports)
  → export via DBSQL
  → PDF via Edge Function
  → store in Supabase Storage
```

## Key Principle

Financial data from Odoo flows ONE WAY into Databricks. Databricks produces analytics artifacts only. Odoo retains all posted records as SOR — never overwrite from lakehouse.

## SSOT/SOR Mapping

- Odoo = SOR for all posted financial records
- Supabase = SSOT for orchestration and job state
- Databricks = analytics layer (read-only from SOR/SSOT)
- BIR report outputs → Supabase Storage (with metadata in Postgres)
