# Skill: Agentic SDLC — Microsoft Pattern

source: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896
extracted: 2026-03-15
applies-to: agents, .github, infra, automations

## Pattern Summary

5-phase loop: Spec → Code → Quality → Deploy → Observe → (back to Spec)

## Phase 1 — Spec-Driven Development

- Entry point: single user story / problem statement
- Tool: GitHub Spec Kit (`/promptkit.specify "<intent>"`)
- Output: requirements + plan + task breakdown (respects constitution/tech stack)
- Bridge to agents: spec-to-issue tool → GitHub issue + auto-assign coding agent
- IPAI equivalent: `agents/spec/` + Supabase `ops.specs` table (SSOT for spec state)

## Phase 2 — Coding Agent

- Agent: GitHub Copilot coding agent (cloud, not IDE)
- Input: scoped GitHub issue with Spec Kit tasks
- Output: branch + PR + tests + Playwright screenshot
- Key principle: small scoped tasks dramatically outperform open-ended prompts
- IPAI equivalent: Claude agents in `agents/` repo using spec tasks as structured input

## Phase 3 — Code Quality

- AI-assisted review: CodeQL + ESLint + Copilot PR summary
- Metric: 81% quality improvement rate (Qodo 2025), 38.7% AI comments → code fixes
- IPAI gate: `.github/workflows/quality-gate.yml` (reusable)

## Phase 4 — CI/CD (Deterministic, Not Agentic)

- Principle: CI/CD stays deterministic — agents call it, not the reverse
- ACA Dynamic Sessions for untrusted agent-generated code isolation
- IPAI: `infra/` Bicep + `.github/workflows/` → Azure Container Apps SEA

## Phase 5 — SRE Agent (Day-2 Loop)

- Continuously watches telemetry (logs, metrics, traces)
- Sub-agent pattern: primary SRE → GitHub sub-agent → creates issue → coding agent
- Closes the loop: ops incident → spec → code → PR → review → merge
- IPAI equivalent: `automations/` runbooks + `ops.run_events` in Supabase

## Closed-Loop Pattern (Full Cycle)

```
problem-statement
  → ops.specs (Supabase SSOT)
  → GitHub issue (auto-created)
  → coding agent (PR)
  → quality gate (CI)
  → ACA deploy (infra/)
  → SRE agent observes
  → GitHub issue (ops incident)
  → ops.run_events (Supabase SSOT)
  → back to coding agent
```

## Key Principles to Preserve

1. Spec Kit constitution = IPAI `agents/system/` doctrine files
2. Deterministic CI/CD is non-negotiable even in agentic systems
3. Human-in-the-loop at PR review, not at every step
4. Sub-agents for narrow context tasks > one omnibus agent
5. ACA Dynamic Sessions = isolation boundary for untrusted code

## Extraction Template (Reusable for Any Source)

```
1. WHAT IS IT?          → 2-sentence summary, no hype
2. WHEN TO USE?         → decision matrix (use vs don't use)
3. CORE PATTERNS?       → minimal code/config snippets only
4. SSOT/SOR MAPPING?    → where does state live? (always Supabase)
5. OBSERVABILITY HOOKS? → what telemetry does it emit → ops.*
6. GAPS / WATCH?        → what it doesn't handle, version pins, security notes
```
