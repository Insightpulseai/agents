# Agentic SDLC Constitution — InsightPulseAI

source: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896
extracted: 2026-03-15
applies-to: agents, .github, infra, automations

## Purpose

This constitution defines how agentic software development lifecycle (SDLC) patterns integrate with InsightPulseAI's SSOT/SOR doctrine. It governs the boundaries between agent autonomy and deterministic infrastructure.

## Core Principles

### 1. Spec-Driven Development

All agent work begins from a specification — never from an open-ended prompt.

- Specifications are structured documents with requirements, constraints, and acceptance criteria
- Specs are stored in `ops.specs` (Supabase SSOT) and materialize as GitHub issues
- Agents receive scoped tasks derived from specs, not free-form instructions
- Constitution files in `agents/system/` define tech stack and org standards that constrain agent output

### 2. Deterministic CI/CD is Non-Negotiable

CI/CD pipelines are deterministic — agents call them, not the reverse.

- No LLM calls in the deploy path
- Agents produce artifacts (code, configs, migrations) → pipelines deploy them predictably
- Pipeline definitions live in `.github/workflows/` (GitHub Actions primary) or `infra/` (Bicep)
- Rollback is always possible without agent involvement

### 3. Human-in-the-Loop at PR Review

Human review gates exist at pull request approval, not at every agent step.

- Agents create PRs autonomously from spec tasks
- Quality gates (CodeQL, ESLint, tests) run automatically
- Human reviewers approve or request changes
- Agents may iterate on review feedback within the same PR

### 4. Sub-Agents Over Omnibus Agents

Narrow-context sub-agents outperform single omnibus agents.

- Each agent has a specific skill and bounded context
- SRE agent → spawns GitHub sub-agent → creates issue → coding agent picks up
- Agent definitions in `agents/*.SKILL.md` define boundaries
- Cross-agent communication via Supabase `ops.run_events` (never direct)

### 5. Supabase SSOT / Odoo SOR

All orchestration state flows through the canonical data planes.

```
Agent Framework (orchestration layer)
        ↓ emits run events / artifacts
Supabase ops.* (SSOT / control plane)
        ↓ posts accounting artifacts
Odoo (SOR / ledger)
```

- Agent state (runs, events, checkpoints) → `ops.runs` + `ops.run_events`
- Spec state (drafts, approved, completed) → `ops.specs`
- Financial artifacts → Odoo (posted journal entries are immutable SOR)
- Analytics derivatives → Databricks lakehouse (read-only from SSOT)

## The 5-Phase Loop

```
Phase 1: Spec → ops.specs (Supabase SSOT) → GitHub issue
Phase 2: Coding agent → branch + PR + tests
Phase 3: Quality gate → CodeQL + lint + AI review
Phase 4: CI/CD → deterministic build → ACA deploy
Phase 5: SRE agent → observe → incident → back to Phase 1
```

## Tech Stack Constraints (for agent output)

| Layer | Technology | Non-Negotiable |
|-------|-----------|----------------|
| Runtime | Azure AI Foundry / Azure Container Apps | Yes |
| ERP | Odoo 19 CE + OCA modules | Yes |
| SSOT | Supabase (Postgres + Auth + Storage + Edge Functions) | Yes |
| Analytics | Databricks (Unity Catalog + DLT + DBSQL) | Yes |
| CI/CD | GitHub Actions (primary), Azure Pipelines (ADO-specific only) | Yes |
| LLM | Claude (primary), Azure OpenAI (secondary) | No |
| Workflow | n8n (integration/webhook), Agent Framework (agentic reasoning) | No |
| Region | Azure Southeast Asia (SEA) | Yes |

## Anti-Patterns

1. **No raw LLM calls** — all agent work goes through tool-based architecture
2. **No agent-managed state** — Supabase owns all checkpoint/event state
3. **No secrets in code** — environment variables only, Key Vault for CI
4. **No LLM in deploy path** — pipelines are deterministic
5. **No bypassing Unity Catalog** — all Databricks tables must be registered
6. **No writing back from analytics** — Databricks reads from SSOT, never writes to it
