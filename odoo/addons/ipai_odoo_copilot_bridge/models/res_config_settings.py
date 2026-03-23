from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ipai_copilot_enabled = fields.Boolean(
        config_parameter="ipai_odoo_copilot_bridge.enabled",
        default=False,
    )
    ipai_copilot_backend_url = fields.Char(
        config_parameter="ipai_odoo_copilot_bridge.backend_url",
    )
    ipai_copilot_environment_mode = fields.Selection(
        [
            ("BUILD", "BUILD"),
            ("STAGING", "STAGING"),
            ("PROD-ADVISORY", "PROD-ADVISORY"),
            ("PROD-ACTION", "PROD-ACTION"),
        ],
        config_parameter="ipai_odoo_copilot_bridge.environment_mode",
        default="PROD-ADVISORY",
    )
