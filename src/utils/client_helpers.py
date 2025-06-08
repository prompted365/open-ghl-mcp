"""Client helper functions for the MCP server"""

from typing import Optional

from ..api.client import GoHighLevelClient
from ..services.oauth import OAuthService


async def get_client_with_token_override(
    oauth_service: Optional[OAuthService],
    ghl_client: Optional[GoHighLevelClient],
    access_token: Optional[str] = None,
) -> GoHighLevelClient:
    """Get GHL client with optional token override"""
    # Ensure clients are initialized
    if oauth_service is None or ghl_client is None:
        raise RuntimeError(
            "MCP server not properly initialized. Please restart the server."
        )

    if access_token:
        # Create a temporary client with the provided token
        temp_oauth = OAuthService()

        # Create an async function that returns the token
        async def return_token() -> str:
            return access_token

        temp_oauth.get_valid_token = return_token  # type: ignore
        return GoHighLevelClient(temp_oauth)
    return ghl_client
