from odoo import fields, models


class IpaiCopilotAudit(models.Model):
    _name = "ipai.copilot.audit"
    _description = "IPAI Copilot Audit"
    _order = "create_date desc"

    user_id = fields.Many2one("res.users", required=True, readonly=True)
    prompt = fields.Text(required=True, readonly=True)
    environment_mode = fields.Selection(
        [
            ("BUILD", "BUILD"),
            ("STAGING", "STAGING"),
            ("PROD-ADVISORY", "PROD-ADVISORY"),
            ("PROD-ACTION", "PROD-ACTION"),
        ],
        required=True,
        default="PROD-ADVISORY",
        readonly=True,
    )
    requested_action = fields.Char(readonly=True)
    audit_external_id = fields.Char(readonly=True)
    blocked = fields.Boolean(default=False, readonly=True)
    reason = fields.Text(readonly=True)
    response_excerpt = fields.Text(readonly=True)
