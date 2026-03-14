# Runtime Contract

## Canonical runtime

Microsoft Foundry Agent Application.

## Publish contract

1. Save version in Foundry
2. Trace
3. Evaluate
4. Publish as Agent Application
5. Consume stable endpoint through backend adapter only

## Allowed production modes

- PROD-ADVISORY
- PROD-ACTION

## Default

PROD-ADVISORY

## PROD-ACTION requirements

- Explicit user confirmation
- Target object identifier (model + ID)
- Change summary presented to user before execution
- Audit event written with request + outcome
- Rollback/recovery note where applicable
