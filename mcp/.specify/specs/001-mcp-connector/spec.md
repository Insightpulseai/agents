# IPAI Remote MCP Connector — Specification

**Version:** 1.0.0
**Status:** Draft
**Owner:** Jake Tolentino
**Created:** 2025-01-22
**Updated:** 2025-01-22

---

## Executive Summary

Build a secure automation bridge (Remote MCP Server) that enables Claude and other AI agents to propose and execute operations across the InsightPulse stack—Odoo, GitHub, Kubernetes, n8n, Vercel, Supabase, DigitalOcean—with explicit user approval at every step.

**Core Value:** Transform 20+ manual cross-platform operations into orchestrated, audited, AI-proposed workflows while maintaining full human control.

---

## Problem Statement

### Current State
You manage a complex multi-service architecture requiring frequent coordinated operations:

**Daily Operations:**
- Deploy code changes across GitHub → Vercel → DigitalOcean
- Manage Odoo modules (install, upgrade, health checks)
- Trigger n8n workflows for BIR compliance
- Monitor Kubernetes pod health and logs
- Coordinate Supabase migrations with app deployments

**Pain Points:**
1. **Manual Context Switching:** 6-8 different UIs/dashboards for a single deployment
2. **Error-Prone Workflows:** Copy-paste commands, forget steps, miss approvals
3. **No Audit Trail:** Hard to track "who did what when and why"
4. **Claude Can't Help:** I can propose solutions but can't execute without you manually running commands
5. **Slow Iteration:** Each change cycle takes 15-30 minutes of manual work

### Desired State
Claude proposes operations → you approve once → Claude executes across all services → full audit trail → you get results in seconds.

---

## Solution Overview

### What We're Building
A **Remote MCP Server** deployed on Vercel that:

1. **Receives Proposals:** I (Claude) analyze your request and propose operations
2. **Gets Approval:** You explicitly approve (single "yes" in chat)
3. **Executes Safely:** Server runs approved operations with proper auth/scopes
4. **Reports Results:** I show you what happened with full audit trail

### Key Capabilities

**GitHub Operations:**
- Create branches, apply patches, commit files
- Open pull requests with proper templates
- Monitor CI/CD workflows
- Fetch files for analysis

**Odoo Operations:**
- Module lifecycle (install, upgrade, uninstall)
- Health checks and diagnostics
- Database queries (read-only by default)
- Backup/restore operations

**Kubernetes Operations:**
- Pod logs and status
- Deployment restarts (with approval)
- Resource metrics
- Config validation

**n8n Operations:**
- Trigger workflows (BIR compliance, sync jobs)
- Monitor execution status
- Fetch workflow definitions

**Vercel Operations:**
- Deployment status and logs
- Environment variable management
- Build cache operations

**Supabase Operations:**
- RPC function calls
- Migration status checks
- Database health monitoring

**DigitalOcean Operations:**
- App Platform deployments
- Droplet status
- Space (CDN) operations

---

## Use Cases

### Primary Use Case: Coordinated Deployment
**Scenario:** Deploy new Odoo module with frontend changes

**Current Workflow (Manual):**
```
1. GitHub UI: Create branch
2. VS Code: Edit files, commit
3. GitHub UI: Open PR
4. GitHub UI: Wait for CI, merge
5. Odoo CLI: Install module
6. Odoo UI: Test functionality
7. Vercel CLI: Deploy frontend
8. Browser: Verify deployment
9. Manual notes: Document what was deployed

Total time: 20-30 minutes
Error rate: 15% (forgotten steps)
```

**Proposed Workflow (MCP-Enabled):**
```
User: "Deploy the expense automation module with frontend"
Claude: "I'll coordinate:
  1. Create feature branch
  2. Commit module files
  3. Open PR
  4. Wait for CI pass
  5. Merge to main
  6. Install module on Odoo
  7. Deploy frontend to Vercel
  8. Verify health checks

  Approve to proceed?"
User: "Approve"
Claude: [Executes all steps via MCP]
Claude: "✅ Deployed successfully:
  - PR #123 merged
  - Module installed: ipai_expense_automation
  - Frontend: https://expenses.insightpulseai.net
  - Health: All checks passed"

Total time: 2-3 minutes
Error rate: <1% (automated)
Audit trail: Complete
```

### Secondary Use Cases

**1. Incident Response**
- Detect Odoo performance issue
- I propose: Check logs, restart if needed, notify team
- You approve
- I execute, report outcome

**2. BIR Compliance Workflow**
- Trigger monthly tax filing workflow (n8n)
- Monitor execution status
- Fetch generated PDFs
- Confirm submission

**3. Multi-Employee Onboarding**
- Create Odoo users across 8 agencies
- Setup GitHub access
- Configure n8n workflow permissions
- Single approval for entire batch

**4. Data Migration**
- Analyze schema changes
- Propose migration script
- You approve with safety checks
- I execute, verify, rollback if issues

---

## Requirements

### Functional Requirements

**FR1: MCP Protocol Compliance**
- Implement Streamable HTTP MCP server (GET + POST)
- Support tool discovery, invocation, result streaming
- OAuth 2.0 Bearer token authentication
- Proper error handling with MCP error codes

**FR2: Tool Suite**
- Minimum 7 tool categories (GitHub, Odoo, K8s, n8n, Vercel, Supabase, DO)
- Each tool has JSON schema, required scopes, examples
- Read operations <2s, write operations <10s response time
- Graceful degradation if downstream service unavailable

**FR3: Approval Flow**
- I propose operations with full context
- You approve explicitly ("yes", "approve", "proceed")
- I execute only after approval
- You can cancel mid-execution

**FR4: Audit Trail**
- Every operation logged (request ID, timestamp, principal, tool, action, outcome)
- Logs stored in Vercel + Supabase (permanent archive)
- Weekly summary to Mattermost
- 90-day retention minimum

**FR5: Safety Controls**
- Scope enforcement (tools cannot escalate privileges)
- Rate limiting (per principal, per tool category)
- High-risk operations require explicit allowlist
- Safety level configuration (0=full manual, 1=read auto, 2=trusted env)

### Non-Functional Requirements

**NFR1: Security**
- All secrets in environment variables
- HMAC signature validation for webhook bridge
- TLS for all external communications
- No secrets in logs (masked/redacted)

**NFR2: Performance**
- Tool invocation <2s for read operations
- Health check endpoint <100ms
- Concurrent request handling (100+ simultaneous)
- Circuit breaker for failing downstream services

**NFR3: Reliability**
- 99.9% uptime target
- Automatic retries with exponential backoff
- Graceful error messages (no stack traces to end user)
- Rollback procedures tested per tool

**NFR4: Observability**
- Structured JSON logging (Pino)
- Request tracing (correlation IDs)
- Health metrics exposed (/api/health)
- Error rates monitored (<1% target)

**NFR5: Developer Experience**
- TypeScript strict mode
- Comprehensive test coverage (80%+)
- Clear error messages with remediation steps
- Documentation per tool (README + examples)

---

## Out of Scope (V1)

- **GUI Dashboard:** V1 is API-only; status via JSON endpoints
- **Multi-User Management:** V1 assumes single principal (you)
- **Advanced Workflow Engine:** Complex DAGs deferred to V2
- **Custom Tool Builder:** V1 ships with predefined tools only
- **Mobile App:** Web/CLI clients only

---

## Success Criteria

**Launch Criteria:**
1. All 7 tool categories operational
2. 80%+ test coverage
3. Security audit passed
4. Documentation complete
5. Successfully coordinate 1 full deployment end-to-end

**Success Metrics (30 days post-launch):**
- Operations coordinated: 50+ workflows
- Time saved: 10+ hours/week
- Error rate: <1%
- User satisfaction: "This is magic" feedback
- Zero security incidents

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Downstream service outage (GitHub, Odoo) | High | Medium | Circuit breaker, graceful degradation, retry logic |
| Unauthorized tool execution | Critical | Low | Scope enforcement, audit trail, explicit approval |
| Secrets leaked in logs | Critical | Low | Automatic masking, code review, secret scanning |
| Performance degradation under load | Medium | Medium | Rate limiting, caching, serverless auto-scaling |
| Breaking changes in MCP protocol | Medium | Low | Version pinning, upgrade testing, fallback modes |

---

## Dependencies

**External Services:**
- GitHub API (authentication, repo operations)
- Vercel API (deployments, logs)
- DigitalOcean API (apps, droplets)
- Kubernetes API (via kubectl proxy or API server)
- n8n API (workflow triggers, execution status)
- Odoo XML-RPC (module operations, queries)
- Supabase REST API + PostgREST (RPC, migrations)

**Development Dependencies:**
- MCP SDK (@modelcontextprotocol/sdk)
- TypeScript 5.x
- Pino (structured logging)
- Vercel serverless runtime
- Vitest (testing)

---

## Timeline

**Week 1: Foundation**
- Repository setup
- MCP server core
- Auth middleware
- Health checks

**Week 2-3: MVP Tools**
- GitHub tool (5 operations)
- Odoo tool (4 operations)
- Vercel tool (3 operations)
- Webhook bridge (ask-approve-execute)

**Week 4: Advanced Tools**
- Kubernetes tool
- n8n tool
- Supabase tool
- DigitalOcean tool

**Week 5: Quality & Launch**
- End-to-end testing
- Security audit
- Documentation
- Production deployment

---

## Approval

**Author:** Jake Tolentino
**Reviewers:** [Pending]
**Approved:** [Pending]

**Change Log:**
- 2025-01-22: Initial draft (v1.0.0)
