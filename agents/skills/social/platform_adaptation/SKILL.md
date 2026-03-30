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
Input: Source content + target platforms + brand voice + campaign context
Process:
  1. Analyze source content for key messages and hooks
  2. For each target platform:
     a. Apply platform character limits and format rules
     b. Shift tone to match platform culture
     c. Select appropriate content format (post, thread, carousel, reel script)
     d. Adjust CTA to platform capabilities
     e. Generate platform-specific hashtag set
  3. Run platform_fit_judge on each variant
Output: Platform-specific content variants with fit scores
```

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
