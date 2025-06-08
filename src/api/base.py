"""Base client for GoHighLevel API v2 with shared functionality"""

from typing import Any, Dict, Optional
import httpx

from ..services.oauth import OAuthService
from ..utils.exceptions import handle_api_error


class BaseGoHighLevelClient:
    """Base client with shared functionality for GoHighLevel API v2"""

    API_BASE_URL = "https://services.leadconnectorhq.com"

    def __init__(self, oauth_service: OAuthService):
        self.oauth_service = oauth_service
        self.client = httpx.AsyncClient(base_url=self.API_BASE_URL)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _get_headers(self, location_id: Optional[str] = None) -> Dict[str, str]:
        """Get request headers with valid token

        Args:
            location_id: If provided, will get location-specific token
        """
        if location_id:
            # Get location-specific token for contact operations
            token = await self.oauth_service.get_location_token(location_id)
        else:
            # Use agency token for general operations
            token = await self.oauth_service.get_valid_token()

        return {
            "Authorization": f"Bearer {token}",
            "Version": "2021-07-28",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        location_id: Optional[str] = None,
        **kwargs,
    ) -> httpx.Response:
        """Make an authenticated request to the API"""
        headers = await self._get_headers(location_id)

        response = await self.client.request(
            method=method,
            url=endpoint,
            headers=headers,
            params=params,
            json=json,
            **kwargs,
        )

        if response.status_code >= 400:
            handle_api_error(response)

        return response
