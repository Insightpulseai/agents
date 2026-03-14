# Sprint Tasks — Phase 1 Foundation

> Sprint: 2026-03-10 to 2026-03-24
> Epic: E-FOUND-01 — Agent Foundation Layer
> Last updated: 2026-03-15

---

## Completed

- [x] **Cosmos DB session persistence** — Implemented 2026-03-14
  - Artifact: `src/lib/cosmos.ts`
  - Graceful fallback to in-memory Map when Cosmos unavailable
  - Session TTL: 24 hours

- [x] **Application Insights telemetry wrapper** — Implemented 2026-03-14
  - Artifact: `src/lib/telemetry.ts`
  - No-op stubs when `APPLICATIONINSIGHTS_CONNECTION_STRING` absent
  - Custom events: `copilot_request`, `copilot_response`, `copilot_error`, `tool_invocation`

- [x] **PII redaction middleware** — Implemented 2026-03-14
  - Artifact: `src/middleware/pii-redact.ts`
  - Patterns: PH TIN (`XXX-XXX-XXX-XXX`), bank account (8+ digits), email, PH phone
  - Applied to: user input before processing, agent output before persistence/logging

- [x] **Foundry KB files drafted** — Completed 2026-03-14
  - Artifact: `docs/foundry-kb/` (6 files, 1302 lines)
  - Files: company overview, BIR calendar, module catalog, Odoo navigation, FAQ, glossary
  - Pending upload to Foundry portal

- [x] **Agent instructions v7 drafted** — Completed 2026-03-14
  - Artifact: `docs/foundry-kb/agent-instructions-v7-draft.md` (480 lines)
  - Covers: constitution rules, source labels, escalation triggers, tool contracts, environment modes
  - Pending replacement in Foundry portal

---

## In Progress

- [ ] **Upload KB files to Foundry portal**
  - Blocked on: Foundry portal access confirmation
  - Action: Upload 6 files via Foundry Agent Studio UI
  - Acceptance: Files visible in agent's file search tool

- [ ] **Replace agent instructions with v7 in Foundry**
  - Blocked on: KB upload (instructions reference KB file names)
  - Action: Paste v7 instructions into Foundry Agent Studio → Instructions field
  - Acceptance: Agent responds with source labels and follows escalation policy

---

## Pending

- [ ] **Run first live eval against Foundry endpoint**
  - Depends on: KB upload + instructions v7 deployed
  - Action: Execute `eval/knowledge_copilot_eval.yaml` smoke set against live endpoint
  - Acceptance: smoke pass rate = 100%, safety pass rate = 100%
  - Evidence: `docs/evidence/{date}/eval/knowledge_eval_report.json`

- [ ] **Wire OpenAPI bridge as Foundry custom tool (read-only)**
  - Depends on: `apps/bridge-api/` deployed to Azure Functions
  - Action: Register bridge-api endpoints as Foundry custom tools (OpenAPI spec)
  - Acceptance: Agent can call `getComplianceFindings` and `getModuleStatus`
  - Evidence: Tool invocation visible in Application Insights

- [ ] **Enable Bing grounding in Foundry**
  - Depends on: Foundry portal access
  - Action: Toggle Bing grounding in Foundry Agent Studio → Tools
  - Acceptance: Agent can answer current-events questions with `[BING-GROUNDED]` label

---

## Sprint Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Tasks completed | 10 | 5 |
| Blockers | 0 | 1 (Foundry portal access) |
| Eval pass rate (smoke) | 100% | Not yet run |
| Eval pass rate (safety) | 100% | Not yet run |
