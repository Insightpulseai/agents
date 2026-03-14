{
    "name": "IPAI Foundry Provider",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "summary": "Azure Foundry provider configuration for Odoo Copilot agent runtime.",
    "description": """
        Azure Foundry Provider Configuration
        =====================================

        Manages canonical Azure Foundry endpoint configuration for the
        Odoo Copilot agent runtime.

        Features:
        - Separate fields for Foundry project, resource, and OpenAI endpoints
        - Endpoint normalization (short-name expansion, trailing-slash cleanup)
        - Cross-endpoint resource-stem consistency validation
        - Auth mode enforcement (Managed Identity vs Service Principal vs API Key)
        - Secret reference shape validation (kv:// prefix required)
        - Audience selection by operation type
        - Connection target resolution
    """,
    "author": "InsightPulse AI",
    "website": "https://insightpulseai.net",
    "license": "LGPL-3",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/foundry_provider_config_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
