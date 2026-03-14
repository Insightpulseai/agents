# Publish Policy

## Pre-publish checklist

- [ ] Instructions finalized
- [ ] Model confirmed
- [ ] Tools explicitly enabled
- [ ] Knowledge files current
- [ ] Traces run against informational, navigational, compliance, and dry-run transactional requests
- [ ] Evaluations pass acceptance thresholds

## Publish targets

| Target | When |
|--------|------|
| STAGING Agent Application | After traces + evals pass |
| PROD Agent Application | After STAGING integration test passes |

## Post-publish validation

- Backend adapter can invoke the published endpoint
- PROD-ADVISORY blocks write actions
- PROD-ACTION requires confirmation for write actions
- Audit records are written for every request

## Rollback

Republish the previous known-good version.
