#!/usr/bin/env python3
"""GoHighLevel MCP Server using FastMCP"""

from typing import Optional, Dict, Any, List

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .api.client import GoHighLevelClient
from .services.oauth import OAuthService
from .models.contact import ContactCreate, ContactUpdate
from .models.conversation import (
    ConversationCreate,
    MessageCreate,
    MessageStatus,
    MessageType,
)


# Initialize FastMCP server
mcp: FastMCP = FastMCP(
    name="ghl-mcp-server",
    version="0.1.0",
    description="MCP server for GoHighLevel API integration",
    dependencies=["httpx", "pydantic", "python-dotenv"],
)

# Global clients
oauth_service: OAuthService = OAuthService()
ghl_client: GoHighLevelClient = GoHighLevelClient(oauth_service)


# Tool Models


class CreateContactParams(BaseModel):
    """Parameters for creating a contact"""

    location_id: str = Field(
        ..., description="The location ID where the contact will be created"
    )
    first_name: Optional[str] = Field(None, description="Contact's first name")
    last_name: Optional[str] = Field(None, description="Contact's last name")
    email: Optional[str] = Field(None, description="Contact's email address")
    phone: Optional[str] = Field(None, description="Contact's phone number")
    tags: Optional[List[str]] = Field(None, description="Tags to assign to the contact")
    source: Optional[str] = Field(None, description="Source of the contact")
    company_name: Optional[str] = Field(None, description="Contact's company name")
    address: Optional[str] = Field(None, description="Contact's street address")
    city: Optional[str] = Field(None, description="Contact's city")
    state: Optional[str] = Field(None, description="Contact's state")
    postal_code: Optional[str] = Field(None, description="Contact's postal code")
    custom_fields: Optional[Dict[str, Any]] = Field(
        None, description="Custom field values"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class UpdateContactParams(BaseModel):
    """Parameters for updating a contact"""

    contact_id: str = Field(..., description="The contact ID to update")
    location_id: str = Field(
        ..., description="The location ID where the contact exists"
    )
    first_name: Optional[str] = Field(None, description="Contact's first name")
    last_name: Optional[str] = Field(None, description="Contact's last name")
    email: Optional[str] = Field(None, description="Contact's email address")
    phone: Optional[str] = Field(None, description="Contact's phone number")
    tags: Optional[List[str]] = Field(None, description="Tags to assign to the contact")
    company_name: Optional[str] = Field(None, description="Contact's company name")
    address: Optional[str] = Field(None, description="Contact's street address")
    city: Optional[str] = Field(None, description="Contact's city")
    state: Optional[str] = Field(None, description="Contact's state")
    postal_code: Optional[str] = Field(None, description="Contact's postal code")
    custom_fields: Optional[Dict[str, Any]] = Field(
        None, description="Custom field values"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class DeleteContactParams(BaseModel):
    """Parameters for deleting a contact"""

    contact_id: str = Field(..., description="The contact ID to delete")
    location_id: str = Field(
        ..., description="The location ID where the contact exists"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class SearchContactsParams(BaseModel):
    """Parameters for searching contacts"""

    location_id: str = Field(..., description="The location ID to search contacts in")
    query: Optional[str] = Field(None, description="Search query string")
    email: Optional[str] = Field(None, description="Filter by email address")
    phone: Optional[str] = Field(None, description="Filter by phone number")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    limit: int = Field(100, description="Number of results to return", ge=1, le=100)
    skip: int = Field(0, description="Number of results to skip", ge=0)
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetContactParams(BaseModel):
    """Parameters for getting a single contact"""

    contact_id: str = Field(..., description="The contact ID to retrieve")
    location_id: str = Field(
        ..., description="The location ID where the contact exists"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class ManageTagsParams(BaseModel):
    """Parameters for managing contact tags"""

    contact_id: str = Field(..., description="The contact ID")
    location_id: str = Field(
        ..., description="The location ID where the contact exists"
    )
    tags: List[str] = Field(..., description="Tags to add or remove")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


# Conversation Tool Models


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


# Helper function to get client with optional token override
async def get_client(access_token: Optional[str] = None) -> GoHighLevelClient:
    """Get GHL client with optional token override"""
    if access_token:
        # Create a temporary client with the provided token
        temp_oauth = OAuthService()

        # Create an async function that returns the token
        async def return_token() -> str:
            return access_token
        temp_oauth.get_valid_token = return_token  # type: ignore
        return GoHighLevelClient(temp_oauth)
    return ghl_client


# Tools


@mcp.tool()
async def create_contact(params: CreateContactParams) -> Dict[str, Any]:
    """Create a new contact in GoHighLevel"""
    client = await get_client(params.access_token)

    contact_data = ContactCreate(
        locationId=params.location_id,
        firstName=params.first_name,
        lastName=params.last_name,
        email=params.email,
        phone=params.phone,
        tags=params.tags,
        source=params.source,
        companyName=params.company_name,
        address1=params.address,
        city=params.city,
        state=params.state,
        postalCode=params.postal_code,
        customFields=[
            {"key": k, "value": v} for k, v in (params.custom_fields or {}).items()
        ],
    )

    contact = await client.create_contact(contact_data)
    return {"success": True, "contact": contact.model_dump()}


@mcp.tool()
async def update_contact(params: UpdateContactParams) -> Dict[str, Any]:
    """Update an existing contact in GoHighLevel"""
    client = await get_client(params.access_token)

    update_data = ContactUpdate(
        firstName=params.first_name,
        lastName=params.last_name,
        email=params.email,
        phone=params.phone,
        tags=params.tags,
        companyName=params.company_name,
        address1=params.address,
        city=params.city,
        state=params.state,
        postalCode=params.postal_code,
        customFields=(
            [{"key": k, "value": v} for k, v in (params.custom_fields or {}).items()]
            if params.custom_fields
            else None
        ),
    )

    contact = await client.update_contact(
        params.contact_id, update_data, params.location_id
    )
    return {"success": True, "contact": contact.model_dump()}


@mcp.tool()
async def delete_contact(params: DeleteContactParams) -> Dict[str, Any]:
    """Delete a contact from GoHighLevel"""
    client = await get_client(params.access_token)

    success = await client.delete_contact(params.contact_id, params.location_id)
    return {
        "success": success,
        "message": (
            "Contact deleted successfully" if success else "Failed to delete contact"
        ),
    }


@mcp.tool()
async def get_contact(params: GetContactParams) -> Dict[str, Any]:
    """Get a single contact by ID"""
    client = await get_client(params.access_token)

    contact = await client.get_contact(params.contact_id, params.location_id)
    return {"success": True, "contact": contact.model_dump()}


@mcp.tool()
async def search_contacts(params: SearchContactsParams) -> Dict[str, Any]:
    """Search contacts in a location"""
    client = await get_client(params.access_token)

    result = await client.get_contacts(
        location_id=params.location_id,
        limit=params.limit,
        skip=params.skip,
        query=params.query,
        email=params.email,
        phone=params.phone,
        tags=params.tags,
    )

    return {
        "success": True,
        "contacts": [c.model_dump() for c in result.contacts],
        "count": result.count,
        "total": result.total,
    }


@mcp.tool()
async def add_contact_tags(params: ManageTagsParams) -> Dict[str, Any]:
    """Add tags to a contact"""
    client = await get_client(params.access_token)

    contact = await client.add_contact_tags(
        params.contact_id, params.tags, params.location_id
    )
    return {"success": True, "contact": contact.model_dump()}


@mcp.tool()
async def remove_contact_tags(params: ManageTagsParams) -> Dict[str, Any]:
    """Remove tags from a contact"""
    client = await get_client(params.access_token)

    contact = await client.remove_contact_tags(
        params.contact_id, params.tags, params.location_id
    )
    return {"success": True, "contact": contact.model_dump()}


# Conversation Tools


@mcp.tool()
async def get_conversations(params: GetConversationsParams) -> Dict[str, Any]:
    """Get conversations for a location"""
    client = await get_client(params.access_token)

    result = await client.get_conversations(
        location_id=params.location_id,
        limit=params.limit,
        skip=params.skip,
        contact_id=params.contact_id,
        starred=params.starred,
        unread_only=params.unread_only,
    )

    return {
        "success": True,
        "conversations": [c.model_dump() for c in result.conversations],
        "count": result.count,
        "total": result.total,
    }


@mcp.tool()
async def get_conversation(params: GetConversationParams) -> Dict[str, Any]:
    """Get a single conversation"""
    client = await get_client(params.access_token)

    conversation = await client.get_conversation(
        params.conversation_id, params.location_id
    )
    return {"success": True, "conversation": conversation.model_dump()}


@mcp.tool()
async def create_conversation(params: CreateConversationParams) -> Dict[str, Any]:
    """Create a new conversation"""
    client = await get_client(params.access_token)

    conversation_data = ConversationCreate(
        locationId=params.location_id,
        contactId=params.contact_id,
        lastMessageType=MessageType(params.message_type) if params.message_type else None,
    )

    conversation = await client.create_conversation(conversation_data)
    return {"success": True, "conversation": conversation.model_dump()}


@mcp.tool()
async def get_messages(params: GetMessagesParams) -> Dict[str, Any]:
    """Get messages from a conversation"""
    client = await get_client(params.access_token)

    result = await client.get_messages(
        conversation_id=params.conversation_id,
        location_id=params.location_id,
        limit=params.limit,
        skip=params.skip,
    )

    return {
        "success": True,
        "messages": [m.model_dump() for m in result.messages],
        "count": result.count,
        "total": result.total,
    }


@mcp.tool()
async def send_message(params: SendMessageParams) -> Dict[str, Any]:
    """Send a message in a conversation"""
    client = await get_client(params.access_token)

    message_data = MessageCreate(
        type=params.message_type,
        contactId=params.contact_id,
        message=params.message,
        phone=params.phone,
        html=params.html,
        text=params.text,
        subject=params.subject,
        attachments=params.attachments,
    )

    message = await client.send_message(
        conversation_id=params.conversation_id,
        message=message_data,
        location_id=params.location_id,
    )

    return {"success": True, "message": message.model_dump()}


@mcp.tool()
async def update_message_status(params: UpdateMessageStatusParams) -> Dict[str, Any]:
    """Update the status of a message"""
    client = await get_client(params.access_token)

    message = await client.update_message_status(
        message_id=params.message_id,
        status=params.status,
        location_id=params.location_id,
    )

    return {"success": True, "message": message.model_dump()}


# Resources


@mcp.resource("contacts://{location_id}")
async def list_contacts_resource(location_id: str) -> str:
    """List all contacts for a location as a resource"""
    result = await ghl_client.get_contacts(location_id=location_id, limit=100)

    # Format contacts as readable text
    lines = [f"# Contacts for Location {location_id}\n"]
    lines.append(f"Total contacts: {result.total or result.count}\n")

    for contact in result.contacts:
        name = (
            contact.name
            or f"{contact.firstName or ''} {contact.lastName or ''}".strip()
            or "Unknown"
        )
        lines.append(f"\n## {name}")
        lines.append(f"- ID: {contact.id}")
        if contact.email:
            lines.append(f"- Email: {contact.email}")
        if contact.phone:
            lines.append(f"- Phone: {contact.phone}")
        if contact.tags:
            lines.append(f"- Tags: {', '.join(contact.tags)}")
        if contact.companyName:
            lines.append(f"- Company: {contact.companyName}")

    return "\n".join(lines)


@mcp.resource("contact://{location_id}/{contact_id}")
async def get_contact_resource(location_id: str, contact_id: str) -> str:
    """Get a single contact as a resource"""
    contact = await ghl_client.get_contact(contact_id, location_id)

    # Format contact as readable text
    name = (
        contact.name
        or f"{contact.firstName or ''} {contact.lastName or ''}".strip()
        or "Unknown"
    )
    lines = [f"# Contact: {name}\n"]
    lines.append(f"**ID:** {contact.id}")
    lines.append(f"**Location:** {contact.locationId}")

    if contact.email:
        lines.append(f"**Email:** {contact.email}")
    if contact.phone:
        lines.append(f"**Phone:** {contact.phone}")
    if contact.companyName:
        lines.append(f"**Company:** {contact.companyName}")
    if contact.tags:
        lines.append(f"**Tags:** {', '.join(contact.tags)}")
    if contact.source:
        lines.append(f"**Source:** {contact.source}")

    if contact.address1:
        address_parts = [contact.address1]
        if contact.city:
            address_parts.append(contact.city)
        if contact.state:
            address_parts.append(contact.state)
        if contact.postalCode:
            address_parts.append(contact.postalCode)
        lines.append(f"**Address:** {', '.join(address_parts)}")

    if contact.dateAdded:
        lines.append(f"**Added:** {contact.dateAdded}")
    if contact.lastActivity:
        lines.append(f"**Last Activity:** {contact.lastActivity}")

    return "\n".join(lines)


@mcp.resource("conversations://{location_id}")
async def list_conversations_resource(location_id: str) -> str:
    """List all conversations for a location as a resource"""
    result = await ghl_client.get_conversations(location_id=location_id, limit=100)

    # Format conversations as readable text
    lines = [f"# Conversations for Location {location_id}\n"]
    lines.append(f"Total conversations: {result.total or result.count}\n")

    for conv in result.conversations:
        contact_name = conv.contactName or conv.fullName or "Unknown"
        lines.append(f"\n## {contact_name}")
        lines.append(f"- ID: {conv.id}")
        lines.append(f"- Contact ID: {conv.contactId}")
        if conv.lastMessageBody:
            lines.append(f"- Last Message: {conv.lastMessageBody[:100]}...")
        if conv.lastMessageType:
            lines.append(f"- Last Message Type: {conv.lastMessageType}")
        if conv.unreadCount > 0:
            lines.append(f"- Unread: {conv.unreadCount}")
        if conv.starred:
            lines.append("- ⭐ Starred")

    return "\n".join(lines)


@mcp.resource("conversation://{location_id}/{conversation_id}")
async def get_conversation_resource(location_id: str, conversation_id: str) -> str:
    """Get a single conversation as a resource"""
    conversation = await ghl_client.get_conversation(conversation_id, location_id)
    messages = await ghl_client.get_messages(conversation_id, location_id, limit=50)

    # Format conversation as readable text
    contact_name = conversation.contactName or conversation.fullName or "Unknown"
    lines = [f"# Conversation with {contact_name}\n"]
    lines.append(f"**ID:** {conversation.id}")
    lines.append(f"**Contact:** {conversation.contactId}")
    lines.append(f"**Location:** {conversation.locationId}")

    if conversation.email:
        lines.append(f"**Email:** {conversation.email}")
    if conversation.phone:
        lines.append(f"**Phone:** {conversation.phone}")
    if conversation.unreadCount > 0:
        lines.append(f"**Unread Messages:** {conversation.unreadCount}")
    if conversation.starred:
        lines.append("**Status:** ⭐ Starred")

    lines.append(
        f"\n## Messages ({messages.count} of {messages.total or messages.count})\n"
    )

    for msg in messages.messages:
        direction = "→ Sent" if msg.direction == "outbound" else "← Received"
        lines.append(f"### {msg.dateAdded} {direction}")
        lines.append(f"- Type: {msg.type}")
        lines.append(f"- Status: {msg.status}")
        lines.append(f"- Message: {msg.body}")
        if msg.attachments:
            lines.append(f"- Attachments: {len(msg.attachments)}")
        lines.append("")

    return "\n".join(lines)


# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:mcp", host="0.0.0.0", port=8000, lifespan="on", reload=True)
