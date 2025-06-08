"""Conversation parameter classes for MCP tools"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from ...models.conversation import MessageStatus


class GetConversationsParams(BaseModel):
    """Parameters for getting conversations"""

    location_id: str = Field(..., description="The location ID")
    contact_id: Optional[str] = Field(None, description="Filter by contact ID")
    starred: Optional[bool] = Field(None, description="Filter by starred status")
    unread_only: Optional[bool] = Field(
        None, description="Only show unread conversations"
    )
    limit: int = Field(100, description="Number of results to return", ge=1, le=100)
    skip: int = Field(0, description="Number of results to skip", ge=0)
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetConversationParams(BaseModel):
    """Parameters for getting a single conversation"""

    conversation_id: str = Field(..., description="The conversation ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class CreateConversationParams(BaseModel):
    """Parameters for creating a conversation"""

    location_id: str = Field(..., description="The location ID")
    contact_id: str = Field(..., description="The contact ID")
    message_type: Optional[str] = Field(
        None,
        description="Initial message type: SMS, Email, WhatsApp, IG, FB, Custom, Live_Chat",
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetMessagesParams(BaseModel):
    """Parameters for getting messages in a conversation"""

    conversation_id: str = Field(..., description="The conversation ID")
    location_id: str = Field(..., description="The location ID")
    limit: int = Field(100, description="Number of results to return", ge=1, le=100)
    skip: int = Field(0, description="Number of results to skip", ge=0)
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class SendMessageParams(BaseModel):
    """Parameters for sending a message"""

    conversation_id: str = Field(..., description="The conversation ID")
    location_id: str = Field(..., description="The location ID")
    message_type: str = Field(
        ...,
        description="Type of message to send: SMS, Email, WhatsApp, IG, FB, Custom, Live_Chat",
    )
    contact_id: str = Field(..., description="Contact ID to send message to")

    # SMS fields
    message: Optional[str] = Field(None, description="Message content for SMS")
    phone: Optional[str] = Field(None, description="Phone number for SMS messages")

    # Email fields
    html: Optional[str] = Field(None, description="HTML content for email messages")
    text: Optional[str] = Field(
        None, description="Plain text content for email messages"
    )
    subject: Optional[str] = Field(None, description="Subject line for email messages")

    # General
    attachments: Optional[List[Dict[str, Any]]] = Field(
        None, description="Optional attachments"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class UpdateMessageStatusParams(BaseModel):
    """Parameters for updating message status"""

    message_id: str = Field(..., description="The message ID")
    location_id: str = Field(..., description="The location ID")
    status: MessageStatus = Field(..., description="New status for the message")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )
