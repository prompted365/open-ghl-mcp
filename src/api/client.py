from typing import Any, Dict, Optional, List
import httpx

from ..services.oauth import OAuthService
from ..models.contact import Contact, ContactCreate, ContactUpdate, ContactList


class GoHighLevelClient:
    """Client for interacting with GoHighLevel API v2"""
    
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
            "Accept": "application/json"
        }
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        location_id: Optional[str] = None,
        **kwargs
    ) -> httpx.Response:
        """Make an authenticated request to the API"""
        headers = await self._get_headers(location_id)
        
        response = await self.client.request(
            method=method,
            url=endpoint,
            headers=headers,
            params=params,
            json=json,
            **kwargs
        )
        
        response.raise_for_status()
        return response
    
    # API Methods will be added here as we implement them
    
    async def get_locations(self, limit: int = 100, skip: int = 0) -> Dict[str, Any]:
        """Get all locations"""
        response = await self._request(
            "GET",
            "/locations/search",
            params={"limit": limit, "skip": skip}
        )
        return response.json()
    
    async def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get a specific location"""
        response = await self._request(
            "GET",
            f"/locations/{location_id}"
        )
        return response.json()
    
    # Contact Methods
    
    async def get_contacts(
        self, 
        location_id: str,
        limit: int = 100,
        skip: int = 0,
        query: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ContactList:
        """Get contacts for a location"""
        params = {
            "locationId": location_id,
            "limit": limit
        }
        
        # Only add skip if it's greater than 0
        if skip > 0:
            params["skip"] = skip
        
        if query:
            params["query"] = query
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone
        if tags:
            params["tags"] = ",".join(tags)
            
        response = await self._request(
            "GET",
            "/contacts",
            params=params,
            location_id=location_id
        )
        data = response.json()
        return ContactList(
            contacts=[Contact(**c) for c in data.get("contacts", [])],
            count=len(data.get("contacts", [])),
            total=data.get("total")
        )
    
    async def get_contact(self, contact_id: str, location_id: str) -> Contact:
        """Get a specific contact"""
        response = await self._request(
            "GET",
            f"/contacts/{contact_id}",
            location_id=location_id
        )
        data = response.json()
        return Contact(**data.get("contact", data))
    
    async def create_contact(self, contact: ContactCreate) -> Contact:
        """Create a new contact"""
        response = await self._request(
            "POST",
            "/contacts",
            json=contact.model_dump(exclude_none=True),
            location_id=contact.locationId
        )
        data = response.json()
        return Contact(**data.get("contact", data))
    
    async def update_contact(self, contact_id: str, updates: ContactUpdate, location_id: str) -> Contact:
        """Update an existing contact"""
        response = await self._request(
            "PUT",
            f"/contacts/{contact_id}",
            json=updates.model_dump(exclude_none=True),
            location_id=location_id
        )
        data = response.json()
        return Contact(**data.get("contact", data))
    
    async def delete_contact(self, contact_id: str, location_id: str) -> bool:
        """Delete a contact"""
        response = await self._request(
            "DELETE",
            f"/contacts/{contact_id}",
            location_id=location_id
        )
        return response.status_code == 200
    
    async def add_contact_tags(self, contact_id: str, tags: List[str], location_id: str) -> Contact:
        """Add tags to a contact"""
        response = await self._request(
            "POST",
            f"/contacts/{contact_id}/tags",
            json={"tags": tags},
            location_id=location_id
        )
        data = response.json()
        return Contact(**data.get("contact", data))
    
    async def remove_contact_tags(self, contact_id: str, tags: List[str], location_id: str) -> Contact:
        """Remove tags from a contact"""
        response = await self._request(
            "DELETE",
            f"/contacts/{contact_id}/tags",
            json={"tags": tags},
            location_id=location_id
        )
        data = response.json()
        return Contact(**data.get("contact", data))