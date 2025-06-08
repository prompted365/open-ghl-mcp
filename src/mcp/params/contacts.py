"""Contact parameter classes for MCP tools"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


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
