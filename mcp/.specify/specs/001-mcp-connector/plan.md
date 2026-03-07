# IPAI Remote MCP Connector — Technical Plan

**Version:** 1.0.0
**Status:** Draft
**Owner:** Jake Tolentino
**Created:** 2025-01-22

---

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│ TIER 1: CLIENT LAYER (User Interaction)                             │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Browser    │  │ Claude Code  │  │   Cursor     │              │
│  │   Agent      │  │              │  │              │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                       │
│         │ Webhook          │ MCP Client       │ MCP Client           │
│         │ (signed)         │ (HTTP)           │ (HTTP)               │
└─────────┼──────────────────┼──────────────────┼───────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TIER 2: MCP SERVER (Vercel Serverless)                              │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ API Routes                                                     │  │
│  │  • POST /api/mcp          (MCP Protocol Handler)             │  │
│  │  • GET  /api/mcp          (Tool Discovery)                   │  │
│  │  • POST /api/bridge/run   (Webhook Bridge - Signed)          │  │
│  │  • GET  /api/bridge/status/:id  (Job Polling)                │  │
│  │  • GET  /api/health       (Health Check)                     │  │
│  │  • GET  /.well-known/oauth-protected-resource                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Middleware Stack                                              │  │
│  │  1. CORS + Origin Validation                                 │  │
│  │  2. Bearer Token Auth + Scope Enforcement                    │  │
│  │  3. Request ID Generation                                    │  │
│  │  4. Rate Limiting (Redis/Upstash)                            │  │
│  │  5. Structured Logging (Pino)                                │  │
│  │  6. Error Handling + Sanitization                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ MCP Tools (7 Categories)                                      │  │
│  │  • github.*         (5 operations)                           │  │
│  │  • odoo.*           (4 operations)                           │  │
│  │  • kubernetes.*     (3 operations)                           │  │
│  │  • n8n.*            (3 operations)                           │  │
│  │  • vercel.*         (3 operations)                           │  │
│  │  • supabase.*       (3 operations)                           │  │
│  │  • digitalocean.*   (3 operations)                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────┘
                                 │
                                 │ API Calls (with retry + circuit breaker)
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TIER 3: INTEGRATION SERVICES                                        │
│                                                                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ GitHub  │  │  Odoo   │  │   K8s   │  │   n8n   │  │ Vercel  │ │
│  │   API   │  │ XML-RPC │  │   API   │  │   API   │  │   API   │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
│                                                                       │
│  ┌─────────┐  ┌─────────┐                                          │
│  │Supabase │  │DigitalO.│                                          │
│  │   API   │  │   API   │                                          │
│  └─────────┘  └─────────┘                                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Patterns

### Pattern A: Ask → Approve → Execute (Browser Agent)

```
1. USER CONTEXT:
   User: "Deploy expense module to production"

2. CLAUDE ANALYZES:
   - Reads current state (GitHub branches, Odoo modules, Vercel deployments)
   - Proposes operation sequence:
     a. Create feature branch
     b. Commit module files
     c. Open PR + wait for CI
     d. Merge PR
     e. Install Odoo module
     f. Deploy Vercel frontend
     g. Verify health

3. CLAUDE ASKS FOR APPROVAL:
   Claude: "I'll coordinate 7 operations across GitHub, Odoo, Vercel.
            Estimated time: 3-5 minutes.
            Approve to proceed?"

4. USER APPROVES:
   User: "Approve"

5. BROWSER AGENT CALLS WEBHOOK BRIDGE:
   POST /api/bridge/run
   Headers:
     X-Signature: HMAC-SHA256(secret, body)
     Authorization: Bearer <token>
   Body:
     {
       "macro": "deploy_expense_module",
       "params": {
         "module_name": "ipai_expense_automation",
         "frontend_app": "expenses"
       },
       "approved_by": "user_123",
       "request_id": "uuid-..."
     }

6. SERVER VALIDATES & ENQUEUES:
   - Verify HMAC signature
   - Check bearer token scopes
   - Log approval event
   - Return job_id + status_url

7. SERVER EXECUTES (async):
   - Call github.repo.create_branch
   - Call github.repo.commit_files
   - Call github.repo.open_pr
   - Poll github.actions.list_runs until CI passes
   - Call github.repo.merge_pr
   - Call odoo.modules.install
   - Call vercel.deployments.create
   - Poll vercel.deployments.get until ready
   - Call odoo.health + vercel.health

8. BROWSER AGENT POLLS STATUS:
   GET /api/bridge/status/:job_id
   Response:
     {
       "status": "in_progress",
       "steps_completed": 5,
       "steps_total": 7,
       "current_step": "Deploying frontend to Vercel",
       "logs": ["✓ Branch created", "✓ Files committed", ...]
     }

9. CLAUDE REPORTS RESULTS:
   Claude: "✅ Deployment completed successfully:
            - PR #456 merged to main
            - Module installed: ipai_expense_automation
            - Frontend: https://expenses.insightpulseai.net
            - Health: All checks passed (3/3)

            Execution time: 4m 32s"
```

### Pattern B: Direct MCP Tool Call (Cursor/Claude Code)

```
1. MCP CLIENT DISCOVERS TOOLS:
   GET /api/mcp
   Response:
     {
       "tools": [
         {
           "name": "github.repo.create_branch",
           "description": "Create a new Git branch",
           "inputSchema": { ... },
           "requiredScopes": ["github:write"]
         },
         ...
       ]
     }

2. USER APPROVES IN CLIENT UI:
   Cursor: "Claude wants to create branch 'feature/expense-fix'. Approve?"
   User: [Clicks Approve]

3. CLIENT CALLS TOOL:
   POST /api/mcp
   Headers:
     Authorization: Bearer <token>
     Content-Type: application/json
   Body:
     {
       "method": "tools/call",
       "params": {
         "name": "github.repo.create_branch",
         "arguments": {
           "repo": "odoo-ce",
           "branch": "feature/expense-fix",
           "from": "main"
         }
       }
     }

4. SERVER EXECUTES:
   - Validate bearer token scopes include "github:write"
   - Log request (request_id, tool, args)
   - Call GitHub API
   - Log response
   - Return result

5. CLIENT RECEIVES RESULT:
   {
     "result": {
       "success": true,
       "branch": "feature/expense-fix",
       "sha": "abc123...",
       "url": "https://github.com/jgtolentino/odoo-ce/tree/feature/expense-fix"
     }
   }
```

---

## Technology Stack

### Core Framework
- **Runtime:** Node.js 20.x (Vercel serverless)
- **Language:** TypeScript 5.x (strict mode)
- **MCP SDK:** @modelcontextprotocol/sdk
- **API Framework:** Next.js 14 (App Router, Route Handlers)

### Authentication & Security
- **Auth:** Bearer tokens (OAuth 2.0 pattern)
- **Signature:** HMAC-SHA256 for webhook bridge
- **Secrets:** Environment variables (Vercel secrets)
- **Rate Limiting:** Upstash Redis (serverless-friendly)

### Logging & Observability
- **Structured Logs:** Pino (JSON output)
- **Tracing:** Request correlation IDs
- **Audit Storage:** Supabase PostgreSQL
- **Monitoring:** Vercel Analytics + custom /api/health

### Testing
- **Unit Tests:** Vitest
- **Integration Tests:** Vitest + MSW (mock service worker)
- **Contract Tests:** MCP schema validation
- **E2E Tests:** Playwright (for browser agent flow)

### External Service Clients
- **GitHub:** @octokit/rest
- **Kubernetes:** @kubernetes/client-node
- **n8n:** Axios (REST API)
- **Odoo:** node-odoo-xmlrpc
- **Vercel:** @vercel/client
- **Supabase:** @supabase/supabase-js
- **DigitalOcean:** axios (REST API)

---

## API Design

### MCP Endpoint

**Tool Discovery:**
```http
GET /api/mcp
Authorization: Bearer <token>

Response 200:
{
  "protocol": "mcp",
  "version": "1.0.0",
  "tools": [
    {
      "name": "github.repo.create_branch",
      "description": "Create a new Git branch from an existing ref",
      "inputSchema": {
        "type": "object",
        "properties": {
          "repo": { "type": "string", "description": "Repository name (owner/repo)" },
          "branch": { "type": "string", "description": "New branch name" },
          "from": { "type": "string", "description": "Source ref (branch/tag/sha)" }
        },
        "required": ["repo", "branch"]
      },
      "requiredScopes": ["github:write"]
    }
  ]
}
```

**Tool Invocation:**
```http
POST /api/mcp
Authorization: Bearer <token>
Content-Type: application/json

{
  "method": "tools/call",
  "params": {
    "name": "github.repo.create_branch",
    "arguments": {
      "repo": "jgtolentino/odoo-ce",
      "branch": "feature/fix-expense",
      "from": "main"
    }
  }
}

Response 200:
{
  "result": {
    "success": true,
    "branch": "feature/fix-expense",
    "sha": "abc123def456...",
    "url": "https://github.com/jgtolentino/odoo-ce/tree/feature/fix-expense"
  }
}

Response 400 (scope missing):
{
  "error": {
    "code": "insufficient_scope",
    "message": "Tool requires scope 'github:write' but token only has 'github:read'"
  }
}
```

### Webhook Bridge Endpoint

**Execute Macro:**
```http
POST /api/bridge/run
Authorization: Bearer <token>
X-Signature: sha256=<hmac-hex>
Content-Type: application/json

{
  "macro": "deploy_expense_module",
  "params": {
    "module_name": "ipai_expense_automation"
  },
  "approved_by": "user_jake",
  "request_id": "req_abc123"
}

Response 202:
{
  "job_id": "job_xyz789",
  "status_url": "/api/bridge/status/job_xyz789",
  "estimated_duration": "180s"
}
```

**Poll Job Status:**
```http
GET /api/bridge/status/job_xyz789
Authorization: Bearer <token>

Response 200:
{
  "job_id": "job_xyz789",
  "status": "in_progress",
  "progress": {
    "steps_completed": 5,
    "steps_total": 7,
    "current_step": "Deploying frontend to Vercel"
  },
  "logs": [
    { "timestamp": "2025-01-22T10:00:00Z", "level": "info", "message": "✓ Branch created" },
    { "timestamp": "2025-01-22T10:00:15Z", "level": "info", "message": "✓ Files committed" }
  ],
  "started_at": "2025-01-22T10:00:00Z",
  "duration_ms": 45000
}

Response 200 (completed):
{
  "job_id": "job_xyz789",
  "status": "completed",
  "result": {
    "pr_url": "https://github.com/jgtolentino/odoo-ce/pull/456",
    "module_status": "installed",
    "frontend_url": "https://expenses.insightpulseai.net",
    "health_checks": ["github:ok", "odoo:ok", "vercel:ok"]
  },
  "completed_at": "2025-01-22T10:04:32Z",
  "duration_ms": 272000
}
```

---

## Security Model

### Authentication Flow

```
1. CLIENT SETUP:
   - Generate bearer token in Vercel dashboard (per principal)
   - Configure scopes (github:read, github:write, odoo:read, etc.)
   - Store token in client environment

2. REQUEST AUTHENTICATION:
   - Client includes: Authorization: Bearer <token>
   - Server validates token against env var ALLOWED_TOKENS
   - Server extracts scopes from token metadata

3. SCOPE ENFORCEMENT:
   - Tool declares required scopes in metadata
   - Server checks: token.scopes ⊇ tool.requiredScopes
   - Reject if insufficient (HTTP 403)

4. WEBHOOK SIGNATURE (Bridge Only):
   - Client computes: HMAC-SHA256(shared_secret, request_body)
   - Client includes: X-Signature: sha256=<hex>
   - Server recomputes HMAC and compares
   - Reject if mismatch (HTTP 401)
```

### Scope Definitions

```typescript
const SCOPES = {
  // GitHub
  'github:read': 'Read repository contents, PR status, workflow runs',
  'github:write': 'Create branches, commit files, open PRs',
  'github:admin': 'Merge PRs, manage branch protection (dangerous)',

  // Odoo
  'odoo:read': 'Query database, check module status, health checks',
  'odoo:write': 'Install/upgrade modules, create records',
  'odoo:admin': 'Database operations, user management (dangerous)',

  // Kubernetes
  'k8s:read': 'View pod logs, deployment status, resource metrics',
  'k8s:write': 'Restart deployments, scale replicas',
  'k8s:admin': 'Delete resources, update configs (dangerous)',

  // n8n
  'n8n:read': 'List workflows, check execution status',
  'n8n:write': 'Trigger workflows, update workflow definitions',

  // Vercel
  'vercel:read': 'List deployments, check build logs',
  'vercel:write': 'Create deployments, manage env vars',

  // Supabase
  'supabase:read': 'Query database via RPC, check migration status',
  'supabase:write': 'Execute RPC functions, apply migrations',

  // DigitalOcean
  'do:read': 'Check app status, list droplets',
  'do:write': 'Deploy apps, restart services'
};
```

### Rate Limiting

```typescript
const RATE_LIMITS = {
  // Per principal (user)
  per_principal: {
    requests_per_minute: 60,
    requests_per_hour: 1000
  },

  // Per tool category
  per_category: {
    'github:*': { requests_per_minute: 30 },
    'odoo:write': { requests_per_minute: 10 },
    'k8s:write': { requests_per_minute: 5 },
    'bridge:*': { concurrent_jobs: 3 }
  },

  // Burst allowance
  burst_multiplier: 2 // Allow 2x rate for short bursts
};
```

---

## Deployment Architecture

### Vercel Configuration

**vercel.json:**
```json
{
  "version": 2,
  "regions": ["sin1"],
  "env": {
    "NODE_ENV": "production",
    "SAFETY_LEVEL": "0"
  },
  "build": {
    "env": {
      "NEXT_PUBLIC_MCP_VERSION": "1.0.0"
    }
  },
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```

### Environment Variables

```bash
# Auth & Security
ALLOWED_TOKENS='{"token_abc123": {"scopes": ["github:write", "odoo:read"]}}'
WEBHOOK_SECRET='secure-random-string-256-bits'
SAFETY_LEVEL='0'  # 0=full manual, 1=read auto, 2=trusted env

# GitHub
GITHUB_TOKEN='ghp_...'
GITHUB_ORG='Insightpulseai-net'

# Odoo
ODOO_URL='https://159.223.75.148'
ODOO_DB='production'
ODOO_USER='admin'
ODOO_PASSWORD='...'

# Kubernetes
K8S_API_SERVER='https://k8s.insightpulseai.net'
K8S_TOKEN='...'

# n8n
N8N_API_KEY='...'
N8N_BASE_URL='https://ipa.insightpulseai.net'

# Vercel
VERCEL_TOKEN='...'
VERCEL_TEAM_ID='...'

# Supabase
SUPABASE_URL='https://xkxyvboeubffxxbebsll.supabase.co'
SUPABASE_SERVICE_ROLE_KEY='...'

# DigitalOcean
DO_ACCESS_TOKEN='...'
DO_PROJECT_ID='29cde7a1-8280-46ad-9fdf-dea7b21a7825'

# Observability
AUDIT_LOG_TABLE='mcp_audit_log'
UPSTASH_REDIS_URL='...'
```

---

## Error Handling Strategy

### Error Categories

```typescript
enum ErrorCategory {
  // Client errors (4xx)
  INVALID_REQUEST = 'invalid_request',
  UNAUTHORIZED = 'unauthorized',
  FORBIDDEN = 'forbidden',
  NOT_FOUND = 'not_found',
  RATE_LIMITED = 'rate_limited',

  // Server errors (5xx)
  INTERNAL_ERROR = 'internal_error',
  DOWNSTREAM_ERROR = 'downstream_error',
  TIMEOUT = 'timeout',

  // Tool-specific
  TOOL_ERROR = 'tool_error',
  VALIDATION_ERROR = 'validation_error'
}
```

### Error Response Format

```json
{
  "error": {
    "code": "insufficient_scope",
    "category": "forbidden",
    "message": "Tool 'github.repo.merge_pr' requires scope 'github:admin' but token only has 'github:write'",
    "details": {
      "tool": "github.repo.merge_pr",
      "required_scopes": ["github:admin"],
      "provided_scopes": ["github:read", "github:write"]
    },
    "remediation": "Request a new token with 'github:admin' scope from your administrator",
    "request_id": "req_abc123",
    "timestamp": "2025-01-22T10:15:30Z"
  }
}
```

### Retry & Circuit Breaker

```typescript
const RETRY_POLICY = {
  max_attempts: 3,
  backoff: 'exponential', // 1s, 2s, 4s
  retryable_errors: [
    'ECONNRESET',
    'ETIMEDOUT',
    'rate_limited',
    'downstream_error'
  ]
};

const CIRCUIT_BREAKER = {
  failure_threshold: 5, // Open circuit after 5 failures
  reset_timeout: 60000, // Try again after 60s
  half_open_requests: 1 // Allow 1 request when half-open
};
```

---

## Testing Strategy

### Test Pyramid

```
           /\
          /  \         E2E Tests (10%)
         /────\        - Full ask→approve→execute flow
        /      \       - Browser agent integration
       /────────\
      /          \     Integration Tests (30%)
     /────────────\    - MCP tool invocations
    /              \   - Downstream service mocking (MSW)
   /────────────────\
  /                  \ Unit Tests (60%)
 /────────────────────\ - Auth middleware
/                      \ - Scope enforcement
────────────────────────  - Error handling
```

### Test Coverage Requirements

```typescript
const COVERAGE_TARGETS = {
  statements: 80,
  branches: 75,
  functions: 80,
  lines: 80,

  critical_paths: {
    auth_middleware: 95,
    scope_enforcement: 95,
    tool_execution: 85,
    error_handling: 90
  }
};
```

### Test Fixtures

**Mock MCP Client Request:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "github.repo.create_branch",
    "arguments": {
      "repo": "test-org/test-repo",
      "branch": "feature/test",
      "from": "main"
    }
  }
}
```

**Mock GitHub API Response:**
```json
{
  "ref": "refs/heads/feature/test",
  "node_id": "REF_kwDOAbc123",
  "url": "https://api.github.com/repos/test-org/test-repo/git/refs/heads/feature/test",
  "object": {
    "sha": "abc123def456",
    "type": "commit",
    "url": "https://api.github.com/repos/test-org/test-repo/git/commits/abc123def456"
  }
}
```

---

## Monitoring & Observability

### Health Check Endpoint

```http
GET /api/health

Response 200:
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "checks": {
    "github_api": { "status": "ok", "latency_ms": 120 },
    "odoo_xmlrpc": { "status": "ok", "latency_ms": 450 },
    "k8s_api": { "status": "ok", "latency_ms": 85 },
    "n8n_api": { "status": "ok", "latency_ms": 200 },
    "vercel_api": { "status": "ok", "latency_ms": 95 },
    "supabase_api": { "status": "ok", "latency_ms": 110 },
    "do_api": { "status": "ok", "latency_ms": 150 },
    "redis": { "status": "ok", "latency_ms": 5 }
  },
  "timestamp": "2025-01-22T10:30:00Z"
}

Response 503 (degraded):
{
  "status": "degraded",
  "version": "1.0.0",
  "checks": {
    "github_api": { "status": "error", "error": "timeout after 5000ms" },
    "odoo_xmlrpc": { "status": "ok", "latency_ms": 450 }
  },
  "timestamp": "2025-01-22T10:30:00Z"
}
```

### Audit Log Schema

**Supabase Table:**
```sql
CREATE TABLE mcp_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id TEXT NOT NULL UNIQUE,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  principal TEXT NOT NULL,
  tool TEXT NOT NULL,
  action TEXT NOT NULL,
  scopes TEXT[] NOT NULL,
  input JSONB NOT NULL,
  output JSONB,
  error JSONB,
  duration_ms INTEGER,
  approved_by TEXT,
  safety_level INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_mcp_audit_timestamp ON mcp_audit_log(timestamp DESC);
CREATE INDEX idx_mcp_audit_principal ON mcp_audit_log(principal);
CREATE INDEX idx_mcp_audit_tool ON mcp_audit_log(tool);
```

---

## Rollback & Disaster Recovery

### Rollback Procedures

**Scenario 1: Bad Deployment**
```bash
# Automatic rollback via Vercel
vercel rollback <deployment-url>

# Or manual revert
git revert <bad-commit-sha>
git push origin main
# Vercel auto-deploys previous version
```

**Scenario 2: Database Migration Failure**
```bash
# Supabase migration rollback
supabase db reset
supabase db push
```

**Scenario 3: Compromised Token**
```bash
# Revoke token in Vercel dashboard
# Or rotate via environment variable
vercel env rm ALLOWED_TOKENS
vercel env add ALLOWED_TOKENS
```

### Disaster Recovery Targets

- **RTO (Recovery Time Objective):** 15 minutes
- **RPO (Recovery Point Objective):** 0 (stateless serverless)
- **MTTR (Mean Time To Repair):** <1 hour
- **Backup Frequency:** Continuous (audit logs in Supabase)

---

## Performance Optimization

### Caching Strategy

```typescript
const CACHE_CONFIG = {
  tool_discovery: {
    ttl: 3600, // 1 hour
    key: 'mcp:tools:list'
  },

  github_file_contents: {
    ttl: 300, // 5 minutes
    key: (repo, path, ref) => `github:file:${repo}:${path}:${ref}`
  },

  odoo_module_status: {
    ttl: 60, // 1 minute
    key: (module) => `odoo:module:${module}:status`
  }
};
```

### Parallel Execution

```typescript
// Example: Parallel health checks
async function healthCheck() {
  const checks = await Promise.allSettled([
    checkGitHubAPI(),
    checkOdooXMLRPC(),
    checkK8sAPI(),
    checkN8nAPI(),
    checkVercelAPI(),
    checkSupabaseAPI(),
    checkDOAPI()
  ]);

  return checks.map((result, i) => ({
    service: SERVICES[i],
    status: result.status === 'fulfilled' ? 'ok' : 'error',
    latency_ms: result.value?.latency
  }));
}
```

---

## Future Enhancements (V2+)

### Planned Features
1. **GUI Dashboard:** Visual job monitoring, approval queue
2. **Workflow Engine:** DAG-based multi-tool orchestration
3. **Custom Tool Builder:** User-defined tools via YAML config
4. **Multi-User Management:** Role-based access control
5. **Advanced Caching:** Redis-backed result caching
6. **Webhook Delivery:** Push notifications for job completion
7. **Metrics Dashboard:** Grafana integration for observability

### Technical Debt Paydown
1. Migrate from Vercel serverless to containerized deployment (optional)
2. Extract tool implementations to separate npm packages
3. Add OpenAPI spec generation
4. Implement GraphQL API (alternative to REST)

---

## Approval

**Author:** Jake Tolentino
**Technical Reviewers:** [Pending]
**Approved:** [Pending]

**Change Log:**
- 2025-01-22: Initial technical plan (v1.0.0)
