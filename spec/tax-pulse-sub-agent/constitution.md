# Constitution — Tax Pulse Sub-Agent

## Non-Negotiable Principles

1. **Tax Pulse is a capability pack, not a new top-level agent.** The canonical runtime remains: Advisory, Ops, Actions, Router.
2. **Odoo 19 CE is the workflow/state engine.** Use Project stages, activities, task dependencies, and milestones for operational workflow.
3. **BIR knowledge must be grounded in authoritative sources.** Never invent regulations, rates, deadlines, or filing outcomes.
4. **Risky actions require approval.** Filing, export, and confirmation transitions must pass through explicit approval gates.
5. **Tax truth lives outside model weights.** Rates, rules, knowledge, and filing policy are externalized — not embedded in prompts or fine-tuning.
6. **PLM-style approval semantics.** Required / Optional / Comments-only approval types for tax workflow gates.

## Benchmark Hierarchy

| Benchmark | Use it for |
|---|---|
| AvaTax | tax engine / calculation quality |
| SAP Tax Compliance | compliance workflow rigor (simulation, versioning, worklists) |
| Joule | assistant capability taxonomy (informational/navigational/transactional) |
| BIR official surfaces | authority and filing endpoints |
| Odoo PH localization | localization baseline and extension points |
| TaxPulse-PH-Pack | PH-specific rules/rates/reports seed asset |
