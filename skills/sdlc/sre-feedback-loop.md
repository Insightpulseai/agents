# Skill: SRE Feedback Loop — Day-2 Operations

source: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896
extracted: 2026-03-15
applies-to: agents, automations, .github

## What it is

A closed-loop pattern where an SRE agent continuously monitors telemetry, detects anomalies, creates incidents, and triggers the coding agent to produce fixes — completing the agentic SDLC cycle.

## When to use

| Scenario | Use SRE Loop | Use Manual Ops |
|----------|-------------|----------------|
| Production service degradation detected | Yes | Escalation path |
| Recurring known-class errors | Yes | No |
| Infrastructure provisioning changes | No | Yes |
| Security incident response | No | Yes (human-led) |
| Performance regression after deploy | Yes | No |

## Core Pattern

```
Telemetry (logs, metrics, traces)
  ↓ SRE agent watches continuously
Anomaly detected
  ↓ classifies severity + root cause hypothesis
ops.incidents (Supabase SSOT)
  ↓ creates structured incident record
GitHub issue (auto-created)
  ↓ scoped task with repro + hypothesis
Coding agent (picks up issue)
  ↓ produces fix PR
Quality gate + human review
  ↓ merge + deploy
SRE agent verifies fix
  ↓ closes incident in ops.incidents
```

## Sub-Agent Architecture

```
SRE Primary Agent
├── Telemetry Analyzer (sub-agent)
│   └── Reads: Azure Monitor, App Insights, Supabase logs
├── Issue Creator (sub-agent)
│   └── Creates: GitHub issue with structured template
├── Incident Manager (sub-agent)
│   └── Updates: ops.incidents status, notifies stakeholders
└── Verification Agent (sub-agent)
    └── Confirms: fix deployed, metrics normalized
```

Each sub-agent has narrow context — no single agent sees the full stack.

## Supabase Schema (ops.incidents)

```sql
CREATE TABLE ops.incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
  status TEXT NOT NULL DEFAULT 'detected',
  detected_at TIMESTAMPTZ DEFAULT now(),
  resolved_at TIMESTAMPTZ,
  root_cause TEXT,
  hypothesis TEXT,
  github_issue_url TEXT,
  fix_pr_url TEXT,
  telemetry_snapshot JSONB,
  created_by TEXT NOT NULL DEFAULT 'sre-agent',
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_incidents_status ON ops.incidents(status);
CREATE INDEX idx_incidents_severity ON ops.incidents(severity);
```

## Telemetry Sources (IPAI)

| Source | What it provides | Integration |
|--------|-----------------|-------------|
| Azure Monitor | ACA container metrics, health | Azure SDK |
| Application Insights | Request traces, exceptions | OTLP export |
| Supabase Logs | Edge Function errors, auth events | Supabase API |
| GitHub Actions | CI/CD failure events | Webhook → n8n |
| Odoo | ERP error logs, cron failures | Odoo XML-RPC |

## Key Principles

1. SRE agent observes — never modifies production directly
2. All incidents are recorded in `ops.incidents` before any action
3. Fixes go through the same PR → review → deploy path as features
4. Human escalation path for critical severity (agent creates, human decides)
5. Verification step required before incident closure

## SSOT/SOR Mapping

- Incident state → `ops.incidents` (Supabase SSOT)
- Incident actions → `ops.run_events` (linked to incident ID)
- Fix artifacts → GitHub PRs (linked from incident record)
- Post-mortem → `ops.incidents.root_cause` (updated after resolution)

## Cross-references

- Agentic SDLC pattern: `skills/sdlc/agentic-sdlc-msft-pattern.md`
- Spec-driven development: `skills/sdlc/spec-driven-development.md`
- Runbooks: `automations/runbooks/`
