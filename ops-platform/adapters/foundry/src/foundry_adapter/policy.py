from .schemas import CopilotRequest

WRITE_ACTION_PREFIXES = (
    "create_",
    "update_",
    "close_",
    "attach_",
    "delete_",
)


def is_write_request(req: CopilotRequest) -> bool:
    if req.requested_action:
        return req.requested_action.startswith(WRITE_ACTION_PREFIXES)
    return False


def validate_policy(req: CopilotRequest) -> tuple[bool, str | None]:
    if req.environment_mode == "PROD-ADVISORY" and is_write_request(req):
        return False, "Write actions are blocked in PROD-ADVISORY."
    if (
        req.environment_mode == "PROD-ACTION"
        and is_write_request(req)
        and not req.confirmation
    ):
        return (
            False,
            "Explicit confirmation required for PROD-ACTION write requests.",
        )
    return True, None
