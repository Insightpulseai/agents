# Implementation Plan — Telegram Expense + Invoice Automation

## Architecture Boundaries

### Components

| Component | Technology | Responsibility |
|---|---|---|
| Telegram Bot / Webhook | Azure Function or Container App | Intake, acknowledgements, clarification dialog |
| File Persistence | Azure Blob Storage | Immutable source file retention |
| Document Intelligence Adapter | Azure Document Intelligence SDK | OCR, field extraction, classification |
| Normalization Layer | Internal service | Map extraction output to canonical schema |
| Foundry Orchestrator | Azure AI Foundry Agent Service | Reasoning, clarification, routing, policy enforcement |
| Odoo Connector Tools | MCP tools (`odoo.*` namespace) | Draft record creation, attachment, audit metadata |
| Odoo Copilot Surface | `ipai-odoo-copilot-advisory` / `ipai-odoo-copilot-actions` | ERP-native explanation and decision support |
| Observability | Foundry tracing + Application Insights | Audit, debugging, evaluation |

### Responsibility Split

- **Telegram**: intake edge, user-facing status, clarification relay
- **Document Intelligence**: OCR + structured field extraction
- **Foundry**: reasoning, clarification, confidence gating, routing, policy enforcement
- **Odoo**: transactional persistence, approval workflow, source of record
- **Copilot**: ERP-native explanation and review surface

## Proposed Service Contracts

### Intake Contract

```
Input:
  - telegram_message (text, file, or both)
  - sender metadata (user id, chat id, timestamp)
  - file metadata (file id, mime type, size)
  - optional caption text

Output:
  - correlation_id
  - stored_file_ref
  - intake_event (persisted)
```

### Extraction Contract

```
Input:
  - stored_file_ref
  - declared/source hints (caption, sender context)

Output:
  - document_type
  - document_type_confidence
  - extracted_fields (canonical schema)
  - confidence_score
  - completeness_score
  - raw_ocr_payload_ref
```

### Orchestration Contract

```
Input:
  - normalized_document
  - policy thresholds (confidence, amount, completeness)
  - vendor/employee matching results
  - duplicate check results

Output:
  - routing_band (green | yellow | red)
  - action_decision (create_draft | clarify | hold_for_review)
  - clarification_questions (if yellow)
  - route_target (odoo model + queue)
  - foundry_trace_id
```

### Odoo Write Contract

**Allowed actions in v1:**
- Create draft `hr.expense`
- Create draft `account.move` (vendor bill)
- Update draft expense/vendor bill fields
- Attach source document to record
- Append audit note / chatter metadata
- Write correlation ids to record metadata

**Disallowed actions in v1:**
- Post journal entries
- Execute payments
- Mutate production configuration
- Delete or archive records
- Bypass approval workflow

## Data Model Additions

### Intake/Audit Model

Introduce a durable intake audit record (Supabase or equivalent) for:

| Field | Purpose |
|---|---|
| correlation_id | Primary linkage key |
| telegram_message_id | Source message reference |
| telegram_file_id | Source file reference |
| stored_file_ref | Blob storage path |
| ocr_result_ref | Extraction result reference |
| foundry_trace_id | Foundry run/trace reference |
| odoo_target_model | Target Odoo model name |
| odoo_target_id | Target Odoo record id |
| routing_band | green / yellow / red |
| review_status | pending / in_review / approved / rejected |
| exception_flags | Array of exception identifiers |
| retry_count | Number of processing attempts |
| created_at | Intake timestamp |
| updated_at | Last state change |

## Phases

### Phase 1 — Intake + OCR + Draft Creation

- Telegram webhook ingestion
- Source file persistence to Azure Blob
- OCR extraction for receipts and invoices (prebuilt models)
- Normalized schema mapping
- Odoo draft expense/vendor bill creation via `odoo.*` MCP tools
- Source file attachment to Odoo record
- Basic status reply to Telegram
- Idempotency handling for repeated Telegram deliveries

### Phase 2 — Clarification + Exception Routing

- Foundry clarification loop (missing fields, ambiguous routing)
- Duplicate detection (invoice number + amount + date + vendor hash)
- Vendor matching against Odoo `res.partner`
- Employee/sender identity mapping
- Green/yellow/red routing enforcement
- Finance review queue in Odoo
- Copilot exception summaries

### Phase 3 — Approval Surfaces + Quality Controls

- Approval packet summaries for high-value invoices
- Threshold-based routing to designated approvers
- Monitoring dashboards (intake volume, failure rate, review rate, auto-draft rate)
- Replay tooling for failed extractions
- Evaluation harness for extraction accuracy and routing correctness
- End-to-end trace completeness audits

## Guardrails

- Draft-only writes for v1 — no journal posting
- Full correlation ids mandatory on every record
- Immutable source file retention — no deletion after intake
- Retry-safe idempotent record creation (dedup by correlation_id)
- No silent drops — every failure produces a visible Telegram status or review queue entry
- Unsupported document types return a clear rejection message, not silent failure

## Cross-References

- [Odoo Copilot Agent Framework Plan](../odoo-copilot-agent-framework/plan.md)
- [MCP Core Tools — odoo namespace](../../mcp-ipai-core/src/tools/odoo.ts)
- [Odoo Expense Core Addon](../../odoo/addons/ipai_expense_core/)
- [OCR-to-Odoo Expense Workflow](../../workflows/ocr-to-odoo-expense.json)
