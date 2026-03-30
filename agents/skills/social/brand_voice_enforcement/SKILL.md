# Skill: Brand Voice Enforcement

**Skill ID**: social.brand_voice_enforcement
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Validates and enforces brand voice consistency across all content. Checks tone, terminology, messaging alignment, and restricted topic avoidance. Acts as a pre-publish gate ensuring every piece of content represents the brand accurately.

## When to Use

- Reviewing any content before approval
- Auditing existing content for brand drift
- Onboarding new content themes or campaign messaging
- After any content generation or adaptation step

## Core Pattern

```
Input: Content item + brand voice guidelines + do-not-say list + terminology glossary
Process:
  1. Score tone alignment against brand voice attributes
  2. Check for do-not-say list violations (exact + semantic match)
  3. Validate terminology usage against approved glossary
  4. Assess messaging alignment with brand pillars
  5. Flag any claims that require legal/compliance review
Output: Brand alignment score + violation list + recommendations
```

## Brand Voice Dimensions

| Dimension | What It Measures | Scoring |
|-----------|-----------------|---------|
| Tone match | Voice attributes (professional, warm, etc.) | 0.0 - 1.0 |
| Terminology | Use of approved terms vs. alternatives | Pass / Fail per term |
| Do-not-say | Absence of restricted words/phrases | Hard fail on any match |
| Messaging alignment | Content supports brand pillars | 0.0 - 1.0 |
| Claim accuracy | Factual statements are verifiable | Flag for review |

## Do-Not-Say Enforcement

```
Enforcement levels:
  hard_block:    Content cannot proceed. Exact match on restricted terms.
  soft_flag:     Content flagged for human review. Semantic proximity to restricted topics.
  suggest_swap:  Alternative terminology suggested. Non-blocking.
```

## Outputs

- Brand alignment score (composite 0.0 - 1.0)
- Per-dimension scores
- Violation list with severity and location
- Suggested rewrites for flagged sections
- Pass / Fail gate recommendation
