# Odoo Copilot Deployment

## Production Shape

```
Odoo UI
  -> Odoo bridge addon (ipai_odoo_copilot_bridge)
    -> Server-side Foundry adapter (ops-platform/adapters/foundry)
      -> Published Foundry Agent Application (Responses API)
```

## Deployment Steps

1. **Finalize the agent in Foundry**
   - Confirm model, tools, knowledge, instructions
   - Run traces against informational, navigational, compliance, transactional prompts

2. **Save a version**

3. **Run evaluations**
   - See `agents/foundry/ipai-odoo-copilot-azure/evals/smoke.md`

4. **Publish as Agent Application**
   - STAGING first, then PROD after integration test

5. **Configure backend adapter**
   - Set `FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT`
   - Ensure `DefaultAzureCredential` is available (managed identity or workload identity)

6. **Deploy backend adapter**
   ```bash
   cd ops-platform/adapters/foundry
   pip install .
   uvicorn foundry_adapter.service:app --host 0.0.0.0 --port 8100
   ```

7. **Install Odoo bridge addon**
   ```bash
   odoo -d <db> -i ipai_odoo_copilot_bridge --stop-after-init
   ```

8. **Configure Odoo settings**
   - Settings -> IPAI Copilot
   - Enable bridge
   - Set backend URL (e.g. `http://foundry-adapter:8100`)
   - Set environment mode (default: PROD-ADVISORY)

9. **Validate**
   - Informational request works
   - Navigational request works
   - Write request blocked in PROD-ADVISORY
   - Write request requires confirmation in PROD-ACTION
   - Audit records created for all requests

## Repo Artifacts

| Path | Purpose |
|------|---------|
| `agents/foundry/ipai-odoo-copilot-azure/` | Foundry agent contract and metadata |
| `ops-platform/adapters/foundry/` | Backend adapter service |
| `odoo/addons/ipai_odoo_copilot_bridge/` | Odoo bridge addon |
| `infra/docs/architecture/FOUNDRY_PUBLISHING_MODEL.md` | Publish lifecycle |

## Guardrails

- No direct browser-to-Foundry privileged access
- Default mode is PROD-ADVISORY (read-only)
- Write actions require PROD-ACTION mode + explicit confirmation
- Every request is audit-logged in both the adapter and Odoo
- Backend adapter enforces policy before forwarding to Foundry

## Assumptions

- Foundry Agent Application supports the Responses API pattern
  (HTTP POST with `input` + `metadata`, returns `output_text`)
- `DefaultAzureCredential` can acquire a token for `https://ai.azure.com/.default`
- Odoo 19 CE with OWL 2 component support
