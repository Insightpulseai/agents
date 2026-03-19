# Skill: Microsoft Agent Framework

source: https://github.com/microsoft/agent-framework
extracted: 2026-03-15
applies-to: agents, ops-platform

## What it is

MIT-licensed Python + .NET agent orchestration framework (7.2k stars, 105 contributors). Microsoft's official replacement for both Semantic Kernel and AutoGen. Actively released (56 releases, latest `python-1.0.0b260212`). Pre-1.0 but production-targeted.

## When to use (decision matrix)

| Scenario | Use MS Agent Framework | Use n8n | Use custom |
|----------|----------------------|---------|------------|
| Graph-based multi-agent workflows | Yes | No | No |
| Pure integration/webhook routing | No | Yes | No |
| Multi-step agentic reasoning chains | Yes | Possible but complex | Evaluate |
| Simple linear automation | No | Yes | No |

## Key Capabilities vs. Current IPAI Stack

| Capability | Agent Framework | Current IPAI Stack |
|------------|----------------|-------------------|
| Graph-based workflows | Native | n8n (linear/branching) |
| Multi-agent orchestration | Native | Manual via n8n + Claude |
| Streaming + checkpointing | Built-in | Custom Supabase queues |
| Human-in-the-loop | Built-in | Custom review tables |
| Time-travel / replay | Built-in | ops.run_events (DIY) |
| OpenTelemetry observability | Built-in | DIY via OTLP |
| DevUI for local debugging | python/packages/devui | None |
| Provider-agnostic (Claude, etc.) | Multi-provider | Claude-first |
| Self-hosted / portable | MIT, no Foundry required | Yes |

## Critical Architecture Note

The framework is **control-plane agnostic** — it doesn't own state. This is the key leverage point for IPAI:

```
Agent Framework (orchestration layer)
        ↓ emits run events / artifacts
Supabase ops.* (SSOT / control plane)
        ↓ posts accounting artifacts
Odoo (SOR / ledger)
```

Use `ops.runs` + `ops.run_events` as the backing store for AF's checkpointing, rather than letting AF manage its own state persistence internally. Supabase remains the canonical source for orchestration state; AF acts as a stateless executor.

## Adoption Path (Low-Risk)

### Phase 1 — Local Evaluation
Run AF locally with DevUI against existing Supabase `ops.*` schema. Use for document processing pipelines (PaddleOCR → Odoo) where multi-step agent reasoning is already needed.

### Phase 2 — ACA Deployment
Deploy as an Azure Container App alongside `ipai-odoo-dev-web/cron/worker` in `rg-ipai-dev`. AF runs stateless; Supabase owns all checkpoint/event state.

### Phase 3 — Workflow Migration
Migrate complex n8n workflows that are really multi-agent reasoning chains (BIR compliance extraction, reconciliation review loops) into AF graph workflows. Keep n8n for pure integration/webhook routing.

## Repo Structure (Reference)

```
microsoft/agent-framework/
├── python/
│   ├── packages/          # installable sub-packages (incl. devui, lab)
│   └── samples/
│       ├── 01-get-started/
│       ├── 02-agents/
│       └── 03-workflows/
├── dotnet/
│   └── samples/GettingStarted/
├── schemas/               # typed workflow/agent schema contracts
├── workflow-samples/
└── docs/
    └── decisions/         # ADRs
```

## Gaps / Watch

- 589 open issues — active but pre-1.0 (`--pre` install flag required)
- Pin versions for any production use
- Migration from AutoGen guide exists if evaluating AutoGen patterns
- `schemas/` directory contains typed workflow contracts — useful as reference for IPAI OpenAPI/SSOT contract layer

## SSOT/SOR Mapping

- AF is NOT SSOT — it is a stateless orchestration layer
- All run state → `ops.runs` + `ops.run_events` (Supabase)
- Workflow definitions → version-controlled in `agents/workflows/`
- Agent configs → `agents/*.SKILL.md` (existing pattern)
