# Skill: Content Calendar

**Skill ID**: social.content_calendar
**Agent**: SocialMediaManager (agent_008)
**Version**: 1.0.0

## What It Is

Generates and manages structured content calendars that map content items to dates, platforms, campaigns, and content pillars. Ensures consistent posting cadence and balanced content mix.

## When to Use

- Building weekly or monthly content schedules
- Balancing content mix across pillars and platforms
- Identifying gaps or over-concentration in the schedule
- Coordinating campaign content with always-on content

## Core Pattern

```
Input: Content strategy + campaign plans + posting cadence targets
Process:
  1. Map available content items to calendar slots
  2. Enforce content mix ratios per platform
  3. Check for posting frequency compliance
  4. Identify gaps and suggest filler content
  5. Flag conflicts (competing campaigns, event overlaps)
Output: Structured calendar with entries, status, and gap analysis
```

## Calendar Entry Schema

```yaml
entry:
  id: string
  date: ISO 8601
  time: HH:MM (platform local timezone)
  platform: linkedin | x | instagram | facebook | tiktok
  content_pillar: educational | inspirational | promotional | community | cultural
  campaign_id: string | null
  content_id: string
  status: planned | drafted | reviewed | approved | published
  copy_preview: string (first 100 chars)
  media_status: not_needed | pending | ready
  approval_status: pending | approved | rejected
```

## Cadence Guidelines

| Platform | Min Posts/Week | Max Posts/Week | Best Times (UTC) |
|----------|---------------|----------------|-------------------|
| LinkedIn | 3 | 5 | Tue-Thu 13:00-15:00 |
| X/Twitter | 5 | 14 | Mon-Fri 12:00-15:00 |
| Instagram | 3 | 7 | Mon-Fri 11:00-14:00 |
| Facebook | 3 | 5 | Tue-Thu 09:00-12:00 |
| TikTok | 3 | 7 | Mon-Sat 19:00-21:00 |

## Outputs

- Calendar view (week/month) with all entries
- Content mix ratio report vs. targets
- Gap analysis (empty slots, pillar imbalances)
- Upcoming approval queue
- Campaign vs. always-on balance report
