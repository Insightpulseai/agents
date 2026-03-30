# Judge: Brand Consistency

**Judge ID**: judge.social.brand_consistency
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0
**Gate Type**: Hard (must pass before publish handoff)

## Purpose

Evaluates whether content consistently reflects the brand's voice, tone, terminology, and messaging pillars. Blocks content that drifts from brand identity.

## Evaluation Dimensions

| Dimension | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Tone alignment | 0.30 | ≥ 0.80 | Voice attributes match brand guidelines |
| Terminology compliance | 0.25 | ≥ 0.90 | Approved terms used, no banned terms |
| Messaging alignment | 0.25 | ≥ 0.75 | Content supports defined brand pillars |
| Visual-verbal coherence | 0.10 | ≥ 0.70 | Copy aligns with visual identity cues |
| Do-not-say compliance | 0.10 | 1.00 | Zero tolerance for restricted terms |

## Scoring Rules

```yaml
scoring:
  composite_threshold: 0.80
  hard_fail_triggers:
    - do_not_say_violation
    - competitor_mention_unapproved
    - off_brand_claim
  soft_flag_triggers:
    - tone_drift_minor (score 0.70-0.80)
    - terminology_alternative_used
    - messaging_tangential
```

## Input

```yaml
input:
  content_item:
    copy: string
    platform: string
    hashtags: string[]
    cta: string
  brand_context:
    voice_guidelines: document
    do_not_say_list: string[]
    terminology_glossary: map<string, string>
    brand_pillars: string[]
```

## Output

```yaml
output:
  pass: boolean
  composite_score: float
  dimension_scores:
    tone_alignment: float
    terminology_compliance: float
    messaging_alignment: float
    visual_verbal_coherence: float
    do_not_say_compliance: float
  violations: violation[]
  recommendations: string[]
```

## Examples

### Pass
```yaml
content: "Streamline your workflow with intelligent automation. See how teams save 10+ hours weekly."
scores: { tone: 0.92, terminology: 1.0, messaging: 0.88, visual_verbal: 0.85, do_not_say: 1.0 }
composite: 0.93
result: PASS
```

### Fail — Do-Not-Say Violation
```yaml
content: "We're the cheapest solution on the market."
violations: ["'cheapest' is on do-not-say list — use 'most cost-effective' or 'best value'"]
composite: 0.0
result: HARD FAIL
```

### Fail — Tone Drift
```yaml
content: "yo check this out fam 🔥🔥 our product is INSANE"
scores: { tone: 0.25, terminology: 0.60, messaging: 0.40 }
composite: 0.38
result: FAIL — tone misalignment, informal language exceeds brand parameters
```
