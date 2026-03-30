# Judge: Content Quality

**Judge ID**: judge.social.content_quality
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0
**Gate Type**: Soft (advisory — flags but does not block)

## Purpose

Evaluates the overall quality of social media content including writing clarity, CTA effectiveness, engagement potential, and originality. Provides quality scores and improvement suggestions.

## Evaluation Dimensions

| Dimension | Weight | Threshold | Description |
|-----------|--------|-----------|-------------|
| Clarity | 0.25 | ≥ 0.75 | Message is clear, unambiguous, easy to understand |
| CTA strength | 0.25 | ≥ 0.70 | Call-to-action is specific, compelling, and actionable |
| Hook effectiveness | 0.20 | ≥ 0.70 | Opening grabs attention within 2 seconds |
| Value density | 0.15 | ≥ 0.65 | Content delivers value relative to its length |
| Originality | 0.15 | ≥ 0.60 | Content is fresh, not generic or template-feeling |

## Scoring Rubric

### CTA Strength
```yaml
cta_scoring:
  1.0: "Specific action + clear benefit + urgency"
  0.8: "Specific action + clear benefit"
  0.6: "Generic action (e.g., 'learn more')"
  0.4: "Vague direction without specific action"
  0.2: "CTA present but buried or unclear"
  0.0: "No CTA"
```

### Hook Effectiveness
```yaml
hook_scoring:
  1.0: "Provocative question or surprising stat that creates curiosity gap"
  0.8: "Strong statement that challenges assumptions"
  0.6: "Clear value proposition stated upfront"
  0.4: "Mildly interesting opening, not compelling"
  0.2: "Generic opening (e.g., 'Excited to share...')"
  0.0: "No discernible hook"
```

### Clarity
```yaml
clarity_scoring:
  1.0: "Single clear message, zero ambiguity, readable at a glance"
  0.8: "Clear primary message, minor secondary complexity"
  0.6: "Message understandable but requires re-reading"
  0.4: "Multiple competing messages, some confusion"
  0.2: "Unclear what the post is about"
  0.0: "Incoherent"
```

## Output

```yaml
output:
  pass: boolean
  composite_score: float
  dimension_scores:
    clarity: float
    cta_strength: float
    hook_effectiveness: float
    value_density: float
    originality: float
  improvement_suggestions: string[]
  rewrite_recommended: boolean
```

## Examples

### High Quality
```yaml
content: "We analyzed 10,000 social posts. The #1 predictor of engagement? Not hashtags. Not timing. It's the first 7 words. Here's the framework we use to nail every hook →"
scores: { clarity: 0.95, cta: 0.85, hook: 0.95, value: 0.90, originality: 0.85 }
composite: 0.91
result: PASS
```

### Low Quality — Weak CTA
```yaml
content: "We're excited to announce our new feature! It's going to change everything. Stay tuned for more updates!"
scores: { clarity: 0.60, cta: 0.20, hook: 0.30, value: 0.25, originality: 0.20 }
composite: 0.31
suggestions: ["Replace vague CTA with specific action", "Add concrete value — what does the feature do?", "Remove 'excited to announce' cliché hook"]
result: FAIL — rewrite recommended
```

## Few-Shot Calibration

To maintain scoring accuracy, the content quality judge uses **calibrated few-shot examples**:

```yaml
calibration:
  method: few_shot
  examples_per_score_band: 2
  score_bands: [0.0-0.3, 0.3-0.6, 0.6-0.8, 0.8-1.0]

  calibration_set:
    - score: 0.95
      platform: linkedin
      copy: "We analyzed 10,000 social posts. The #1 predictor of engagement? Not hashtags. Not timing. It's the first 7 words. Here's the framework we use →"
      rationale: "Strong stat hook, curiosity gap, specific CTA, high value density"

    - score: 0.72
      platform: linkedin
      copy: "AI is transforming marketing. Here are 5 ways to stay ahead of the curve in 2026."
      rationale: "Decent structure but generic hook, overused format, vague promise"

    - score: 0.35
      platform: linkedin
      copy: "Excited to announce we've been named a leader! Thank you to our amazing team and customers."
      rationale: "Cliché hook, self-congratulatory, no value for reader, no CTA"

    - score: 0.10
      platform: linkedin
      copy: "Check out our website."
      rationale: "No hook, no value, no context, minimal effort"

  human_calibration_loop:
    frequency: "Monthly"
    process: "Sample 20 scored posts, have human rate same posts, compare. Adjust rubric weights if drift > 0.15"
```

## Ensemble Scoring

For high-stakes content (campaign launches, sensitive topics), use ensemble judging:

```yaml
ensemble:
  enabled_when: "campaign.objective == 'conversion' OR content.escalation_flag == true"
  judge_calls: 3
  aggregation: "median"
  variance_threshold: 0.15
  action_on_high_variance: "flag for human review"
```
