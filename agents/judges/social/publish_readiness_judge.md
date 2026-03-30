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

## Confidence-Based Routing

The publish readiness judge computes a composite confidence score from all upstream judges and routes content accordingly. This is the mechanism that enables the **single-operator model** — high-confidence content flows through without human intervention.

```yaml
routing:
  auto_approve:
    threshold: 0.85
    conditions:
      - all hard-gate judges passed
      - no compliance escalations
      - no campaign requiring manual sign-off
    action: "Emit to publish handoff immediately"

  human_review:
    threshold: 0.65-0.84
    conditions:
      - hard-gate judges passed but with soft flags
      - content_quality_judge score below optimal
      - first post for new campaign or brand
    action: "Queue for operator review with judge context"

  reject:
    threshold: "<0.65"
    conditions:
      - any hard-gate judge failed
      - compliance escalation required
      - multiple soft flags accumulated
    action: "Reject with specific feedback, trigger regeneration"
```

### Routing Signal Computation

```
composite_confidence =
  brand_consistency_score × 0.25 +
  compliance_score × 0.25 +
  platform_fit_score × 0.25 +
  content_quality_score × 0.15 +
  checklist_completeness × 0.10

If compliance_score < 1.0 → FORCE REJECT (override composite)
If brand_consistency_score < 0.70 → FORCE REJECT (override composite)
```

## Output

```yaml
output:
  publish_ready: boolean
  routing_decision: auto_approve | human_review | reject
  composite_confidence: float
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

### Auto-Approve (score: 0.92)
```yaml
judge_gates: all passed
content: complete
media: 1 image, specs valid
schedule: 2026-04-01T14:00:00Z, no conflicts
composite_confidence: 0.92
routing: auto_approve
result: PUBLISH READY — auto-approved, no human review needed
```

### Human Review (score: 0.78)
```yaml
judge_gates: hard gates passed
content_quality_judge: 0.68 (below optimal, weak hook)
composite_confidence: 0.78
routing: human_review
result: QUEUED FOR REVIEW — "Content quality below threshold. Hook effectiveness: 0.45. Suggest strengthening opening line."
```

### Reject (score: 0.41)
```yaml
judge_gates: compliance_judge=FAIL
violation: "Unsubstantiated performance claim"
composite_confidence: 0.41
routing: reject
result: REJECTED — "Compliance violation: remove unsubstantiated claim or add source citation. Regenerate with feedback."
```

### Blocked — Missing Media
```yaml
judge_gates: all passed
content: complete
media: 0 refs, platform=instagram (media required)
result: BLOCKED — "Instagram post requires media attachment. Request creative brief or attach asset."
```
