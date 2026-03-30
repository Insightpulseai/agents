# Skill: Caption Writing

**Skill ID**: social.caption_writing
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Writes platform-native captions, post copy, and thread content. Adapts tone, length, format, and CTA style to each platform's conventions and audience expectations.

## When to Use

- Drafting individual posts for any social platform
- Writing threads or carousel copy
- Repurposing long-form content into social snippets
- Generating caption variations for A/B testing

## Core Pattern

```
Input: Topic + key messages + platform + brand voice + campaign objective
Process:
  1. Select tone modifier based on platform and content type
  2. Draft copy within platform character limits
  3. Craft CTA aligned to campaign objective and funnel stage
  4. Generate hashtag set with relevance scoring
  5. Run brand_voice_enforcement check
  6. Run platform_fit check
Output: Platform-ready caption with hashtags, CTA, and quality scores
```

## Platform Specifications

| Platform | Max Chars | Hashtag Limit | CTA Style |
|----------|-----------|---------------|-----------|
| LinkedIn | 3,000 | 3-5 | Professional, link-embedded |
| X/Twitter | 280 | 1-2 | Direct, thread-continued |
| Instagram | 2,200 | 10-15 (of 30 max) | Link-in-bio reference |
| Facebook | 63,206 | 2-3 | Inline link, comment CTA |
| TikTok | 4,000 | 3-5 | Overlay text, comment pin |

## Copy Structure Templates

### Hook → Value → CTA (Universal)
```
[Hook: question, bold statement, or stat]

[Value: insight, story, or framework]

[CTA: specific action request]

[Hashtags]
```

### Thread Format (X/Twitter, LinkedIn)
```
1/ [Hook — the reason to keep reading]
2/ [Context — set the scene]
3-N/ [Value points — one per post]
N+1/ [Summary + CTA]
```

### Visual-First (Instagram, TikTok)
```
[Caption supports the visual — don't repeat what's obvious in the image/video]
[Add context the visual can't convey]
[CTA]
[Hashtags below fold]
```

## Quality Checks

- Character count within platform limit
- CTA present and aligned to objective
- Brand voice alignment ≥ 0.85
- No do-not-say list violations
- Hashtags relevant and not banned
- No broken or placeholder links
