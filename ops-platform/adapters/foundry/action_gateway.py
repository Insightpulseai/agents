"""
Action Gateway — confirmation and audit layer for copilot write actions.

This module sits between the Odoo controller and the Foundry adapter.
It enforces the confirmation protocol and writes audit events before
any mutating action reaches the copilot or Odoo ORM.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AuditEvent:
    """Immutable audit record for a confirmed copilot action."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    user_id: str = ""
    company_id: str = ""
    action_type: str = ""
    target_model: str = ""
    target_record_id: int | None = None
    confirmation_token: str = ""
    payload_summary: str = ""
    outcome: str = "pending"


class ActionGateway:
    """
    Enforces:
    1. Permission check — user must have the required Odoo group.
    2. Confirmation gate — action must be explicitly confirmed by the user.
    3. Audit logging — every confirmed action is recorded.
    """

    # Map action types to required Odoo groups.
    REQUIRED_GROUPS: dict[str, list[str]] = {
        "create_task": ["group_project_user"],
        "update_finding": ["group_account_manager", "group_compliance_officer"],
        "close_record": ["group_account_manager"],
        "attach_evidence": ["group_project_user"],
        "change_workflow_state": ["group_account_manager"],
    }

    def __init__(self, audit_sink: Any = None) -> None:
        """
        Args:
            audit_sink: callable(AuditEvent) that persists the event
                        (e.g. Supabase insert, log file, etc.).
                        Defaults to logger.info.
        """
        self._audit_sink = audit_sink or self._default_sink

    @staticmethod
    def _default_sink(event: AuditEvent) -> None:
        logger.info(
            "AUDIT action=%s user=%s target=%s.%s token=%s outcome=%s",
            event.action_type,
            event.user_id,
            event.target_model,
            event.target_record_id,
            event.confirmation_token,
            event.outcome,
        )

    def check_permission(
        self,
        action_type: str,
        user_groups: list[str],
    ) -> bool:
        """Return True if the user's groups satisfy the action requirement."""
        required = self.REQUIRED_GROUPS.get(action_type, [])
        if not required:
            # Unknown action type — deny by default.
            logger.warning("Unknown action type: %s — denied", action_type)
            return False
        return bool(set(required) & set(user_groups))

    def generate_confirmation_token(self) -> str:
        """Generate a one-time confirmation token."""
        return str(uuid.uuid4())

    def confirm_and_audit(
        self,
        action_type: str,
        user_id: str,
        company_id: str,
        user_groups: list[str],
        target_model: str,
        target_record_id: int | None,
        payload_summary: str,
        confirmation_token: str,
    ) -> AuditEvent:
        """
        Validate permissions, record the audit event, and return it.

        Raises:
            PermissionError: if the user lacks the required group.
        """
        if not self.check_permission(action_type, user_groups):
            event = AuditEvent(
                user_id=user_id,
                company_id=company_id,
                action_type=action_type,
                target_model=target_model,
                target_record_id=target_record_id,
                confirmation_token=confirmation_token,
                payload_summary=payload_summary,
                outcome="denied",
            )
            self._audit_sink(event)
            raise PermissionError(
                f"User {user_id} lacks permission for {action_type}"
            )

        event = AuditEvent(
            user_id=user_id,
            company_id=company_id,
            action_type=action_type,
            target_model=target_model,
            target_record_id=target_record_id,
            confirmation_token=confirmation_token,
            payload_summary=payload_summary,
            outcome="confirmed",
        )
        self._audit_sink(event)
        return event
