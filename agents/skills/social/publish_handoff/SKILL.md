# Skill: Publish Handoff

**Skill ID**: social.publish_handoff
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Packages approved content into structured payloads for downstream automation systems. Ensures all required fields are present, all judge gates have passed, and content is ready for scheduling and publishing.

## When to Use

- Content has passed all judge gates (brand, compliance, quality, platform fit)
- Content is approved by operator (if manual approval required)
- Ready to emit to automations surface for scheduling/posting

## Core Pattern

```
Input: Approved content items + judge results + campaign context + schedule
Process:
  1. Validate all required judge gates passed
  2. Verify content completeness (copy, media refs, platform, time)
  3. Package into PublishHandoff payload schema
  4. Emit to automations via publish_handoff_emit tool
  5. Record handoff status and tracking ID
Output: Structured publish payload + handoff confirmation
```

## Handoff Payload Schema

```yaml
publish_handoff:
  handoff_id: string         # unique tracking ID
  timestamp: ISO 8601
  content_id: string
  campaign_id: string | null
  platform: string
  copy: string
  hashtags: string[]
  cta: string
  media_refs: string[]       # URIs to ready creative assets
  scheduled_time: ISO 8601
  timezone: string
  approval_chain:
    brand_judge: pass | fail
    compliance_judge: pass | fail
    quality_judge: pass | fail
    platform_fit_judge: pass | fail
    operator_approval: approved | not_required
  status: ready | blocked
  blocked_reason: string | null
```

## Pre-Handoff Checklist

- [ ] All judge gates passed
- [ ] Copy within platform character limit
- [ ] Media assets referenced and available
- [ ] Scheduled time is in the future
- [ ] No conflicting posts on same platform/time
- [ ] Campaign association correct (if applicable)
- [ ] Hashtags validated (not banned, relevant)

## Outputs

- PublishHandoff payload (structured)
- Handoff confirmation with tracking ID
- Blocked items list with reasons (if any)
