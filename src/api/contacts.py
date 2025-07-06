"""Contact management client for GoHighLevel API v2"""

from typing import List, Optional

from .base import BaseGoHighLevelClient
from ..models.contact import Contact, ContactCreate, ContactUpdate, ContactList


class ContactsClient(BaseGoHighLevelClient):
    """Client for contact-related endpoints"""

    async def get_contacts(
        self,
        location_id: str,
        limit: int = 100,
        skip: int = 0,
        query: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> ContactList:
        """Get contacts for a location"""
        params = {"locationId": location_id, "limit": limit}

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
            "GET", "/contacts", params=params, location_id=location_id
        )
        data = response.json()
        return ContactList(
            contacts=[Contact(**c) for c in data.get("contacts", [])],
            count=len(data.get("contacts", [])),
            total=data.get("meta", {}).get("total") or data.get("total"),
            meta=data.get("meta"),
            traceId=data.get("traceId"),
        )

    async def get_contact(self, contact_id: str, location_id: str) -> Contact:
        """Get a specific contact"""
        response = await self._request(
            "GET", f"/contacts/{contact_id}", location_id=location_id
        )
        data = response.json()
        return Contact(**data.get("contact", data))

    async def create_contact(self, contact: ContactCreate) -> Contact:
        """Create a new contact"""
        response = await self._request(
            "POST",
            "/contacts",
            json=contact.model_dump(exclude_none=True),
            location_id=contact.locationId,
        )
        data = response.json()
        return Contact(**data.get("contact", data))

    async def update_contact(
        self, contact_id: str, updates: ContactUpdate, location_id: str
    ) -> Contact:
        """Update an existing contact"""
        response = await self._request(
            "PUT",
            f"/contacts/{contact_id}",
            json=updates.model_dump(exclude_none=True),
            location_id=location_id,
        )
        data = response.json()
        return Contact(**data.get("contact", data))

    async def delete_contact(self, contact_id: str, location_id: str) -> bool:
        """Delete a contact"""
        response = await self._request(
            "DELETE", f"/contacts/{contact_id}", location_id=location_id
        )
        return response.status_code == 200

    async def add_contact_tags(
        self, contact_id: str, tags: List[str], location_id: str
    ) -> Contact:
        """Add tags to a contact"""
        await self._request(
            "POST",
            f"/contacts/{contact_id}/tags",
            json={"tags": tags},
            location_id=location_id,
        )
        # Tags endpoint returns {tags: [...], tagsAdded: [...]}
        # Need to fetch the updated contact
        return await self.get_contact(contact_id, location_id)

    async def remove_contact_tags(
        self, contact_id: str, tags: List[str], location_id: str
    ) -> Contact:
        """Remove tags from a contact"""
        await self._request(
            "DELETE",
            f"/contacts/{contact_id}/tags",
            json={"tags": tags},
            location_id=location_id,
        )
        # Tags endpoint returns {tags: [...], tagsRemoved: [...]}
        # Need to fetch the updated contact
        return await self.get_contact(contact_id, location_id)