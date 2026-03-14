# Foundation → Runtime Handoff

> Status: **Design-complete → Implementation**
> Date: 2026-03-14

## Purpose

Bridge document between the spec/SSOT design phase and live-runtime realization.
Tracks what is shipped, what is live, what is stubbed, and what blocks progress.

---

## Inventory

### Shipped (merged to main)

| Artifact | Path | Status |
|----------|------|--------|
| Agent capability matrix | `infra/ssot/agents/agent_capability_matrix.yaml` | Merged |
| Agent ingress matrix | `infra/ssot/platform/agent_ingress_matrix.yaml` | Merged |
| Advisory eval dataset | `eval/datasets/advisory.yaml` | Merged |
| Ops eval dataset | `eval/datasets/ops.yaml` | Merged |
| Actions eval dataset | `eval/datasets/actions.yaml` | Merged |
| Router eval dataset | `eval/datasets/router.yaml` | Merged |
| System evals config | `eval/config/system_evals.yaml` | Merged |
| Process evals config | `eval/config/process_evals.yaml` | Merged |
| Safety evals config | `eval/config/safety_evals.yaml` | Merged |
| BIR SFT training set | `eval/training/bir_sft_train.jsonl` | Merged |
| BIR SFT validation set | `eval/training/bir_sft_valid.jsonl` | Merged |
| BIR SFT catalog | `eval/training/bir_sft_catalog.yaml` | Merged |
| BIR SFT README | `eval/training/README_bir_sft.md` | Merged |
| Copilot framework spec | `spec/odoo-copilot-agent-framework/` | Merged |
| Tax Pulse sub-agent spec | `spec/tax-pulse-sub-agent/` | Merged |
| CI SSOT validator | `scripts/ci/validate_agent_ssot.py` | Merged |
| CI workflow | `.github/workflows/agent-ssot-check.yml` | Merged |
| SSOT tests (3 files) | `tests/test_agent_*.py`, `tests/test_spec_*.py` | Merged |

### Live (running in Foundry / Azure)

| Component | Environment | Status |
|-----------|-------------|--------|
| `ipai-odoo-copilot-azure` | Foundry `data-intel-ph` | Deployed — needs Advisory role mapping (F.1) |
| App Insights | Azure | Active — needs Foundry trace correlation (F.4) |

### Stubbed (defined but not yet wired)

| Component | Blocker |
|-----------|---------|
| Router workflow | Needs Agent Framework graph implementation (F.5) |
| Ops agent runtime | Needs read-only Odoo + Databricks tools attached (F.6) |
| Actions agent runtime | Needs approval-gated tool contracts (F.7) |
| APIM AI Gateway | Needs gateway config + route definitions (F.8) |
| BIR knowledge grounding | Needs corpus loaded into Foundry IQ / Azure AI Search (T.1) |
| BIR rates/rules in Odoo 19 | Needs TaxPulse-PH-Pack port to canonical path (T.2) |
| BIR tool contracts | Needs registration in Advisory/Ops/Actions (T.3) |
| Odoo BIR project tasks | Needs recurring templates + PLM gates (T.4) |

---

## Blockers

| # | Blocker | Owner | Impact |
|---|---------|-------|--------|
| 1 | Foundry SDK project-client auth setup for `data-intel-ph` | Platform | Blocks F.1, F.2, F.3 |
| 2 | Agent Framework graph runtime not yet provisioned | Platform | Blocks F.5, F.6, F.7 |
| 3 | APIM AI Gateway not configured | Platform | Blocks F.8, F.15 |
| 4 | Odoo 19 CE module path for BIR tools not finalized | Odoo team | Blocks T.2, T.3 |
| 5 | Databricks gold/platinum views not exposed | Data team | Blocks F.12, F.13 |

---

## Realization Sequence

```
Phase A — Foundry         Phase B — Odoo           Phase C — Databricks
F.1 Advisory mapping      F.9  PPM/BIR projects    F.12 Gold views
F.2 Knowledge assets      F.10 Task templates      F.13 Pipeline health
F.3 Guardrails/evals      F.11 PLM approval gates
F.4 Tracing
F.5 Router runtime                                 Phase D — Integration
F.6 Ops runtime                                    F.14 Wire agents to Odoo+DB
F.7 Actions runtime                                F.15 APIM verification
F.8 APIM ingress                                   F.16 E2E trace

Tax Pulse Realization (parallel with Phase B)
T.1 BIR knowledge corpus
T.2 Rates/rules port
T.3 Tool contract registration
T.4 Odoo workflow binding
T.5 First eval baseline
```

---

## Success Criteria

1. All 4 SSOT components respond behind APIM AI Gateway
2. Advisory grounds answers against Foundry IQ knowledge index
3. Router correctly classifies and routes advisory / ops / action intents
4. Ops reads Odoo workflow state and Databricks health without writes
5. Actions executes only with human approval and produces rollback notes
6. App Insights shows correlated traces from request → agent → tool → response
7. BIR eval baseline published with system, process, and safety scores
