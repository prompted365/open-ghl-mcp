"""Calendar and appointment models for GoHighLevel API v2"""

from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class AppointmentStatus(str, Enum):
    """Appointment status values"""

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    SHOWED = "showed"
    NO_SHOW = "no_show"
    INVALID = "invalid"


class MeetingLocationType(str, Enum):
    """Meeting location type values"""

    PHYSICAL = "physical"
    PHONE = "phone"
    ZOOM = "zoom"
    GOOGLE_MEET = "google_meet"
    CUSTOM = "custom"


class CalendarType(str, Enum):
    """Calendar type values"""

    ROUND_ROBIN = "round_robin"
    INDIVIDUAL = "individual"
    COLLECTIVE = "collective"


class AppointmentCreate(BaseModel):
    """Model for creating an appointment"""

    calendarId: str = Field(
        ..., description="Calendar ID where the appointment will be created"
    )
    locationId: str = Field(..., description="Location ID")
    contactId: str = Field(
        ..., description="Contact ID associated with the appointment"
    )
    startTime: Union[datetime, str] = Field(..., description="Appointment start time")
    endTime: Optional[Union[datetime, str]] = Field(
        None, description="Appointment end time"
    )
    title: Optional[str] = Field(None, description="Appointment title/subject")
    meetingLocationType: Optional[MeetingLocationType] = Field(
        None, description="Meeting location type"
    )
    appointmentStatus: Optional[AppointmentStatus] = Field(
        default=AppointmentStatus.CONFIRMED, description="Appointment status"
    )
    assignedUserId: Optional[str] = Field(
        None, description="User ID of the assigned user"
    )
    notes: Optional[str] = Field(None, description="Appointment notes")
    address: Optional[str] = Field(None, description="Physical meeting address")
    ignoreDateRange: Optional[bool] = Field(
        None, description="Ignore date range restrictions"
    )
    toNotify: Optional[bool] = Field(None, description="Send notifications")

    @field_validator("startTime", "endTime", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    return datetime.fromisoformat(v)
                else:
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                return None
        return v


class AppointmentUpdate(BaseModel):
    """Model for updating an appointment"""

    startTime: Optional[Union[datetime, str]] = Field(
        None, description="Appointment start time"
    )
    endTime: Optional[Union[datetime, str]] = Field(
        None, description="Appointment end time"
    )
    title: Optional[str] = Field(None, description="Appointment title/subject")
    meetingLocationType: Optional[MeetingLocationType] = Field(
        None, description="Meeting location type"
    )
    appointmentStatus: Optional[AppointmentStatus] = Field(
        None, description="Appointment status"
    )
    assignedUserId: Optional[str] = Field(
        None, description="User ID of the assigned user"
    )
    notes: Optional[str] = Field(None, description="Appointment notes")
    address: Optional[str] = Field(None, description="Physical meeting address")
    toNotify: Optional[bool] = Field(None, description="Send notifications")

    @field_validator("startTime", "endTime", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    return datetime.fromisoformat(v)
                else:
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                return None
        return v


class Appointment(BaseModel):
    """Complete appointment model from API response"""

    # Core fields
    id: str = Field(..., description="Appointment ID")
    calendarId: str = Field(..., description="Calendar ID")
    locationId: str = Field(..., description="Location ID")
    contactId: str = Field(..., description="Contact ID")

    # Scheduling
    startTime: Union[datetime, str] = Field(..., description="Appointment start time")
    endTime: Optional[Union[datetime, str]] = Field(
        None, description="Appointment end time"
    )
    title: Optional[str] = Field(None, description="Appointment title/subject")

    # Meeting details
    meetingLocationType: Optional[MeetingLocationType] = Field(
        None, description="Meeting location type"
    )
    appointmentStatus: AppointmentStatus = Field(..., description="Appointment status")
    assignedUserId: Optional[str] = Field(
        None, description="User ID of the assigned user"
    )
    notes: Optional[str] = Field(None, description="Appointment notes")
    address: Optional[str] = Field(None, description="Physical meeting address")

    # Timestamps
    createdAt: Union[datetime, str] = Field(..., description="Creation timestamp")
    updatedAt: Union[datetime, str] = Field(..., description="Last update timestamp")

    @field_validator("startTime", "endTime", "createdAt", "updatedAt", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    return datetime.fromisoformat(v)
                else:
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                return None
        return v

    # Additional fields that might be in the API response
    calendarEventId: Optional[str] = Field(None, description="Calendar event ID")
    ignoreDateRange: Optional[bool] = Field(
        None, description="Ignore date range restrictions"
    )
    toNotify: Optional[bool] = Field(None, description="Send notifications")


class Calendar(BaseModel):
    """Calendar model"""

    id: str = Field(..., description="Calendar ID")
    name: str = Field(..., description="Calendar name")
    locationId: str = Field(..., description="Location ID")
    calendarType: Optional[CalendarType] = Field(None, description="Calendar type")
    eventTitle: Optional[str] = Field(None, description="Default event title")
    eventDuration: Optional[int] = Field(
        None, description="Default event duration in minutes"
    )
    description: Optional[str] = Field(None, description="Calendar description")
    slug: Optional[str] = Field(None, description="Calendar URL slug")
    widgetSlug: Optional[str] = Field(None, description="Widget URL slug")
    isActive: Optional[bool] = Field(None, description="Is calendar active")

    # Timestamps
    createdAt: Union[datetime, str] = Field(..., description="Creation timestamp")
    updatedAt: Union[datetime, str] = Field(..., description="Last update timestamp")

    @field_validator("createdAt", "updatedAt", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    return datetime.fromisoformat(v)
                else:
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                return None
        return v


class AppointmentList(BaseModel):
    """Result model for appointment list"""

    appointments: List[Appointment] = Field(
        default_factory=list, description="List of appointments"
    )
    count: int = Field(..., description="Count of appointments in this response")
    total: Optional[int] = Field(None, description="Total count of appointments")


class CalendarList(BaseModel):
    """Result model for calendar list"""

    calendars: List[Calendar] = Field(
        default_factory=list, description="List of calendars"
    )
    count: int = Field(..., description="Count of calendars in this response")
    total: Optional[int] = Field(None, description="Total count of calendars")


class FreeSlot(BaseModel):
    """Free time slot model"""

    startTime: Union[datetime, str] = Field(..., description="Slot start time")
    endTime: Union[datetime, str] = Field(..., description="Slot end time")
    available: bool = Field(..., description="Is slot available")

    @field_validator("startTime", "endTime", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    return datetime.fromisoformat(v)
                else:
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                return None
        return v


class FreeSlotsResult(BaseModel):
    """Result model for free slots"""

    slots: List[FreeSlot] = Field(
        default_factory=list, description="List of free slots"
    )
    date: str = Field(..., description="Date for the slots")
    timezone: Optional[str] = Field(None, description="Timezone for the slots")
