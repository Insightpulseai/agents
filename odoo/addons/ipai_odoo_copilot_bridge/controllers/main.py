import logging

import requests

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class IpaiCopilotController(http.Controller):

    @http.route("/ipai/copilot/respond", type="json", auth="user")
    def respond(
        self,
        prompt,
        record_model=None,
        record_id=None,
        requested_action=None,
        confirmation=False,
    ):
        ICP = request.env["ir.config_parameter"].sudo()
        enabled = ICP.get_param("ipai_odoo_copilot_bridge.enabled") == "True"
        backend_url = ICP.get_param("ipai_odoo_copilot_bridge.backend_url")
        environment_mode = ICP.get_param(
            "ipai_odoo_copilot_bridge.environment_mode", "PROD-ADVISORY"
        )

        if not enabled or not backend_url:
            return {"blocked": True, "reason": "Copilot backend not configured."}

        payload = {
            "prompt": prompt,
            "user_id": str(request.env.user.id),
            "session_id": request.session.sid,
            "environment_mode": environment_mode,
            "record_model": record_model,
            "record_id": str(record_id) if record_id else None,
            "requested_action": requested_action,
            "confirmation": confirmation,
            "extra_context": {
                "odoo_db": request.db,
                "odoo_user": request.env.user.login,
            },
        }

        try:
            response = requests.post(
                f"{backend_url}/copilot/respond",
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            _logger.exception("Copilot backend request failed")
            return {"blocked": True, "reason": "Copilot backend unavailable."}

        request.env["ipai.copilot.audit"].sudo().create(
            {
                "user_id": request.env.user.id,
                "prompt": prompt,
                "environment_mode": environment_mode,
                "requested_action": requested_action,
                "audit_external_id": data.get("audit_id"),
                "blocked": data.get("blocked", False),
                "reason": data.get("reason"),
                "response_excerpt": (data.get("content") or "")[:1000],
            }
        )
        return data
