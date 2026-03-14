# Plan — Tax Pulse Sub-Agent

## Implementation Waves

### Wave 1 — Knowledge Foundation
- Ingest BIR RR/RMO/issuance corpus
- Ingest TRAIN law references
- Populate pgvector / Azure AI Search index
- Wire `bir_compliance_search` to actual knowledge store
- Add source metadata and citation support

### Wave 2 — Rates and Rules Port
- Port `ph_rates_2025.json` from TaxPulse-PH-Pack
- Port `vat.rules.yaml` and `ewt.rules.yaml`
- Port JSONLogic rules evaluator
- Adapt to Odoo 19 CE packaging
- Remove `account_reports` EE dependency

### Wave 3 — Compute and Validate Tools
- Add `compute_bir_vat_return`
- Add `compute_bir_withholding_return`
- Add `validate_bir_return`
- Add `check_overdue_filings`
- Refactor compute paths to use externalized rates/rules
- Fix TRAIN bracket application in WHT
- Add fixture-backed computation tests

### Wave 4 — Filing Artifacts
- Port PDF/report templates (1601-C, 2550Q, 1702-RT)
- Add eFPS XML export
- Add alphalist generation
- Add filing package preparation workflow

### Wave 5 — Project/Task Orchestration
- Configure Odoo Project with BIR compliance stages
- Create recurring task templates per form/period
- Set up task dependencies and milestones
- Implement PLM-style approval gates
- Wire activity-based reminders

### Wave 6 — Evaluations and SFT
- Create BIR advisory eval dataset
- Create BIR ops eval dataset
- Create BIR actions eval dataset
- Collect gold responses
- Create SFT training set (150 train / 30 valid)
- Run baseline evaluation
- Fine-tune and compare

### Wave 7 — Production Wiring
- Enable notifications module (`ipai_bir_notifications`)
- Wire Foundry tracing for BIR tools
- Add APIM routes for BIR-related actions
- Add App Insights correlation IDs

## Risk Mitigations

| Risk | Mitigation |
|---|---|
| account_reports EE dependency in TaxPulse | Replace with OCA account_financial_report or direct compute |
| Odoo 18 → 19 port issues | tree→list, groups_id→group_ids migration |
| Empty BIR knowledge base | Populate before eval/SFT work |
| Hardcoded tax logic | Use externalized rates/rules from Wave 2 |
| Missing PDF/DAT export in Odoo PH | Build in Wave 4 |
