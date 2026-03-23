from fastapi import FastAPI, HTTPException

from .schemas import CopilotRequest, CopilotResponse
from .policy import validate_policy
from .audit import write_audit_event
from .client import FoundryClient

app = FastAPI(title="Foundry Adapter")
client = FoundryClient()


@app.post("/copilot/respond", response_model=CopilotResponse)
async def respond(req: CopilotRequest) -> CopilotResponse:
    ok, reason = validate_policy(req)
    if not ok:
        audit_id = write_audit_event(req, "blocked")
        return CopilotResponse(
            mode=req.environment_mode,
            content="",
            blocked=True,
            reason=reason,
            audit_id=audit_id,
        )

    audit_id = write_audit_event(req, "accepted")

    payload = {
        "input": req.prompt,
        "metadata": {
            "user_id": req.user_id,
            "session_id": req.session_id,
            "environment_mode": req.environment_mode,
            "record_model": req.record_model,
            "record_id": req.record_id,
            "requested_action": req.requested_action,
            "audit_id": audit_id,
            **req.extra_context,
        },
    }

    try:
        result = await client.invoke(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Foundry invocation failed: {exc}",
        ) from exc

    text = result.get("output_text") or str(result)
    return CopilotResponse(
        mode=req.environment_mode,
        content=text,
        audit_id=audit_id,
        blocked=False,
    )
