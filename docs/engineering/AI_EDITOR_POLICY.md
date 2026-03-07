# AI Editor Policy — InsightPulseAI

> Canonical policy for AI-assisted development across all InsightPulseAI repos.

---

## Required Entrypoint Files

| File | Status | Purpose |
|------|--------|---------|
| `CLAUDE.md` | **Mandatory** | Claude Code / Claude agent instructions |
| `.github/copilot-instructions.md` | Recommended | GitHub Copilot Chat context |
| `GEMINI.md` | Optional | Gemini CLI instructions |
| `codex.md` | Optional | OpenAI Codex instructions |

Every repo MUST have a `CLAUDE.md` at root. Other entrypoints are optional.

---

## Operating Rules

1. **Read before write** — always read existing code before modifying
2. **Minimal changes** — smallest diff that solves the problem
3. **Evidence over assumptions** — verify before claiming success
4. **No guides or tutorials** — execute, don't explain how to execute
5. **No time estimates** — focus on what, not when

---

## Secrets Policy

- Never hardcode secrets in source code
- Never echo/log secrets in CI or debug output
- Never ask users to paste tokens or passwords
- Secrets live in: `.env*` files (local), GitHub Actions secrets (CI), env vars (runtime)
- `.env*` files must be in `.gitignore`

---

## Commit Convention

```
feat|fix|refactor|docs|test|chore(scope): description
```

Keep messages concise. Scope should match the domain area being changed.

---

## Quality Gates

All changes must pass:

1. Lint / format checks
2. Type checking (where applicable)
3. Tests (where applicable)
4. Evidence of working state

---

## Tool-Specific Configuration

### Claude Code

- Reads `CLAUDE.md` at repo root automatically
- Nested `CLAUDE.md` files refine but never contradict root
- Rules files in `.claude/rules/` for cross-cutting concerns

### GitHub Copilot

- Set `"github.copilot.chat.codeGeneration.useInstructionFiles": true` in VS Code settings
- Instruction file at `.github/copilot-instructions.md`

### Gemini CLI

- Reads `GEMINI.md` at repo root
- Keep in sync with `CLAUDE.md` for consistency

### Codex

- Reads `codex.md` at repo root
- Follows same conventions as `CLAUDE.md`

---

## Cross-Repo Map

| Repo | Purpose |
|------|---------|
| `.github` | Org governance, workflows, labels, templates |
| `odoo` | Odoo CE 19 + OCA + custom ipai_* modules |
| `agents` | Agent framework, MCP servers, tool definitions |
| `ops-platform` | Supabase control plane, secrets, automations |
| `lakehouse` | Databricks: medallion pipelines, Unity Catalog |
| `web` | Product web surfaces: console, marketing, docs |
| `infra` | IaC: Azure, DigitalOcean, Cloudflare, Terraform |
| `design-system` | Design tokens, components, icon pipeline |
| `templates` | Repo templates: OCA scaffolds, starters |
