# agents

Agent personas, skills, judges, evals, metadata, and prompt contracts.

## Owns

- Agent definitions and personas
- Skill specifications
- Judge and evaluator assets
- Agent registries and metadata
- Prompt and policy contracts

## Does not own

- Agent runtime hosting (`agent-platform`)
- Chat backend services (`agent-platform`)
- ERP business workflows (`odoo`)
- Document ingestion pipelines (`agent-platform`)

## Boundary

This repo **defines** agents. It does not **run** them. Runtime and orchestration live in `agent-platform`.

## Related

- `agent-platform` — runtime and orchestration plane
- `platform` — shared control-plane contracts
- `docs` — governance and operating model

## Status

Canonical agent specification repository.
