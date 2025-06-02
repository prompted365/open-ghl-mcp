#!/usr/bin/env python3
"""GoHighLevel MCP Server using FastMCP"""

import os
import asyncio
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .api.client import GoHighLevelClient
from .services.oauth import OAuthService
from .models.contact import Contact, ContactCreate, ContactUpdate


# Initialize FastMCP server
mcp = FastMCP(
    name="ghl-mcp-server",
    version="0.1.0",
    description="MCP server for GoHighLevel API integration",
    dependencies=["httpx", "pydantic", "python-dotenv"]
)

# Global clients
oauth_service: Optional[OAuthService] = None
ghl_client: Optional[GoHighLevelClient] = None


# Initialize on import
oauth_service = OAuthService()
ghl_client = GoHighLevelClient(oauth_service)


# Tool Models

class CreateContactParams(BaseModel):
    """Parameters for creating a contact"""
    location_id: str = Field(..., description="The location ID where the contact will be created")
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
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Custom field values")
    access_token: Optional[str] = Field(None, description="Optional access token to use instead of stored token")


class UpdateContactParams(BaseModel):
    """Parameters for updating a contact"""
    contact_id: str = Field(..., description="The contact ID to update")
    location_id: str = Field(..., description="The location ID where the contact exists")
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
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Custom field values")
    access_token: Optional[str] = Field(None, description="Optional access token to use instead of stored token")


class DeleteContactParams(BaseModel):
    """Parameters for deleting a contact"""
    contact_id: str = Field(..., description="The contact ID to delete")
    location_id: str = Field(..., description="The location ID where the contact exists")
    access_token: Optional[str] = Field(None, description="Optional access token to use instead of stored token")


class SearchContactsParams(BaseModel):
    """Parameters for searching contacts"""
    location_id: str = Field(..., description="The location ID to search contacts in")
    query: Optional[str] = Field(None, description="Search query string")
    email: Optional[str] = Field(None, description="Filter by email address")
    phone: Optional[str] = Field(None, description="Filter by phone number")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    limit: int = Field(100, description="Number of results to return", ge=1, le=100)
    skip: int = Field(0, description="Number of results to skip", ge=0)
    access_token: Optional[str] = Field(None, description="Optional access token to use instead of stored token")


class GetContactParams(BaseModel):
    """Parameters for getting a single contact"""
    contact_id: str = Field(..., description="The contact ID to retrieve")
    location_id: str = Field(..., description="The location ID where the contact exists")
    access_token: Optional[str] = Field(None, description="Optional access token to use instead of stored token")


class ManageTagsParams(BaseModel):
    """Parameters for managing contact tags"""
    contact_id: str = Field(..., description="The contact ID")
    location_id: str = Field(..., description="The location ID where the contact exists")
    tags: List[str] = Field(..., description="Tags to add or remove")
    access_token: Optional[str] = Field(None, description="Optional access token to use instead of stored token")


# Helper function to get client with optional token override
async def get_client(access_token: Optional[str] = None) -> GoHighLevelClient:
    """Get GHL client with optional token override"""
    if access_token:
        # Create a temporary client with the provided token
        temp_oauth = OAuthService()
        # Override the get_valid_token method to return the provided token
        temp_oauth.get_valid_token = lambda: access_token
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
        customFields=[{"key": k, "value": v} for k, v in (params.custom_fields or {}).items()]
    )
    
    contact = await client.create_contact(contact_data)
    return {
        "success": True,
        "contact": contact.model_dump()
    }


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
        customFields=[{"key": k, "value": v} for k, v in (params.custom_fields or {}).items()] if params.custom_fields else None
    )
    
    contact = await client.update_contact(params.contact_id, update_data, params.location_id)
    return {
        "success": True,
        "contact": contact.model_dump()
    }


@mcp.tool()
async def delete_contact(params: DeleteContactParams) -> Dict[str, Any]:
    """Delete a contact from GoHighLevel"""
    client = await get_client(params.access_token)
    
    success = await client.delete_contact(params.contact_id, params.location_id)
    return {
        "success": success,
        "message": "Contact deleted successfully" if success else "Failed to delete contact"
    }


@mcp.tool()
async def get_contact(params: GetContactParams) -> Dict[str, Any]:
    """Get a single contact by ID"""
    client = await get_client(params.access_token)
    
    contact = await client.get_contact(params.contact_id, params.location_id)
    return {
        "success": True,
        "contact": contact.model_dump()
    }


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
        tags=params.tags
    )
    
    return {
        "success": True,
        "contacts": [c.model_dump() for c in result.contacts],
        "count": result.count,
        "total": result.total
    }


@mcp.tool()
async def add_contact_tags(params: ManageTagsParams) -> Dict[str, Any]:
    """Add tags to a contact"""
    client = await get_client(params.access_token)
    
    contact = await client.add_contact_tags(params.contact_id, params.tags, params.location_id)
    return {
        "success": True,
        "contact": contact.model_dump()
    }


@mcp.tool()
async def remove_contact_tags(params: ManageTagsParams) -> Dict[str, Any]:
    """Remove tags from a contact"""
    client = await get_client(params.access_token)
    
    contact = await client.remove_contact_tags(params.contact_id, params.tags, params.location_id)
    return {
        "success": True,
        "contact": contact.model_dump()
    }


# Resources

@mcp.resource("contacts://{location_id}")
async def list_contacts_resource(location_id: str) -> str:
    """List all contacts for a location as a resource"""
    result = await ghl_client.get_contacts(location_id=location_id, limit=100)
    
    # Format contacts as readable text
    lines = [f"# Contacts for Location {location_id}\n"]
    lines.append(f"Total contacts: {result.total or result.count}\n")
    
    for contact in result.contacts:
        name = contact.name or f"{contact.firstName or ''} {contact.lastName or ''}".strip() or "Unknown"
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
    name = contact.name or f"{contact.firstName or ''} {contact.lastName or ''}".strip() or "Unknown"
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


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:mcp",
        host="0.0.0.0",
        port=8000,
        lifespan="on",
        reload=True
    )