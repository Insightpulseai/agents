# ATC Codes Reference — Philippines Withholding Tax

**Version:** 1.0.0
**Last updated:** 2026-03-14
**Scope:** Bureau of Internal Revenue (BIR), Philippines — Alphanumeric Tax Code (ATC) reference
**Use:** Grounding context for InsightPulseAI Foundry copilot. Source label: [IPAI-KB]

---

## Overview

Alphanumeric Tax Codes (ATCs) are BIR-assigned identifiers that classify each type of withholding tax transaction. Every withholding tax entry in Odoo must be tagged with the correct ATC code. The ATC determines the applicable rate, BIR form, and reporting category.

When a user asks "what ATC code should I use for [transaction type]", reference this document. Cite as `[IPAI-KB]`.

---

## ATC Code Reference Table

### Expanded Withholding Tax (EWT) — Form 0619-E / 1604-E

| ATC Code | Full Name | Rate | Tax Type | BIR Form | Common Use Case |
|---|---|---|---|---|---|
| WC010 | EWT on professional fees — individuals | 10% | EWT | 0619-E, 2307 | Payments to lawyers, CPAs, consultants, doctors, and other licensed professionals who are individuals |
| WC011 | EWT on professional fees — non-individuals | 15% | EWT | 0619-E, 2307 | Payments to professional service firms, law firms, accounting firms |
| WC158 | EWT on labor and materials — contractors | 2% | EWT | 0619-E, 2307 | Payments to contractors and sub-contractors for construction or installation work; also applies to service contracts involving both labor and materials |
| WC080 | EWT on rental — real property | 5% | EWT | 0619-E, 2307 | Monthly or annual rent payments to lessors of real property (land, buildings, warehouses, offices) |
| WB010 | EWT on purchases of goods from regular suppliers | 1% | EWT | 0619-E, 2307 | Purchases of goods from regular suppliers where the withholding agent is a top 20,000 or other classified corporation |
| WB011 | EWT on purchases of services from regular suppliers | 2% | EWT | 0619-E, 2307 | Purchases of services from regular suppliers; applies broadly to service invoices not covered by a more specific ATC |
| WI010 | EWT on interest income — bank deposits | 20% | EWT (creditable) | 0619-E, 2307 | Interest earned on bank deposits; withheld by the depository institution at source |
| WC120 | EWT on commissions — regular | 10% | EWT | 0619-E, 2307 | Commissions paid to agents or brokers who are individuals; covers sales commissions, real estate broker fees |
| WC122 | EWT on talent fees — individuals | 10% | EWT | 0619-E, 2307 | Payments to entertainers, TV personalities, musicians, athletes, and other talent on a per-performance or engagement basis |
| WC150 | EWT on payments to medical practitioners | 10% | EWT | 0619-E, 2307 | Payments to doctors and medical professionals for services rendered (distinct from professional fees in some BIR rulings) |
| WC160 | EWT on gross receipts of proprietors of hospitals | 15% | EWT | 0619-E, 2307 | Payments to hospital owners/proprietors for use of facilities |
| WM001 | EWT on management fees | 15% | EWT | 0619-E, 2307 | Management service fees paid to a non-resident foreign corporation's Philippine branch or related party |

---

### Final Withholding Tax (FWT) — Form 0619-F / 1604-F

| ATC Code | Full Name | Rate | Tax Type | BIR Form | Common Use Case |
|---|---|---|---|---|---|
| WF001 | FWT on cash dividends — resident individual | 10% | FWT | 0619-F, 2306 | Cash dividends declared and paid to Filipino individual shareholders |
| WF002 | FWT on property dividends — resident individual | 10% | FWT | 0619-F, 2306 | Property dividends distributed to resident individual shareholders |
| WF120 | FWT on dividends — non-resident alien | 15% | FWT | 0619-F, 2306 | Dividends remitted to non-resident alien individuals (reduced rate subject to tax treaty eligibility) |
| WF130 | FWT on dividends — non-resident foreign corporation | 15% | FWT | 0619-F, 2306 | Dividends remitted to non-resident foreign corporations (subject to tax treaty) |
| WF040 | FWT on royalties | 20% | FWT | 0619-F, 2306 | Royalties paid for use of intellectual property, patents, trademarks, or literary/musical works |
| WF050 | FWT on prizes exceeding PHP 10,000 | 20% | FWT | 0619-F, 2306 | Monetary prizes from competitions, raffles, or promotions exceeding the PHP 10,000 threshold |
| WF060 | FWT on winnings | 20% | FWT | 0619-F, 2306 | Gambling or lottery winnings (PCSO winnings above PHP 10,000) |

---

### Withholding VAT (WVAT) — Form 1600 / 1600-WP

| ATC Code | Full Name | Rate | Tax Type | BIR Form | Common Use Case |
|---|---|---|---|---|---|
| WE001 | WVAT on purchases of goods — government | 5% | WVAT | 1600 | VAT withheld by government agencies (national and local) on purchases of goods from VAT-registered sellers; 5% is the applicable portion of the 12% VAT |
| WE002 | WVAT on purchases of services — government | 5% | WVAT | 1600 | VAT withheld by government agencies on purchases of services from VAT-registered suppliers |
| WE003 | WVAT on lease of real property — government | 5% | WVAT | 1600 | VAT withheld by government agencies on rental payments to real property lessors |

---

## ATC Code Selection Decision Tree

Use this logic to select the correct ATC code when entering a vendor bill or payment:

```
Is the payment to a GOVERNMENT agency as buyer/payor?
  YES → Use WE001 (goods), WE002 (services), or WE003 (lease) — WVAT
  NO  → Continue below

Is the payment a DIVIDEND, ROYALTY, PRIZE, or INTEREST on deposit?
  YES → Use appropriate FWT code (WF001, WF040, WF050, WI010)
  NO  → Continue below

What type of EWT applies?
  Professional fee (individual)       → WC010 (10%)
  Professional fee (non-individual)   → WC011 (15%)
  Contractor / construction service   → WC158 (2%)
  Rental of real property             → WC080 (5%)
  Purchase of goods (regular supplier)→ WB010 (1%)
  Purchase of services (general)      → WB011 (2%)
  Commission to individual            → WC120 (10%)
  Talent fee                          → WC122 (10%)
  Management fee (related party)      → WM001 (15%)
```

---

## Common Errors and Corrections

| Mistake | Correct Approach |
|---|---|
| Using WC010 for a law firm invoice | Law firms are non-individuals; use WC011 (15%) |
| Using WB011 for a lease payment | Lease payments use WC080 (5%); WB011 is for general service purchases |
| Using WF001 for dividends to a foreign company | Foreign corporation dividends use WF130 (15%), not WF001 |
| Applying WE001 for private-sector purchases | WE001 is only for government agencies as the payor; private entities use WB010/WB011 |
| Omitting 2307 issuance | A BIR 2307 Creditable Tax Certificate must be issued to the payee for every EWT deduction |

---

## Odoo Configuration

ATC codes are configured at the tax level in Odoo:

**Path:** Accounting > Configuration > Taxes > [select tax] > ATC field

The `ipai_bir_tax_compliance` module provides pre-configured tax records with correct ATC assignments. Do not modify the ATC field on existing tax records without a compliance review.

To verify an ATC assignment on a vendor bill:
1. Open the bill in Accounting > Vendors > Bills
2. Inspect the Withholding Tax field on each line
3. The ATC code is visible in the tax configuration linked from that field

---

## Regulatory Basis

ATC codes are defined and updated by the BIR through Revenue Regulations. Key regulations:

| Regulation | Scope |
|---|---|
| RR 2-98 (as amended) | Expanded Withholding Tax rules |
| RR 12-2001 (as amended) | Final Withholding Tax on passive income |
| RR 1-2012 | Withholding VAT on government purchases |
| TRAIN Law (RA 10963) | Rate adjustments effective 2018 |
| RR 11-2018 | TRAIN Law implementing rules for withholding |
