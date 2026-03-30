# Skill: Performance Review

**Skill ID**: social.performance_review
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Analyzes engagement metrics and campaign performance data to generate actionable insights and strategy recommendations. Produces post-campaign retrospectives and ongoing performance reports.

## When to Use

- End-of-campaign retrospective
- Weekly/monthly performance reporting
- Identifying top and bottom performing content
- Adjusting content strategy based on data

## Core Pattern

```
Input: Performance metrics + campaign KPIs + content metadata (PostPerformanceRecord[])
Process:
  1. Aggregate metrics by platform, content pillar, and campaign
  2. Compare actuals vs. KPI targets
  3. Identify top-performing content (by engagement rate, reach, conversion)
  4. Identify underperforming areas
  5. Extract winning patterns from top performers
  6. Update few-shot example pool for next generation cycle
  7. Generate recommendations for strategy adjustments
Output: Performance summary + insights + recommendations + updated few-shot pool
```

## Feedback Loop Architecture

The performance review skill closes the loop between publishing and generation:

```
[Publish] → [Collect Metrics (24h, 48h, 7d)] → [PostPerformanceRecord DB]
                                                        ↓
[Pattern Extraction]
  - Which hook_types get highest engagement per platform?
  - Which content_pillars drive shares vs. clicks?
  - Which cta_types convert best per funnel_stage?
  - What posting times yield peak engagement?
  - Which source content atoms produced the best derived posts?
                                                        ↓
[Update Generation Context]
  - Refresh top-5 few-shot examples per platform/pillar
  - Adjust content mix ratios based on pillar performance
  - Update cadence recommendations based on time-of-day data
  - Flag underperforming atoms for retirement
                                                        ↓
[Next Generation Cycle uses updated context]
```

### Pattern Query Examples

The structured `PostPerformanceRecord` schema enables queries like:
- "Question hooks on LinkedIn get 2.3x engagement on Tuesday mornings"
- "Statistics-led posts outperform story-led posts for awareness campaigns"
- "Posts with media get 1.8x engagement on X/Twitter but only 1.1x on LinkedIn"
- "CTA 'Download the report' converts 3x better than 'Learn more' for consideration-stage content"

## Metrics Framework

| Metric Category | Metrics | Source |
|----------------|---------|--------|
| Reach | Impressions, reach, follower growth | Platform analytics |
| Engagement | Likes, comments, shares, saves, engagement rate | Platform analytics |
| Traffic | Clicks, CTR, landing page visits | UTM tracking |
| Conversion | Sign-ups, purchases, leads, conversion rate | Analytics + CRM |
| Content health | Post frequency, content mix adherence, approval rate | Internal tracking |

## Report Sections

1. **Executive Summary** — KPI status (on track / at risk / missed)
2. **Platform Breakdown** — Per-platform performance vs. targets
3. **Content Pillar Analysis** — Which pillars drive engagement
4. **Top/Bottom Performers** — Specific posts with analysis
5. **Audience Insights** — Growth, demographics, peak times
6. **Recommendations** — Data-backed strategy adjustments
7. **Next Period Plan** — Proposed changes to content mix or cadence

## Outputs

- Performance summary report (structured)
- KPI achievement scorecard
- Top/bottom content rankings with context
- Strategy adjustment recommendations
- Content mix rebalancing suggestions
