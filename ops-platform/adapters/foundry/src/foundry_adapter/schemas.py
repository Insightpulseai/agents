from pydantic import BaseModel, Field
from typing import Literal, Optional, Any, Dict

EnvironmentMode = Literal["BUILD", "STAGING", "PROD-ADVISORY", "PROD-ACTION"]


class CopilotRequest(BaseModel):
    prompt: str
    user_id: str
    session_id: str
    environment_mode: EnvironmentMode = "PROD-ADVISORY"
    record_model: Optional[str] = None
    record_id: Optional[str] = None
    confirmation: bool = False
    requested_action: Optional[str] = None
    extra_context: Dict[str, Any] = Field(default_factory=dict)


class CopilotResponse(BaseModel):
    mode: str
    content: str
    audit_id: Optional[str] = None
    blocked: bool = False
    reason: Optional[str] = None
