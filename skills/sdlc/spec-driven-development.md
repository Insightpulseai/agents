# Skill: Spec-Driven Development

source: https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896
extracted: 2026-03-15
applies-to: agents, ops-platform

## What it is

A development methodology where all agent work begins from structured specifications rather than open-ended prompts. Specifications define requirements, constraints, acceptance criteria, and tech stack boundaries before any code generation begins.

## When to use

| Scenario | Use Spec-Driven | Use Direct Prompt |
|----------|----------------|-------------------|
| New feature development | Yes | No |
| Bug fix with clear repro | Evaluate | Yes (if scoped) |
| Multi-agent workflow task | Yes | No |
| Refactoring / migration | Yes | No |
| One-off script or query | No | Yes |

## Core Pattern

```
1. Problem statement (human input)
   ↓
2. Spec generation (agent + constitution constraints)
   ↓
3. Spec stored in ops.specs (Supabase SSOT)
   ↓
4. Task breakdown → GitHub issues (auto-created)
   ↓
5. Coding agent picks up scoped issue
   ↓
6. PR + tests + review
```

## Spec Structure (IPAI Standard)

```yaml
spec:
  id: "spec-{uuid}"
  title: "Short descriptive title"
  status: "draft | approved | in-progress | completed | cancelled"
  author: "human or agent ID"
  created_at: "ISO 8601"

  requirements:
    - id: "req-001"
      description: "What must be true when this is done"
      priority: "must | should | could"
      acceptance_criteria:
        - "Criterion 1"
        - "Criterion 2"

  constraints:
    tech_stack: "See agents/system/agentic-sdlc-constitution.md"
    repos_affected: ["agents", "infra"]
    security: "No secrets in code, RLS enforced"

  tasks:
    - id: "task-001"
      title: "Scoped task for coding agent"
      github_issue: "Insightpulseai/agents#123"
      assigned_agent: "agent_003"  # CodeGenerator
      status: "pending | in-progress | completed"
```

## Supabase Schema (ops.specs)

```sql
CREATE TABLE ops.specs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  author TEXT NOT NULL,
  spec_body JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX idx_specs_status ON ops.specs(status);
```

## Key Principles

1. Small scoped tasks dramatically outperform open-ended prompts
2. Constitution files constrain agent output to org standards
3. Specs are version-controlled artifacts, not ephemeral prompts
4. Every spec task maps to exactly one GitHub issue
5. Spec state is always queryable from Supabase (not scattered across repos)

## SSOT/SOR Mapping

- Spec definitions → `ops.specs` (Supabase SSOT)
- Task tracking → GitHub Issues (linked from spec)
- Agent assignments → `ops.runs` (which agent is working on which task)
- Completed artifacts → PRs in relevant repos
