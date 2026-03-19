# Telegram Expense + Invoice Automation

## Purpose

Operational intake edge for finance documents using Telegram, Azure Document Intelligence, Foundry orchestration, and Odoo draft creation.

## Core Rule

Telegram is an intake channel, not a ledger. Odoo is the transactional source of record. All financial writes are draft-only in v1.

## System Flow

```
Telegram Bot
  -> Webhook / Intake Service
  -> File Store (Azure Blob)
  -> Document Intelligence (OCR + Extraction)
  -> Normalization Layer (Canonical Schema)
  -> Foundry Agent (Validation + Routing + Clarification)
  -> Odoo Connector Tools (Draft Creation + Attachment)
  -> Odoo Copilot (Review + Explanation Surface)
  -> Observability (Foundry Tracing + App Insights)
```

## Correlation Chain

Every submission maintains an immutable linkage:

```
telegram_message_id / telegram_file_id
  -> stored_file_ref (Azure Blob)
  -> ocr_result_ref (Document Intelligence output)
  -> foundry_trace_id (Foundry agent run)
  -> odoo_target_model / odoo_target_id (Odoo record)
  -> review/approval events
```

## Routing Bands

| Band | Criteria | Action |
|---|---|---|
| Green | High confidence, complete, matched, below threshold | Auto-create draft |
| Yellow | Missing fields, low confidence, ambiguous | Clarification / review |
| Red | Duplicate, high value, vendor mismatch, unsupported | Manual approval required |

## Key Constraints

- Draft-only writes in v1 — no autonomous journal posting
- Full correlation chain required on every record
- Immutable source file retention
- Human approval for all material exceptions
- Foundry handles reasoning, Document Intelligence handles extraction — no overlap

## Component Responsibilities

| Component | Scope |
|---|---|
| Telegram Bot | Intake, status, clarification relay |
| Document Intelligence | OCR, field extraction, classification |
| Foundry Agent | Orchestration, reasoning, routing, policy |
| Odoo Connector | Draft writes, attachment, audit metadata |
| Odoo Copilot | Review surface, exception explanation |

## Related Specs

- [Spec Bundle](../../spec/telegram-expense-automation/)
- [SSOT Integration](../../ssot/integrations/telegram_expense_automation.yaml)
- [SSOT Contract](../../ssot/contracts/document_ingestion/normalized_finance_document.yaml)
- [Odoo Copilot Agent Framework](../../spec/odoo-copilot-agent-framework/)
- [MCP Odoo Tools](../../mcp-ipai-core/src/tools/odoo.ts)
- [Odoo Expense Core](../../odoo/addons/ipai_expense_core/)
