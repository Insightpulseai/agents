# Judge: Publish Readiness

**Judge ID**: judge.social.publish_readiness
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0
**Gate Type**: Hard (final gate before handoff)

## Purpose

Final pre-publish gate that validates all upstream judge results, content completeness, and scheduling readiness. Ensures nothing is handed off to automations in an incomplete or unapproved state.

## Evaluation Dimensions

| Dimension | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Upstream judges passed | 0.30 | 1.00 | All hard-gate judges must have passed |
| Content completeness | 0.25 | 1.00 | All required fields populated |
| Media readiness | 0.20 | 1.00 | Referenced assets exist and meet specs |
| Schedule validity | 0.15 | 1.00 | Scheduled time is valid and conflict-free |
| Approval chain | 0.10 | 1.00 | Required approvals obtained |

## Pre-Publish Checklist

```yaml
checklist:
  judge_gates:
    - brand_consistency_judge: required
    - compliance_judge: required
    - platform_fit_judge: required
    - content_quality_judge: advisory

  content_fields:
    - copy: required
    - platform: required
    - hashtags: required (may be empty array)
    - cta: required
    - scheduled_time: required
    - timezone: required
    - campaign_id: optional

  media:
    - refs_valid: "All media_refs resolve to existing assets"
    - specs_match: "Media dimensions/format match platform requirements"
    - fallback: "If media pending, content cannot proceed"

  schedule:
    - future_time: "Scheduled time must be in the future"
    - no_conflict: "No duplicate post on same platform within 1 hour"
    - within_cadence: "Does not exceed max posts/day for platform"

  approval:
    - operator_approval: "Required if campaign requires manual sign-off"
    - auto_approved: "Allowed if all judge gates pass and no escalation flags"
```

## Output

```yaml
output:
  publish_ready: boolean
  blocking_issues: issue[]
  advisory_notes: string[]
  handoff_approved: boolean
  checklist_status:
    judge_gates: pass | fail
    content_completeness: pass | fail
    media_readiness: pass | fail
    schedule_validity: pass | fail
    approval_chain: pass | fail
```

## Examples

### Ready
```yaml
judge_gates: all passed
content: complete
media: 1 image, specs valid
schedule: 2026-04-01T14:00:00Z, no conflicts
approval: auto-approved (no escalation flags)
result: PUBLISH READY
```

### Blocked — Missing Media
```yaml
judge_gates: all passed
content: complete
media: 0 refs, platform=instagram (media required)
result: BLOCKED — "Instagram post requires media attachment. Request creative brief or attach asset."
```

### Blocked — Upstream Judge Failed
```yaml
judge_gates: compliance_judge=FAIL
result: BLOCKED — "Compliance judge failed. Resolve violations before publish handoff."
```
