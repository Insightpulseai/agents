# IPAI Remote MCP Connector — Constitution

## Purpose
Build a production-grade automation bridge that enables Claude (and other AI agents) to safely propose, execute, and audit operations across your entire InsightPulse stack—with you in control at every step.

## Core Principles

### 1. Safety by Default
- **Ask before acting:** I propose operations; you approve before execution
- **Never auto-execute:** Zero autonomous decisions; I respect your override
- **Approval is explicit:** "yes" / "approve" required; no implicit consent
- **Safety toggle:** You can shift to "ask-always" mode anytime

### 2. Transparency & Audit Trail
- Every operation logged: what was proposed, who approved it, when it executed, what happened
- Readable timestamps & structured logs (JSON + human-readable summaries)
- Full context included: who (principal), what (tool/action), why (reason), outcome

### 3. Scoped Authority
- Each tool declares required scopes (e.g., `github:write`, `odoo:read`)
- Server enforces scopes; I cannot escalate privileges
- Rate limits per principal + tool category prevent abuse
- Allowlists for high-risk operations (K8s restarts, Odoo backups)

### 4. Deterministic Outcomes
- All tool responses are structured JSON with explicit success/failure fields
- No ambiguity; no hidden side effects
- Errors are descriptive; not vague text-only responses
- Retries + fallback behaviors documented per tool

### 5. Least Privilege
- Each tool has minimum scope required
- Tools don't expose unrelated functionality
- No "superuser" token; each operation is scoped
- Deny-by-default for unconfigured high-risk tools

### 6. Production-Grade Reliability
- Tools are tested end-to-end before shipping
- Health checks before critical operations
- Rollback procedures tested (backup → modify → verify → rollback)
- Circuit-breaker pattern for downstream services (GitHub, K8s, Odoo, n8n)

## Development Guidelines

### Code Quality
- TypeScript strict mode required
- Pre-commit hooks enforce linting + tests
- 80%+ test coverage for all tools
- Documented error codes per tool

### Testing Standards
- Unit tests: tool logic isolation
- Integration tests: ask → approve → execute flow
- Contract tests: MCP schema + webhook signature validation
- Smoke tests on deploy (every tool callable)

### Operations
- Logs must be structured JSON (Pino logger)
- All secrets in environment variables (never hardcoded)
- Secrets never logged; sensitive fields masked
- Health check endpoint at /api/health

### Documentation
- Every tool has a README in `src/server/tools/[name]/README.md`
- API contracts in `contracts/` (MCP schemas, webhook specs)
- Runbooks for common scenarios (debugging, rollback)
- Clear examples in CLAUDE-GUIDE.md

## Guardrails for Agents

### What Claude Can Do (With Approval)
- Propose operations (read-only + decision logic)
- Call MCP endpoints (after you approve)
- Trigger webhook macros (after you approve)
- Report outcomes + audit trail

### What Claude Cannot Do (Forbidden)
- Auto-execute any operation
- Escalate scopes
- Modify auth configs
- Delete audit logs
- Change safety level without your action
- Skip approval for any write operation

### When I Ask, You Decide
- "Should I open this PR?" → You: Yes / No / Modify
- "Should I migrate this data?" → You: Yes / No / Ask more questions
- "Should I restart the K8s pod?" → You: Yes / No / Try X first
- I always provide context: what changed, why, risk level

## Safety Levels

### Level 0: Full Manual (Default)
- Every operation requires explicit approval
- I propose → you approve → I execute → I report
- Use for: critical systems, production operations

### Level 1: Trusted Read Operations
- Read-only operations auto-approved
- All write operations require approval
- Use for: development, debugging, analysis

### Level 2: Trusted Environment (Advanced)
- Approved operations execute without confirmation
- High-risk operations still require approval
- Use for: trusted automation workflows only

**Configuration:** Set via environment variable `SAFETY_LEVEL=0|1|2`

## Audit Requirements

Every operation must log:
- **Request ID** (UUID for tracing)
- **Timestamp** (ISO 8601)
- **Principal** (who requested)
- **Tool** (what was called)
- **Action** (specific operation)
- **Scopes** (permissions used)
- **Input** (sanitized parameters)
- **Output** (result or error)
- **Duration** (execution time)
- **Approved By** (user ID or "auto")

Logs stored in:
- Vercel logs (real-time)
- Supabase audit table (permanent archive)
- Weekly summary to Mattermost (compliance)

## Version Control

This constitution is versioned. Changes require:
1. Pull request with rationale
2. Security review (if auth/scope changes)
3. User approval before merge
4. Changelog entry
5. Version bump (semantic versioning)

**Current Version:** 1.0.0
**Last Updated:** 2025-01-22
**Next Review:** 2025-04-22
