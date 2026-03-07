# IPAI Remote MCP Connector — Task Breakdown

**Version:** 1.0.0
**Status:** Ready for Execution
**Owner:** Jake Tolentino
**Created:** 2025-01-22

---

## Overview

This document breaks down the MCP Connector implementation into discrete, testable tasks organized by phase. Each task includes acceptance criteria, dependencies, and estimated effort.

---

## Phase 0: Foundation & Infrastructure (Week 1)

**Goal:** Establish repository structure, core MCP server, and authentication layer

### Task 0.1: Repository Setup
**Priority:** Critical
**Effort:** 2 hours
**Dependencies:** None

**Acceptance Criteria:**
- [ ] GitHub repository created: `Insightpulseai-net/pulser-mcp`
- [ ] Initial commit with Spec-Kit structure (`.specify/`, `src/`, `tests/`, `docs/`)
- [ ] TypeScript configured with strict mode
- [ ] ESLint + Prettier configured
- [ ] Vitest configured for testing
- [ ] Git hooks configured (pre-commit: lint + test)
- [ ] README.md with quick start guide

**Verification:**
```bash
npm run lint        # Passes
npm run test        # Passes (no tests yet, but framework works)
npm run type-check  # Passes
```

---

### Task 0.2: MCP Server Core
**Priority:** Critical
**Effort:** 4 hours
**Dependencies:** Task 0.1

**Acceptance Criteria:**
- [ ] `/api/mcp` route handler (GET + POST) implemented
- [ ] Request ID generation (UUID v4)
- [ ] Structured logging with Pino (JSON output)
- [ ] Tool discovery endpoint returns empty list (scaffold)
- [ ] Tool invocation endpoint returns "not implemented" (scaffold)
- [ ] Unit tests for core MCP protocol handling

**Implementation Files:**
- `src/app/api/mcp/route.ts` - Route handler
- `src/server/mcp.ts` - MCP protocol logic
- `src/lib/types.ts` - TypeScript interfaces
- `tests/mcp.test.ts` - Unit tests

**Verification:**
```bash
curl http://localhost:3000/api/mcp
# Returns: {"tools": []}

curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "test"}}'
# Returns: {"error": {"code": "not_implemented"}}
```

---

### Task 0.3: Authentication Middleware
**Priority:** Critical
**Effort:** 3 hours
**Dependencies:** Task 0.2

**Acceptance Criteria:**
- [ ] Bearer token validation middleware
- [ ] Token-to-scopes mapping from environment variable
- [ ] Scope enforcement logic (check tool requirements vs token scopes)
- [ ] HTTP 401 for missing/invalid token
- [ ] HTTP 403 for insufficient scopes
- [ ] Unit tests for auth + scope enforcement

**Implementation Files:**
- `src/server/auth.ts` - Auth middleware
- `src/lib/scopes.ts` - Scope definitions
- `tests/auth.test.ts` - Unit tests

**Environment Variables:**
```bash
ALLOWED_TOKENS='{"token_dev_abc": {"scopes": ["github:read", "odoo:read"]}}'
```

**Verification:**
```bash
# No token → 401
curl http://localhost:3000/api/mcp

# Invalid token → 401
curl -H "Authorization: Bearer invalid" http://localhost:3000/api/mcp

# Valid token → 200
curl -H "Authorization: Bearer token_dev_abc" http://localhost:3000/api/mcp
```

---

### Task 0.4: Health Check & Observability
**Priority:** High
**Effort:** 2 hours
**Dependencies:** Task 0.2

**Acceptance Criteria:**
- [ ] `/api/health` endpoint implemented
- [ ] Returns service version, uptime, timestamp
- [ ] Downstream service health checks (stubbed for now)
- [ ] Response time <100ms
- [ ] Unit tests for health endpoint

**Implementation Files:**
- `src/app/api/health/route.ts` - Health endpoint
- `tests/health.test.ts` - Unit tests

**Verification:**
```bash
curl http://localhost:3000/api/health
# Returns:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "uptime_seconds": 42,
#   "timestamp": "2025-01-22T10:00:00Z"
# }
```

---

### Task 0.5: Vercel Deployment Setup
**Priority:** High
**Effort:** 2 hours
**Dependencies:** Tasks 0.1-0.4

**Acceptance Criteria:**
- [ ] Vercel project created and linked
- [ ] Environment variables configured in Vercel dashboard
- [ ] `vercel.json` configuration file created
- [ ] Staging deployment successful
- [ ] Health check accessible via public URL
- [ ] GitHub Actions workflow for CI/CD

**Verification:**
```bash
# Deploy to staging
vercel

# Check health
curl https://pulser-mcp-staging.vercel.app/api/health
# Returns: {"status": "healthy"}
```

---

## Phase 1: MVP Tools (Week 2-3)

**Goal:** Implement GitHub, Odoo, Vercel tools + webhook bridge

### Task 1.1: GitHub Tool - File Operations
**Priority:** Critical
**Effort:** 4 hours
**Dependencies:** Task 0.5

**Acceptance Criteria:**
- [ ] `github.repo.get_file` - Fetch file contents
- [ ] `github.repo.apply_patch` - Apply Git patch
- [ ] `github.repo.commit_files` - Commit multiple files
- [ ] Proper error handling (404, 403, rate limits)
- [ ] Unit tests + integration tests (mocked GitHub API)
- [ ] Tool registered in MCP tool list

**Implementation Files:**
- `src/server/tools/github.ts`
- `tests/tools/github.test.ts`

**Tool Schemas:**
```json
{
  "name": "github.repo.get_file",
  "description": "Fetch file contents from a GitHub repository",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo": {"type": "string", "pattern": "^[\\w-]+/[\\w-]+$"},
      "path": {"type": "string"},
      "ref": {"type": "string", "default": "main"}
    },
    "required": ["repo", "path"]
  },
  "requiredScopes": ["github:read"]
}
```

**Verification:**
```bash
curl -X POST http://localhost:3000/api/mcp \
  -H "Authorization: Bearer token_dev_abc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "github.repo.get_file",
      "arguments": {
        "repo": "Insightpulseai-net/pulser-mcp",
        "path": "README.md"
      }
    }
  }'
# Returns: {"result": {"content": "...", "sha": "..."}}
```

---

### Task 1.2: GitHub Tool - Branch & PR Operations
**Priority:** Critical
**Effort:** 4 hours
**Dependencies:** Task 1.1

**Acceptance Criteria:**
- [ ] `github.repo.create_branch` - Create new branch
- [ ] `github.repo.open_pr` - Open pull request with template
- [ ] `github.actions.list_runs` - List CI/CD workflow runs
- [ ] Scope requirements enforced (`github:write` for PR creation)
- [ ] Unit tests + integration tests

**Tool Schemas:**
```json
{
  "name": "github.repo.create_branch",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo": {"type": "string"},
      "branch": {"type": "string"},
      "from": {"type": "string", "default": "main"}
    },
    "required": ["repo", "branch"]
  },
  "requiredScopes": ["github:write"]
}
```

---

### Task 1.3: Webhook Bridge Implementation
**Priority:** Critical
**Effort:** 5 hours
**Dependencies:** Task 0.5

**Acceptance Criteria:**
- [ ] `POST /api/bridge/run` - Execute signed webhook request
- [ ] HMAC-SHA256 signature validation
- [ ] Job queue system (in-memory for MVP, Redis later)
- [ ] `GET /api/bridge/status/:id` - Poll job status
- [ ] Macro allowlist validation
- [ ] Security tests (signature tampering, replay attacks)

**Implementation Files:**
- `src/app/api/bridge/run/route.ts`
- `src/app/api/bridge/status/[id]/route.ts`
- `src/server/bridge.ts`
- `src/lib/macros.ts`
- `tests/bridge.test.ts`

**Verification:**
```bash
# Compute HMAC signature
echo -n '{"macro":"test"}' | openssl dgst -sha256 -hmac "secret"

# Call bridge
curl -X POST http://localhost:3000/api/bridge/run \
  -H "Authorization: Bearer token_dev_abc" \
  -H "X-Signature: sha256=<computed-hmac>" \
  -H "Content-Type: application/json" \
  -d '{"macro": "test", "params": {}}'
# Returns: {"job_id": "job_xyz", "status_url": "/api/bridge/status/job_xyz"}

# Poll status
curl http://localhost:3000/api/bridge/status/job_xyz
# Returns: {"status": "in_progress", "logs": [...]}
```

---

### Task 1.4: Odoo Tool - Module Lifecycle
**Priority:** High
**Effort:** 4 hours
**Dependencies:** Task 0.5

**Acceptance Criteria:**
- [ ] `odoo.health` - Health check + version info
- [ ] `odoo.modules.install` - Install Odoo module
- [ ] `odoo.modules.upgrade` - Upgrade existing module
- [ ] `odoo.modules.list` - List installed modules
- [ ] XML-RPC client with connection pooling
- [ ] Unit tests + integration tests (mocked Odoo XML-RPC)

**Implementation Files:**
- `src/server/tools/odoo.ts`
- `tests/tools/odoo.test.ts`

**Tool Schemas:**
```json
{
  "name": "odoo.modules.install",
  "inputSchema": {
    "type": "object",
    "properties": {
      "module_name": {"type": "string"},
      "database": {"type": "string", "default": "production"}
    },
    "required": ["module_name"]
  },
  "requiredScopes": ["odoo:write"]
}
```

---

### Task 1.5: Vercel Tool - Deployment Operations
**Priority:** Medium
**Effort:** 3 hours
**Dependencies:** Task 0.5

**Acceptance Criteria:**
- [ ] `vercel.deployments.list` - List recent deployments
- [ ] `vercel.deployments.logs` - Fetch deployment logs
- [ ] `vercel.deployments.get` - Get deployment status
- [ ] Vercel API client with retry logic
- [ ] Unit tests + integration tests

**Implementation Files:**
- `src/server/tools/vercel.ts`
- `tests/tools/vercel.test.ts`

---

## Phase 2: Advanced Tools (Week 4)

**Goal:** Implement K8s, n8n, Supabase, DigitalOcean tools

### Task 2.1: Kubernetes Tool
**Priority:** Medium
**Effort:** 4 hours
**Dependencies:** Task 1.5

**Acceptance Criteria:**
- [ ] `k8s.deployments.logs` - Fetch pod logs
- [ ] `k8s.deployments.restart` - Restart deployment (requires approval)
- [ ] `k8s.deployments.status` - Get deployment status
- [ ] Kubernetes client library integration
- [ ] Scope enforcement for write operations
- [ ] Unit tests + integration tests

**Implementation Files:**
- `src/server/tools/kubernetes.ts`
- `tests/tools/kubernetes.test.ts`

---

### Task 2.2: n8n Tool
**Priority:** Medium
**Effort:** 3 hours
**Dependencies:** Task 1.5

**Acceptance Criteria:**
- [ ] `n8n.workflow.trigger` - Trigger workflow execution
- [ ] `n8n.executions.list` - List recent executions
- [ ] `n8n.executions.get` - Get execution details
- [ ] n8n API client with auth
- [ ] Unit tests + integration tests

**Implementation Files:**
- `src/server/tools/n8n.ts`
- `tests/tools/n8n.test.ts`

---

### Task 2.3: Supabase Tool
**Priority:** Medium
**Effort:** 3 hours
**Dependencies:** Task 1.5

**Acceptance Criteria:**
- [ ] `supabase.rpc.call` - Execute RPC function
- [ ] `supabase.migrations.status` - Check migration status
- [ ] `supabase.health` - Database health check
- [ ] Supabase client library integration
- [ ] Unit tests + integration tests

**Implementation Files:**
- `src/server/tools/supabase.ts`
- `tests/tools/supabase.test.ts`

---

### Task 2.4: DigitalOcean Tool
**Priority:** Medium
**Effort:** 3 hours
**Dependencies:** Task 1.5

**Acceptance Criteria:**
- [ ] `do.apps.deploy` - Deploy app to App Platform
- [ ] `do.apps.status` - Check app status
- [ ] `do.apps.logs` - Fetch app logs
- [ ] DigitalOcean API client with retry
- [ ] Unit tests + integration tests

**Implementation Files:**
- `src/server/tools/digitalocean.ts`
- `tests/tools/digitalocean.test.ts`

---

### Task 2.5: Rate Limiting System
**Priority:** High
**Effort:** 4 hours
**Dependencies:** Task 2.4

**Acceptance Criteria:**
- [ ] Upstash Redis integration for distributed rate limiting
- [ ] Per-principal limits (60 req/min, 1000 req/hour)
- [ ] Per-tool-category limits (github:write 30/min, k8s:write 5/min)
- [ ] HTTP 429 responses with Retry-After header
- [ ] Unit tests + load tests

**Implementation Files:**
- `src/server/ratelimit.ts`
- `tests/ratelimit.test.ts`

**Verification:**
```bash
# Spam requests to trigger rate limit
for i in {1..100}; do
  curl http://localhost:3000/api/mcp \
    -H "Authorization: Bearer token_dev_abc"
done

# Should eventually return HTTP 429:
# {
#   "error": {
#     "code": "rate_limited",
#     "message": "Rate limit exceeded: 60 requests per minute",
#     "retry_after": 30
#   }
# }
```

---

## Phase 3: Quality & Launch (Week 5)

**Goal:** Documentation, testing, security audit, production deployment

### Task 3.1: Documentation Suite
**Priority:** Critical
**Effort:** 6 hours
**Dependencies:** Task 2.5

**Acceptance Criteria:**
- [ ] `CLAUDE-GUIDE.md` - How Claude uses this server
- [ ] `WEBHOOK-MACROS.md` - Available macros + examples
- [ ] `SAFETY-POLICIES.md` - Safety level configuration guide
- [ ] `ARCHITECTURE.md` - System design + diagrams
- [ ] Tool README files (one per tool category)
- [ ] API reference documentation (auto-generated from schemas)

**Files to Create:**
- `docs/CLAUDE-GUIDE.md`
- `docs/WEBHOOK-MACROS.md`
- `docs/SAFETY-POLICIES.md`
- `docs/ARCHITECTURE.md`
- `src/server/tools/github/README.md`
- `src/server/tools/odoo/README.md`
- `src/server/tools/kubernetes/README.md`
- `src/server/tools/n8n/README.md`
- `src/server/tools/vercel/README.md`
- `src/server/tools/supabase/README.md`
- `src/server/tools/digitalocean/README.md`

---

### Task 3.2: Contract Tests
**Priority:** High
**Effort:** 4 hours
**Dependencies:** Task 2.5

**Acceptance Criteria:**
- [ ] MCP protocol schema validation tests
- [ ] Tool input schema validation (JSON Schema)
- [ ] Webhook signature validation tests
- [ ] Error response format validation
- [ ] All tests passing with 100% coverage for validation logic

**Implementation Files:**
- `tests/contracts/mcp-schema.test.ts`
- `tests/contracts/tool-schemas.test.ts`
- `tests/contracts/webhook-signature.test.ts`

---

### Task 3.3: End-to-End Tests
**Priority:** High
**Effort:** 5 hours
**Dependencies:** Task 3.2

**Acceptance Criteria:**
- [ ] Full ask → approve → execute flow test
- [ ] Browser agent workflow test (Playwright)
- [ ] Multi-tool orchestration test (GitHub + Odoo + Vercel)
- [ ] Error recovery test (rollback on failure)
- [ ] Audit log verification test

**Implementation Files:**
- `tests/integration/ask-approve-execute.test.ts`
- `tests/integration/browser-agent.test.ts`
- `tests/integration/multi-tool-orchestration.test.ts`

---

### Task 3.4: Security Audit
**Priority:** Critical
**Effort:** 4 hours
**Dependencies:** Task 3.3

**Acceptance Criteria:**
- [ ] Dependency audit (npm audit, Snyk)
- [ ] Secret scanning (no hardcoded tokens)
- [ ] OWASP Top 10 checklist completed
- [ ] Scope escalation attack test (fail-safe)
- [ ] HMAC replay attack test (fail-safe)
- [ ] Rate limit bypass test (fail-safe)
- [ ] Security findings documented + remediated

**Verification:**
```bash
npm audit --production
# 0 vulnerabilities

snyk test
# No high or critical vulnerabilities

git secrets --scan
# No secrets found
```

---

### Task 3.5: Load Testing
**Priority:** Medium
**Effort:** 3 hours
**Dependencies:** Task 3.4

**Acceptance Criteria:**
- [ ] 100 concurrent requests test (success rate >99%)
- [ ] Tool invocation latency <2s (p95)
- [ ] Health check latency <100ms (p95)
- [ ] Rate limiter holds under load
- [ ] No memory leaks detected

**Load Test Script:**
```bash
# Using autocannon
npx autocannon -c 100 -d 60 \
  -H "Authorization: Bearer token_dev_abc" \
  http://localhost:3000/api/health

# Expected:
# 100 connections, 60s duration
# Success rate: >99%
# p95 latency: <100ms
```

---

### Task 3.6: Production Deployment
**Priority:** Critical
**Effort:** 2 hours
**Dependencies:** Tasks 3.1-3.5

**Acceptance Criteria:**
- [ ] Vercel production deployment successful
- [ ] Environment variables configured in production
- [ ] Health check returns 200 OK
- [ ] All tools callable from production URL
- [ ] Audit logs flowing to Supabase
- [ ] Mattermost notification on deployment success
- [ ] GitHub release created with changelog

**Deployment Checklist:**
```bash
# 1. Final test run
npm run test
npm run lint
npm run type-check

# 2. Build production bundle
npm run build

# 3. Deploy to Vercel production
vercel --prod

# 4. Verify health
curl https://pulser-mcp.vercel.app/api/health

# 5. Smoke test all tools
curl -X POST https://pulser-mcp.vercel.app/api/mcp \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{"method": "tools/list"}'

# 6. Create GitHub release
gh release create v1.0.0 \
  --title "IPAI Remote MCP Connector v1.0.0" \
  --notes "Initial production release"

# 7. Monitor logs for 24h
vercel logs --follow
```

---

### Task 3.7: Post-Launch Monitoring
**Priority:** High
**Effort:** Ongoing
**Dependencies:** Task 3.6

**Acceptance Criteria:**
- [ ] Monitor error rate (<1% target)
- [ ] Monitor latency (p95 <2s for tools, <100ms for health)
- [ ] Monitor rate limit usage (alerts if >80% quota)
- [ ] Weekly audit log summary to Mattermost
- [ ] No security incidents reported

**Monitoring Checklist:**
```bash
# Daily for first week:
- Check Vercel dashboard for errors
- Review audit logs in Supabase
- Verify health check passing
- Check rate limit usage

# Weekly summary to Mattermost:
- Total operations executed
- Success rate
- Top 5 most-used tools
- Error breakdown by tool
```

---

## Task Dependencies Graph

```
Phase 0 (Foundation):
0.1 → 0.2 → 0.3 → 0.5
      ↓
      0.4 → 0.5

Phase 1 (MVP Tools):
0.5 → 1.1 → 1.2
      ↓
      1.3
      ↓
      1.4 → 1.5

Phase 2 (Advanced Tools):
1.5 → 2.1 → 2.5
      ↓
      2.2 → 2.5
      ↓
      2.3 → 2.5
      ↓
      2.4 → 2.5

Phase 3 (Quality & Launch):
2.5 → 3.1
      ↓
      3.2 → 3.3 → 3.4 → 3.5 → 3.6 → 3.7
```

---

## Effort Summary

| Phase | Tasks | Total Hours | Workdays (8h) |
|-------|-------|-------------|---------------|
| Phase 0 | 5 | 13 hours | 1.6 days |
| Phase 1 | 5 | 20 hours | 2.5 days |
| Phase 2 | 5 | 17 hours | 2.1 days |
| Phase 3 | 7 | 24 hours | 3.0 days |
| **Total** | **22** | **74 hours** | **9.2 days** |

**Target Timeline:** 5 weeks (allowing buffer for unknowns)

---

## Approval

**Author:** Jake Tolentino
**Reviewers:** [Pending]
**Approved:** [Pending]

**Change Log:**
- 2025-01-22: Initial task breakdown (v1.0.0)
