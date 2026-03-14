# IPAI Odoo Copilot — Description

Production copilot for Odoo-based Philippine finance, tax compliance,
calendar management, evidence workflows, and control-tower summaries.

## Runtime surface

- Microsoft Foundry Agent Application
- Backend-mediated consumption only
- Responses API protocol

## Capabilities

| Capability | Description |
|------------|-------------|
| Informational | Deadline lookups, regulation summaries, status queries |
| Navigational | Guide users to Odoo views, reports, and workflows |
| Compliance intelligence | Overdue tasks, BIR calendar, readiness scores |
| Transactional (gated) | Draft task creation, finding updates, evidence attachment |

## Consumers

| Consumer | Allowed |
|----------|---------|
| ops-platform backend adapter | Yes |
| Odoo bridge addon | Yes (via adapter) |
| Web backend | Yes (via adapter) |
| Direct browser-side calls | No |
