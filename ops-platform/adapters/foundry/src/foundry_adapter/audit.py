from uuid import uuid4

from .schemas import CopilotRequest


def write_audit_event(req: CopilotRequest, status: str) -> str:
    """Write an audit event and return the audit ID.

    TODO: Replace with durable storage (Supabase, Azure Table, etc.).
    """
    audit_id = f"audit_{status}_{uuid4().hex}"
    return audit_id
