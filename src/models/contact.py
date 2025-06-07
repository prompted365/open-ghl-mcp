from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ContactPhone(BaseModel):
    """Phone number for a contact"""

    phone: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None


class ContactEmail(BaseModel):
    """Email address for a contact"""

    email: Optional[str] = None
    label: Optional[str] = None


class ContactAddress(BaseModel):
    """Address for a contact"""

    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = Field(default="US")
    postalCode: Optional[str] = None


class Contact(BaseModel):
    """GoHighLevel Contact model"""

    id: Optional[str] = None
    locationId: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = Field(default="US")
    postalCode: Optional[str] = None
    website: Optional[str] = None
    timezone: Optional[str] = None
    dnd: bool = False
    dndSettings: Optional[Dict[str, Any]] = None
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = None
    customFields: Optional[List[Dict[str, Any]]] = None
    dateAdded: Optional[datetime] = None
    dateUpdated: Optional[datetime] = None
    lastActivity: Optional[datetime] = None

    # Additional fields from API
    companyName: Optional[str] = None
    assignedTo: Optional[str] = None
    followers: Optional[List[str]] = None
    additionalEmails: Optional[List[ContactEmail]] = None
    additionalPhones: Optional[List[ContactPhone]] = None

    model_config = {"populate_by_name": True}


class ContactCreate(BaseModel):
    """Model for creating a contact"""

    locationId: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    website: Optional[str] = None
    timezone: Optional[str] = None
    dnd: bool = False
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    customFields: Optional[List[Dict[str, Any]]] = None
    companyName: Optional[str] = None


class ContactUpdate(BaseModel):
    """Model for updating a contact"""

    firstName: Optional[str] = None
    lastName: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    website: Optional[str] = None
    timezone: Optional[str] = None
    dnd: Optional[bool] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    customFields: Optional[List[Dict[str, Any]]] = None
    companyName: Optional[str] = None


class ContactList(BaseModel):
    """Response model for contact list"""

    contacts: List[Contact]
    count: int
    total: Optional[int] = None


class ContactSearchParams(BaseModel):
    """Parameters for searching contacts"""

    locationId: str
    query: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=100)
    skip: int = Field(default=0, ge=0)
    email: Optional[str] = None
    phone: Optional[str] = None
    tags: Optional[List[str]] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
