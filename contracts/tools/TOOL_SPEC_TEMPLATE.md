# Tool Spec: {TOOL_NAME}

> Version: 1.0.0
> Last updated: {DATE}
> Gate: tool_spec_contract_gate

## Tool Name

{Human-readable name}

## Endpoint

| Field | Value |
|-------|-------|
| Method | GET / POST / PATCH / DELETE |
| URL | `{base_url}/{path}` |
| Auth | Bearer token / API key / Managed identity |

## Auth

- **Type**: {auth_type}
- **Header**: `Authorization: Bearer {token}` or `X-IPAI-Key: {key}`
- **Scope**: {required_permissions}

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "example_field": {
      "type": "string",
      "description": "Description of the field"
    }
  },
  "required": ["example_field"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "result": {
      "type": "array",
      "items": {
        "type": "object"
      }
    }
  }
}
```

## Scope

- **Read/Write**: {read_only | read_write}
- **Models accessed**: {list of Odoo models}
- **Record scope**: {all | user_scoped | company_scoped}
- **Environment modes**: {which env modes this tool is available in}

## Guardrails

- [ ] PII redaction applied to output
- [ ] Input validation enforced
- [ ] Rate limiting configured
- [ ] Audit log entry created per invocation
- [ ] Confirmation required for write operations
- [ ] Scope restricted to declared models only

## Eval Cases

| Input | Expected | Criteria |
|-------|----------|----------|
| {example input} | {expected behavior} | {pass criteria} |

## Rollback

- **On failure**: {what happens if the tool fails mid-operation}
- **Idempotent**: {yes/no}
- **Retry safe**: {yes/no}
