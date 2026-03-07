# CLAUDE.md — Project Orchestration Rules (IPAI Remote MCP Connector)

## 0. Purpose

This file describes **how Claude Code should behave in THIS repo only**:
- What to execute
- What tools/CLIs are allowed
- What infra is in scope
- What gates must pass before work is considered "done"

All framework-level behavior (personas, wave mode, skills, etc.) lives in `~/.claude/CLAUDE.md` and related global docs.

---

## 1. Execution Model

- **Claude Code = orchestrator + executor** in this repo.
- Use **direct terminal access** (npm, git, curl, vercel).
- **No guides instead of actions** – respond with runnable commands, not UI click-paths.
- Assume **execution intent by default**: once a plan is formed, act until acceptance gates pass.

---

## 2. Project Context

**Name:** IPAI Remote MCP Connector (`pulser-mcp`)
**Purpose:** Secure automation bridge enabling Claude to propose and execute operations across InsightPulse stack
**Owner:** Jake Tolentino
**Stack:** Next.js 14 (App Router) + TypeScript + Vercel Serverless

---

## 3. Development Environment

**Allowed CLIs:**
- `npm` - Package management, testing, linting
- `git` - Version control operations
- `vercel` - Deployment to staging/production
- `curl` - API testing
- `psql` - Supabase audit log queries (read-only)

**Prohibited:**
- Direct database writes to Supabase (use RPC only)
- Local Docker (project is serverless-only)
- Azure services (project uses Vercel + Supabase + DigitalOcean)
- Notion API (deprecated for this project)

---

## 4. Repository Structure (Spec-Kit Compliant)

**Core Directories:**
- `.specify/` - Spec-Kit memory (constitution, spec, plan, tasks, contracts)
- `src/` - TypeScript source code
- `tests/` - Test suites (unit, integration, contract, e2e)
- `docs/` - Documentation (CLAUDE-GUIDE, WEBHOOK-MACROS, etc.)
- `.github/workflows/` - CI/CD pipelines

**Key Files:**
- `CLAUDE.md` - This file (project-specific orchestration rules)
- `README.md` - Public-facing documentation
- `package.json` - npm configuration
- `tsconfig.json` - TypeScript configuration
- `vercel.json` - Vercel deployment configuration

---

## 5. Spec-Kit Integration

**Memory Location:** `.specify/memory/constitution.md`
**Specifications:** `.specify/specs/001-mcp-connector/`

**Available Documents:**
- `spec.md` - Functional specification (what/why)
- `plan.md` - Technical architecture (how/architecture)
- `tasks.md` - Actionable task breakdown (implementation roadmap)
- `contracts/` - API contracts (MCP schemas, webhook specs)

**Usage:**
- Always reference Spec-Kit docs before making architectural decisions
- Update tasks.md when completing implementation phases
- Add new contracts to `contracts/` when adding tools

---

## 6. Development Workflow

### Standard Task Flow

**1. Read Spec:**
```bash
# Consult relevant specification
cat .specify/specs/001-mcp-connector/tasks.md | grep "Task 1.1"
```

**2. Write Tests First:**
```bash
# Create test file
touch tests/tools/github.test.ts

# Write failing test
npm run test:watch
```

**3. Implement:**
```bash
# Create implementation file
touch src/server/tools/github.ts

# Implement until tests pass
npm run test
```

**4. Verify Quality:**
```bash
npm run lint
npm run type-check
npm run test:coverage
```

**5. Commit:**
```bash
git add .
git commit -m "feat(github): implement get_file tool

- Add github.repo.get_file tool
- Add tests with 95% coverage
- Update MCP tool registry
- Closes #12"
```

### Branch Strategy

- `main` - Production (protected, requires PR)
- `staging` - Pre-production testing
- `feature/*` - Feature branches
- `fix/*` - Bug fixes

**Never commit directly to main** - always use pull requests.

---

## 7. Testing Requirements

**Minimum Coverage:** 80% (statements, branches, functions, lines)

**Test Types:**
1. **Unit Tests** (`tests/*.test.ts`) - Pure logic, no external dependencies
2. **Integration Tests** (`tests/integration/*.test.ts`) - Mocked external services (MSW)
3. **Contract Tests** (`tests/contracts/*.test.ts`) - MCP schema validation
4. **E2E Tests** (`tests/integration/ask-approve-execute.test.ts`) - Full workflow

**Test Commands:**
```bash
npm run test              # Run all tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
npm run test:integration  # Integration only
```

---

## 8. Acceptance Gates

**ALL must pass before marking task complete:**

1. **Tests:** `npm run test` - All tests pass
2. **Lint:** `npm run lint` - Zero warnings
3. **Type Check:** `npm run type-check` - Zero errors
4. **Coverage:** ≥80% on new code
5. **Security:** No high/critical vulnerabilities (`npm audit`)
6. **Functionality:** Manual verification via curl or Vercel preview URL
7. **Documentation:** Updated README/docs if API changes
8. **Task Status:** Mark task complete in `.specify/specs/001-mcp-connector/tasks.md`

**Never claim "done" without all gates passing.**

---

## 9. Environment Variables

**Storage:** Never commit secrets to git. Use `.env.local` (gitignored) for local dev.

**Required Variables:**
```bash
# Auth & Security
ALLOWED_TOKENS='{"token_dev_abc": {"scopes": ["github:read", "odoo:read"]}}'
WEBHOOK_SECRET='<256-bit random string>'
SAFETY_LEVEL='0'  # 0=full manual, 1=read auto, 2=trusted env

# GitHub
GITHUB_TOKEN='ghp_...'
GITHUB_ORG='Insightpulseai-net'

# Odoo (production - use with caution)
ODOO_URL='https://159.223.75.148'
ODOO_DB='production'
ODOO_USER='admin'
ODOO_PASSWORD='<from ~/.zshrc>'

# Add other service tokens as needed
```

**Reference:** See `.env.example` for full list.

---

## 10. Deployment Workflow

**Staging:**
```bash
# Deploy to staging
vercel

# Verify health
curl https://pulser-mcp-staging.vercel.app/api/health

# Test tools
curl -X POST https://pulser-mcp-staging.vercel.app/api/mcp \
  -H "Authorization: Bearer $STAGING_TOKEN" \
  -d '{"method": "tools/list"}'
```

**Production:**
```bash
# Final checks
npm run test
npm run lint
npm run type-check

# Deploy to production
vercel --prod

# Verify health
curl https://pulser-mcp.vercel.app/api/health

# Smoke test all tools
curl -X POST https://pulser-mcp.vercel.app/api/mcp \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{"method": "tools/list"}'

# Monitor for 5 minutes
vercel logs --follow
```

**Never deploy to production without:**
- All tests passing
- PR reviewed and approved
- Staging deployment successful
- Manual smoke testing completed

---

## 11. Tool Development Guidelines

**When adding a new MCP tool:**

1. **Define Contract First:**
   ```bash
   # Create contract file
   touch .specify/specs/001-mcp-connector/contracts/[tool-name].json
   ```

2. **Write JSON Schema:**
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

3. **Write Test:**
   ```typescript
   // tests/tools/github.test.ts
   import { describe, it, expect } from 'vitest';
   import { githubGetFile } from '@/server/tools/github';

   describe('github.repo.get_file', () => {
     it('should fetch file contents', async () => {
       const result = await githubGetFile({
         repo: 'Insightpulseai-net/pulser-mcp',
         path: 'README.md'
       });

       expect(result.success).toBe(true);
       expect(result.content).toContain('# IPAI Remote MCP Connector');
     });
   });
   ```

4. **Implement:**
   ```typescript
   // src/server/tools/github.ts
   import { Octokit } from '@octokit/rest';

   export async function githubGetFile(args: {
     repo: string;
     path: string;
     ref?: string;
   }) {
     const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
     const [owner, repoName] = args.repo.split('/');

     const { data } = await octokit.repos.getContent({
       owner,
       repo: repoName,
       path: args.path,
       ref: args.ref || 'main'
     });

     if ('content' in data) {
       return {
         success: true,
         content: Buffer.from(data.content, 'base64').toString('utf-8'),
         sha: data.sha
       };
     }

     throw new Error('Path is not a file');
   }
   ```

5. **Register Tool:**
   ```typescript
   // src/server/mcp.ts
   const TOOLS = [
     {
       name: 'github.repo.get_file',
       description: 'Fetch file contents from a GitHub repository',
       handler: githubGetFile,
       requiredScopes: ['github:read']
     },
     // ... other tools
   ];
   ```

---

## 12. SuperClaude Framework Integration

**This project inherits global SuperClaude behavior from `~/.claude/CLAUDE.md`.**

**Auto-Activation:**
- `backend` persona (API development, serverless architecture)
- `security` persona (auth, scopes, HMAC signatures)
- `qa` persona (testing, validation, contract compliance)

**MCP Integration:**
- This project IS an MCP server
- Uses `@modelcontextprotocol/sdk` for protocol implementation
- Supports Streamable HTTP transport

**Skills:**
- No custom skills required for this project
- Leverages global backend and security skills from `~/.claude/superclaude/skills/`

---

## 13. Debugging & Troubleshooting

**Common Issues:**

**1. Tests Failing:**
```bash
# Check error messages
npm run test -- --reporter=verbose

# Run specific test file
npm run test tests/tools/github.test.ts

# Debug with watch mode
npm run test:watch
```

**2. TypeScript Errors:**
```bash
# Check types
npm run type-check

# Fix auto-fixable issues
npm run lint:fix
```

**3. Deployment Failures:**
```bash
# Check Vercel logs
vercel logs

# Verify environment variables
vercel env ls

# Redeploy with verbose output
vercel --debug
```

**4. Tool Not Working:**
```bash
# Test tool directly via curl
curl -X POST http://localhost:3000/api/mcp \
  -H "Authorization: Bearer token_dev_abc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "github.repo.get_file",
      "arguments": {"repo": "test/repo", "path": "README.md"}
    }
  }' | jq

# Check server logs
npm run dev  # Watch terminal for errors
```

---

## 14. Safety & Security

**Prohibited Actions:**
- Never hardcode tokens in source code
- Never commit `.env.local` or `.env`
- Never log full secrets (mask with `${TOKEN:0:10}`)
- Never execute operations without explicit approval (when `SAFETY_LEVEL=0`)
- Never skip scope validation
- Never bypass HMAC signature validation

**Required Actions:**
- Always validate input schemas
- Always enforce scope requirements
- Always log operations to audit trail
- Always use HTTPS for external API calls
- Always implement retry logic with exponential backoff
- Always use circuit breaker for flaky downstream services

---

## 15. Documentation Requirements

**When adding features:**
- Update `README.md` if user-facing changes
- Update `docs/CLAUDE-GUIDE.md` if Claude usage changes
- Update `.specify/specs/001-mcp-connector/tasks.md` to mark tasks complete
- Add tool README in `src/server/tools/[category]/README.md`

**Documentation Standards:**
- Examples must be runnable
- Code blocks must specify language
- All public APIs documented
- Error codes explained with remediation steps

---

## 16. Version Control

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `test` - Test-related changes
- `refactor` - Code refactoring
- `chore` - Build/tooling changes

**Example:**
```
feat(github): add branch creation tool

- Implement github.repo.create_branch
- Add tests with 90% coverage
- Update MCP tool registry
- Add contract schema

Closes #15
```

---

## 17. Performance Requirements

**Response Time Targets:**
- Health check: <100ms (p95)
- Tool invocation (read): <2s (p95)
- Tool invocation (write): <10s (p95)
- Webhook bridge execution: <30s per macro

**Resource Limits:**
- Memory: <512MB per serverless function
- Execution timeout: 60s max (Vercel limit)
- Concurrent connections: 100+ without degradation

---

## 18. Monitoring & Observability

**Health Check:**
```bash
curl https://pulser-mcp.vercel.app/api/health | jq
```

**Audit Logs (Supabase):**
```sql
SELECT
  timestamp,
  principal,
  tool,
  action,
  duration_ms,
  approved_by,
  error
FROM mcp_audit_log
WHERE timestamp > NOW() - INTERVAL '24 hours'
  AND error IS NOT NULL
ORDER BY timestamp DESC
LIMIT 10;
```

**Vercel Logs:**
```bash
# Real-time logs
vercel logs --follow

# Filter by function
vercel logs --follow --function api/mcp

# Last 100 lines
vercel logs --tail 100
```

---

## 19. Rollback Procedures

**Scenario 1: Bad Deployment**
```bash
# Rollback to previous deployment
vercel rollback <deployment-url>

# Or revert commit and redeploy
git revert <bad-commit-sha>
git push origin main
```

**Scenario 2: Compromised Token**
```bash
# Revoke token in Vercel dashboard
# Or rotate via CLI
vercel env rm ALLOWED_TOKENS
vercel env add ALLOWED_TOKENS
vercel redeploy --prod
```

**Scenario 3: Database Issue**
```bash
# Audit logs are append-only
# No rollback needed, just stop writing
```

---

## 20. Approval & Change Management

**Before Major Changes:**
1. Create spec update in `.specify/specs/001-mcp-connector/`
2. Get approval from project owner (Jake Tolentino)
3. Create feature branch
4. Implement with tests
5. Open PR with clear description
6. Wait for review and approval
7. Merge to main
8. Deploy to staging, then production

**This file is versioned and subject to review.**

---

**Last Updated:** 2025-01-22
**Version:** 1.0.0
**Owner:** Jake Tolentino
