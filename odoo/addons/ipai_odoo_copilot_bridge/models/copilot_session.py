# -*- coding: utf-8 -*-
import logging
import uuid

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CopilotSession(models.Model):
    """Tracks copilot conversation sessions per user."""

    _name = "ipai.copilot.session"
    _description = "IPAI Copilot Session"
    _order = "create_date desc"

    name = fields.Char(
        string="Session ID",
        default=lambda self: str(uuid.uuid4()),
        readonly=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="User",
        default=lambda self: self.env.uid,
        required=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company.id,
        required=True,
        readonly=True,
    )
    state = fields.Selection(
        [("active", "Active"), ("closed", "Closed")],
        default="active",
        readonly=True,
    )
    message_ids = fields.One2many(
        "ipai.copilot.message",
        "session_id",
        string="Messages",
    )


class CopilotMessage(models.Model):
    """Individual messages within a copilot session."""

    _name = "ipai.copilot.message"
    _description = "IPAI Copilot Message"
    _order = "create_date asc"

    session_id = fields.Many2one(
        "ipai.copilot.session",
        string="Session",
        required=True,
        ondelete="cascade",
    )
    role = fields.Selection(
        [("user", "User"), ("assistant", "Assistant"), ("system", "System")],
        required=True,
    )
    content = fields.Text(string="Content", required=True)
    mode_used = fields.Char(string="Mode Used")
    sources = fields.Text(string="Sources (JSON)")
    suggested_actions = fields.Text(string="Suggested Actions (JSON)")
    requires_confirmation = fields.Boolean(default=False)


class CopilotAuditLog(models.Model):
    """Audit log for confirmed copilot write actions."""

    _name = "ipai.copilot.audit"
    _description = "IPAI Copilot Audit Log"
    _order = "create_date desc"

    user_id = fields.Many2one("res.users", string="User", required=True)
    company_id = fields.Many2one("res.company", string="Company", required=True)
    session_id = fields.Many2one("ipai.copilot.session", string="Session")
    action_type = fields.Char(string="Action Type", required=True)
    target_model = fields.Char(string="Target Model")
    target_record_id = fields.Integer(string="Target Record ID")
    confirmation_token = fields.Char(string="Confirmation Token")
    payload_summary = fields.Text(string="Payload Summary")
    outcome = fields.Selection(
        [
            ("confirmed", "Confirmed"),
            ("denied", "Denied"),
            ("error", "Error"),
        ],
        required=True,
    )
