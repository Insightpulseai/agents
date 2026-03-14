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

- [ ] **M.1** Add agent matrix to PRD
- [ ] **M.2** Add capability-pack matrix to PRD
- [ ] **M.3** Add ingress matrix to plan
- [ ] **M.4** Add component ingress ownership table to plan
- [ ] **M.5** Add Foundry vs Agent Framework split section
- [ ] **M.6** Add evaluation model section
- [ ] **M.7** Add safety-evaluation caveat section
- [ ] **M.8** Create `infra/ssot/platform/agent_ingress_matrix.yaml`
- [ ] **M.9** Create `infra/ssot/agents/agent_capability_matrix.yaml`
- [ ] **M.10** Create eval dataset manifests for advisory / ops / actions / router
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
- [ ] **X.2** Add YAML parse validation to CI
- [ ] **X.3** Add spec-SSOT consistency checks to CI
- [ ] **X.4** Ensure no deprecated web-owned SSOT paths remain
- [ ] **X.5** Add capability-class tagging to all tools (informational/navigational/transactional)
