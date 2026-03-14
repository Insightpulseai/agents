# -*- coding: utf-8 -*-
{
    "name": "IPAI Odoo Copilot Bridge",
    "version": "18.0.1.0.0",
    "category": "Productivity/AI",
    "summary": "Bridge module connecting Odoo to the InsightPulseAI Copilot via Azure AI Foundry",
    "description": """
InsightPulseAI Odoo Copilot Bridge
==================================

Connects the Odoo ERP to the InsightPulseAI Copilot Agent Application
published on Azure AI Foundry.

Features:
---------
* Copilot sidebar panel on key views
* Compliance dashboard copilot widget
* Record-level copilot actions (explain, summarize, draft task)
* Write-action confirmation gate with audit logging
* Server-side adapter — never exposes Foundry credentials to the browser

Surfaces:
---------
* Systray copilot toggle
* Sidebar assistant panel (chat)
* Record action menu entries
* Control tower dashboard widget

Architecture:
-------------
Odoo UI -> Odoo Controller -> Backend Adapter -> Foundry Agent Application

All write actions go through a permission check and confirmation gate
before reaching the copilot or Odoo ORM.
    """,
    "author": "InsightPulseAI",
    "website": "https://insightpulseai.net",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "web",
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/copilot_menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ipai_odoo_copilot_bridge/static/src/js/copilot_service.js",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
