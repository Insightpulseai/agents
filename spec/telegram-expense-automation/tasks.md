# Tasks — Telegram Expense + Invoice Automation

## Phase 1 — Intake + OCR + Draft Creation

- [ ] Define Telegram webhook intake contract
- [ ] Implement Telegram bot webhook handler (Azure Function or Container App)
- [ ] Implement source file persistence to Azure Blob Storage
- [ ] Implement intake metadata capture (sender, chat id, message id, file id, timestamp)
- [ ] Add canonical normalized document schema (TypeScript types + YAML contract)
- [ ] Implement Azure Document Intelligence adapter for receipt extraction
- [ ] Implement Azure Document Intelligence adapter for invoice extraction
- [ ] Implement document type classification (receipt / invoice / official_receipt / unsupported)
- [ ] Implement normalization layer mapping extraction output to canonical schema
- [ ] Map receipt extraction to draft Odoo `hr.expense` creation via `odoo.*` MCP tools
- [ ] Map invoice extraction to draft Odoo `account.move` vendor bill creation
- [ ] Attach source artifacts and extraction summaries to Odoo records
- [ ] Write correlation ids (correlation_id, telegram refs, ocr ref, foundry trace) to Odoo metadata
- [ ] Return Telegram success / needs-review / error status messages
- [ ] Add idempotency handling for repeated Telegram deliveries (dedup by correlation_id)

## Phase 2 — Matching + Clarification + Review

- [ ] Implement vendor matching against Odoo `res.partner`
- [ ] Implement employee/sender identity mapping
- [ ] Implement duplicate suspicion checks (invoice number + amount + date + vendor hash)
- [ ] Define green/yellow/red routing rules and confidence thresholds
- [ ] Implement Foundry clarification loop for missing fields
- [ ] Implement Foundry clarification loop for ambiguous routing
- [ ] Add review_status and exception_flags to Odoo record metadata
- [ ] Add finance review queue / filtered views in Odoo
- [ ] Add retry/replay path for failed extractions
- [ ] Implement Telegram reply for clarification questions from Foundry

## Phase 3 — Copilot + Observability

- [ ] Add Odoo Copilot review card for extracted documents
- [ ] Surface confidence / completeness / duplicate flags in Copilot
- [ ] Add approval packet summary generation for high-value invoices
- [ ] Persist Foundry trace ids alongside Odoo records
- [ ] Add operational dashboards (intake volume, failure rate, review rate, auto-draft rate)
- [ ] Add evaluation fixtures for sample receipts and invoices
- [ ] Add routing correctness evaluation dataset
- [ ] Add audit report for end-to-end trace completeness

## Policy / Safety

- [ ] Enforce draft-only writes in Odoo connector layer
- [ ] Enforce threshold-based approval routing
- [ ] Enforce immutable source file linkage (no post-intake deletion)
- [ ] Add unsupported-document fallback handling with user notification
- [ ] Validate correlation chain completeness before marking intake as successful
