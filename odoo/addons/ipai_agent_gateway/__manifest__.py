{
    "name": "IPAI Agent Gateway",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "summary": "Agent gateway for Odoo Copilot — provides typed, policy-safe tool endpoints for the agent runtime.",
    "description": """
        Odoo Agent Gateway
        ==================

        Provides HTTP controller endpoints for the Odoo Copilot agent runtime.
        All agent-to-Odoo interactions go through this gateway.

        Features:
        - Read tools: partners, invoices, bills, projects, inventory
        - Write tools: draft creation, activities, messages
        - Knowledge tools: documentation, SOPs, model help
        - Policy tools: permission checks, dry-run previews, audit logging
        - Authentication: API key + user context delegation
        - Audit: immutable logging of all operations
        - Tenant scoping: company isolation on every request
    """,
    "author": "InsightPulse AI",
    "website": "https://insightpulseai.net",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "account",
        "project",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/agent_gateway_data.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
