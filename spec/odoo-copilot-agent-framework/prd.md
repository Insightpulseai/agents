# PRD — Odoo Copilot Agent Framework

## Overview

One Odoo Copilot product surface backed by a governed multi-role runtime:
- 1 visible front-door Foundry prompt agent
- 3 logical agent roles (Advisory, Ops, Actions)
- 1 Agent Framework router workflow
- APIM as production ingress
- Foundry tracing + App Insights
- Knowledge, tools, evals, and approval gates

## Target Top-Level Components

| Component | Form | Purpose |
|---|---|---|
| `ipai-odoo-copilot-advisory` | Foundry prompt agent | user-facing grounded Q&A, guidance, strategy |
| `ipai-odoo-copilot-ops` | Agent Framework agent | internal diagnostics, read-only operational inspection |
| `ipai-odoo-copilot-actions` | Agent Framework agent | controlled execution and bounded writes |
| `ipai-odoo-copilot-router` | Agent Framework workflow | deterministic routing, approvals, checkpoints, handoffs |

## Agent Matrix

| Component | Primary responsibility | Core tools / packs | Allowed actions | Hard blocks | Required evaluations |
|---|---|---|---|---|---|
| `ipai-odoo-copilot-advisory` | user-facing Q&A, grounded explanation, strategy guidance | Azure AI Search / Foundry knowledge, Marketing Strategy & Insight Pack, Databricks Intelligence Pack | explain, summarize, recommend, compare, hand off | no writes, no admin/security changes, no direct publish/export, no finance execution | Task Completion, Task Adherence, Intent Resolution, Relevance, Groundedness where applicable |
| `ipai-odoo-copilot-ops` | internal diagnostics, read-only operational inspection | read-only Odoo tools, Databricks monitoring/health, infra/runtime reads | inspect, diagnose, compare state, summarize incidents, propose remediation | no record mutation, no secret changes, no role changes, no uncontrolled job execution | Task Completion, Task Adherence, Tool Selection, Tool Call Success, Tool Output Utilization |
| `ipai-odoo-copilot-actions` | controlled execution and bounded writes | approved Odoo write tools, approved Databricks job/app actions, fal Creative Production Pack actions | create/update allowed records, trigger approved jobs, launch approved creative runs, prepare exports, write evidence | no unrestricted writes, no destructive ops, no policy bypass, no silent batch execution | Tool Selection, Tool Input Accuracy, Tool Call Success, approval compliance, unauthorized-action refusal |
| `ipai-odoo-copilot-router` | deterministic routing, approvals, handoffs, checkpointing | workflow graph, approval steps, evidence correlation | route, pause for approval, resume, hand off, checkpoint, collect trace context | no free-form business reasoning, no broad vendor logic, no direct domain mutation | routing correctness, handoff success, approval compliance, end-to-end task completion |

## Capability Classes (Joule Benchmark)

| Class | Owner | Meaning |
|---|---|---|
| Informational | Advisory | grounded explanations, summaries, source-backed guidance |
| Navigational | Ops + Router | finding records, apps, workflows, next steps, richer execution surfaces |
| Transactional | Actions | approved create/update/trigger/export actions |

## Capability Packs (Cross-Agent Attachment)

| Capability pack | Advisory | Ops | Actions | Router |
|---|---:|---:|---:|---:|
| Databricks Intelligence Pack | Yes | Yes | Yes | Yes |
| fal Creative Production Pack | Yes | Yes | Yes | Yes |
| Marketing Strategy & Insight Pack | Yes | Yes | Light | No |
| BIR Compliance Pack | Yes | Yes | Yes | Yes |
| Document Intake & Extraction Pack | Yes | Yes | Yes | No |

## Foundry + Agent Framework Split

- **Foundry** is the control plane for prompt agents, datasets, evaluations, tracing, and project-scoped resources.
- **Agent Framework** is the execution plane for graph workflows, checkpointing, middleware, and multi-agent orchestration.
- Do not add more than 3 agents + 1 workflow until eval coverage and tracing are stable.

## Capability Pack Details

### Databricks Intelligence Pack

Covers: Lakeflow/data engineering explanations, Databricks Apps guidance, job health, refresh/run triggers, industry-solution interpretation, retail/marketing/media/financial-services intelligence.

### fal Creative Production Pack

Covers: brief-to-prompt guidance, generation queue health, model/cost/speed guidance, approved batch generation, export/package preparation, Live Avatar and talking-avatar flows.

### Marketing Strategy & Insight Pack

Covers: campaign strategy (Smartly benchmark), consumer insight synthesis (Quilt.AI benchmark), creative benchmarking (LIONS benchmark), performance interpretation and MMM/GEO (Data Intelligence benchmark), next-best-action suggestions.

### BIR Compliance Pack

Covers: BIR regulation grounding, form guidance, deadline/overdue inspection, return computation, validation, alphalist generation, filing artifact generation (eFPS XML, PDF), notification workflow, human-in-loop filing flow.

Three internal layers:
- **Tax Calculation Layer** (AvaTax benchmark): versioned rates, rule engine, deterministic compute APIs
- **Tax Workflow Layer** (SAP Tax Compliance benchmark): simulation, validation, approval, filing/export, worklists
- **Tax Knowledge Layer** (Joule + Foundry IQ benchmark): regulation grounding, authority registry, cited answers

### Document Intake & Extraction Pack

Covers: OCR/read, layout/table extraction, invoice/receipt ingestion, contract extraction, BIR attachment classification, evidence normalization, document-to-record linking. Uses Azure AI Document Intelligence / Vision + Document.

## Benchmark Hierarchy

| Benchmark | Use it for |
|---|---|
| AvaTax | tax engine / calculation quality |
| SAP Tax Compliance | compliance workflow rigor |
| Joule | assistant capability taxonomy + enterprise distribution |
| BIR official surfaces | authority and filing endpoints |
| Odoo PH localization | localization baseline |
| TaxPulse-PH-Pack | PH-specific rules/rates/reports seed |

## SDK Client Model

Most apps should use both:
- **Project client** (`AIProjectClient`) for Foundry-native operations (config, connections, tracing)
- **OpenAI-compatible client** (`project.get_openai_client(...)`) for agents, evaluations, and model calls

## Not In Scope

- Teams/BizChat publishing (future, depends on M365 Agents SDK maturity)
- Hosted agent deployment (Action agent may migrate later)
- Fine-tuning (deferred until datasets and evaluations are stable)
- More than 3 agents + 1 workflow
