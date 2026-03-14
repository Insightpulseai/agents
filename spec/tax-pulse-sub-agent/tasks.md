# Tasks — Tax Pulse Sub-Agent

## Workstream — BIR Compliance Pack

- [ ] **B.1** Add BIR Compliance Pack to agent capability matrix
- [ ] **B.2** Create BIR KB ingestion manifest
- [ ] **B.3** Populate `bir_compliance_search` source mapping and indexing pipeline
- [ ] **B.4** Port `ph_rates_2025.json` to `ipai_bir_tax_compliance/data/rates/`
- [ ] **B.5** Port `vat.rules.yaml` and `ewt.rules.yaml` to `ipai_bir_tax_compliance/data/rules/`
- [ ] **B.6** Port JSONLogic rules evaluator to `ipai_bir_tax_compliance/engine/`
- [ ] **B.7** Remove `account_reports` EE dependency from ported code
- [ ] **B.8** Add `check_overdue_filings` read-only tool
- [ ] **B.9** Add `compute_bir_vat_return` action tool
- [ ] **B.10** Add `compute_bir_withholding_return` action tool
- [ ] **B.11** Add `validate_bir_return` action tool
- [ ] **B.12** Add `generate_alphalist` action tool
- [ ] **B.13** Add `generate_efps_xml` action tool
- [ ] **B.14** Add `generate_bir_pdf` action tool
- [ ] **B.15** Port PDF/report templates (1601-C, 2550Q, 1702-RT)
- [ ] **B.16** Fix `_compute_compensation_wht` to use TRAIN brackets
- [ ] **B.17** Complete `_compute_final_wht` stub
- [ ] **B.18** Add computation fixture tests
- [ ] **B.19** Add rules engine unit tests
- [ ] **B.20** Enable `ipai_bir_notifications` module (flip installable)

## Workstream — Month-End + Filing Orchestration

- [ ] **F.1** Configure Odoo Project with BIR compliance stages
- [ ] **F.2** Create recurring task templates per form/period/company
- [ ] **F.3** Set up task dependencies (reconcile → compute → validate → approve → export → confirm)
- [ ] **F.4** Add milestones (Books Ready, Computation Complete, Filed, Confirmed)
- [ ] **F.5** Implement PLM-style approval gates at validation and filing
- [ ] **F.6** Wire activity-based deadline reminders
- [ ] **F.7** Normalize month-end closing workbook into seed data

## Workstream — BIR Evaluations

- [ ] **E.1** Create BIR advisory eval dataset
- [ ] **E.2** Create BIR ops eval dataset
- [ ] **E.3** Create BIR actions eval dataset
- [ ] **E.4** Add approval-path tests for BIR filing workflow
- [ ] **E.5** Add unauthorized-action refusal tests for BIR
- [ ] **E.6** Collect 150+ gold training responses
- [ ] **E.7** Create BIR SFT training set (bir_sft_train.jsonl)
- [ ] **E.8** Create BIR SFT validation set (bir_sft_valid.jsonl)
- [ ] **E.9** Run baseline evaluation (prompt-only)
- [ ] **E.10** Fine-tune and compare against baseline
