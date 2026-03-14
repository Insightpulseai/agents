# Odoo Navigation Guide — InsightPulseAI

**Version:** 1.0.0
**Last updated:** 2026-03-14
**Odoo version:** 19.0 CE
**Use:** Grounding context for InsightPulseAI Foundry copilot. Source label: [IPAI-KB]

---

## Overview

This document is the navigation cheatsheet for the InsightPulseAI Odoo 19 CE instance. It maps common compliance, tax, and accounting tasks to their exact Odoo menu paths.

When a user asks "how do I get to X" or "where do I find Y in Odoo", cite this document with `[IPAI-KB]` and provide the exact path.

**Instance URL:** `erp.insightpulseai.com`
**Access:** Managed identity via Keycloak SSO (`auth.insightpulseai.com`)

---

## Accounting — Vendor Bills and Withholding Tax

| Task | Odoo Path | Notes |
|---|---|---|
| Create vendor bill with EWT | Accounting > Vendors > Bills > New | Set vendor, invoice date, and add bill lines before applying withholding |
| Apply withholding tax to a bill | On the bill form > Withholding Tax field (l10n_ph module) | The Withholding Tax field is provided by the Philippine localization module (`l10n_ph`); select the tax type matching the ATC code |
| Print BIR 2307 (Creditable Tax Certificate) | Accounting > Vendors > Bills > [open bill] > Print > BIR 2307 | Available on validated bills with EWT applied; one 2307 per payee per period |
| View all vendor bills | Accounting > Vendors > Bills | Filter by date range or status (Draft / Posted / Cancelled) |
| Post / validate a vendor bill | On bill form > Confirm button | Must have at least one bill line; posting locks the entry |
| Register payment on a vendor bill | On posted bill > Register Payment button | Select journal, payment date, and amount |
| Create customer invoice | Accounting > Customers > Invoices > New | Standard sales invoice workflow |

---

## Accounting — VAT and Tax Reporting

| Task | Odoo Path | Notes |
|---|---|---|
| Run VAT Declaration (2550M) | Accounting > Reporting > Philippines > VAT Declaration | Select period (month); generates 2550M data for review and export |
| Run VAT Quarterly Return (2550Q) | Accounting > Reporting > Philippines > VAT Quarterly Return | Consolidates three monthly periods into one quarterly return |
| Run SLSP (Summary List of Sales and Purchases) | Accounting > Reporting > Philippines > SLSP | Quarterly; must match period of 2550Q filing |
| View tax audit trail | Accounting > Reporting > Audit Reports > Tax Report | Detailed breakdown of tax entries by period |
| Configure tax rates | Accounting > Configuration > Taxes | Modify tax amounts, ATC codes, and withholding settings |
| Configure ATC codes | Accounting > Configuration > Taxes > [select tax] > ATC field | Set or verify the ATC code on each withholding tax record |
| View chart of accounts | Accounting > Configuration > Chart of Accounts | Standard Philippine CoA installed by `l10n_ph` |
| Run general ledger | Accounting > Reporting > General Ledger | Filter by account, date range, or journal |
| Reconcile bank transactions | Accounting > Accounting > Bank and Cash > [journal] > Reconcile | Match bank statement lines to posted journal entries |

---

## Compliance Module (ipai_bir_tax_compliance)

| Task | Odoo Path | Notes |
|---|---|---|
| View compliance dashboard | Compliance > Dashboard | High-level view of open items, overdue filings, and completion status by period |
| Check open compliance tasks | Compliance > My Tasks | Filtered to current user's assigned tasks; shows due dates and status |
| Create a compliance check | Compliance > Checks > New | Manual check creation; set form type, period, responsible user |
| View all compliance findings | Compliance > Findings | List of all open and closed findings across all periods |
| Upload evidence to a finding | Compliance > Findings > [select record] > Attachments tab | Supports PDF, PNG, JPG; document name and type required |
| View BIR tax returns | Compliance > BIR Returns | Lists all `bir.tax.return` records; filter by state, form type, or period |
| Create a BIR VAT return | Compliance > BIR Returns > New > Select type: VAT | Creates a `bir.vat.return` record; initializes in Draft state |
| Create a BIR withholding return | Compliance > BIR Returns > New > Select type: Withholding | Creates a `bir.withholding.return` record in Draft state |
| View filing deadlines | Compliance > Filing Deadlines | Displays all `bir.filing.deadline` records with computed due dates |
| Filter overdue filings | Compliance > Filing Deadlines > Filter: Overdue | Pre-configured filter showing deadlines past due with unconfirmed status |

---

## Finance Close (ipai_finance_close_seed)

| Task | Odoo Path | Notes |
|---|---|---|
| View month-end close checklist | Project > Projects > [Month-End Close project] | Lists all 39 month-end tasks and 50 BIR filing tasks as `project.task` records |
| Mark a close task complete | Project > Tasks > [select task] > Stage: Done | Move task to Done stage; requires evidence attachment for BIR tasks |
| Assign close task to user | On the task form > Assignees field | Set responsible person per task |
| Filter BIR tasks in close project | Project > Tasks > Filter: Tag = "BIR" | All 50 BIR-specific tasks are tagged for easy isolation |
| View close task by due date | Project > Tasks > Group By: Deadline | Sorts tasks by deadline; critical for period-end visibility |

---

## Configuration and Administration

| Task | Odoo Path | Notes |
|---|---|---|
| Manage users | Settings > Users & Companies > Users | Create, deactivate, and modify user permissions |
| Set up company TIN | Settings > General Settings > Company > Tax ID field | Required for BIR form generation |
| Configure fiscal years | Accounting > Configuration > Fiscal Years | InsightPulseAI uses calendar year (January–December) |
| Install Philippine localization | Apps > [search: Philippines] > l10n_ph | Pre-installed; provides CoA, BIR forms, and ATC framework |
| Configure withholding agents | Accounting > Configuration > Settings > Philippine Localization | Enable automatic withholding agent classification |

---

## Common Workflow: Vendor Bill with EWT

Complete end-to-end path for processing a vendor bill with expanded withholding tax:

1. **Accounting > Vendors > Bills > New**
2. Set Vendor (partner with TIN configured)
3. Set Invoice Date and Bill Reference
4. Add line items (product/account, quantity, unit price)
5. In the Withholding Tax field: select the appropriate EWT tax (e.g., EWT Professional Fee 10% — WC010)
6. Verify computed withholding amount
7. Click **Confirm** to post the bill
8. Click **Register Payment** and set net payment amount (invoice amount minus withheld tax)
9. Print BIR 2307: **Print > BIR 2307** — issue to vendor

---

## Common Workflow: Monthly VAT Filing (2550M)

1. **Accounting > Reporting > Philippines > VAT Declaration**
2. Select period: month/year
3. Review output tax (sales), input tax (purchases), and net VAT due
4. Export to PDF or BIR-prescribed format
5. File via eBIRForms or eFPS before the 20th of the following month
6. Record filing in **Compliance > BIR Returns** — update state to Filed
7. Record payment (if VAT payable) in **Accounting > Accounting > Payments**

---

## Navigation Notes

- **l10n_ph** is the Philippine localization module provided by Odoo CE. It must be active for BIR form menus to appear.
- **ipai_bir_tax_compliance** extends `l10n_ph` with the full compliance workflow (states, findings, deadlines). The Compliance menu is provided by this module.
- **ipai_finance_close_seed** adds the month-end close task list. It uses the standard Project module (`project.task`).
- Menu paths assume the user has Accounting Officer or Compliance Officer role. Some paths require Administrator access.
- The copilot can guide a user to the correct menu path (Navigational mode) but cannot execute Odoo actions directly until the OpenAPI bridge tool is connected (planned Phase 2).
