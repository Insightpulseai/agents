# Skill: Platform Adaptation

**Skill ID**: social.platform_adaptation
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Transforms a single content concept into platform-native variants. Adapts copy length, tone, format, media requirements, hashtag strategy, and CTA style to match each platform's conventions and audience expectations.

## When to Use

- Repurposing a single message across multiple platforms
- Adapting long-form content (blog, whitepaper) into social formats
- Ensuring cross-posted content doesn't feel cross-posted
- Localizing content format for platform-specific features (Reels, Threads, Carousels)

## Core Pattern

```
Input: Source content (or content atoms) + target platforms + brand voice + campaign context
Process:
  1. If source is pillar content → atomize first (extract key points, quotes, stats, stories)
  2. Select relevant atoms for each target platform (not all atoms suit all platforms)
  3. For each target platform:
     a. Recombine selected atoms into platform-native structure
     b. Apply platform character limits and format rules
     c. Shift tone to match platform culture
     d. Select appropriate content format (post, thread, carousel, reel script)
     e. Adjust CTA to platform capabilities
     f. Generate platform-specific hashtag set
  4. Run platform_fit_judge on each variant
Output: Platform-specific content variants with fit scores and source atom references
```

### Content Atomization (prerequisite)

Never transform directly between platforms. Always go through atomic units:

```
[Pillar Content]
    ↓
[Content Atoms: key_points[], quotes[], statistics[], stories[], frameworks[]]
    ↓
[Platform Recombination]
    ├── LinkedIn: key_point + statistic + framework → long-form professional post
    ├── X/Twitter: statistic + bold claim → punchy thread
    ├── Instagram: story + quote → visual caption
    ├── Facebook: key_point + story → community discussion
    └── TikTok: story + statistic → hook + script outline
```

Each derived post maintains `source_atoms[]` references for performance attribution back to the pillar content.

## Adaptation Matrix

| Dimension | LinkedIn | X/Twitter | Instagram | Facebook | TikTok |
|-----------|----------|-----------|-----------|----------|--------|
| Tone | Professional, insightful | Sharp, concise | Visual, aspirational | Conversational, inclusive | Authentic, unfiltered |
| Length | Long (500-1500 chars) | Short (< 280 chars) | Medium (150-500 chars) | Medium (200-800 chars) | Short (50-200 chars) |
| Format | Article posts, documents | Threads, single posts | Carousels, Reels, Stories | Posts, events, groups | Short-form video, duets |
| Hashtags | 3-5 niche/professional | 1-2 trending | 10-15 mixed | 2-3 broad | 3-5 trending |
| CTA | Link in post, DM | Reply, retweet, link | Link in bio, DM | Link in post, comment | Comment, follow, link in bio |
| Media | Optional, documents preferred | Optional, images boost | Required (image/video) | Optional, video preferred | Required (video) |

## Anti-Patterns

- Cross-posting identical copy across platforms
- Using LinkedIn tone on TikTok
- Ignoring platform-specific features (polls, carousels, duets)
- Hashtag stuffing on platforms where it hurts reach (X/Twitter)
- Including links in Instagram captions (not clickable)
