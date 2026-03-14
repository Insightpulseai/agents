# Constitution — Odoo Copilot Agent Framework

## Non-Negotiable Principles

1. **3 agents + 1 workflow only.** Do not add more top-level agents until eval coverage and tracing are stable.
2. **Foundry is the control plane.** Prompt agents, guardrails, datasets, evaluations, tracing, and project-scoped resources live in Foundry.
3. **Agent Framework is the execution plane.** Graph workflows, checkpointing, middleware, human-in-the-loop approvals, and multi-agent orchestration live in Agent Framework.
4. **APIM is the production front door.** All production traffic enters through Azure API Management AI Gateway.
5. **Playgrounds are not production.** Foundry Playgrounds are for rapid prototyping and validation only.
6. **Vendor capabilities are packs, not agents.** Databricks, fal, Smartly, Quilt, LIONS, Data Intelligence, and BIR compliance are capability packs attached to the 3-agent backbone — never separate top-level agents.
7. **Odoo owns workflow state.** The copilot explains, inspects, routes, and triggers approved actions. It does not replace the Odoo task/project/activity engine.
8. **Tax truth lives outside model weights.** Rates, regulations, deadlines, and filing rules stay in knowledge, rules, tools, and workflow policy — not in prompts or fine-tuning.
9. **Safety evals are necessary but not sufficient.** Always pair automated safety evaluations with human review and domain-specific policy tests before production.
10. **Secrets via environment variables, never hardcoded.** No credentials in prompts, tool args, or trace attributes.

## Role Boundaries

| Component | Can do | Cannot do |
|---|---|---|
| Advisory | explain, summarize, recommend, compare, route | write records, execute business changes, bypass approvals |
| Ops | inspect, diagnose, compare state, recommend remediation | mutate records, change secrets/roles, trigger uncontrolled jobs |
| Actions | create/update allowed records, trigger approved jobs, write evidence | unrestricted writes, destructive ops, policy bypass, silent batch |
| Router | route, pause for approval, resume, hand off, checkpoint | free-form business reasoning, direct domain mutation |

## Evaluation Requirement

Every agent and workflow must have:
- At least one system evaluation dataset
- At least one process evaluation dataset (where tools are used)
- Safety evaluation coverage
- Tracing enabled and linked to Application Insights
