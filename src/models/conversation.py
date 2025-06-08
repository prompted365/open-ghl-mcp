from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """Message types supported by GoHighLevel API"""

    # API sending types (for outbound messages)
    SMS = "SMS"
    EMAIL = "Email"
    WHATSAPP = "WhatsApp"
    IG = "IG"
    FB = "FB"
    CUSTOM = "Custom"
    LIVE_CHAT = "Live_Chat"

    # Legacy types (for reading existing messages)
    TYPE_CALL = "TYPE_CALL"
    TYPE_SMS = "TYPE_SMS"
    TYPE_EMAIL = "TYPE_EMAIL"
    TYPE_SMS_REVIEW_REQUEST = "TYPE_SMS_REVIEW_REQUEST"
    TYPE_WEBCHAT = "TYPE_WEBCHAT"
    TYPE_FB_MESSENGER = "TYPE_FB_MESSENGER"
    TYPE_INSTAGRAM = "TYPE_INSTAGRAM"
    TYPE_WHATSAPP = "TYPE_WHATSAPP"
    TYPE_VOICE_MAIL = "TYPE_VOICE_MAIL"
    TYPE_NO_SHOW = "TYPE_NO_SHOW"
    TYPE_ACTIVITY_OPPORTUNITY = "TYPE_ACTIVITY_OPPORTUNITY"
    TYPE_LIVE_CHAT_INFO_MESSAGE = "TYPE_LIVE_CHAT_INFO_MESSAGE"


# Message type numeric codes used by the API (for reading responses)
MESSAGE_TYPE_CODES = {
    # Current API sending types
    MessageType.SMS: 1,
    MessageType.EMAIL: 2,
    MessageType.WHATSAPP: 5,
    MessageType.FB: 7,
    MessageType.IG: 15,
    MessageType.LIVE_CHAT: 11,
    # Legacy types (for compatibility)
    MessageType.TYPE_SMS: 1,
    MessageType.TYPE_EMAIL: 2,
    MessageType.TYPE_CALL: 3,
    MessageType.TYPE_WHATSAPP: 5,
    MessageType.TYPE_FB_MESSENGER: 7,
    MessageType.TYPE_INSTAGRAM: 15,
    MessageType.TYPE_WEBCHAT: 11,
    MessageType.TYPE_SMS_REVIEW_REQUEST: 13,
    MessageType.TYPE_VOICE_MAIL: 14,
}


class MessageStatus(str, Enum):
    """Message delivery status"""

    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    PENDING = "pending"
    VOICEMAIL = "voicemail"


class MessageDirection(str, Enum):
    """Message direction"""

    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Message(BaseModel):
    """Message model"""

    id: str
    conversationId: str
    locationId: Optional[str] = None
    contactId: Optional[str] = None
    body: Optional[str] = None  # Body can be missing for some message types
    type: Union[int, MessageType]  # API returns numeric type
    messageType: Optional[MessageType] = None  # String type
    direction: Optional[MessageDirection] = None
    status: Optional[Union[MessageStatus, str]] = (
        None  # Allow any string for flexibility
    )
    dateAdded: Optional[Union[datetime, str]] = None  # Can be datetime or ISO string
    dateUpdated: Optional[Union[datetime, str]] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    meta: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    userId: Optional[str] = None
    contentType: Optional[str] = None


class MessageCreate(BaseModel):
    """Create a new message"""

    type: Union[int, str, MessageType] = Field(
        ..., description="Message type (numeric or string)"
    )
    contactId: str = Field(..., description="Contact ID to send message to")

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
    attachments: Optional[List[Dict[str, Any]]] = None


class Conversation(BaseModel):
    """Conversation model"""

    id: str
    locationId: str
    contactId: str
    lastMessageBody: Optional[str] = None
    lastMessageType: Optional[str] = None  # API returns "TYPE_SMS", "TYPE_EMAIL", etc.
    lastMessageDate: Optional[int] = None  # Unix timestamp in milliseconds
    lastMessageDirection: Optional[str] = None
    lastOutboundMessageAction: Optional[str] = None
    lastManualMessageDate: Optional[int] = None
    unreadCount: int = 0
    dateAdded: Optional[int] = None  # Unix timestamp in milliseconds
    dateUpdated: Optional[int] = None  # Unix timestamp in milliseconds
    starred: Optional[bool] = False
    deleted: Optional[bool] = False
    inbox: Optional[bool] = True
    assignedTo: Optional[str] = None
    userId: Optional[str] = None
    followers: Optional[List[str]] = Field(default_factory=list)
    isLastMessageInternalComment: Optional[bool] = False
    fullName: Optional[str] = None
    contactName: Optional[str] = None
    companyName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    type: Optional[Union[str, int]] = None  # "TYPE_PHONE" or numeric (1, etc.)
    scoring: Optional[List[Any]] = Field(default_factory=list)
    attributed: Optional[Union[bool, None]] = None
    sort: Optional[List[int]] = None


class ConversationCreate(BaseModel):
    """Create a new conversation"""

    locationId: str = Field(..., description="Location ID")
    contactId: str = Field(..., description="Contact ID")
    lastMessageType: Optional[MessageType] = None


class ConversationList(BaseModel):
    """List of conversations"""

    conversations: List[Conversation]
    total: Optional[int] = None
    count: int
    traceId: Optional[str] = None


class MessageList(BaseModel):
    """List of messages"""

    messages: List[Message]
    total: Optional[int] = None
    count: int
