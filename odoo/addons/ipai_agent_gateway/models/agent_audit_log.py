"""
Agent Audit Log Model

Persistent audit trail for all agent gateway operations.
Records are immutable — no write or unlink operations.
"""

from odoo import models, fields


class AgentAuditLog(models.Model):
    _name = "ipai.agent.audit.log"
    _description = "Agent Gateway Audit Log"
    _order = "create_date desc"
    _rec_name = "trace_id"

    trace_id = fields.Char("Trace ID", required=True, index=True)
    tool = fields.Char("Tool", required=True, index=True)
    user_id = fields.Many2one("res.users", "User", required=True, index=True)
    company_id = fields.Many2one("res.company", "Company", required=True, index=True)
    input_summary = fields.Text("Input Summary")
    output_summary = fields.Text("Output Summary")
    duration_ms = fields.Integer("Duration (ms)")
    success = fields.Boolean("Success", default=True)
    error_message = fields.Text("Error Message")
    request_timestamp = fields.Datetime("Request Timestamp", required=True)

    def write(self, vals):
        """Audit logs are immutable."""
        raise models.ValidationError("Audit log records cannot be modified.")

    def unlink(self):
        """Audit logs cannot be deleted."""
        raise models.ValidationError("Audit log records cannot be deleted.")
