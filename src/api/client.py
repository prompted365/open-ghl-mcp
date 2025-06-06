from typing import Any, Dict, Optional, List
import httpx

from ..services.oauth import OAuthService
from ..models.contact import Contact, ContactCreate, ContactUpdate, ContactList
from ..models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationList,
    Message,
    MessageCreate,
    MessageList,
)
from ..utils.exceptions import handle_api_error


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

    # API Methods will be added here as we implement them

    async def get_locations(self, limit: int = 100, skip: int = 0) -> Dict[str, Any]:
        """Get all locations"""
        response = await self._request(
            "GET", "/locations/search", params={"limit": limit, "skip": skip}
        )
        return response.json()

    async def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get a specific location"""
        response = await self._request("GET", f"/locations/{location_id}")
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
            total=data.get("total"),
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
        response = await self._request(
            "POST",
            f"/contacts/{contact_id}/tags",
            json={"tags": tags},
            location_id=location_id,
        )
        data = response.json()
        return Contact(**data.get("contact", data))

    async def remove_contact_tags(
        self, contact_id: str, tags: List[str], location_id: str
    ) -> Contact:
        """Remove tags from a contact"""
        response = await self._request(
            "DELETE",
            f"/contacts/{contact_id}/tags",
            json={"tags": tags},
            location_id=location_id,
        )
        data = response.json()
        return Contact(**data.get("contact", data))

    # Conversation Methods

    async def get_conversations(
        self,
        location_id: str,
        limit: int = 100,
        skip: int = 0,
        contact_id: Optional[str] = None,
        starred: Optional[bool] = None,
        unread_only: Optional[bool] = None,
    ) -> ConversationList:
        """Get conversations for a location"""
        params = {"locationId": location_id, "limit": limit}

        if skip > 0:
            params["skip"] = skip
        if contact_id:
            params["contactId"] = contact_id
        if starred is not None:
            params["starred"] = starred
        if unread_only is not None:
            params["unreadOnly"] = unread_only

        response = await self._request(
            "GET", "/conversations/search", params=params, location_id=location_id
        )
        data = response.json()
        return ConversationList(
            conversations=[Conversation(**c) for c in data.get("conversations", [])],
            count=len(data.get("conversations", [])),
            total=data.get("total"),
        )

    async def get_conversation(
        self, conversation_id: str, location_id: str
    ) -> Conversation:
        """Get a specific conversation"""
        response = await self._request(
            "GET", f"/conversations/{conversation_id}", location_id=location_id
        )
        data = response.json()
        return Conversation(**data.get("conversation", data))

    async def create_conversation(
        self, conversation: ConversationCreate
    ) -> Conversation:
        """Create a new conversation"""
        response = await self._request(
            "POST",
            "/conversations",
            json=conversation.model_dump(exclude_none=True),
            location_id=conversation.locationId,
        )
        data = response.json()
        return Conversation(**data.get("conversation", data))

    async def get_messages(
        self, conversation_id: str, location_id: str, limit: int = 100, skip: int = 0
    ) -> MessageList:
        """Get messages for a conversation"""
        params = {"limit": limit}

        if skip > 0:
            params["skip"] = skip

        response = await self._request(
            "GET",
            f"/conversations/{conversation_id}/messages",
            params=params,
            location_id=location_id,
        )
        data = response.json()
        # Handle nested response structure
        if isinstance(data.get("messages"), dict):
            # Messages are nested under messages.messages
            messages_data = data["messages"].get("messages", [])
            total = len(messages_data)  # or data["messages"].get("total")
        else:
            # Direct array of messages
            messages_data = data.get("messages", [])
            total = data.get("total")

        return MessageList(
            messages=[Message(**m) for m in messages_data if isinstance(m, dict)],
            count=len(messages_data),
            total=total,
        )

    async def send_message(
        self, conversation_id: str, message: MessageCreate, location_id: str
    ) -> Message:
        """Send a message in a conversation"""
        # Extract phone from message if present
        message_data = message.model_dump(exclude_none=True)
        phone = message_data.pop("phone", None)

        # Build payload with phone at top level if needed
        payload = {"conversationId": conversation_id, **message_data}
        if phone:
            # Try different field names the API might expect
            payload["phoneNumber"] = phone  # Try phoneNumber instead of phone

        response = await self._request(
            "POST", "/conversations/messages", json=payload, location_id=location_id
        )
        data = response.json()
        # API returns {conversationId, messageId} for sent messages
        # Convert message type to int for the response
        message_type_int = (
            1 if message.type == "SMS" else 2 if message.type == "Email" else 0
        )
        return Message(
            id=data.get("messageId", data.get("id", "unknown")),
            conversationId=data.get("conversationId", conversation_id),
            body=message.message,
            type=message_type_int,
            contactId=message.contactId,
            status="sent",
        )

    async def update_message_status(
        self, message_id: str, status: str, location_id: str
    ) -> Message:
        """Update the status of a message"""
        response = await self._request(
            "PUT",
            f"/conversations/messages/{message_id}/status",
            json={"status": status},
            location_id=location_id,
        )
        data = response.json()
        return Message(**data.get("message", data))
