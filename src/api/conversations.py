"""Conversation and messaging client for GoHighLevel API v2"""

from typing import Optional

from .base import BaseGoHighLevelClient
from ..models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationList,
    Message,
    MessageCreate,
    MessageList,
)


class ConversationsClient(BaseGoHighLevelClient):
    """Client for conversation and messaging endpoints"""

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
        params = {"location_id": location_id, "limit": limit}

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
        # API returns the conversation directly, not wrapped
        return Conversation(**data)

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
        """Update the status of a message

        NOTE: This endpoint is only for custom conversation providers (Marketplace App feature).
        Regular messages cannot have their status updated via API.
        """
        raise NotImplementedError(
            "Message status updates are only supported for custom conversation providers. "
            "This is a Marketplace App feature and not available for standard messages."
        )
