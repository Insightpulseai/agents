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
├── agents/             # Agent definitions
├── mcp-server/         # MCP server implementations
├── mcp-ipai-core/      # Core MCP tools
├── tools/              # Tool definitions
├── skills/             # Agent skills
├── prompts/            # Prompt templates
├── eval/               # Evaluation framework
├── tests/              # Test suites
└── mcp/                # Migrated from mcp-core repo
```

## Rules

1. Agents use tool-based architecture (no raw LLM calls)
2. All tools must have schema definitions
3. Secrets via environment variables, never hardcoded
4. MCP servers follow the MCP protocol specification
5. Evaluation required for agent quality changes

## Cross-Repo Map

| Repo | Relationship |
|------|-------------|
| `odoo` | ERP tools and data access |
| `ops-platform` | Supabase state/coordination |
| `lakehouse` | Data intelligence layer |
| `.github` | CI workflows, org governance |
| `infra` | Azure Foundry infrastructure |
