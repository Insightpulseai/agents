# Skill: Databricks — Marketing, Retail, Media Use Cases

source: databricks.com/solutions/industries/marketing + retail + media-and-entertainment
extracted: 2026-03-15
applies-to: lakehouse, agents

## What it is

Databricks industry solutions for marketing (Composable CDP), retail (unified commerce), and media/entertainment (audience intelligence) — mapped to IPAI lakehouse architecture.

## Marketing (Data Intelligence for Marketing)

Core capability: unified customer + campaign data on lakehouse.

Key pattern: **Composable CDP**
- No data movement: warehouse-native activation
- Identity resolution (Amperity: 45min from login to completed ID resolution)
- Delta Sharing → martech tools (Salesforce, Adobe, Braze, Hightouch, Census)
- Unity Catalog enforces GDPR/CCPA governance on all marketing data

Benchmark results (launch customers):
- 324% increase in click-through rates (Skechers/ActionIQ)
- 68% decrease in cost-per-click
- 28% increase in ROAS

IPAI relevance: If clients include marketing orgs, this is the architecture template. Partner integrations pre-built: Adobe, Braze, Salesforce, OneTrust (consent).

## Retail

Core pattern: unified commerce data (POS + e-commerce + supply chain).

Use cases:
- Real-time personalization (product recommendations)
- Inventory optimization (demand forecasting with DLT + MLflow)
- Merchandising analytics (Gold layer rollups)
- Loyalty program orchestration (65M+ member example: sync to SFMC daily)

IPAI relevance: Project Scout (sari-sari store analytics) fits retail medallion pattern.

## Media & Entertainment

Core use cases:
- Audience segmentation (first + third party data unification)
- Content performance analytics (streaming metrics, engagement)
- Ad traffic + performance intelligence (Agent Bricks accelerator by Indicium)
- Network reliability (Networklytics: OSS/BSS + CRM + telemetry unified)

## Shared Medallion Pattern (All Three Verticals)

```
Bronze: raw events (clickstream, transactions, interactions)
Silver: cleansed + identity-resolved
Gold: audience segments, campaign KPIs, attribution models
AI layer: embeddings + recommendations + churn prediction
Activation: Delta Sharing → downstream martech/adtech tools
```

## SSOT/SOR Mapping

- Databricks = analytics/intelligence layer only
- Customer data governed by Unity Catalog (GDPR/CCPA compliance)
- Activation via Delta Sharing (zero-copy to downstream tools)
- No operational state in Databricks — orchestration in Supabase SSOT
