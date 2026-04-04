# Instagram Direct — Rules

Confirmed patterns to apply by default when building Instagram Direct integrations.

## R1: Always implement human agent handoff

- **Rule:** Every automated Instagram DM experience MUST include an escalation path to a human agent
- **Reason:** This is a Meta platform requirement — apps will fail review without it
- **Implementation:** Use Meta's Handover Protocol to pass conversation control between bot and agent apps

## R2: Design for the 24-hour messaging window

- **Rule:** Assume you cannot message a user after 24 hours of inactivity from their side
- **Reason:** Hard platform constraint — messages will be rejected outside this window
- **Implementation:** Build urgency into flows; capture key information early; set user expectations about response timing

## R3: Require Instagram Professional account + Facebook Page linkage

- **Rule:** Only Instagram Business or Creator accounts linked to a Facebook Page can use the messaging API
- **Reason:** Technical prerequisite enforced by Meta's API
- **Implementation:** Validate account type and Page linkage during onboarding before attempting API setup

## R4: Respect the 200 DM/hour rate limit

- **Rule:** Budget automated message sending to stay well under 200 DMs per hour per account
- **Reason:** Hard API rate limit as of 2026 (reduced from 5,000)
- **Implementation:** Implement rate limiting, queuing, and prioritization in any automated messaging system

## R5: Quick replies are text-only with required payloads

- **Rule:** Do not attempt to include images or media in quick reply buttons; always include a payload string
- **Reason:** Platform constraint — media quick replies will fail; payloads are required for webhook routing
- **Implementation:** Use generic templates (carousels) when visual elements are needed in structured responses
