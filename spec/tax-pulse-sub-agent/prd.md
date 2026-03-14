# PRD — Tax Pulse Sub-Agent (BIR Compliance Pack)

## Overview

Tax Pulse is a BIR Compliance capability pack for Odoo Copilot that combines grounded tax knowledge, deterministic tax rules, approval-gated actions, and Odoo-native task/workflow orchestration.

## Three Internal Layers

### 1. Tax Calculation Layer (AvaTax benchmark)
- Versioned rates (ph_rates_2025.json)
- JSONLogic rules engine (vat.rules.yaml, ewt.rules.yaml)
- Deterministic compute APIs
- Batch + real-time support
- Explainable calculation traces

### 2. Tax Workflow Layer (SAP Tax Compliance benchmark)
- Simulation / preview mode before validate/export
- Stage progression: Draft → Computed → Validated → Approved → Filed → Confirmed
- PLM-style approval gates (required / optional / comments-only)
- Worklists and task templates
- Filing package review and evidence collection

### 3. Tax Knowledge Layer (Joule + Foundry IQ benchmark)
- BIR regulation grounding (RRs, RMOs, TRAIN law)
- Authority registry with source tiering
- Citation-first retrieval
- Knowledge freshness and provenance tracking

## Capability Assignment by Component

| Component | BIR role |
|---|---|
| Advisory | explain forms, rules, deadlines, filing requirements, summarize regulations, guide next steps |
| Ops | inspect return state, diagnose missing data, list overdue filings, verify KB/tool availability |
| Actions | compute return, validate return, generate alphalist, create export artifacts, trigger approved notifications |
| Router | orchestrate compute → validate → review → export → confirm with human-in-loop |

## BIR Tools

### Advisory tools
- `bir_compliance_search` — search BIR regulation corpus
- `search_knowledge_bir` — search Odoo/BIR domain knowledge

### Ops tools
- `check_overdue_filings` — list filings past due date
- `inspect_bir_return_state` — inspect lifecycle state
- `inspect_bir_configuration` — check entity/tax setup
- `inspect_bir_kb_index_status` — verify KB population

### Action tools
- `compute_bir_vat_return` — compute 2550Q/2550M
- `compute_bir_withholding_return` — compute 1601-C/1601-E
- `validate_bir_return` — validate return for filing readiness
- `generate_alphalist` — generate 1604-CF/1604-E alphalist
- `generate_efps_xml` — generate eFPS-compatible XML
- `generate_bir_pdf` — generate PDF report artifact

## BIR Forms Covered

| Form | Purpose |
|---|---|
| 2550Q | Quarterly VAT return |
| 2550M | Monthly VAT return |
| 1601-C | Monthly compensation withholding |
| 1601-E | Monthly expanded withholding |
| 1601-EQ | Quarterly expanded withholding |
| 1601-F | Monthly final withholding (stub) |
| 1600 | Monthly VAT withholding |
| 1702Q | Quarterly income tax return |
| 1604-CF | Annual compensation alphalist |
| 1604-E | Annual expanded alphalist |
| 2316 | Certificate of compensation (future) |

## Port from TaxPulse-PH-Pack

Source: `jgtolentino/TaxPulse-PH-Pack`

Port into `addons/ipai/ipai_bir_tax_compliance/`:
- `data/rates/ph_rates_2025.json` — externalized TRAIN brackets, EWT codes, VAT rate
- `data/rules/vat.rules.yaml` — declarative VAT rules
- `data/rules/ewt.rules.yaml` — declarative EWT rules
- `engine/rules_engine/` — JSONLogic evaluator
- `reports/` — XML report templates (1601-C, 2550Q, 1702-RT)
- `tests/fixtures/` — CSV test fixtures

Do NOT port:
- `account_reports` EE dependency
- Odoo 18 assumptions
- Deprecated Supabase project references

## Month-End + Filing Workflow

Use Odoo Project with:
- Recurring tasks per form/period/company
- Task dependencies: reconcile → compute → validate → approve → export → submit → confirm
- Milestones: Books Ready, Computation Complete, Validation Complete, Filed, Confirmed
- Activities: reminders, approvals, missing-data follow-ups
- PLM-style approval gates at validation and filing transitions

## SFT Training Strategy

Order: ground it → tool it → evaluate it → then fine-tune

1. Populate BIR knowledge base
2. Add BIR tools
3. Run eval datasets
4. Collect 150+ gold responses
5. SFT with consistent system prompt
6. Compare SFT vs prompt-only on same eval harness
