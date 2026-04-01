# CLAUDE.md — Agents

## Purpose

Agent framework, MCP servers, tool definitions, AI runtime coordination.

## Stack

| Item | Value |
|------|-------|
| Runtime | Azure AI Foundry (target), Node.js |
| MCP | Model Context Protocol servers |
| Languages | TypeScript, Python |
| Orchestration | Tool-based agent framework |

## Key Directories

```
/
├── .claude/            # Claude Code config (settings, commands)
├── .mcp.json           # MCP server configuration
├── agents/             # Agent definitions (.yml) and SKILL.md files
├── mcp-server/         # MCP server implementations
├── mcp-ipai-core/      # Core MCP tools
├── tools/              # Tool definitions
├── skills/             # Agent skills
├── prompts/            # Prompt templates
├── eval/               # Evaluation framework
├── tests/              # Test suites (unit, integration, e2e)
├── scripts/            # Build, deploy, and hook scripts
├── docs/               # Architecture and API documentation
├── mcp/                # Migrated from mcp-core repo
└── knowledge/          # Living knowledge system (rules, hypotheses, facts)
```

## Slash Commands

Custom commands available via `.claude/commands/`:
- `/review` — Code quality, security, and convention check
- `/deploy` — Pre-deployment validation checklist
- `/test-all` — Run full test suite with summary

## Rules

1. Agents use tool-based architecture (no raw LLM calls)
2. All tools must have schema definitions
3. Secrets via environment variables, never hardcoded
4. MCP servers follow the MCP protocol specification
5. Evaluation required for agent quality changes

## Knowledge System

Before starting a new task, review existing rules and hypotheses for this domain.
Apply rules by default. Check if any hypothesis can be tested with today's work.

At the end of each task, extract insights.
Store them in domain folders, e.g.:
```
/knowledge/pricing/
    knowledge.md    (facts and patterns)
    hypotheses.md   (need more data)
    rules.md        (confirmed — apply by default)
```

Maintain a `/knowledge/INDEX.md` that routes to each domain folder.

When a hypothesis gets confirmed 5+ times, promote it to a rule.
When a rule gets contradicted by new data, demote it back to a hypothesis.

## Cross-Repo Map

| Repo | Relationship |
|------|-------------|
| `odoo` | ERP tools and data access |
| `ops-platform` | Supabase state/coordination |
| `lakehouse` | Data intelligence layer |
| `.github` | CI workflows, org governance |
| `infra` | Azure Foundry infrastructure |
