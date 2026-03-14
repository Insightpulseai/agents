# Environment Modes — ipai-odoo-copilot-azure

## PROD-ADVISORY (Default)

- All responses are read-only and informational.
- No Odoo records are created, updated, or deleted.
- Tools may read data but never write.
- This is the safe default for all production traffic.

## PROD-CONFIRMED

- Write actions are permitted **only** after the user explicitly confirms
  through the backend confirmation gate.
- The confirmation flow:
  1. Agent proposes a draft action with `requires_confirmation: true`.
  2. Backend adapter renders confirmation dialog in Odoo UI.
  3. User clicks "Confirm" or "Cancel".
  4. If confirmed, backend sends the action to the agent with
     `mode: PROD-CONFIRMED` and a confirmation token.
  5. Agent executes the action and returns an audit reference.
- Every confirmed action is logged with: user_id, timestamp, action type,
  record affected, and confirmation token.

## DEV

- Used only in development and local testing.
- All tools enabled, no confirmation gates.
- Never deployed to staging or production.

## Mode Selection

The backend adapter sets the mode per-request based on:
- The action type (read vs. write)
- The user's role and permissions
- The environment (dev / staging / prod)

The agent itself does not choose its mode — the backend enforces it.
