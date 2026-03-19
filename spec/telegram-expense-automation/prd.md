# PRD — Telegram Expense + Invoice Automation

## Summary

Enable users to submit receipts, invoices, and supporting finance documents via Telegram. The platform ingests files, performs OCR and structured extraction using Azure Document Intelligence, uses Foundry agents for validation and clarification, creates draft-stage Odoo records, and exposes review/approval context via Odoo Copilot.

## Problem

Expense and AP intake currently depends on fragmented channels, manual re-entry, delayed clarification, and inconsistent attachment-to-transaction linkage. Finance teams lose time reconciling low-quality images, incomplete metadata, duplicate submissions, and ambiguous routing.

## Goals

- Reduce manual intake effort for expense receipts and supplier invoices
- Standardize document ingestion from Telegram into Odoo draft objects
- Use OCR + agentic clarification to improve completeness before finance review
- Preserve auditability across source file, extraction, reasoning, and ERP state
- Keep Odoo as transactional source of record

## Non-Goals (v1)

- Autonomous posting of journal entries
- Full vendor onboarding
- Full tax determination automation
- End-to-end payment execution
- Unsupported document types beyond defined receipt/invoice classes

## Personas

| Persona | Role |
|---|---|
| Employee | Submits reimbursable expenses via Telegram |
| AP Reviewer | Processes supplier invoices in Odoo review queue |
| Finance Approver | Reviews exceptions and high-value items |
| Operations/Admin | Monitors intake pipeline and failures |

## Primary User Stories

1. As an employee, I can send a receipt photo or PDF to Telegram and receive confirmation that a draft expense was created or that more data is needed.
2. As an AP reviewer, I can receive a draft vendor bill in Odoo with extracted fields, source attachment, confidence state, and exception flags.
3. As a finance approver, I can review material invoices with summarized risk and missing-field context before approval.
4. As an operator, I can trace a Telegram submission end-to-end across OCR, Foundry, and Odoo.

## Functional Requirements

### Intake

- Accept Telegram file uploads: image, PDF, and supported document attachments
- Persist source file and intake metadata before downstream processing
- Capture Telegram sender, chat id, message id, timestamp, caption/text, and attachment ids

### Classification and Extraction

- Classify documents into at minimum:
  - receipt
  - invoice
  - official_receipt
  - unsupported
- Run Azure Document Intelligence extraction using prebuilt models where applicable
- Store raw OCR/extraction payloads for replay and troubleshooting
- Normalize all extracted fields into a canonical document schema

### Clarification and Orchestration

- Invoke Foundry agent when:
  - required fields are missing
  - confidence is below threshold
  - duplicate suspicion exists
  - routing is ambiguous
- Agent may ask the user follow-up questions in Telegram
- Agent must not finalize accounting records beyond allowed draft/update actions

### Odoo Integration

- Create draft `hr.expense` or equivalent expense object for employee receipts
- Create draft `account.move` vendor bill or equivalent AP object for supplier invoices
- Attach original source file and normalized extraction summary to the Odoo record
- Link correlation ids back into Odoo metadata / chatter / audit fields
- Route to finance review queue when required

### Copilot Review Surface

- Odoo Copilot must display:
  - extracted summary
  - confidence
  - exception flags
  - duplicate suspicion
  - missing required fields
  - recommended next action
- Copilot may explain why a record is blocked or routed for human review

### Risk Gating

Documents must be routed using:

| Band | Criteria | Action |
|---|---|---|
| Green | high-confidence, complete, matched, below approval threshold | auto-create draft |
| Yellow | missing fields, low confidence, ambiguous routing | clarification / review |
| Red | duplicate suspicion, high value, unsupported tax or vendor mismatch | manual approval required |

## Canonical Normalized Schema

```yaml
document_id:
correlation_id:
source_channel: telegram
telegram_chat_id:
telegram_message_id:
telegram_file_id:
sender_identity:
document_type:
document_type_confidence:
legal_entity:
employee_contact:
vendor_name:
vendor_tax_id:
invoice_number:
receipt_number:
transaction_date:
due_date:
currency:
subtotal:
tax_amount:
total_amount:
line_items: []
project_code:
cost_center:
department:
payment_method:
reimbursable:
confidence_score:
completeness_score:
duplicate_suspected:
exception_flags: []
extraction_model:
raw_ocr_payload_ref:
source_file_ref:
foundry_trace_id:
review_status:
odoo_target_model:
odoo_target_id:
```

## Workflow Definitions

### Workflow A: Employee Receipt

1. User sends receipt image/PDF to Telegram
2. Intake service stores file + metadata
3. OCR extraction runs
4. Normalization occurs
5. Foundry asks for missing project/cost center if needed
6. Draft expense is created in Odoo
7. User receives Telegram confirmation

### Workflow B: Supplier Invoice

1. User or vendor contact sends invoice PDF to Telegram
2. Intake service stores file + metadata
3. OCR extraction runs
4. Vendor match + duplicate check executes
5. Draft vendor bill is created or held for review
6. AP team sees structured draft in Odoo Copilot/review queue

### Workflow C: Exception Handling

1. OCR confidence or completeness falls below threshold
2. Foundry asks clarification questions in Telegram
3. Answers update normalized payload
4. Record is retried for Odoo draft creation or sent to manual review

## Acceptance Criteria

- Telegram submission creates a durable intake event and file record
- OCR output is normalized into the canonical schema
- Draft Odoo record is created for supported high-confidence documents
- Low-confidence or incomplete documents enter clarification/review flow
- Each transaction is traceable from Telegram to Odoo
- Odoo Copilot surfaces structured review context for finance users

## Success Metrics

| Metric | Description |
|---|---|
| Auto-draft rate | % of supported documents reaching auto-draft creation |
| Clarification rate | % of documents requiring Foundry follow-up |
| Manual review rate | % of documents routed to human review |
| Duplicate detection rate | % of true duplicates caught before draft creation |
| Intake-to-draft latency | Average time from submission to draft creation |
| Trace completeness | % of records with full correlation chain present |

## Cross-References

- [Odoo Copilot Agent Framework PRD](../odoo-copilot-agent-framework/prd.md) — Copilot agent roles and capability classes
- [Odoo Copilot Agent Framework Constitution](../odoo-copilot-agent-framework/constitution.md) — agent write boundaries
- SSOT integration: `ssot/integrations/telegram_expense_automation.yaml`
- SSOT contract: `ssot/contracts/document_ingestion/normalized_finance_document.yaml`
