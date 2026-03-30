# Judge: Compliance

**Judge ID**: judge.social.compliance
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0
**Gate Type**: Hard (must pass — zero tolerance)

## Purpose

Ensures content complies with legal, regulatory, and organizational policies. Checks for disclosure requirements, restricted claims, regulated topics, and platform-specific advertising rules.

## Evaluation Dimensions

| Dimension | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Legal compliance | 0.30 | 1.00 | No unsubstantiated claims, proper disclaimers |
| Regulatory compliance | 0.25 | 1.00 | Industry-specific rules (finance, health, etc.) |
| Platform policy | 0.20 | 1.00 | Adheres to platform ToS and ad policies |
| AI disclosure | 0.15 | 1.00 | AI-generated content disclosed where required |
| Data privacy | 0.10 | 1.00 | No PII, no unauthorized data references |

## Compliance Rules

```yaml
rules:
  claims:
    - type: performance_claim
      rule: "Must be verifiable with cited source"
      severity: hard_fail
    - type: comparison_claim
      rule: "Must not disparage competitors without factual basis"
      severity: hard_fail
    - type: guarantee_claim
      rule: "Must include appropriate disclaimers"
      severity: hard_fail

  disclosures:
    - type: ai_generated
      rule: "Disclose when required by platform policy"
      platforms: [instagram, tiktok, facebook]
      severity: hard_fail
    - type: sponsored_content
      rule: "Must include #ad or #sponsored if paid"
      severity: hard_fail
    - type: affiliate_link
      rule: "Must disclose affiliate relationship"
      severity: hard_fail

  restricted_topics:
    - topic: medical_advice
      rule: "Cannot provide specific medical recommendations"
      severity: hard_fail
    - topic: financial_advice
      rule: "Cannot provide specific investment recommendations"
      severity: hard_fail
    - topic: political_content
      rule: "Requires explicit organizational approval"
      severity: escalate

  privacy:
    - rule: "No personally identifiable information without consent"
      severity: hard_fail
    - rule: "No customer data in public posts"
      severity: hard_fail
```

## Output

```yaml
output:
  pass: boolean
  composite_score: float
  dimension_scores:
    legal_compliance: float
    regulatory_compliance: float
    platform_policy: float
    ai_disclosure: float
    data_privacy: float
  violations: violation[]
  required_actions: string[]
  escalation_required: boolean
  escalation_reason: string | null
```

## Examples

### Fail — Unsubstantiated Claim
```yaml
content: "Our product cures anxiety in 7 days."
violation: "Medical claim without substantiation"
result: HARD FAIL
required_action: "Remove medical claim or provide clinical citation"
```

### Fail — Missing Disclosure
```yaml
content: "Love this product! Check it out at [link]"
context: sponsored_partnership
violation: "Sponsored content missing #ad or #sponsored disclosure"
result: HARD FAIL
required_action: "Add FTC-compliant sponsorship disclosure"
```

### Pass with Escalation
```yaml
content: "Here's our take on the proposed legislation..."
topic: political_content
result: PASS (content is factual) — ESCALATION REQUIRED
escalation_reason: "Political content requires organizational approval"
```
