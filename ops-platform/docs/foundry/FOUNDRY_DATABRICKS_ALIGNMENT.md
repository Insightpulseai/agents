# FOUNDRY_DATABRICKS_ALIGNMENT.md

## Purpose

This document defines the canonical split between **Azure Databricks** and
**Azure AI Foundry** in the InsightPulseAI platform.

It exists to prevent architectural drift and answer these questions clearly:

1. What belongs in Databricks?
2. What belongs in Azure AI Foundry?
3. Which repo owns each layer?
4. How should Odoo integrate with both?
5. What is the immediate next maturity path from the current state?

This document is normative for platform ownership and implementation direction.

---

## Canonical statement

**Azure Databricks is the enterprise data intelligence substrate.
Azure AI Foundry is the governed generative AI and agent control plane on top
of it.**

---

## Why this split exists

Databricks and Azure AI Foundry are **complementary**, not interchangeable.

### Azure Databricks is optimized for

- large-scale data ingestion
- batch and streaming pipelines
- medallion architecture
- governed analytics and SQL serving
- ML and feature/vector data preparation
- lakehouse-scale enterprise data management

Databricks' end-to-end reference architecture explicitly centers on ingestion,
transformation, Delta Lake storage, Unity Catalog governance, Databricks SQL,
Jobs orchestration, Power BI/Fabric consumption, and enterprise
telemetry/governance services.

### Azure AI Foundry is optimized for

- generative AI applications
- prompt agents
- tool-connected agents
- model deployment selection for AI apps
- agent workflows
- guardrails
- tracing and evaluations

Microsoft's guidance positions Foundry as the genAI and agent platform, while
Databricks remains the broader data/analytics/ML backbone.

---

## Canonical architecture layers

### 1. Data intelligence layer — Azure Databricks

This is the governed enterprise data backbone.

#### Responsibilities

- ingest data from Odoo and other systems
- process batch and streaming data
- implement bronze / silver / gold medallion layers
- curate business-ready data products
- expose governed SQL/BI consumption surfaces
- produce AI-facing structured data contracts
- host analytics and data-science workloads
- manage metadata and governance via Unity Catalog

#### Typical outputs

- finance close KPI marts
- ERP master-data views
- product, category, partner, and transaction marts
- agent-facing semantic tables
- feature/vector-ready corpora
- Power BI / Fabric-facing governed datasets

#### Not responsible for

- prompt-agent lifecycle
- agent system prompts
- tool attachment logic
- guardrail policy
- agent evaluations and red-team loops
- app-facing generative AI runtime policy

---

### 2. Agent control plane — Azure AI Foundry

This is the managed generative AI and agent layer.

#### Responsibilities

- define prompt agents
- attach tools
- bind model deployments for genAI apps
- manage guardrails
- manage agent traces and monitoring
- manage evaluations
- host agent workflows
- govern prompt/runtime versions

#### Typical outputs

- agent responses
- grounded retrieval answers
- tool-augmented actions
- trace records
- eval outputs
- publishable agent versions

#### Not responsible for

- bronze/silver/gold ETL
- lakehouse data transformations
- general-purpose enterprise warehousing
- Power BI semantic modeling
- SQL marts as the source of truth
- large-scale feature engineering as the primary platform role

---

## Canonical platform relationship

The relationship is:

- **Databricks prepares and governs**
- **Foundry reasons and acts**

### Databricks does

- data ingestion
- normalization
- enrichment
- semantic shaping
- analytics serving
- AI-facing data contract production

### Foundry does

- prompt orchestration
- tool usage
- model invocation
- knowledge grounding
- policy enforcement
- evaluation and traceability

### Odoo does

- business process interaction
- operator-facing UI
- ERP transaction execution
- human approval and workflow entry points

---

## Current observed platform state

The currently observed Azure AI Foundry project is:

### Foundry project

- `data-intel-ph`

### Current Foundry assets

- one prompt agent: `ipai-odoo-copilot-azure`
- two model deployments:
  - `gpt-4.1`
  - `text-embedding-3-small`
- one Azure AI Search tool attached
- uploaded markdown data/knowledge assets
- guardrails configured
- no workflows yet
- no evaluations yet
- no fine-tunes yet

### Interpretation

This is a valid **Phase 1 Foundry shape**:

- prompt agent exists
- model deployments exist
- grounding tool exists
- guardrails exist

The missing maturity layers are:

- workflow definitions
- evaluation suites
- stronger repo-backed mirroring of portal state
- clearer governed data contracts from Databricks into the agent layer

---

## Repo ownership model

### `lakehouse`

#### Owns

- Databricks notebooks
- Databricks jobs
- medallion pipelines
- Databricks SQL
- curated marts
- AI-facing structured data contracts
- analytics deployment assets
- workspace sync discipline for analytics assets

#### Must not own

- prompt agents
- guardrail policy
- agent system prompts
- Foundry workflow definitions
- Odoo runtime integration code
- Search/Foundry infra provisioning

#### Why

`lakehouse` is the source-of-truth repo for the Databricks intelligence layer,
not for the genAI control plane.

---

### `agents`

#### Owns

- agent manifests
- system prompts
- workflow specs
- evaluation specs
- knowledge markdown source files
- tool references at the logical/attachment level
- agent-side orchestration metadata

#### Must not own

- Databricks infra
- Odoo module logic
- APIM / Front Door IaC
- enterprise secret governance
- medallion transformations

#### Why

`agents` is the source-of-truth repo for the agent definition layer.

---

### `ops-platform`

#### Owns

- Foundry project inventory
- model deployment inventory
- tool inventory
- guardrail inventory
- control-plane doctrine
- sync policies between repos and portal resources
- auth-mode policy
- endpoint taxonomy

#### Must not own

- lakehouse transformation logic
- Odoo runtime code
- frontend business logic
- infra manifests except SSOT/inventory files

#### Why

`ops-platform` is the source-of-truth repo for platform governance and
inventories.

---

### `infra`

#### Owns

- Foundry resource IaC where applicable
- Search resource IaC
- Databricks workspace IaC
- IAM / RBAC wiring
- Key Vault
- APIM
- Front Door
- networking

#### Must not own

- prompts
- workflows
- eval specs
- medallion business rules
- Odoo business logic

#### Why

`infra` owns resource provisioning, not application meaning.

---

### `odoo`

#### Owns

- Odoo-side settings/configuration models
- Odoo bridge/controllers
- ERP-specific tools/actions
- Odoo UX for agent invocation
- business-side tool contracts that execute in ERP

#### Must not own

- global Foundry control-plane doctrine
- Databricks medallion transformations
- Search/Foundry provisioning
- central guardrail inventory

#### Why

`odoo` is the ERP runtime and integration consumer, not the platform control
plane.

---

## Canonical ownership matrix

| Surface | Repo owner |
|---|---|
| Databricks notebooks/jobs/pipelines/SQL | `lakehouse` |
| Curated AI-facing data contracts | `lakehouse` |
| Agent definitions/manifests | `agents` |
| System prompts | `agents` |
| Agent workflows | `agents` |
| Eval specs | `agents` |
| Knowledge markdown source files | `agents` |
| Foundry project inventory | `ops-platform` |
| Model deployment inventory | `ops-platform` |
| Tool inventory | `ops-platform` |
| Guardrail inventory/policy | `ops-platform` |
| Search/Foundry/Databricks/IAM IaC | `infra` |
| Odoo bridge + ERP-side invocation | `odoo` |

---

## Integration rules

### Rule 1 — Databricks never owns prompt behavior

Prompts, guardrails, workflows, and agent versions belong to Foundry and
repo-backed agent artifacts.

### Rule 2 — Foundry never owns medallion logic

Bronze/silver/gold engineering remains a Databricks concern.

### Rule 3 — Odoo is the business interaction layer

Odoo invokes AI behavior and executes ERP-side actions, but is not the
platform owner of data intelligence or the genAI control plane.

### Rule 4 — Search grounding is a bridge, not the whole platform

Azure AI Search is an access/grounding mechanism for the agent, not the
substitute for Databricks as the enterprise data backbone. Foundry's Azure
AI Search tool is an attachment mechanism into the agent layer.

### Rule 5 — Repo is the source of truth, portal is the managed execution surface

Portal-created assets must be mirrored and governed from repos wherever
possible.

---

## Immediate next maturity steps

### 1. Mirror current Foundry state into repos

Start with:

- current prompt agent
- current model bindings
- current Search tool reference
- current guardrails
- current knowledge markdown

### 2. Add evaluations

Current state shows no evaluations. That is the next major governance gap.

Recommended eval directories:

- `automatic/`
- `human/`
- `redteam/`

### 3. Add workflows

Current state shows no workflows. Workflows are the next maturity step for
orchestrated/multi-step agent execution.

### 4. Define Databricks-to-Foundry curated contracts

Start with:

- finance close KPIs
- ERP semantic crosswalks
- taxonomy/reference views
- policy/procedure corpora
- structured domain vocabularies

### 5. Defer fine-tuning

Current state shows no fine-tunes. Keep it that way until:

- grounding is mature
- tools are stable
- evaluations exist
- workflow behavior is measured

---

## Anti-patterns

Do not:

- make Databricks the owner of prompt agents
- store agent definitions only in the Foundry portal
- treat Search as the enterprise data backbone
- put guardrail policy inside lakehouse
- put Search/Foundry infra inside agents
- put platform doctrine inside odoo
- fine-tune before grounding, tooling, and evals are stable

---

## Decision rules

**Use Databricks** when the question is:

- where is the governed truth data?
- how is the data ingested, cleaned, transformed, and served?
- how are SQL, BI, and analytics workloads delivered?
- how are AI-facing structured data contracts prepared?

**Use Foundry** when the question is:

- which model/agent should answer?
- what tools can the agent call?
- what guardrails apply?
- how is the agent traced and evaluated?
- how is the prompt/runtime version published?

**Use Odoo** when the question is:

- how does a business user invoke the capability?
- what ERP object/action should be read or changed?
- where should approval and execution happen in the transaction system?

---

## Owner

Primary owner: InsightPulseAI platform governance

Canonical repo homes:

| Layer | Repo |
|---|---|
| agent layer | `agents` |
| control-plane doctrine | `ops-platform` |
| data intelligence layer | `lakehouse` |
| ERP integration layer | `odoo` |
| infrastructure | `infra` |
