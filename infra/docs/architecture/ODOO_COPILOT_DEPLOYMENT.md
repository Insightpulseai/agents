# Odoo Copilot Deployment

## Production shape

```
Odoo UI
  → Odoo bridge addon (/ipai/copilot/respond)
    → Server-side Foundry adapter (FastAPI)
      → Published Foundry Agent Application (Responses API)
```

## Deployment steps

1. **Finalize agent in Foundry** — instructions, model, tools, knowledge
2. **Save a version** — named release version
3. **Run traces** — informational, navigational, compliance, transactional
4. **Run evaluations** — smoke eval suite passes
5. **Publish as Agent Application** — stable endpoint created
6. **Configure backend adapter**:
   - Set `FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT`
   - Deploy as container or App Service
7. **Deploy backend adapter** — FastAPI service with Entra auth
8. **Install `ipai_odoo_copilot_bridge` in Odoo**
9. **Configure Odoo settings**:
   - Enable copilot bridge
   - Set backend URL
   - Set environment mode (default: PROD-ADVISORY)
10. **Validate end-to-end**:
    - Informational request works
    - Navigational request works
    - Write blocked in PROD-ADVISORY
    - Write confirmed in PROD-ACTION
    - Audit records created

## Guardrails

- No direct browser-to-Foundry privileged access
- All writes require backend mediation
- PROD-ACTION writes require explicit user confirmation
- Every request creates an audit record in Odoo

## Infrastructure requirements

| Component | Runtime |
|-----------|---------|
| Foundry Agent Application | Azure AI Foundry |
| Backend adapter | Azure Container Apps or App Service |
| Odoo bridge addon | Self-hosted Odoo 19 |
| Authentication | Entra ID / DefaultAzureCredential |

## Environment variables

| Variable | Where | Description |
|----------|-------|-------------|
| `FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT` | Backend adapter | Published Agent Application URL |
| `ipai_odoo_copilot_bridge.enabled` | Odoo config params | Enable/disable bridge |
| `ipai_odoo_copilot_bridge.backend_url` | Odoo config params | Adapter base URL |
| `ipai_odoo_copilot_bridge.environment_mode` | Odoo config params | Default mode |

## Rollback

1. Disable bridge in Odoo settings
2. Republish previous Agent Application version in Foundry
3. Redeploy previous adapter version

## Related documents

- `agents/foundry/ipai-odoo-copilot-azure/runtime-contract.md`
- `agents/foundry/ipai-odoo-copilot-azure/publish-policy.md`
- `infra/docs/architecture/FOUNDRY_PUBLISHING_MODEL.md`
