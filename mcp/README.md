# IPAI Remote MCP Connector

**Secure automation bridge for InsightPulse AI stack**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Insightpulseai-net/pulser-mcp/releases)
[![License](https://img.shields.io/badge/license-AGPL--3.0-green.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)

---

## Overview

The **IPAI Remote MCP Connector** is a production-grade Model Context Protocol (MCP) server that enables Claude and other AI agents to safely propose and execute operations across your entire InsightPulse stack—with you in control at every step.

**Core Value:** Transform 20+ manual cross-platform operations into orchestrated, audited, AI-proposed workflows while maintaining full human control.

---

## Features

- **✅ Ask-Approve-Execute:** Claude proposes → you approve → Claude executes
- **🔒 Security First:** Bearer token auth, scope enforcement, HMAC signatures
- **📊 Full Audit Trail:** Every operation logged (who, what, when, why, outcome)
- **🚀 Multi-Service:** GitHub, Odoo, Kubernetes, n8n, Vercel, Supabase, DigitalOcean
- **⚡ Fast:** <2s tool invocations, <100ms health checks
- **🛡️ Safe by Default:** Explicit approval required, no auto-execution
- **🔄 Production-Grade:** Retry logic, circuit breakers, rate limiting

---

## Quick Start

### Prerequisites

- Node.js 20+ and npm 10+
- GitHub account with API token
- Vercel account (for deployment)
- InsightPulse stack access (Odoo, K8s, n8n, etc.)

### Installation

```bash
# Clone repository
git clone https://github.com/Insightpulseai-net/pulser-mcp.git
cd pulser-mcp

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local with your tokens

# Start development server
npm run dev
```

### Configuration

Create `.env.local` with required tokens:

```bash
# Auth & Security
ALLOWED_TOKENS='{"token_dev_abc": {"scopes": ["github:read", "odoo:read"]}}'
WEBHOOK_SECRET='secure-random-string-256-bits'
SAFETY_LEVEL='0'  # 0=full manual, 1=read auto, 2=trusted env

# GitHub
GITHUB_TOKEN='ghp_...'

# Odoo
ODOO_URL='https://159.223.75.148'
ODOO_DB='production'
ODOO_USER='admin'
ODOO_PASSWORD='...'

# Add other service tokens as needed
```

### Verify Installation

```bash
# Run tests
npm run test

# Check health endpoint
curl http://localhost:3000/api/health

# List available tools
curl -H "Authorization: Bearer token_dev_abc" \
  http://localhost:3000/api/mcp
```

---

## Architecture

```
┌─────────────────┐
│  Browser Agent  │  ← User approves operations
│  Claude Code    │
│  Cursor         │
└────────┬────────┘
         │ MCP Protocol (HTTP)
         ▼
┌─────────────────────────────┐
│  Vercel Serverless (SG)     │
│  • Bearer Token Auth        │
│  • Scope Enforcement        │
│  • Rate Limiting            │
│  • Audit Logging            │
└────────┬────────────────────┘
         │ API Calls
         ▼
┌─────────────────────────────┐
│  Integration Services       │
│  • GitHub • Odoo • K8s      │
│  • n8n • Vercel • Supabase  │
│  • DigitalOcean             │
└─────────────────────────────┘
```

**Key Components:**

- **MCP Server:** `/api/mcp` (tool discovery + invocation)
- **Webhook Bridge:** `/api/bridge` (signed macros for browser agents)
- **Health Check:** `/api/health` (service status)
- **Tools:** 7 categories, 24+ operations

---

## Usage

### Example: Deploy Odoo Module

**1. Claude Proposes:**
```
User: "Deploy expense automation module to production"

Claude: "I'll coordinate:
  1. Create feature branch
  2. Commit module files
  3. Open PR + wait for CI
  4. Merge PR
  5. Install module on Odoo
  6. Deploy frontend to Vercel
  7. Verify health checks

  Approve to proceed?"
```

**2. User Approves:**
```
User: "Approve"
```

**3. Claude Executes:**
```bash
# Claude calls MCP tools via bridge
POST /api/bridge/run
{
  "macro": "deploy_expense_module",
  "params": {"module_name": "ipai_expense_automation"}
}
```

**4. Claude Reports:**
```
Claude: "✅ Deployed successfully:
  - PR #456 merged
  - Module installed: ipai_expense_automation
  - Frontend: https://expenses.insightpulseai.net
  - Health: All checks passed (3/3)

  Execution time: 4m 32s"
```

---

## Available Tools

### GitHub (`github.*`)
- `repo.get_file` - Fetch file contents
- `repo.apply_patch` - Apply Git patch
- `repo.commit_files` - Commit multiple files
- `repo.create_branch` - Create new branch
- `repo.open_pr` - Open pull request
- `actions.list_runs` - List CI/CD runs

### Odoo (`odoo.*`)
- `health` - Health check + version
- `modules.install` - Install module
- `modules.upgrade` - Upgrade module
- `modules.list` - List installed modules

### Kubernetes (`k8s.*`)
- `deployments.logs` - Fetch pod logs
- `deployments.restart` - Restart deployment
- `deployments.status` - Get deployment status

### n8n (`n8n.*`)
- `workflow.trigger` - Trigger workflow
- `executions.list` - List executions
- `executions.get` - Get execution details

### Vercel (`vercel.*`)
- `deployments.list` - List deployments
- `deployments.logs` - Fetch logs
- `deployments.get` - Get status

### Supabase (`supabase.*`)
- `rpc.call` - Execute RPC function
- `migrations.status` - Check migrations
- `health` - Database health

### DigitalOcean (`do.*`)
- `apps.deploy` - Deploy to App Platform
- `apps.status` - Check app status
- `apps.logs` - Fetch app logs

---

## Development

### Project Structure

```
pulser-mcp/
├── .specify/              # Spec-Kit memory
│   ├── memory/
│   │   └── constitution.md
│   └── specs/001-mcp-connector/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── contracts/
├── src/
│   ├── server/            # MCP server core
│   │   ├── mcp.ts
│   │   ├── auth.ts
│   │   ├── bridge.ts
│   │   └── tools/
│   ├── app/api/           # Next.js routes
│   │   ├── mcp/
│   │   ├── bridge/
│   │   └── health/
│   └── lib/               # Shared utilities
├── tests/                 # Test suites
├── docs/                  # Documentation
└── CLAUDE.md              # AI agent instructions
```

### Running Tests

```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage

# Integration tests only
npm run test:integration
```

### Linting & Formatting

```bash
# Lint
npm run lint

# Auto-fix lint issues
npm run lint:fix

# Format code
npm run format

# Check formatting
npm run format:check
```

---

## Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Link project
vercel link

# Deploy to staging
vercel

# Deploy to production
vercel --prod
```

### Environment Variables (Vercel)

Configure in Vercel dashboard:
1. Go to Project Settings → Environment Variables
2. Add all tokens from `.env.local`
3. Redeploy

---

## Security

### Scope System

Every tool declares required scopes:
- `github:read` - Read-only GitHub operations
- `github:write` - Branch/PR creation
- `odoo:write` - Module installation
- `k8s:write` - Deployment restarts

Tokens are validated on every request. Insufficient scopes → HTTP 403.

### HMAC Signatures (Webhook Bridge)

```typescript
// Client computes signature
const signature = crypto
  .createHmac('sha256', WEBHOOK_SECRET)
  .update(JSON.stringify(body))
  .digest('hex');

// Include in request
headers: {
  'X-Signature': `sha256=${signature}`
}
```

Server validates signature before executing.

### Rate Limiting

- **Per Principal:** 60 req/min, 1000 req/hour
- **Per Tool Category:** `github:write` 30/min, `k8s:write` 5/min
- **Burst Allowance:** 2x rate for short bursts

---

## Monitoring

### Health Check

```bash
curl https://pulser-mcp.vercel.app/api/health

# Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "checks": {
    "github_api": {"status": "ok", "latency_ms": 120},
    "odoo_xmlrpc": {"status": "ok", "latency_ms": 450}
  }
}
```

### Audit Logs

All operations logged to Supabase table `mcp_audit_log`:

```sql
SELECT
  timestamp,
  principal,
  tool,
  action,
  duration_ms,
  approved_by
FROM mcp_audit_log
WHERE timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;
```

---

## Documentation

- **[Constitution](/.specify/memory/constitution.md)** - Project principles & guardrails
- **[Specification](/.specify/specs/001-mcp-connector/spec.md)** - Functional spec
- **[Technical Plan](/.specify/specs/001-mcp-connector/plan.md)** - Architecture & design
- **[Tasks](/.specify/specs/001-mcp-connector/tasks.md)** - Implementation roadmap
- **[CLAUDE Guide](/docs/CLAUDE-GUIDE.md)** - How Claude uses this server
- **[Webhook Macros](/docs/WEBHOOK-MACROS.md)** - Available macros
- **[Safety Policies](/docs/SAFETY-POLICIES.md)** - Safety level configuration

---

## Contributing

This is an internal project for InsightPulse AI. External contributions are not currently accepted.

### Development Workflow

1. **Create Feature Branch:**
   ```bash
   git checkout -b feature/new-tool
   ```

2. **Write Tests First:**
   ```bash
   # Add tests to tests/tools/
   npm run test:watch
   ```

3. **Implement Tool:**
   ```bash
   # Add implementation to src/server/tools/
   ```

4. **Verify:**
   ```bash
   npm run lint
   npm run type-check
   npm run test
   ```

5. **Open PR:**
   ```bash
   git push origin feature/new-tool
   gh pr create
   ```

---

## License

AGPL-3.0 - See [LICENSE](LICENSE) file for details.

---

## Support

- **Issues:** [GitHub Issues](https://github.com/Insightpulseai-net/pulser-mcp/issues)
- **Internal Docs:** See `.specify/specs/` for detailed specifications
- **Owner:** Jake Tolentino (Finance SSC Manager / Odoo Developer)

---

**Built with ❤️ for InsightPulse AI**
