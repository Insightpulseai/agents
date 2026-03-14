{
    "name": "IPAI Odoo Copilot Bridge",
    "version": "19.0.1.0.0",
    "category": "Productivity",
    "summary": "Bridge to the Foundry-backed IPAI copilot via server-side adapter",
    "depends": ["base", "web", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/copilot_menu_views.xml",
        "data/ir_cron.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ipai_odoo_copilot_bridge/static/src/js/copilot_panel.js",
            "ipai_odoo_copilot_bridge/static/src/xml/copilot_panel.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
