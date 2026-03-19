"""
Foundry Agent Application client.

Consumes the published ipai-odoo-copilot-azure Agent Application via the
Azure AI Foundry Responses API, using Entra ID / Managed Identity auth.
"""

from __future__ import annotations

import logging
import os
import uuid
from dataclasses import dataclass, field
from typing import Any

import httpx
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30  # seconds
_DEFAULT_SCOPE = "https://cognitiveservices.azure.com/.default"


@dataclass
class CopilotContext:
    """Context envelope sent with every copilot request."""

    user_id: str
    company_id: str
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    environment: str = "production"
    mode: str = "PROD-ADVISORY"
    locale: str = "en_PH"
    current_model: str | None = None
    current_record_id: int | None = None
    user_groups: list[str] = field(default_factory=list)


@dataclass
class CopilotResponse:
    """Parsed response from the copilot agent."""

    reply: str
    sources: list[str] = field(default_factory=list)
    suggested_actions: list[dict[str, Any]] = field(default_factory=list)
    mode_used: str = "advisory"
    requires_confirmation: bool = False
    raw: dict[str, Any] = field(default_factory=dict)


class FoundryAgentClient:
    """Client for the published Foundry Agent Application."""

    def __init__(
        self,
        endpoint: str | None = None,
        agent_app_id: str | None = None,
        credential: Any | None = None,
        timeout: int = _DEFAULT_TIMEOUT,
    ) -> None:
        self.endpoint = endpoint or os.environ["FOUNDRY_ENDPOINT"]
        self.agent_app_id = agent_app_id or os.environ["FOUNDRY_AGENT_APP_ID"]
        self.timeout = timeout
        self._credential = credential or self._default_credential()

    @staticmethod
    def _default_credential() -> Any:
        managed_client_id = os.environ.get("AZURE_MANAGED_IDENTITY_CLIENT_ID")
        if managed_client_id:
            return ManagedIdentityCredential(client_id=managed_client_id)
        return DefaultAzureCredential()

    def _get_token(self) -> str:
        scope = os.environ.get("FOUNDRY_TOKEN_SCOPE", _DEFAULT_SCOPE)
        token = self._credential.get_token(scope)
        return token.token

    async def send(
        self,
        message: str,
        context: CopilotContext,
    ) -> CopilotResponse:
        """Send a user message to the copilot and return the response."""
        payload = {
            "user_id": context.user_id,
            "session_id": context.session_id,
            "environment": context.environment,
            "mode": context.mode,
            "locale": context.locale,
            "context": {
                "current_model": context.current_model,
                "current_record_id": context.current_record_id,
                "company_id": context.company_id,
                "user_groups": context.user_groups,
            },
            "message": message,
        }

        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

        url = f"{self.endpoint}/agents/{self.agent_app_id}/responses"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
            except httpx.TimeoutException:
                logger.error("Foundry agent request timed out after %ds", self.timeout)
                return CopilotResponse(
                    reply="The copilot is temporarily unavailable. Please try again.",
                    mode_used="error",
                )
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "Foundry agent returned %s: %s",
                    exc.response.status_code,
                    exc.response.text,
                )
                return CopilotResponse(
                    reply="An error occurred while contacting the copilot.",
                    mode_used="error",
                    raw={"status": exc.response.status_code},
                )

        return CopilotResponse(
            reply=data.get("reply", ""),
            sources=data.get("sources", []),
            suggested_actions=data.get("suggested_actions", []),
            mode_used=data.get("mode_used", "advisory"),
            requires_confirmation=data.get("requires_confirmation", False),
            raw=data,
        )

    async def confirm_action(
        self,
        action_payload: dict[str, Any],
        context: CopilotContext,
        confirmation_token: str,
    ) -> CopilotResponse:
        """Send a confirmed write action to the copilot."""
        confirmed_context = CopilotContext(
            user_id=context.user_id,
            company_id=context.company_id,
            session_id=context.session_id,
            environment=context.environment,
            mode="PROD-CONFIRMED",
            locale=context.locale,
            current_model=context.current_model,
            current_record_id=context.current_record_id,
            user_groups=context.user_groups,
        )

        payload_message = (
            f"CONFIRMED_ACTION token={confirmation_token} "
            f"payload={action_payload}"
        )

        return await self.send(payload_message, confirmed_context)
