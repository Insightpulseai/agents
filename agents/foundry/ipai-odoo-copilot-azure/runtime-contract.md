# Runtime Contract — ipai-odoo-copilot-azure

## Endpoint

The published Agent Application exposes a stable endpoint consumed via
the Azure AI Foundry Responses API.

## Request Format

The backend adapter sends requests with the following context envelope:

```json
{
  "user_id": "<odoo_user_id>",
  "session_id": "<session_uuid>",
  "environment": "staging|production",
  "mode": "PROD-ADVISORY|PROD-CONFIRMED",
  "locale": "en_PH",
  "context": {
    "current_model": "<odoo.model.name>",
    "current_record_id": "<record_id|null>",
    "company_id": "<company_id>",
    "user_groups": ["group_account_manager", "..."]
  },
  "message": "<user_query>"
}
```

## Response Contract

The agent returns:

```json
{
  "reply": "<markdown_formatted_response>",
  "sources": ["<source_reference>", "..."],
  "suggested_actions": [
    {
      "type": "navigate|draft|action",
      "label": "<button_label>",
      "payload": {}
    }
  ],
  "mode_used": "advisory|execution_design|execution_action|escalation",
  "requires_confirmation": false
}
```

## Write Action Flow

1. User requests a write action.
2. Agent responds with `requires_confirmation: true` and a draft payload.
3. Backend adapter presents confirmation UI to the user.
4. User confirms → backend sends confirmed action request.
5. Agent executes via Execution Action mode.
6. Backend logs audit event.

## Rate Limits

- Max 60 requests per user per minute.
- Max 500 requests per company per minute.
- Requests exceeding limits receive HTTP 429 with retry-after header.

## Timeouts

- Backend adapter timeout: 30 seconds.
- If the agent does not respond within 30 seconds, return a graceful
  fallback message to the user.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Agent timeout | Return fallback message, log incident |
| Agent error | Return generic error, log full trace |
| Auth failure | Return 401, do not retry |
| Rate limited | Return 429 with retry-after |
