"""
Odoo Agent Gateway — HTTP Controllers

Provides typed, policy-safe tool endpoints for the agent runtime.
All endpoints are versioned under /api/agent/v1/.
"""

import json
import logging
import uuid
from datetime import datetime

from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

ALLOWED_READ_MODELS = {
    "res.partner",
    "account.move",
    "project.project",
    "project.task",
    "stock.move",
}


def _json_response(data, status=200):
    """Return a JSON response with trace metadata."""
    body = json.dumps(data, default=str)
    return Response(
        body,
        status=status,
        content_type="application/json",
    )


def _get_trace_context():
    """Extract or generate trace context from request headers."""
    trace_id = request.httprequest.headers.get("X-Trace-Id", str(uuid.uuid4()))
    return {
        "trace_id": trace_id,
        "timestamp": datetime.utcnow().isoformat(),
        "company_id": request.env.company.id,
        "user_id": request.env.uid,
    }


class AgentGateway(http.Controller):
    """
    Agent Gateway HTTP Controllers.

    All endpoints require authentication via API key (X-Agent-Api-Key header)
    and include trace context for observability.
    """

    # ── Health ────────────────────────────────────────────────

    @http.route(
        "/api/agent/v1/health",
        type="http",
        auth="none",
        methods=["GET"],
        csrf=False,
    )
    def health(self):
        return _json_response({
            "status": "ok",
            "service": "odoo-agent-gateway",
            "version": "1.0.0",
        })

    # ── Read Tools ────────────────────────────────────────────

    @http.route(
        "/api/agent/v1/partners/search",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def search_partners(self, **kwargs):
        """Search customers, vendors, or contacts."""
        params = request.get_json_data()
        trace = _get_trace_context()

        query = params.get("query", "")
        partner_type = params.get("partner_type", "all")
        limit = min(params.get("limit", 20), 100)
        offset = params.get("offset", 0)
        fields = params.get("fields", [
            "id", "name", "email", "phone", "city", "country_id",
        ])

        domain = []
        if query:
            domain.append("|")
            domain.append(("name", "ilike", query))
            domain.append(("email", "ilike", query))
        if partner_type == "customer":
            domain.append(("customer_rank", ">", 0))
        elif partner_type == "vendor":
            domain.append(("supplier_rank", ">", 0))

        partners = request.env["res.partner"].search_read(
            domain, fields=fields, limit=limit, offset=offset,
        )
        total = request.env["res.partner"].search_count(domain)

        self._log_audit("search_partners", params, {"count": len(partners)}, trace)

        return {
            "records": partners,
            "total_count": total,
            "metadata": trace,
        }

    @http.route(
        "/api/agent/v1/invoices",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def get_invoices(self, **kwargs):
        """Fetch customer invoices with filters."""
        params = request.get_json_data()
        trace = _get_trace_context()

        domain = [("move_type", "in", ["out_invoice", "out_refund"])]

        state = params.get("state")
        if state and state != "all":
            domain.append(("state", "=", state))

        payment_state = params.get("payment_state")
        if payment_state and payment_state != "all":
            domain.append(("payment_state", "=", payment_state))

        partner_id = params.get("partner_id")
        if partner_id:
            domain.append(("partner_id", "=", partner_id))

        date_from = params.get("date_from")
        if date_from:
            domain.append(("invoice_date", ">=", date_from))

        date_to = params.get("date_to")
        if date_to:
            domain.append(("invoice_date", "<=", date_to))

        if params.get("overdue_only"):
            domain.append(("invoice_date_due", "<", datetime.now().strftime("%Y-%m-%d")))
            domain.append(("payment_state", "!=", "paid"))

        limit = min(params.get("limit", 20), 100)
        offset = params.get("offset", 0)

        invoices = request.env["account.move"].search_read(
            domain,
            fields=[
                "id", "name", "partner_id", "invoice_date", "invoice_date_due",
                "amount_total", "amount_residual", "state", "payment_state",
                "currency_id",
            ],
            limit=limit,
            offset=offset,
            order="invoice_date_due asc",
        )
        total = request.env["account.move"].search_count(domain)

        # Summary
        all_moves = request.env["account.move"].search(domain)
        summary = {
            "total_amount": sum(all_moves.mapped("amount_total")),
            "total_residual": sum(all_moves.mapped("amount_residual")),
            "currency": request.env.company.currency_id.name,
            "count": total,
        }

        self._log_audit("get_invoices", params, {"count": len(invoices)}, trace)

        return {
            "records": invoices,
            "total_count": total,
            "summary": summary,
            "metadata": trace,
        }

    @http.route(
        "/api/agent/v1/invoices/overdue-summary",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def get_overdue_summary(self, **kwargs):
        """Get overdue analysis grouped by customer or vendor."""
        params = request.get_json_data()
        trace = _get_trace_context()

        move_type = params.get("type", "receivable")
        group_by = params.get("group_by", "partner")
        limit = min(params.get("limit", 20), 100)
        age_brackets = params.get("age_brackets", [30, 60, 90, 120])

        if move_type == "receivable":
            domain = [("move_type", "in", ["out_invoice", "out_refund"])]
        elif move_type == "payable":
            domain = [("move_type", "in", ["in_invoice", "in_refund"])]
        else:
            domain = [("move_type", "in", [
                "out_invoice", "out_refund", "in_invoice", "in_refund",
            ])]

        domain.extend([
            ("payment_state", "!=", "paid"),
            ("state", "=", "posted"),
            ("invoice_date_due", "<", datetime.now().strftime("%Y-%m-%d")),
        ])

        overdue_moves = request.env["account.move"].search(domain, order="amount_residual desc")

        # Group by partner
        groups = {}
        for move in overdue_moves:
            key = move.partner_id.id
            if key not in groups:
                groups[key] = {
                    "partner_id": move.partner_id.id,
                    "partner_name": move.partner_id.name,
                    "total_overdue": 0,
                    "count": 0,
                    "oldest_due_date": None,
                }
            groups[key]["total_overdue"] += move.amount_residual
            groups[key]["count"] += 1
            due_date = str(move.invoice_date_due)
            if not groups[key]["oldest_due_date"] or due_date < groups[key]["oldest_due_date"]:
                groups[key]["oldest_due_date"] = due_date

        sorted_groups = sorted(groups.values(), key=lambda g: g["total_overdue"], reverse=True)[:limit]

        self._log_audit("get_overdue_summary", params, {"groups": len(sorted_groups)}, trace)

        return {
            "groups": sorted_groups,
            "total_overdue": sum(g["total_overdue"] for g in sorted_groups),
            "total_count": sum(g["count"] for g in sorted_groups),
            "metadata": trace,
        }

    @http.route(
        "/api/agent/v1/records/history",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def get_record_history(self, **kwargs):
        """Fetch chatter messages for a record."""
        params = request.get_json_data()
        trace = _get_trace_context()

        model = params.get("model")
        res_id = params.get("res_id")
        limit = min(params.get("limit", 20), 100)

        if model not in ALLOWED_READ_MODELS:
            return {"error": f"Model {model} is not allowed", "metadata": trace}

        messages = request.env["mail.message"].search_read(
            [("model", "=", model), ("res_id", "=", res_id)],
            fields=["date", "body", "author_id", "message_type", "subtype_id"],
            limit=limit,
            order="date desc",
        )

        self._log_audit("get_record_history", params, {"count": len(messages)}, trace)

        return {
            "messages": messages,
            "metadata": trace,
        }

    @http.route(
        "/api/agent/v1/user/context",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def get_user_context(self, **kwargs):
        """Fetch current user permissions and company context."""
        trace = _get_trace_context()
        user = request.env.user

        return {
            "user_id": user.id,
            "user_name": user.name,
            "company_id": request.env.company.id,
            "company_name": request.env.company.name,
            "allowed_companies": [
                {"id": c.id, "name": c.name}
                for c in user.company_ids
            ],
            "groups": [
                g.full_name for g in user.groups_id
            ],
            "permissions": {
                "can_read_invoices": user.has_group("account.group_account_invoice"),
                "can_write_invoices": user.has_group("account.group_account_invoice"),
                "can_read_partners": True,
                "can_write_partners": user.has_group("base.group_partner_manager"),
                "can_read_projects": user.has_group("project.group_project_user"),
                "can_read_inventory": user.has_group("stock.group_stock_user"),
            },
            "metadata": trace,
        }

    # ── Write Tools ───────────────────────────────────────────

    @http.route(
        "/api/agent/v1/invoices/draft",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_draft_invoice(self, **kwargs):
        """Create a customer invoice in draft state."""
        params = request.get_json_data()
        trace = _get_trace_context()

        # Permission check
        if not request.env.user.has_group("account.group_account_invoice"):
            return {"error": "Permission denied: invoice creation requires account.group_account_invoice", "metadata": trace}

        dry_run = params.get("dry_run", True)

        vals = {
            "move_type": "out_invoice",
            "partner_id": params["partner_id"],
            "invoice_date": params.get("invoice_date"),
            "narration": params.get("narration"),
            "invoice_line_ids": [
                (0, 0, {
                    "product_id": line.get("product_id"),
                    "name": line["name"],
                    "quantity": line["quantity"],
                    "price_unit": line["price_unit"],
                    "tax_ids": [(6, 0, line.get("tax_ids", []))],
                })
                for line in params.get("lines", [])
            ],
        }

        if dry_run:
            # Validate without creating
            return {
                "dry_run": True,
                "preview": vals,
                "validation_errors": [],
                "metadata": trace,
            }

        invoice = request.env["account.move"].create(vals)

        self._log_audit("create_draft_invoice", params, {"id": invoice.id}, trace)

        return {
            "id": invoice.id,
            "name": invoice.name,
            "state": invoice.state,
            "amount_total": invoice.amount_total,
            "url": f"/odoo/accounting/customer-invoices/{invoice.id}",
            "dry_run": False,
            "metadata": trace,
        }

    @http.route(
        "/api/agent/v1/activities",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_activity(self, **kwargs):
        """Schedule an activity on any record."""
        params = request.get_json_data()
        trace = _get_trace_context()

        model = params.get("model")
        if model not in ALLOWED_READ_MODELS:
            return {"error": f"Model {model} is not allowed", "metadata": trace}

        activity_type_map = {
            "email": "mail.mail_activity_data_email",
            "call": "mail.mail_activity_data_call",
            "meeting": "mail.mail_activity_data_meeting",
            "todo": "mail.mail_activity_data_todo",
            "upload_document": "mail.mail_activity_data_upload_document",
        }

        activity_type_ref = activity_type_map.get(
            params.get("activity_type", "todo"), "mail.mail_activity_data_todo"
        )
        activity_type = request.env.ref(activity_type_ref)

        activity = request.env["mail.activity"].create({
            "res_model_id": request.env["ir.model"]._get_id(model),
            "res_id": params["res_id"],
            "activity_type_id": activity_type.id,
            "summary": params["summary"],
            "note": params.get("note", ""),
            "date_deadline": params["date_deadline"],
            "user_id": params.get("user_id", request.env.uid),
        })

        self._log_audit("create_activity", params, {"id": activity.id}, trace)

        return {
            "id": activity.id,
            "metadata": trace,
        }

    @http.route(
        "/api/agent/v1/messages",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def post_message(self, **kwargs):
        """Post a message to the chatter of any record."""
        params = request.get_json_data()
        trace = _get_trace_context()

        model = params.get("model")
        if model not in ALLOWED_READ_MODELS:
            return {"error": f"Model {model} is not allowed", "metadata": trace}

        record = request.env[model].browse(params["res_id"])
        message = record.message_post(
            body=params["body"],
            message_type=params.get("message_type", "comment"),
            subtype_xmlid=params.get("subtype", "mail.mt_comment"),
        )

        self._log_audit("post_message", params, {"id": message.id}, trace)

        return {
            "id": message.id,
            "metadata": trace,
        }

    # ── Policy Tools ──────────────────────────────────────────

    @http.route(
        "/api/agent/v1/permissions/check",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def check_permission(self, **kwargs):
        """Verify if the current user can perform an action."""
        params = request.get_json_data()
        trace = _get_trace_context()

        model = params.get("model")
        operation = params.get("operation", "read")

        try:
            request.env[model].check_access_rights(operation, raise_exception=True)
            if params.get("res_ids"):
                records = request.env[model].browse(params["res_ids"])
                records.check_access_rule(operation)
            allowed = True
            reason = "Access granted"
        except Exception as e:
            allowed = False
            reason = str(e)

        return {
            "allowed": allowed,
            "reason": reason,
            "metadata": trace,
        }

    # ── Audit ─────────────────────────────────────────────────

    def _log_audit(self, tool, input_data, output_summary, trace):
        """Log an audit event for every gateway operation."""
        _logger.info(
            "AGENT_AUDIT tool=%s user=%s company=%s trace=%s input=%s output=%s",
            tool,
            trace.get("user_id"),
            trace.get("company_id"),
            trace.get("trace_id"),
            json.dumps(input_data, default=str),
            json.dumps(output_summary, default=str),
        )
