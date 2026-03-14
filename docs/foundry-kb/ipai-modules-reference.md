# IPAI Odoo Modules Reference

**Version:** 1.0.0
**Last updated:** 2026-03-14
**Odoo version:** 19.0 CE
**Use:** Grounding context for InsightPulseAI Foundry copilot. Source label: [IPAI-KB]

---

## Overview

This document describes the custom InsightPulseAI Odoo modules (`ipai_*`) that are deployed in the production ERP. Use this document when answering questions about module functionality, available models, fields, states, or capabilities.

Do not confuse these with OCA modules or vanilla Odoo CE features. These are InsightPulseAI-specific (`ipai_*` prefix).

---

## Module 1: ipai_bir_tax_compliance

**Version:** 19.0.1.0.0
**Category:** Accounting / Compliance
**Depends on:** `account`, `l10n_ph`, `project`
**Summary:** Full BIR tax return filing workflow for Philippine corporations

### What it does

Implements the complete Bureau of Internal Revenue (BIR) compliance lifecycle for a Philippine corporation: from period initialization, through data gathering and computation, to validation, filing, and confirmation. Covers all 36 BIR form types tracked by InsightPulseAI.

### Models

| Model | Description | Key Fields |
|---|---|---|
| `bir.tax.return` | Master record for a single BIR filing obligation | `form_type`, `period_start`, `period_end`, `state`, `company_id`, `responsible_id`, `due_date`, `filed_date`, `amount_due`, `amount_paid` |
| `bir.vat.return` | VAT-specific return (2550M, 2550Q) | Inherits `bir.tax.return` + `output_vat`, `input_vat`, `net_vat_due`, `period_type` (monthly/quarterly) |
| `bir.withholding.return` | EWT/FWT remittance return (0619-E, 0619-F, 1601-C) | Inherits `bir.tax.return` + `withholding_type` (EWT/FWT/compensation), `total_tax_withheld`, `alphalist_ids` |
| `bir.filing.deadline` | Computed deadline registry | `form_type`, `frequency`, `reference_period`, `computed_due_date`, `state`, `is_overdue` |

### Form Types Covered (36 total)

| Group | Forms |
|---|---|
| VAT | 2550M, 2550Q |
| EWT | 0619-E, 1604-E, 2307 |
| FWT | 0619-F, 1604-F, 2306 |
| WVAT | 1600, 1600-WP |
| Income Tax | 1702-RT, 1702-Q |
| Payroll | 1601-C, 1604-C |
| Informational | SLSP, SAWT/QAP |
| Other | All remaining forms tracked under `bir.filing.deadline` |

### State Machine

All `bir.tax.return` records follow this state progression:

```
draft → computed → validated → filed → confirmed
```

| State | Meaning | Who Transitions | Conditions |
|---|---|---|---|
| `draft` | Return period initialized; no data computed | System (auto-created) or Compliance Officer | Created from filing deadline trigger or manually |
| `computed` | Period data pulled and amounts calculated | Compliance Officer or system | Accounting period must be closed; trial balance available |
| `validated` | Return reviewed and approved for filing | Finance Manager | Amount due verified; discrepancies resolved |
| `filed` | Filed with BIR (eBIRForms / eFPS) | Compliance Officer | Filed date recorded; confirmation number entered if applicable |
| `confirmed` | Payment confirmed and evidence uploaded | Finance Manager | Payment journal entry exists; BIR 2307 or receipt attached |

Backward transitions are blocked by default. A `draft` reset is available to Finance Managers on validated or filed returns if an amendment is required.

### Access Control

| Role | Permissions |
|---|---|
| Compliance Officer | Create, read, write `bir.tax.return`; transition draft→computed→filed |
| Finance Manager | Validate (computed→validated); confirm (filed→confirmed); reset to draft |
| Accounting Officer | Read-only on all BIR return records |
| Administrator | Full access including configuration |

---

## Module 2: ipai_finance_close_seed

**Version:** 19.0.1.0.0
**Category:** Accounting / Finance Operations
**Depends on:** `project`, `account`, `ipai_bir_tax_compliance`
**Summary:** Month-end and BIR close checklist seeder for `project.task`

### What it does

Seeds a structured month-end close checklist into Odoo's Project module as `project.task` records. Provides 89 tasks total per closing period:

- **39 month-end accounting tasks:** Accruals, reconciliations, prepaid amortizations, depreciation runs, trial balance review, AP/AR aging, bank reconciliation, inventory count, ledger lock
- **50 BIR filing tasks:** One task per BIR obligation per period, linked to the corresponding `bir.tax.return` record

### Task Structure

All tasks are created under a dedicated project (default name: "Month-End Close — [YYYY-MM]") as `project.task` records.

| Field | Value / Behavior |
|---|---|
| `project_id` | Month-End Close project for the period |
| `name` | Task name (e.g., "File BIR 2550M — January 2026") |
| `tag_ids` | Tagged `BIR` for all 50 BIR tasks; `ACCOUNTING` for the 39 accounting tasks |
| `date_deadline` | Set from `bir.filing.deadline` for BIR tasks; set from close calendar for accounting tasks |
| `user_ids` | Assigned by role (Compliance Officer for BIR tasks, Accounting Officer for accounting tasks) |
| `stage_id` | Starts in `To Do`; progresses to `In Progress`, `Done` |

### Month-End Accounting Tasks (39)

Key tasks in sequence order:

1. Post all accrual journal entries
2. Post prepaid expense amortization
3. Post depreciation for all asset groups
4. Reconcile all bank accounts
5. Reconcile intercompany accounts
6. Review and clear suspense accounts
7. Complete AP aging review
8. Complete AR aging review
9. Post payroll journal entries
10. Reconcile payroll clearing accounts
11. Review inventory count variance
12. Post inventory adjustments
13. Run trial balance and review for anomalies
14. Review fixed asset schedule
15. Post month-end provisions
16. Review deferred revenue schedule
17. Post revenue recognition adjustments
18. Prepare management accounts package
19. Lock accounting period
20. Submit trial balance to Finance Manager for sign-off
21–39: Supporting review and sign-off tasks

### BIR Filing Tasks (50)

Tasks are seeded for every active BIR obligation based on the company's registration:

| Task Pattern | Count | Trigger |
|---|---|---|
| Monthly EWT remittances (0619-E) | 12/year (1/month) | Per month |
| Monthly FWT remittances (0619-F) | 12/year | Per month |
| Monthly VAT declarations (2550M) | 12/year | Per month |
| Monthly payroll withholding (1601-C) | 12/year | Per month |
| Quarterly VAT returns (2550Q) | 4/year | Per quarter |
| Quarterly SLSP | 4/year | Per quarter |
| Quarterly income tax (1702-Q) | 4/year | Per quarter |
| Annual returns (1702-RT, 1604-E, 1604-F, 1604-C) | 4/year total | Per year |
| 2307 issuance reminders | Varies | Per vendor with EWT |

Total seeded per calendar year: approximately 50 BIR task types across all periods.

### How to Re-seed

If tasks are accidentally deleted or a new period needs initialization:

```
Odoo shell or XML-RPC:
model: ipai.finance.close.seed
method: action_seed_period
args: [period_start, period_end]
```

Or via UI: **Accounting > Configuration > Finance Close Seed > Actions > Seed Period**

---

## Module Interaction

```
ipai_finance_close_seed
  → creates project.task records
      → task for each bir.filing.deadline record
          → linked to bir.tax.return via bir.vat.return or bir.withholding.return
              → transitions state: draft → computed → validated → filed → confirmed
```

When a BIR task in the close checklist is moved to Done, it triggers a state validation check on the linked `bir.tax.return`. If the return is not in `filed` or `confirmed` state, the task cannot be marked Done.

---

## Known Model Name Corrections

The Foundry agent instructions (v6) reference the following incorrect module names. Do not use these names — they do not exist:

| Incorrect (do not use) | Correct |
|---|---|
| `ipai_tax_compliance` | `ipai_bir_tax_compliance` |
| `ipai_tax_compliance_vat` | `bir.vat.return` (model within `ipai_bir_tax_compliance`) |
| `ipai_tax_compliance_ewt` | `bir.withholding.return` (model within `ipai_bir_tax_compliance`) |
| `ipai_tax_compliance_payroll` | `bir.withholding.return` with `withholding_type = compensation` |
| `ipai_tax_compliance_audit` | No separate module; audit trail is in `bir.tax.return` chatter |
| `ipai_tax_compliance_reports` | Reporting is part of `ipai_bir_tax_compliance` core |

---

## Future Modules (Not Yet Available)

The following modules are on the roadmap but not yet deployed:

| Planned Module | Phase | Purpose |
|---|---|---|
| `ipai_ai_copilot` (19.0 migration) | Phase 4 | In-ERP sidebar copilot; currently archived at v18.0 |
| OpenAPI bridge (tool definition) | Phase 2 | Expose Odoo read/write actions to Foundry agent |
| `ipai_expense_advanced` | Phase 3 | Concur-like expense and cash advance module |
