# Compliance Module State Machines

**Version:** 1.0.0
**Last updated:** 2026-03-14
**Odoo version:** 19.0 CE
**Module:** ipai_bir_tax_compliance
**Use:** Grounding context for InsightPulseAI Foundry copilot. Source label: [IPAI-KB]

---

## Overview

This document defines the complete state machines for all compliance-related models in the `ipai_bir_tax_compliance` module. Each section covers the model's states, allowed transitions, triggering actions, required fields per state, and error conditions.

Use this document when a user asks about the current state of a return, why a transition failed, or what they need to do to move a record forward.

---

## Model 1: bir.tax.return (Master Compliance Record)

The `bir.tax.return` model is the root record for every BIR filing obligation. All form-specific models (`bir.vat.return`, `bir.withholding.return`) inherit from or relate to this base model.

### State Diagram

```
[draft] ──→ [computed] ──→ [validated] ──→ [filed] ──→ [confirmed]
               ↑                ↑
               │ reset_to_draft  │ reset_to_draft
               └────────────────┘
```

### State Definitions

| State | Internal Name | Description |
|---|---|---|
| Draft | `draft` | Period initialized. No amounts computed. Awaiting data from Odoo accounting. |
| Computed | `computed` | Amounts pulled from accounting entries. Tax due calculated. Awaiting review. |
| Validated | `validated` | Finance Manager reviewed and approved for external filing. Ready for BIR submission. |
| Filed | `filed` | Filed with BIR via eBIRForms, eFPS, or manual filing. Awaiting payment confirmation. |
| Confirmed | `confirmed` | Payment made and evidence (receipt, BIR stamp, 2307 copy) attached. Period closed. |

### Allowed Transitions

| From | To | Action Name | Who Can Execute | Conditions |
|---|---|---|---|---|
| `draft` | `computed` | Compute Return | Compliance Officer, Finance Manager | Accounting period must be posted; `period_start` and `period_end` set |
| `computed` | `validated` | Validate Return | Finance Manager, Administrator | `amount_due` must be non-negative; no unreconciled discrepancies |
| `validated` | `filed` | Mark as Filed | Compliance Officer, Finance Manager | `filed_date` must be set; `filing_reference` recommended |
| `filed` | `confirmed` | Confirm Filing | Finance Manager, Administrator | `amount_paid` must equal `amount_due` (or zero if no payment due); evidence attachment required |
| `validated` | `draft` | Reset to Draft | Finance Manager, Administrator | Allowed only for amendments; creates audit log entry |
| `filed` | `draft` | Reset to Draft | Administrator only | Restricted action; requires justification text in `reset_reason` field |

### Required Fields by State

| State | Required Fields | Optional but Recommended |
|---|---|---|
| `draft` | `form_type`, `period_start`, `period_end`, `company_id`, `responsible_id` | `due_date` (auto-computed from `bir.filing.deadline`) |
| `computed` | All draft fields + `amount_due` | `tax_basis`, computation notes in chatter |
| `validated` | All computed fields + `validated_by`, `validated_date` | Variance notes if `amount_due` differs from prior period |
| `filed` | All validated fields + `filed_date` | `filing_reference` (eFPS confirmation number), `filing_channel` |
| `confirmed` | All filed fields + `amount_paid`, `payment_date` | Receipt attachment, `confirmation_number` |

### Error Conditions

| Error | Cause | Resolution |
|---|---|---|
| Cannot compute: period not closed | Journal entries in period are still in draft | Post all journal entries in the period via Accounting > Journal Entries |
| Cannot validate: amount mismatch | Computed amount differs from expected by >5% | Review computation source; reconcile with trial balance |
| Cannot file: no filed_date | `filed_date` field is empty | Set the actual date the return was submitted to BIR |
| Cannot confirm: payment missing | `amount_paid` is zero but `amount_due` > 0 | Register payment in Accounting and link to this return |
| Cannot reset: unauthorized | Current user role is Compliance Officer (no reset permission) | Request Finance Manager or Administrator to perform reset |

---

## Model 2: bir.vat.return

Extends `bir.tax.return` for VAT-specific returns (2550M monthly, 2550Q quarterly).

### Additional States (Extends Base)

`bir.vat.return` uses the same 5-state machine as `bir.tax.return` with the following additional constraints:

### State Transitions — VAT Specific

| Transition | Additional Conditions |
|---|---|
| `draft` → `computed` | All posted sales invoices and vendor bills in the period must have VAT journal entries; no unreconciled VAT accounts |
| `computed` → `validated` | Output VAT, input VAT, and net VAT due must all be non-null; SLSP data must be generated if quarterly |
| `validated` → `filed` | For 2550Q: corresponding 2550M returns for the quarter's months must be in `filed` or `confirmed` state |
| `filed` → `confirmed` | If net VAT due > 0: payment must be registered; if overpayment: carryforward or refund route must be selected |

### Required Fields — VAT Extension

| State | Additional Required Fields |
|---|---|
| `computed` | `output_vat`, `input_vat`, `net_vat_due`, `period_type` (`monthly` or `quarterly`) |
| `validated` | `slsp_generated` (boolean, True if SLSP report generated); for quarterly only |
| `filed` | `vat_payment_mode` (`efps`, `ebirforms`, `manual`) |

### VAT Carryforward Logic

If `net_vat_due` < 0 (input VAT exceeds output VAT), the record enters an additional sub-status:

- `excess_input_vat`: amount available for carryforward to next period
- `refund_applied`: taxpayer applied for cash refund (requires BIR LOA)
- `carryforward_applied`: excess applied to next period's output VAT

This sub-status is recorded in `vat_disposition` field. It does not block the main state transition to `confirmed`.

---

## Model 3: bir.withholding.return

Extends `bir.tax.return` for withholding tax remittance returns (0619-E, 0619-F, 1601-C).

### Withholding Type

Each `bir.withholding.return` has a `withholding_type` field:

| `withholding_type` | Form | ATC Group | Description |
|---|---|---|---|
| `ewt` | 0619-E | WC*, WB*, WM*, WI* | Expanded Withholding Tax on income payments |
| `fwt` | 0619-F | WF* | Final Withholding Tax on passive income |
| `compensation` | 1601-C | WC001 | Withholding of Compensation (payroll tax) |

### State Transitions — Withholding Specific

| Transition | Additional Conditions |
|---|---|
| `draft` → `computed` | All vendor bills with withholding tax in the period must be posted; EWT entries reconciled |
| `computed` → `validated` | `total_tax_withheld` must match sum of withholding tax journal entries for the period; QAP/alphalist count verified |
| `validated` → `filed` | 2307 certificates must have been issued to all payees with EWT deductions in the period |
| `filed` → `confirmed` | Remittance payment registered; bank confirmation or eFPS receipt attached |

### Required Fields — Withholding Extension

| State | Additional Required Fields |
|---|---|
| `computed` | `withholding_type`, `total_tax_withheld`, `payee_count` |
| `validated` | `alphalist_ids` (linked payee alphalist records); `2307_issued_all` boolean flag |
| `filed` | `remittance_date` (actual payment date to BIR), `remittance_channel` |
| `confirmed` | `remittance_receipt` (attachment), `bank_reference` |

### Alphalist Model

The `bir.withholding.alphalist` model stores per-payee withholding data linked to each `bir.withholding.return`:

| Field | Description |
|---|---|
| `return_id` | FK to `bir.withholding.return` |
| `partner_id` | Vendor / payee |
| `tin` | Taxpayer Identification Number |
| `atc_code` | ATC code used |
| `gross_amount` | Gross payment amount |
| `tax_withheld` | Amount withheld |
| `2307_issued` | Boolean: 2307 certificate issued to this payee |

---

## Model 4: bir.filing.deadline

Manages the registry of computed filing deadlines. Read-only in normal workflow — used as a source for task seeding and overdue alerts.

### States

| State | Description |
|---|---|
| `pending` | Deadline is in the future; filing not yet initiated |
| `in_progress` | A `bir.tax.return` record exists in `draft` or `computed` state for this deadline |
| `filed` | Linked `bir.tax.return` is in `filed` or `confirmed` state |
| `overdue` | `computed_due_date` has passed and linked return is not in `filed` or `confirmed` state |

### State Transition Rules

```
[pending] ──→ [in_progress]  (when bir.tax.return created for this period)
[pending] ──→ [overdue]       (when computed_due_date < today and no return filed)
[in_progress] ──→ [filed]     (when linked bir.tax.return reaches filed or confirmed)
[in_progress] ──→ [overdue]   (when computed_due_date passes and return not filed)
[overdue] ──→ [filed]         (late filing — return filed after deadline)
```

### Required Fields

| Field | Type | Description |
|---|---|---|
| `form_type` | Selection | BIR form identifier (2550M, 0619-E, etc.) |
| `frequency` | Selection | `monthly`, `quarterly`, `annual`, `per_transaction` |
| `reference_period` | Date | Period start date |
| `computed_due_date` | Date | Automatically computed from `reference_period` + frequency rules |
| `state` | Selection | `pending`, `in_progress`, `filed`, `overdue` |
| `is_overdue` | Boolean | Computed field: True if `computed_due_date` < today and state not `filed` |
| `bir_return_id` | M2O | Linked `bir.tax.return` (optional until return created) |

---

## State Machine Summary

### Quick Reference — All Models

| Model | States | Entry State | Terminal State |
|---|---|---|---|
| `bir.tax.return` | draft, computed, validated, filed, confirmed | `draft` | `confirmed` |
| `bir.vat.return` | (inherits base) + vat_disposition sub-status | `draft` | `confirmed` |
| `bir.withholding.return` | (inherits base) | `draft` | `confirmed` |
| `bir.filing.deadline` | pending, in_progress, filed, overdue | `pending` | `filed` |

### State Lock Rules

- **No backward transition** without Finance Manager or Administrator role
- **No skip transitions** (cannot jump from `draft` to `filed` directly)
- **Overdue flag** on `bir.filing.deadline` is read-only computed; it cannot be manually cleared
- **Confirmed returns are immutable**: amendments require creating a new amended return record with link to original

---

## Diagnosing State Issues

When a user reports a compliance record is "stuck", follow this decision tree:

```
Record is in 'draft' and cannot compute?
  → Check: are all journal entries for the period posted?
  → Check: is period_start and period_end set correctly?

Record is in 'computed' and cannot validate?
  → Check: is the user role Finance Manager or higher?
  → Check: does amount_due match the trial balance?

Record is in 'validated' and cannot file?
  → Check: is filed_date field populated?
  → For 2550Q: are all three 2550M returns for the quarter filed?

Record is in 'filed' and cannot confirm?
  → Check: is amount_paid set and does it equal amount_due?
  → Check: is there at least one attachment (receipt/evidence)?

Filing deadline shows 'overdue' but return was filed?
  → Check: is the linked bir.tax.return in 'filed' or 'confirmed' state?
  → If return exists but is still 'validated': transition it to 'filed'
```
