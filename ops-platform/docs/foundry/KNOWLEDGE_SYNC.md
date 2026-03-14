# KNOWLEDGE_SYNC.md

## Purpose

Defines the sync doctrine between knowledge source files in repos and
knowledge assets in the Azure AI Foundry portal.

---

## Canonical knowledge sources

| Source file | Repo | Purpose |
|---|---|---|
| `agents/foundry/knowledge/ipai-odoo-knowledge-base.md` | `agents` | Odoo docs, SOPs, runbooks, field references |
| `agents/foundry/knowledge/ipai-knowledge.md` | `agents` | Platform-wide knowledge articles |

---

## Sync rules

### Rule 1 — Repo is the source of truth

Knowledge markdown files are authored and versioned in the `agents` repo.
Portal uploads are derived from repo content, not the other way around.

### Rule 2 — Portal uploads are deployment artifacts

Uploading knowledge to the Foundry portal is a deployment step, not an
authoring step. The repo content is canonical.

### Rule 3 — Knowledge files use standard markdown

No proprietary formatting. Plain markdown with headers, lists, and code
blocks. This ensures portability across search indexing, portal upload,
and local testing.

### Rule 4 — Knowledge assets are referenced in agent manifests

Every knowledge source used by an agent must appear in the agent's
`agent.manifest.yaml` under `knowledge_sources`.

### Rule 5 — Knowledge assets are inventoried in SSOT

Every knowledge file must appear in
`ops-platform/ssot/foundry/knowledge-assets.yaml` for drift detection.

---

## Sync workflow

```
1. Author/edit markdown in agents/foundry/knowledge/
2. Commit and push to agents repo
3. CI validates knowledge-assets.yaml references
4. Upload to Foundry portal (manual or automated)
5. Foundry agent uses uploaded knowledge for grounding
```

---

## Future automation

When the platform matures, the upload step (step 4) should be automated via:

- GitHub Actions workflow triggered on knowledge file changes
- Azure AI Foundry SDK or REST API for programmatic upload
- Validation that portal state matches repo state
