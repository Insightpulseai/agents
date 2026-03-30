# Skill: Campaign Planning

**Skill ID**: social.campaign_planning
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Structures multi-platform campaign timelines with coordinated messaging, content milestones, KPI targets, and creative briefs. Ensures cross-channel consistency while respecting platform-native formats.

## When to Use

- Launching a new marketing campaign
- Coordinating a product launch across platforms
- Planning seasonal or event-driven content pushes
- Building an always-on content program

## Core Pattern

```
Input: Campaign brief + objectives + platforms + timeline + budget context
Process:
  1. Define campaign phases (tease → launch → sustain → close)
  2. Map content types to phases and platforms
  3. Set per-phase KPI targets
  4. Generate content briefs for each deliverable
  5. Build timeline with dependencies
  6. Identify creative asset needs → handoff to ugc-mediaops-kit
Output: Campaign plan with timeline, content briefs, KPIs, and creative requests
```

## Campaign Phase Framework

| Phase | Duration | Purpose | Content Types |
|-------|----------|---------|---------------|
| Tease | 1-2 weeks | Build anticipation | Sneak peeks, countdowns, polls |
| Launch | 1-3 days | Maximum impact | Announcements, live content, PR |
| Sustain | 2-6 weeks | Deepen engagement | Testimonials, tutorials, UGC |
| Close | 1 week | Drive final action | Last-chance CTAs, recaps |

## KPI Framework

| Objective | Primary KPI | Secondary KPIs |
|-----------|------------|----------------|
| Awareness | Reach / Impressions | Follower growth, share rate |
| Engagement | Engagement rate | Comments, saves, shares |
| Traffic | Click-through rate | Landing page visits, bounce rate |
| Conversion | Conversion rate | Sign-ups, purchases, leads |
| Retention | Return engagement | Repeat interactions, community growth |

## Outputs

- Campaign timeline (phases × platforms × dates)
- Content brief per deliverable
- KPI targets per phase
- Creative asset request list (for ugc-mediaops-kit handoff)
- Cross-channel messaging matrix
- Approval checkpoints
