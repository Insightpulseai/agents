# Publish Policy — ipai-odoo-copilot-azure

## Pre-Publish Checklist

Before publishing any version as an Agent Application:

- [ ] All instructions reviewed and finalized
- [ ] Model selection confirmed (currently `gpt-4o`)
- [ ] Tools enabled intentionally — no stale or unused tools
- [ ] Knowledge files are current and version-tagged
- [ ] Traces run against all four query categories:
  - Informational
  - Navigational
  - Compliance-calendar
  - Dry-run transactional
- [ ] Evaluation suite passed (see `evals/`)
- [ ] No false-positive write recommendations in PROD-ADVISORY mode
- [ ] Latency p95 < 8 seconds

## Staging

- Publish to staging Agent Application first.
- Soak for minimum 24 hours with real traffic patterns.
- Review traces and metrics before promoting to production.

## Production

- Only promote after staging soak passes.
- Tag the published version with semver (e.g. `v1.0.0`).
- Update `metadata.yaml` version field to match.
- Notify the ops channel after production publish.

## Rollback

- Keep the previous production version available.
- Rollback by republishing the prior version — do not delete.
- Document the rollback reason in the release log.

## Access Control

- Only authorized team members may publish to production.
- Publishing requires review from at least one compliance-domain owner.
