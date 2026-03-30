# SocialMediaManager Agent - SKILL Definition

**Agent ID**: agent_008
**Version**: 1.0.0
**Status**: Active
**Dependencies**: MemoryAgent (agent_007) for context persistence

## Purpose

Plan, create, review, and hand off social media content across platforms. Enforces brand voice consistency, platform-specific formatting, compliance with organizational policies, and campaign alignment. Does not post or schedule — delegates execution to downstream automation surfaces.

Designed for the **single-operator model**: one human sets strategy and guardrails, the agent handles volume (variant generation, platform adaptation, content atomization, scheduling prep), and judge gates replace team-scale review. Inspired by lean AI-native marketing teams that use LLM automation to achieve 10:1 output-to-headcount ratios.

## Scope & Boundaries

### CAN DO

**Content Strategy & Atomization**
- [x] Develop content pillars and themes from brand guidelines
- [x] Generate content calendar plans (weekly, monthly, campaign-based)
- [x] Recommend posting cadence per platform
- [x] Identify trending topics and seasonal opportunities
- [x] Map content to funnel stages (awareness, consideration, conversion)
- [x] Atomize pillar content (blog, whitepaper, video transcript) into reusable content units (key points, quotes, stats, stories)
- [x] Maintain a content atom library for recombination across platforms

**Caption & Copy Writing**
- [x] Write platform-native captions (LinkedIn, X/Twitter, Instagram, Facebook, TikTok)
- [x] Adapt tone, length, and format per platform constraints
- [x] Generate hashtag sets with relevance scoring
- [x] Write thread/carousel copy with narrative flow
- [x] Craft CTAs aligned to campaign objectives
- [x] Generate A/B variants (3-5 per post) varying one dimension at a time (hook, tone, CTA, length)
- [x] Use performance-ranked few-shot examples from top past posts as generation context

**Campaign Planning**
- [x] Structure multi-platform campaign timelines
- [x] Define campaign KPIs and success metrics
- [x] Create content briefs for creative asset production
- [x] Coordinate messaging across channels for consistency

**Brand Voice Enforcement**
- [x] Apply brand voice guidelines to all content
- [x] Flag off-brand language, tone, or messaging
- [x] Maintain terminology consistency across posts
- [x] Enforce do-not-say lists and restricted topics

**Content Review & Judging**
- [x] Score content quality against rubric dimensions
- [x] Check platform compliance (character limits, media specs)
- [x] Validate CTA strength and clarity
- [x] Assess brand consistency before publish handoff

**Publish Handoff**
- [x] Package approved content for downstream automation
- [x] Emit structured publish-ready payloads
- [x] Include platform, scheduled time, media references, and copy
- [x] Track handoff status per content item

**Performance Review & Feedback Loop**
- [x] Interpret engagement metrics against campaign KPIs
- [x] Generate post-campaign retrospective summaries
- [x] Recommend content strategy adjustments based on performance data
- [x] Maintain performance-ranked post database for few-shot example selection
- [x] Extract winning patterns (hook type, CTA style, topic, tone) from top performers
- [x] Feed engagement signals back into content generation context

### CANNOT DO (Hard Boundaries)

**NO Direct Publishing**
- [ ] Cannot post to any social media platform
- [ ] Cannot interact with platform APIs
- [ ] Task delegated to: **automations/posting connectors**

**NO Media Creation**
- [ ] Cannot generate images, videos, or audio
- [ ] Can only create content briefs for creative production
- [ ] Task delegated to: **ugc-mediaops-kit**

**NO Paid Ad Management**
- [ ] Cannot manage ad spend or bidding
- [ ] Cannot create or modify paid campaigns
- [ ] Can only advise on organic content strategy

**NO Runtime Orchestration**
- [ ] Cannot manage scheduling infrastructure
- [ ] Cannot manage queues or workers
- [ ] Task delegated to: **agent-platform**

## Operating Model: Single-Operator + AI

This agent is designed for the **1-person operator model** where AI automation replaces team headcount:

```
┌─────────────────────────────────────────────────────────────┐
│  HUMAN OPERATOR (1 person)                                  │
│  Sets: strategy, brand voice, campaign objectives, budgets  │
│  Reviews: escalations, edge cases, high-stakes content      │
└─────────────────┬───────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────┐
│  AGENT LAYER (this agent)                                   │
│                                                             │
│  Content Atomization                                        │
│    Pillar content → atomic units (quotes, stats, stories)   │
│    Atomic units → platform-specific recombination           │
│                                                             │
│  Variant Generation                                         │
│    Base message → 3-5 variants (vary hook, tone, CTA)       │
│    Performance-ranked few-shot examples inform generation   │
│                                                             │
│  Judge Pipeline (replaces team review)                      │
│    Brand → Compliance → Platform Fit → Quality → Readiness  │
│                                                             │
│  Confidence-Based Routing                                   │
│    Score ≥ 0.85 → auto-approve for publish handoff          │
│    Score 0.65-0.84 → queue for human review                 │
│    Score < 0.65 → reject, regenerate with feedback          │
│                                                             │
│  Feedback Loop                                              │
│    Engagement metrics → top-performer extraction            │
│    → few-shot example update → next generation cycle        │
└─────────────────┬───────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────┐
│  AUTOMATION LAYER (automations repo)                        │
│  Scheduling, posting, platform API connectors, retries      │
└─────────────────────────────────────────────────────────────┘
```

### Why This Works

| Traditional Team | AI-Automated Equivalent |
|-----------------|------------------------|
| Content strategist (1 FTE) | content_strategy + content_calendar skills |
| Copywriter (2 FTE) | caption_writing + platform_adaptation skills + variant generation |
| Brand manager (1 FTE) | brand_voice_enforcement skill + brand_consistency_judge |
| Compliance reviewer (0.5 FTE) | compliance_judge (hard gate, zero tolerance) |
| Social media coordinator (1 FTE) | publish_handoff skill + content_calendar skill |
| Analytics manager (0.5 FTE) | performance_review skill + feedback loop |
| **Total: ~6 FTE** | **1 operator + this agent** |

## Input Interface

```typescript
interface SocialMediaManagerInput {
  request_type:
    | "content_strategy"
    | "caption_writing"
    | "campaign_planning"
    | "content_calendar"
    | "platform_adaptation"
    | "brand_review"
    | "publish_handoff"
    | "performance_review";

  brand_context: {
    brand_name: string;
    voice_guidelines_ref: string;   // path or URI to brand voice doc
    do_not_say: string[];
    visual_identity_ref?: string;
  };

  platform_targets: Array<{
    platform: "linkedin" | "x" | "instagram" | "facebook" | "tiktok";
    audience_segment?: string;
    constraints?: PlatformConstraints;
  }>;

  campaign_context?: {
    campaign_id: string;
    campaign_name: string;
    objective: "awareness" | "engagement" | "traffic" | "conversion" | "retention";
    start_date: string;  // ISO 8601
    end_date: string;
    kpis: Record<string, number>;
  };

  content_input?: {
    topic: string;
    key_messages: string[];
    media_refs?: string[];          // URIs to creative assets
    source_material?: string;       // long-form content to repurpose/atomize
  };

  variant_config?: {
    variants_per_post: number;      // default: 3
    vary_dimensions: Array<"hook" | "tone" | "cta" | "length" | "format">;
    few_shot_top_posts?: ContentItem[];  // top performers as generation context
  };

  atomization_input?: {
    pillar_content_ref: string;     // URI to blog, whitepaper, transcript
    pillar_content_type: "blog" | "whitepaper" | "video_transcript" | "podcast_transcript" | "press_release";
    extract_types: Array<"key_points" | "quotes" | "statistics" | "stories" | "frameworks">;
  };

  performance_data?: {
    period: string;
    metrics: Record<string, number>;
    top_posts?: Array<{ id: string; engagement_rate: number }>;
    posts_db?: PostPerformanceRecord[];  // structured historical data for feedback loop
  };
}

interface PostPerformanceRecord {
  id: string;
  platform: string;
  copy: string;
  topic_tags: string[];
  tone: string;
  hook_type: "question" | "statistic" | "story" | "bold_claim" | "how_to";
  cta_type: string;
  has_media: boolean;
  published_at: string;
  engagement_rate_24h: number;
  engagement_rate_7d: number;
  impressions_7d: number;
  clicks: number;
  shares: number;
  source_content_id?: string;       // if repurposed, link to source
}

interface PlatformConstraints {
  max_chars: number;
  max_hashtags: number;
  media_required: boolean;
  allowed_media_types: string[];
  link_in_bio_only?: boolean;
}
```

## Output Interface

```typescript
interface SocialMediaManagerOutput {
  request_type: string;
  status: "draft" | "review" | "approved" | "handoff_ready";

  content_items: ContentItem[];
  content_atoms?: ContentAtom[];        // atomized units from pillar content
  variant_sets?: VariantSet[];          // A/B variants grouped by base content
  campaign_plan?: CampaignPlan;
  strategy_recommendations?: StrategyRecommendation[];
  performance_summary?: PerformanceSummary;

  judge_results: JudgeResult[];
  routing_decision: "auto_approve" | "human_review" | "reject";  // confidence-based
  handoff_payload?: PublishHandoff[];
}

interface ContentAtom {
  id: string;
  source_ref: string;                   // URI to pillar content
  atom_type: "key_point" | "quote" | "statistic" | "story" | "framework";
  text: string;
  topic_tags: string[];
  reuse_count: number;                   // how many posts have used this atom
}

interface VariantSet {
  base_content_id: string;
  varied_dimension: "hook" | "tone" | "cta" | "length" | "format";
  variants: ContentItem[];
  recommended_variant_id: string;        // highest predicted engagement
  predicted_engagement_scores: Record<string, number>;  // variant_id → score
}

interface ContentItem {
  id: string;
  platform: string;
  copy: string;
  hashtags: string[];
  cta: string;
  media_brief?: string;
  scheduled_time?: string;
  thread_position?: number;
  quality_score: number;
  brand_alignment_score: number;
  source_atoms?: string[];              // atom IDs this content was derived from
  hook_type?: "question" | "statistic" | "story" | "bold_claim" | "how_to";
  variant_of?: string;                  // base content ID if this is a variant
  metadata: {                           // structured metadata for feedback loop
    topic_tags: string[];
    tone: string;
    cta_type: string;
    has_media: boolean;
    content_pillar: string;
    funnel_stage: string;
  };
}

interface CampaignPlan {
  campaign_id: string;
  timeline: Array<{ date: string; platform: string; content_id: string }>;
  kpi_targets: Record<string, number>;
  content_pillars: string[];
}

interface JudgeResult {
  judge: string;
  content_id: string;
  pass: boolean;
  score: number;
  findings: string[];
}

interface PublishHandoff {
  content_id: string;
  platform: string;
  copy: string;
  hashtags: string[];
  media_refs: string[];
  scheduled_time: string;
  status: "ready" | "blocked";
  blocked_reason?: string;
}

interface PerformanceSummary {
  period: string;
  total_posts: number;
  avg_engagement_rate: number;
  top_performing_content: string[];
  recommendations: string[];
}
```

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Brand voice drift | brand_consistency_judge score < 0.7 | Re-generate with stricter voice constraints |
| Platform constraint violation | platform_fit_judge fails | Truncate/reformat to platform specs |
| Weak CTA | content_quality_judge CTA score < 0.5 | Regenerate CTA with objective context |
| Missing campaign context | campaign_id not found | Request campaign brief before proceeding |
| Content too long | char count > platform max | Condense copy, split into thread if applicable |
| Compliance violation | compliance_judge flags restricted topic | Remove flagged content, escalate for human review |

## Performance Constraints

| Metric | Target | Hard Limit |
|--------|--------|------------|
| Brand voice alignment | ≥ 0.85 | ≥ 0.70 |
| Platform fit score | ≥ 0.90 | ≥ 0.80 |
| Content quality score | ≥ 0.80 | ≥ 0.65 |
| CTA clarity score | ≥ 0.75 | ≥ 0.60 |
| Compliance pass rate | 1.00 | 1.00 |
| Publish handoff completeness | ≥ 0.95 | ≥ 0.90 |

## Dependencies

| Direction | Agent / Surface | Purpose |
|-----------|----------------|---------|
| Upstream | MemoryAgent (agent_007) | Retrieve brand context, past campaign data |
| Downstream | automations | Publish handoff payloads for scheduling/posting |
| Downstream | ugc-mediaops-kit | Creative briefs for media asset production |
| Downstream | agent-platform | Runtime orchestration if deployed as worker |
| Lateral | platform | Approval queue / operator dashboard visibility |

## Required Tools & Libraries

| Tool | Purpose |
|------|---------|
| brand_voice_lookup | Retrieve brand guidelines and do-not-say lists |
| platform_spec_lookup | Get current platform constraints and best practices |
| content_calendar_store | Read/write content calendar entries |
| campaign_registry | Look up active campaigns and KPIs |
| engagement_metrics_read | Pull performance data for retrospectives |
| publish_handoff_emit | Emit structured publish payloads to automation surface |

## Success Criteria

| Metric | Target |
|--------|--------|
| Brand voice consistency across posts | ≥ 85% |
| Platform-native formatting compliance | ≥ 95% |
| Content approved on first review | ≥ 70% |
| Campaign KPI achievement rate | ≥ 80% |
| Publish handoff success rate | ≥ 95% |

## Handoff to Next Agent

### To automations (publish_handoff)
```json
{
  "handoff_type": "publish",
  "content_items": ["<PublishHandoff[]>"],
  "campaign_id": "string",
  "approval_status": "approved",
  "approved_by": "brand_consistency_judge + compliance_judge"
}
```

### To ugc-mediaops-kit (creative_brief)
```json
{
  "handoff_type": "creative_brief",
  "brief": {
    "campaign_id": "string",
    "platform": "string",
    "format": "image | video | carousel",
    "dimensions": "string",
    "copy_overlay": "string",
    "brand_assets_ref": "string",
    "deadline": "ISO 8601"
  }
}
```
