# Judge: Platform Fit

**Judge ID**: judge.social.platform_fit
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0
**Gate Type**: Hard (must pass before publish handoff)

## Purpose

Evaluates whether content conforms to platform-specific constraints and conventions. Checks character limits, media requirements, hashtag usage, CTA format, and content structure.

## Evaluation Dimensions

| Dimension | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Character compliance | 0.30 | 1.00 | Copy within platform char limit |
| Format compliance | 0.25 | ≥ 0.85 | Content uses platform-appropriate format |
| Hashtag compliance | 0.15 | ≥ 0.80 | Count and relevance within platform norms |
| Media compliance | 0.15 | ≥ 0.90 | Required media present with correct specs |
| CTA compliance | 0.15 | ≥ 0.75 | CTA uses platform-native action pattern |

## Platform Rules

```yaml
platforms:
  linkedin:
    max_chars: 3000
    max_hashtags: 5
    media_required: false
    link_in_post: true
    thread_support: false
  x:
    max_chars: 280
    max_hashtags: 2
    media_required: false
    link_in_post: true
    thread_support: true
  instagram:
    max_chars: 2200
    max_hashtags: 30
    optimal_hashtags: 10-15
    media_required: true
    link_in_post: false
    link_in_bio: true
  facebook:
    max_chars: 63206
    max_hashtags: 3
    media_required: false
    link_in_post: true
  tiktok:
    max_chars: 4000
    max_hashtags: 5
    media_required: true
    link_in_bio: true
```

## Scoring Rules

```yaml
scoring:
  composite_threshold: 0.85
  hard_fail_triggers:
    - character_limit_exceeded
    - required_media_missing
  soft_flag_triggers:
    - hashtag_count_suboptimal
    - cta_format_non_native
    - posting_time_suboptimal
```

## Output

```yaml
output:
  pass: boolean
  composite_score: float
  platform: string
  dimension_scores:
    character_compliance: float
    format_compliance: float
    hashtag_compliance: float
    media_compliance: float
    cta_compliance: float
  violations: violation[]
  fix_suggestions: string[]
```

## Examples

### Fail — Character Limit
```yaml
platform: x
content_length: 312
max_allowed: 280
result: HARD FAIL — exceeds character limit by 32 chars
fix: "Condense copy or split into thread"
```

### Fail — Missing Media
```yaml
platform: instagram
media_refs: []
result: HARD FAIL — Instagram requires media attachment
fix: "Attach image or video, or request creative brief via ugc-mediaops-kit"
```
