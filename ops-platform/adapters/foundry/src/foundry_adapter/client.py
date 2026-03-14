import os

import httpx
from azure.identity import DefaultAzureCredential


class FoundryClient:
    """HTTP client for the published Foundry Agent Application.

    Uses DefaultAzureCredential (Entra ID) for authentication.
    Calls the Responses API against the stable Agent Application endpoint.
    """

    def __init__(self) -> None:
        self.endpoint = os.environ["FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT"]
        self.credential = DefaultAzureCredential()

    async def invoke(self, payload: dict) -> dict:
        token = self.credential.get_token("https://ai.azure.com/.default").token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.endpoint, json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json()
