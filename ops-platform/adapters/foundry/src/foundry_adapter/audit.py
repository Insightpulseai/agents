import logging
from uuid import uuid4

from .schemas import CopilotRequest

logger = logging.getLogger(__name__)


def write_audit_event(req: CopilotRequest, status: str) -> str:
    """Write an audit event and return the audit ID.

    Currently logs to stdout. Replace with durable storage
    (Supabase, ADLS, or dedicated audit table) in production.
    """
    audit_id = f"audit_{status}_{uuid4().hex}"
    logger.info(
        "audit_event",
        extra={
            "audit_id": audit_id,
            "status": status,
            "user_id": req.user_id,
            "session_id": req.session_id,
            "environment_mode": req.environment_mode,
            "requested_action": req.requested_action,
            "record_model": req.record_model,
            "record_id": req.record_id,
        },
    )
    return audit_id
