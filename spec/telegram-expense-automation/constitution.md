# Constitution — Telegram Expense + Invoice Automation

## Non-Negotiable Principles

### Channel Intake Boundary

Telegram is an intake and clarification channel only. It must not become the accounting system of record. All approved accounting objects, attachments, statuses, and audit events must persist in Odoo.

### Draft-First Financial Automation

All expense and invoice documents received from Telegram must create draft-stage artifacts only unless an explicit rule-based exception is defined and approved. Autonomous posting of journal-impacting records is prohibited in v1.

### OCR + Agent Separation of Concerns

Azure Document Intelligence is the canonical OCR and extraction subsystem.
Foundry agents are responsible for orchestration, clarification, confidence gating, and exception reasoning.
Odoo Copilot is the ERP-native review and explanation surface.
No single component may both extract and unilaterally finalize finance records.

### Confidence and Risk Gating

Every extracted document must carry:
- extraction confidence
- document type confidence
- duplicate suspicion state
- required-field completeness state
- approval threshold result

These states determine green/yellow/red routing and must be retained as auditable metadata.

### Traceability and Replay

Each Telegram submission must have an immutable correlation chain across:
- Telegram message/file id
- stored source artifact id
- OCR result id
- Foundry trace/run id
- Odoo target model/id
- review/approval events

### Human-in-the-Loop for Material Exceptions

Human approval is mandatory for:
- low-confidence extraction
- unknown vendor / unmatched employee
- suspected duplicates
- tax mismatch / unsupported tax structure
- amount over threshold
- unsupported or ambiguous document type

## Role Boundaries

| Component | Can do | Cannot do |
|---|---|---|
| Telegram Bot | receive files, send status/clarification messages, relay user answers | write Odoo records, execute accounting actions, store files long-term |
| Document Intelligence | OCR, field extraction, document classification, confidence scoring | make routing decisions, write ERP records, ask users questions |
| Foundry Agent | orchestrate workflows, ask clarification questions, gate by confidence/policy, route exceptions | directly extract from documents, post journal entries, bypass approval gates |
| Odoo Connector | create/update draft expenses and vendor bills, attach documents, write audit metadata | post journal entries, execute payments, mutate production config |
| Odoo Copilot | explain extraction results, surface exceptions, recommend next actions | finalize postings, bypass approval workflow, override risk routing |

## Evaluation Requirement

Every workflow must have:
- At least one extraction accuracy evaluation dataset
- At least one routing correctness evaluation dataset
- Tracing enabled and linked to Foundry observability
- End-to-end correlation chain validation

## Cross-References

- [Odoo Copilot Agent Framework Constitution](../odoo-copilot-agent-framework/constitution.md) — agent role boundaries and eval requirements
- [Odoo Copilot Agent Framework PRD](../odoo-copilot-agent-framework/prd.md) — `ipai-odoo-copilot-actions` governs allowed write actions
