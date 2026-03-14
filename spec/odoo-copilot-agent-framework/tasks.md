# Tasks — Odoo Copilot Agent Framework

## Workstream 1 — Advisory Agent Stabilization

- [ ] **1.1** Attach custom guardrail to advisory agent
- [ ] **1.2** Clean up knowledge indexing (11 dataset files → governed knowledge plane)
- [ ] **1.3** Create advisory system eval dataset
- [ ] **1.4** Create advisory grounded/RAG eval dataset
- [ ] **1.5** Enable Foundry tracing + connect App Insights
- [ ] **1.6** Run baseline evaluation and document results
- [ ] **1.7** Add scoped refusal rules (finance, HR, admin, security)

## Workstream 2 — Ops Agent

- [ ] **2.1** Create Ops agent definition
- [ ] **2.2** Attach read-only Odoo tools
- [ ] **2.3** Attach Databricks monitoring/health tools
- [ ] **2.4** Create ops system eval dataset
- [ ] **2.5** Create ops process eval dataset
- [ ] **2.6** Add diagnostic correctness tests
- [ ] **2.7** Add secret-leakage prevention tests

## Workstream 3 — Router Workflow

- [ ] **3.1** Create Router workflow in Agent Framework
- [ ] **3.2** Implement intent classification logic
- [ ] **3.3** Implement Advisory → Ops handoff
- [ ] **3.4** Implement Advisory/Ops → Actions escalation
- [ ] **3.5** Implement approval pause/resume
- [ ] **3.6** Add trace correlation and context attachment
- [ ] **3.7** Create routing eval dataset
- [ ] **3.8** Add end-to-end workflow tests

## Workstream 4 — Action Agent

- [ ] **4.1** Create Action agent definition
- [ ] **4.2** Define smallest safe write scope
- [ ] **4.3** Attach approved write tools
- [ ] **4.4** Implement evidence + rollback note generation
- [ ] **4.5** Create action safety eval dataset
- [ ] **4.6** Add approval-path compliance tests
- [ ] **4.7** Add unauthorized-action refusal tests
- [ ] **4.8** Add idempotency checks

## Workstream 5 — Capability Packs

- [ ] **5.1** Add Databricks Intelligence Pack tool contracts
- [ ] **5.2** Add fal Creative Production Pack tool contracts
- [ ] **5.3** Add Marketing Strategy & Insight Pack tool contracts
- [ ] **5.4** Add BIR Compliance Pack (see tax-pulse-sub-agent spec)
- [ ] **5.5** Add Document Intake & Extraction Pack tool contracts

## Workstream 6 — Agent Matrix + Ingress Matrix SSOT

- [x] **M.1** Add agent matrix to PRD
- [x] **M.2** Add capability-pack matrix to PRD
- [x] **M.3** Add ingress matrix to plan
- [x] **M.4** Add component ingress ownership table to plan
- [x] **M.5** Add Foundry vs Agent Framework split section
- [x] **M.6** Add evaluation model section
- [x] **M.7** Add safety-evaluation caveat section
- [x] **M.8** Create `infra/ssot/platform/agent_ingress_matrix.yaml`
- [x] **M.9** Create `infra/ssot/agents/agent_capability_matrix.yaml`
- [x] **M.10** Create eval dataset manifests for advisory / ops / actions / router
- [ ] **M.11** Wire App Insights + Foundry tracing correlation IDs
- [ ] **M.12** Add APIM AI gateway as required production ingress

## Workstream 7 — Production Ingress

- [ ] **7.1** Design APIM AI gateway configuration
- [ ] **7.2** Define Foundry client usage contract (project client vs OpenAI-compatible)
- [ ] **7.3** Define endpoint routing contract
- [ ] **7.4** Add auth/quotas/caching policy at APIM layer
- [ ] **7.5** Migrate from prototype ingress to governed ingress

## Cross-Cutting

- [ ] **X.1** Ensure all agent invocations produce App Insights telemetry
- [x] **X.2** Add YAML parse validation to CI
- [x] **X.3** Add spec-SSOT consistency checks to CI
- [x] **X.4** Ensure no deprecated web-owned SSOT paths remain
- [ ] **X.5** Add capability-class tagging to all tools (informational/navigational/transactional)

## Workstream 8 — Live Environment Realization

### Phase A — Foundry realization

- [ ] **F.1** Map `ipai-odoo-copilot-azure` to Advisory role in Foundry `data-intel-ph`
- [ ] **F.2** Upload / connect canonical knowledge assets to Foundry IQ / Azure AI Search
- [ ] **F.3** Register guardrails and eval configurations in Foundry project
- [ ] **F.4** Enable tracing + App Insights correlation for agent runs
- [ ] **F.5** Stand up Router runtime behind Advisory surface
- [ ] **F.6** Stand up Ops runtime with read-only Odoo and Databricks inspection tools
- [ ] **F.7** Stand up Actions runtime with approval-gated Odoo action contracts
- [ ] **F.8** Put APIM in front as production ingress

### Phase B — Odoo realization

- [ ] **F.9** Create Odoo company-scoped Finance PPM / BIR projects with recurring tasks, dependencies, milestones, and activities
- [ ] **F.10** Normalize and import month-end/BIR workbook into Odoo task templates
- [ ] **F.11** Implement PLM-style approval gates at validation and filing stage transitions

### Phase C — Databricks realization

- [ ] **F.12** Expose Databricks gold/platinum views for Finance PPM status, close progress, and tax compliance signals
- [ ] **F.13** Verify scheduled jobs/pipelines and restore healthy execution evidence

### Phase D — Integration

- [ ] **F.14** Wire Foundry Advisory / Ops / Actions to inspect Odoo workflow state and Databricks intelligence views
- [ ] **F.15** Verify APIM routes, auth, quotas, and observability are operational
- [ ] **F.16** Run first end-to-end trace from user request through Advisory → Router → Ops/Actions → Odoo/Databricks and back
