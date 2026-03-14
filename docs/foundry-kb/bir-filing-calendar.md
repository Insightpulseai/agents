# BIR Filing Calendar — Philippines Tax Compliance

**Version:** 1.0.0
**Last updated:** 2026-03-14
**Scope:** Bureau of Internal Revenue (BIR), Philippines
**Use:** Grounding context for InsightPulseAI Foundry copilot. Source label: [BIR-CALENDAR]

---

## Overview

This document is the canonical reference for all Philippine BIR filing obligations tracked by the InsightPulseAI compliance system. It covers monthly, quarterly, and annual filing requirements across VAT, withholding taxes, payroll, and income tax obligations.

When answering questions about filing deadlines, form numbers, or frequencies, cite this document with the label `[BIR-CALENDAR]`.

---

## Complete BIR Filing Calendar

| Filing | Form | Frequency | Deadline | Notes |
|---|---|---|---|---|
| VAT Declaration | 2550M | Monthly | 20th of following month | For VAT-registered taxpayers with monthly VAT obligations |
| VAT Quarterly Return | 2550Q | Quarterly | 25th of month after quarter-end | Consolidates the three monthly 2550M declarations |
| EWT Remittance | 0619-E | Monthly | 10th of following month | Expanded Withholding Tax (EWT) on income payments |
| EWT Annual Alphalist | 1604-E | Annual | March 1 | Annual alphalist of payees subject to EWT |
| FWT Remittance | 0619-F | Monthly | 10th of following month | Final Withholding Tax (FWT) on passive income |
| FWT Annual Alphalist | 1604-F | Annual | January 31 | Annual alphalist of payees subject to FWT |
| Creditable Tax Certificate | 2307 | Per transaction | With payment | Issued to payees; must accompany payment of EWT |
| WVAT Remittance | 1600 | Monthly | 10th of following month | Withholding VAT (WVAT) for government or franchise payments |
| Expanded WVAT | 1600-WP | Monthly | 10th of following month | Withholding VAT for non-resident payees |
| Income Tax (Corporate) | 1702-RT | Annual | 15th day of 4th month after FYE | For regular corporations on calendar year: April 15 |
| Quarterly Income Tax | 1702-Q | Quarterly | 60 days after quarter-end | Quarterly income tax return for corporations |
| SLSP | N/A (summary list) | Quarterly | 25th of month after quarter-end | Summary List of Sales and Purchases; filed with 2550Q |
| SAWT/QAP | 2307 summary | Quarterly | With 2550Q | Summary Alphalist of Withholding Taxes; accompanies 2550Q |
| Payroll Tax | 1601-C | Monthly | 10th of following month | Withholding of Compensation tax remittance |
| Annual Payroll Alphalist | 1604-C | Annual | January 31 | Annual alphalist of employees with compensation income |

---

## Deadline Quick Reference by Day

### 10th of following month (monthly remittances)
- 0619-E — EWT Remittance
- 0619-F — FWT Remittance
- 1600 — WVAT Remittance
- 1600-WP — Expanded WVAT Remittance
- 1601-C — Payroll Tax (Withholding of Compensation)

### 20th of following month
- 2550M — VAT Declaration (monthly)

### 25th of month after quarter-end
- 2550Q — VAT Quarterly Return
- SLSP — Summary List of Sales and Purchases

### January 31 (annual)
- 1604-F — FWT Annual Alphalist
- 1604-C — Annual Payroll Alphalist

### March 1 (annual)
- 1604-E — EWT Annual Alphalist

### 15th day of 4th month after fiscal year-end (annual)
- 1702-RT — Corporate Annual Income Tax Return
- Calendar-year corporations: April 15

### 60 days after quarter-end (quarterly)
- 1702-Q — Quarterly Income Tax Return

### Per transaction (event-triggered)
- 2307 — Creditable Tax Certificate; must be issued at time of payment

---

## Quarterly Schedule Reference

Philippine fiscal quarters (calendar year):

| Quarter | Period | 2550Q/SLSP Due | 1702-Q Due |
|---|---|---|---|
| Q1 | January – March | April 25 | May 29 |
| Q2 | April – June | July 25 | August 29 |
| Q3 | July – September | October 25 | November 29 |
| Q4 | October – December | January 25 (following year) | March 1 (following year) |

---

## Tax Type Glossary

| Abbreviation | Full Name | Description |
|---|---|---|
| VAT | Value Added Tax | 12% tax on sale of goods and services by VAT-registered entities |
| EWT | Expanded Withholding Tax | Creditable withholding tax deducted at source by withholding agents |
| FWT | Final Withholding Tax | Full and final tax on specific passive income; payee cannot claim credit |
| WVAT | Withholding VAT | VAT withheld by government agencies and corporations on purchases |
| BIR | Bureau of Internal Revenue | Philippine national tax authority |
| TIN | Taxpayer Identification Number | Unique identifier issued by BIR |
| FYE | Fiscal Year End | End of accounting period |
| SLSP | Summary List of Sales and Purchases | Quarterly summary submitted with VAT return |
| SAWT | Summary Alphalist of Withholding Taxes | Quarterly summary of withholding taxes claimed as tax credit |
| QAP | Quarterly Alphalist of Payees | Quarterly alphalist accompanying 0619-E and 0619-F |

---

## Filing Penalties (Reference)

| Violation | Penalty |
|---|---|
| Late filing | 25% surcharge on tax due + 12% annual interest + compromise penalty |
| Non-filing | 50% surcharge on tax due + 12% annual interest + criminal liability exposure |
| Late payment | 12% annual interest on unpaid amount |
| Failure to withhold | Withholding agent liable for the unwithheld amount |

Penalties are governed by the National Internal Revenue Code (NIRC) as amended by the Tax Reform for Acceleration and Inclusion Act (TRAIN Law, RA 10963) and subsequent BIR Revenue Regulations.

---

## Integration Notes (InsightPulseAI)

The following Odoo modules implement these filing deadlines:

- **`ipai_bir_tax_compliance`** (v19.0.1.0.0): Contains the `bir.filing.deadline` model which tracks all 36 BIR form types, their frequencies, and computed due dates. Deadlines are auto-calculated from period end dates.
- **`ipai_finance_close_seed`** (v19.0.1.0.0): Seeds 50 BIR-specific filing tasks into `project.task` as part of the month-end close checklist.

When a user asks about the status of a specific filing, direct them to: **Compliance > My Tasks** in Odoo, filtered by the relevant BIR form number.
