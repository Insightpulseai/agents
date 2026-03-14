# Publish Policy

## Pre-publish checklist

- [ ] Agent instructions finalized
- [ ] Model selection confirmed
- [ ] Tools enabled intentionally (no accidental tool exposure)
- [ ] Knowledge files current
- [ ] Traces run against informational, navigational, compliance, and dry-run transactional requests
- [ ] Evaluations pass acceptance threshold

## Publishing

- Save a named version before publishing
- Publish as Agent Application to get a stable endpoint
- Record the Agent Application ID and endpoint URL

## Post-publish

- Configure backend adapter with the published endpoint
- Validate end-to-end from Odoo bridge through adapter to Agent Application
- Monitor traces for unexpected behavior

## Versioning

- Each publish creates a new version
- Previous versions remain available for rollback
- Document version changes in the agent changelog
