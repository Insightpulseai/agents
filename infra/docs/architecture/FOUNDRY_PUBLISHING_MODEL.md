# Foundry Publishing Model

## Overview

The IPAI Odoo Copilot is deployed as a Microsoft Foundry Agent Application.
This document defines the publish lifecycle and consumption model.

## Publish Lifecycle

```
Build (Foundry Studio)
  -> Save Version
    -> Trace (run against test prompts)
      -> Evaluate (acceptance thresholds)
        -> Publish as Agent Application
          -> STAGING endpoint
            -> Integration test from backend adapter
              -> PROD endpoint
```

## Consumption Model

```
Odoo UI
  -> Odoo bridge addon (ipai_odoo_copilot_bridge)
    -> Backend adapter (ops-platform/adapters/foundry)
      -> Published Agent Application (Responses API)
```

No direct browser-to-Foundry privileged access is allowed.

## Authentication

The backend adapter uses `DefaultAzureCredential` which supports:
- Managed identity (production)
- Workload identity federation (Kubernetes)
- Azure CLI credential (development)

## Environment Modes

| Mode | Behavior |
|------|----------|
| BUILD | Sandbox, no production assumptions |
| STAGING | Non-prod Agent Application, integration validation |
| PROD-ADVISORY | Read-only, informational, navigational |
| PROD-ACTION | Audited, confirmed write actions only |

## Versioning

- Each publish creates an immutable Agent Application version
- Rollback = republish previous known-good version
- No in-place mutation of published versions

## Monitoring

- Foundry traces for runtime behavior
- Backend adapter audit log for policy enforcement
- Odoo `ipai.copilot.audit` model for request/response records
