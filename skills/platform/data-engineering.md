# Skill: Databricks Data Engineering

source: databricks.com/product/data-engineering
extracted: 2026-03-15
applies-to: lakehouse, automations

## What it is

Databricks data engineering primitives: Delta Live Tables (DLT), Lakeflow Jobs, Lakeflow Connect, Structured Streaming, DBSQL, and Delta Sharing. Foundation for the IPAI medallion architecture.

## Core Primitives

| Primitive | Use for |
|-----------|---------|
| Delta Live Tables (DLT) | Declarative medallion pipelines (Bronze→Silver→Gold) |
| Lakeflow Jobs | Orchestrated multi-task workflows (cron, trigger, dependency) |
| Lakeflow Connect | Managed connectors (Salesforce, SharePoint, JDBC, Kafka) |
| Streaming (Spark Structured) | Real-time ingestion from Kafka/Event Hubs/Kinesis |
| DBSQL | Serverless SQL warehouse for analytics + transformations |
| Delta Sharing | Zero-copy data sharing to external consumers |

## Medallion Pattern for IPAI

```
Bronze (stipaidevlake/bronze/*)
  Sources: Odoo webhooks → Supabase → export → ADLS
           n8n automation exports
           External API pulls (fal.ai outputs, etc.)
  Format: raw Parquet/JSON, partitioned by date

Silver (Unity Catalog: ipai_silver.*)
  Transformations: DLT with expectations (data quality rules)
  Schema: validated, typed, deduplicated
  Latency: near-real-time (streaming DLT) or hourly batch

Gold (Unity Catalog: ipai_gold.*)
  Aggregations: business-metric rollups
  Consumers: AI/BI Dashboards, Databricks Apps, Delta Sharing
  SLA: refreshed every 15min for operational, daily for financial

AI layer (Unity Catalog: ipai_ai.*)
  Vector indexes, embeddings, feature tables
  MLflow registered models
  Inference tables (request/response logging)
```

## DLT Pipeline Skeleton (Standard for IPAI)

```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
  name="silver_odoo_journal_entries",
  comment="Validated Odoo journal entries from Bronze",
  table_properties={"quality": "silver"}
)
@dlt.expect_all({
  "valid_amount": "amount IS NOT NULL AND amount != 0",
  "valid_date": "date >= '2020-01-01'",
  "valid_company": "company_id IS NOT NULL"
})
def silver_journal_entries():
  return (
    dlt.read_stream("bronze_odoo_journal_entries")
      .withColumn("ingested_at", current_timestamp())
      .dropDuplicates(["odoo_id", "company_id"])
  )
```

## Lakehouse Federation for Supabase (Priority)

Zero-copy reads from Supabase PG directly into Databricks DBSQL — no ETL pipeline needed.

```sql
-- Register Supabase as foreign catalog in Unity Catalog
CREATE CONNECTION supabase_prod
  TYPE POSTGRESQL
  OPTIONS (
    host 'db.spdtwktxdalcfigzeqrz.supabase.co',
    port '5432',
    user secret('supabase_ro_user'),
    password secret('supabase_ro_password')
  );

-- Create foreign catalog
CREATE FOREIGN CATALOG supabase
  USING CONNECTION supabase_prod;

-- Now query Supabase tables directly from Databricks
SELECT * FROM supabase.ops.runs WHERE status = 'failed';
-- No ETL, no ADLS copy, governed by Unity Catalog
```

Benefits:
- Collapses a full Bronze ingestion stage for many Supabase tables
- Supabase stays canonical (SSOT doctrine preserved)
- Unity Catalog governs access — row-level filters supported
- `ipai_gold` views can JOIN Supabase live data with Databricks Delta tables

## 2025-2026 Data Engineering Features (Relevant to IPAI)

| Feature | Relevance |
|---------|-----------|
| SQL Stored Procedures (Aug 2025) | Encapsulate BIR report logic in SQL |
| Recursive CTEs (Jul 2025) | Org hierarchy + account tree traversals |
| Spatial SQL 80+ functions (Sep 2025) | Geospatial for Project Scout / retail |
| Lakehouse Federation GA | Federate Supabase PG into Unity Catalog |
| Managed Apache Iceberg | Open format tables for multi-engine access |
| Multi-statement transactions (upcoming) | Atomic updates across tables |

## SSOT/SOR Mapping

- Databricks = analytics/intelligence layer only
- Bronze data sourced from SSOT (Supabase) and SOR (Odoo)
- Silver/Gold = derived, governed by Unity Catalog
- Never write back to operational systems from Databricks
- Lakehouse Federation = read-only bridge to Supabase (zero-copy)
