# -*- coding: utf-8 -*-
"""
Odoo HTTP controllers for the copilot bridge.

These endpoints are called by the Odoo frontend (JS) and relay
requests to the backend Foundry adapter. Foundry credentials
never leave the server side.
"""
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CopilotController(http.Controller):
    """Endpoints consumed by the copilot sidebar / widget JS."""

    # ------------------------------------------------------------------
    # Chat endpoint
    # ------------------------------------------------------------------
    @http.route(
        "/ipai/copilot/chat",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def chat(self, message, session_id=None, context_model=None, context_record_id=None):
        """
        Send a user message to the copilot and return the response.

        Args:
            message: The user's query text.
            session_id: Optional existing session ID for continuity.
            context_model: Odoo model the user is currently viewing.
            context_record_id: Record ID the user is currently viewing.

        Returns:
            dict with keys: reply, sources, suggested_actions,
            mode_used, requires_confirmation, session_id.
        """
        user = request.env.user
        company = request.env.company

        # Find or create session
        Session = request.env["ipai.copilot.session"]
        if session_id:
            session = Session.search(
                [("name", "=", session_id), ("user_id", "=", user.id)],
                limit=1,
            )
        else:
            session = None

        if not session:
            session = Session.create({
                "user_id": user.id,
                "company_id": company.id,
            })

        # Record user message
        request.env["ipai.copilot.message"].create({
            "session_id": session.id,
            "role": "user",
            "content": message,
        })

        # Build context for the adapter
        user_groups = [
            g.full_name for g in user.groups_id if g.full_name
        ]

        # --- Adapter call placeholder ---
        # In production, this calls FoundryAgentClient.send().
        # For now, return a structured placeholder so the UI contract
        # is established and testable without a live Foundry endpoint.
        copilot_reply = {
            "reply": (
                "Copilot bridge is connected. "
                "The Foundry Agent Application endpoint is not yet configured. "
                "Set FOUNDRY_ENDPOINT and FOUNDRY_AGENT_APP_ID in the server environment."
            ),
            "sources": [],
            "suggested_actions": [],
            "mode_used": "advisory",
            "requires_confirmation": False,
        }

        # Record assistant message
        request.env["ipai.copilot.message"].create({
            "session_id": session.id,
            "role": "assistant",
            "content": copilot_reply["reply"],
            "mode_used": copilot_reply["mode_used"],
            "sources": json.dumps(copilot_reply["sources"]),
            "suggested_actions": json.dumps(copilot_reply["suggested_actions"]),
            "requires_confirmation": copilot_reply["requires_confirmation"],
        })

        copilot_reply["session_id"] = session.name
        return copilot_reply

    # ------------------------------------------------------------------
    # Confirm action endpoint
    # ------------------------------------------------------------------
    @http.route(
        "/ipai/copilot/confirm",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def confirm_action(self, session_id, action_payload, confirmation_token):
        """
        Confirm and execute a copilot-proposed write action.

        The action gateway checks permissions and logs an audit event
        before the action is sent to the copilot in PROD-CONFIRMED mode.

        Args:
            session_id: The active copilot session.
            action_payload: Dict describing the action to execute.
            confirmation_token: One-time token from the original proposal.

        Returns:
            dict with the copilot's confirmation response.
        """
        user = request.env.user
        company = request.env.company

        action_type = action_payload.get("type", "unknown")

        # Audit log
        request.env["ipai.copilot.audit"].create({
            "user_id": user.id,
            "company_id": company.id,
            "action_type": action_type,
            "target_model": action_payload.get("target_model", ""),
            "target_record_id": action_payload.get("target_record_id"),
            "confirmation_token": confirmation_token,
            "payload_summary": json.dumps(action_payload),
            "outcome": "confirmed",
        })

        # --- Adapter call placeholder ---
        # In production, this calls FoundryAgentClient.confirm_action().
        return {
            "reply": f"Action '{action_type}' confirmed and logged. Foundry endpoint not yet configured.",
            "mode_used": "execution_action",
            "audit_ref": confirmation_token,
        }

    # ------------------------------------------------------------------
    # Session history
    # ------------------------------------------------------------------
    @http.route(
        "/ipai/copilot/history",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def history(self, session_id):
        """Return message history for a session."""
        session = request.env["ipai.copilot.session"].search(
            [("name", "=", session_id), ("user_id", "=", request.env.uid)],
            limit=1,
        )
        if not session:
            return {"messages": []}

        messages = []
        for msg in session.message_ids:
            messages.append({
                "role": msg.role,
                "content": msg.content,
                "mode_used": msg.mode_used,
                "requires_confirmation": msg.requires_confirmation,
                "timestamp": msg.create_date.isoformat() if msg.create_date else None,
            })
        return {"messages": messages}
