# DATABRICKS_AI_DATA_CONTRACTS.md

## Purpose

Defines the curated data contracts that the Databricks intelligence layer
exposes for consumption by the AI/agent layer (Azure AI Foundry) and
analytics surfaces (Power BI).

These contracts represent the **governed interface** between the lakehouse
and downstream consumers. They are not raw tables — they are semantic,
versioned, quality-gated data products.

---

## Contract inventory

### `odoo_finance_close_kpis`

| Property | Value |
|---|---|
| Layer | gold |
| Serving mode | Databricks SQL |
| Owner repo | `lakehouse` |
| Consumers | `foundry:data-intel-ph`, `powerbi` |

**Contents:**
- period close summaries
- revenue/expense aggregates
- AR/AP aging snapshots
- cash flow indicators
- variance metrics

**Quality gates:**
- completeness check on required dimensions
- freshness SLA (updated within 24h of period close)
- referential integrity against Odoo master data

---

### `odoo_domain_taxonomy`

| Property | Value |
|---|---|
| Layer | silver |
| Serving mode | Delta table |
| Owner repo | `lakehouse` |
| Consumers | `foundry:data-intel-ph` |

**Contents:**
- Odoo model/field taxonomy
- module dependency graph
- field type mappings
- business domain classifications

**Quality gates:**
- schema validation against Odoo model registry
- no orphaned references
- freshness SLA (updated on each Odoo upgrade)

---

## Contract rules

### Rule 1 — Contracts are the interface, not the implementation

Consumers (Foundry agents, Power BI) depend on the contract schema and
SLAs, not on the internal medallion implementation.

### Rule 2 — Contracts are owned by `lakehouse`

The `lakehouse` repo is the sole owner of contract definitions. Foundry
agents consume contracts but never modify them.

### Rule 3 — Contract changes require downstream notification

Schema changes to a contract must be communicated to all declared consumers
before deployment.

### Rule 4 — Contracts have quality gates

Every contract must declare freshness SLAs, completeness checks, and
referential integrity rules. Ungated tables are not contracts.

---

## SSOT reference

Machine-readable inventory:
`lakehouse/ssot/databricks/curated-ai-contracts.yaml`

---

## Adding a new contract

1. Define the contract in `lakehouse/ssot/databricks/curated-ai-contracts.yaml`.
2. Implement the medallion pipeline in `lakehouse/`.
3. Document the contract in this file.
4. Declare consumers (Foundry project names, Power BI, etc.).
5. CI validates the contract inventory on push.
