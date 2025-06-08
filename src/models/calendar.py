"""Calendar and appointment models for GoHighLevel API v2"""

from datetime import datetime
from typing import Optional, List, Union, Dict, Any
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

    # Timestamps (from API)
    dateAdded: Optional[Union[datetime, str]] = Field(
        None, description="Creation timestamp", alias="createdAt"
    )
    dateUpdated: Optional[Union[datetime, str]] = Field(
        None, description="Last update timestamp", alias="updatedAt"
    )

    # Legacy timestamp fields (for backward compatibility)
    createdAt: Optional[Union[datetime, str]] = Field(
        None, description="Creation timestamp"
    )
    updatedAt: Optional[Union[datetime, str]] = Field(
        None, description="Last update timestamp"
    )

    @field_validator(
        "startTime",
        "endTime",
        "createdAt",
        "updatedAt",
        "dateAdded",
        "dateUpdated",
        mode="before",
    )
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
    """Calendar model - comprehensive model supporting both list and single calendar responses"""

    # Core required fields
    id: str = Field(..., description="Calendar ID")
    name: str = Field(..., description="Calendar name")
    locationId: str = Field(..., description="Location ID")

    # Calendar configuration
    calendarType: Optional[str] = Field(
        None, description="Calendar type: round_robin, event, personal"
    )
    eventType: Optional[str] = Field(None, description="Event type")
    eventTitle: Optional[str] = Field(None, description="Default event title template")
    eventColor: Optional[str] = Field(None, description="Event color hex code")
    description: Optional[str] = Field(None, description="Calendar description")

    # URL and widget configuration
    slug: Optional[str] = Field(None, description="Calendar URL slug")
    widgetSlug: Optional[str] = Field(None, description="Widget URL slug")
    widgetType: Optional[str] = Field(None, description="Widget type")

    # Slot and timing configuration
    slotDuration: Optional[int] = Field(None, description="Slot duration in minutes")
    slotDurationUnit: Optional[str] = Field(
        None, description="Slot duration unit (mins, hours)"
    )
    slotInterval: Optional[int] = Field(None, description="Slot interval in minutes")
    slotIntervalUnit: Optional[str] = Field(None, description="Slot interval unit")
    slotBuffer: Optional[int] = Field(None, description="Buffer time between slots")
    slotBufferUnit: Optional[str] = Field(None, description="Buffer time unit")
    appointmentPerSlot: Optional[int] = Field(
        None, description="Appointments per slot", alias="appoinmentPerSlot"
    )
    appointmentPerDay: Optional[Union[int, str]] = Field(
        None, description="Appointments per day", alias="appoinmentPerDay"
    )

    # Booking configuration
    isActive: Optional[bool] = Field(None, description="Is calendar active")
    autoConfirm: Optional[bool] = Field(None, description="Auto-confirm appointments")
    stickyContact: Optional[bool] = Field(None, description="Sticky contact setting")
    allowReschedule: Optional[bool] = Field(
        None, description="Allow appointment rescheduling"
    )
    allowCancellation: Optional[bool] = Field(
        None, description="Allow appointment cancellation"
    )

    # Team and assignment
    shouldAssignContactToTeamMember: Optional[bool] = Field(
        None, description="Assign contact to team member"
    )
    shouldSkipAssigningContactForExisting: Optional[bool] = Field(
        None, description="Skip assignment for existing contacts"
    )
    shouldSendAlertEmailsToAssignedMember: Optional[bool] = Field(
        None, description="Send alerts to assigned member"
    )

    # Notifications and integrations
    googleInvitationEmails: Optional[bool] = Field(
        None, description="Send Google invitation emails"
    )

    # Booking restrictions
    allowBookingAfter: Optional[int] = Field(
        None, description="Allow booking after X units"
    )
    allowBookingAfterUnit: Optional[str] = Field(
        None, description="Unit for booking after restriction"
    )
    allowBookingFor: Optional[int] = Field(
        None, description="Allow booking for X units ahead"
    )
    allowBookingForUnit: Optional[str] = Field(
        None, description="Unit for booking ahead restriction"
    )
    preBufferUnit: Optional[str] = Field(None, description="Pre-buffer time unit")

    # Form and submission configuration
    formId: Optional[str] = Field(None, description="Associated form ID")
    formSubmitType: Optional[str] = Field(None, description="Form submission type")
    formSubmitRedirectUrl: Optional[str] = Field(
        None, description="Form submit redirect URL"
    )
    formSubmitThanksMessage: Optional[str] = Field(
        None, description="Form thank you message"
    )

    # Guest and consent
    guestType: Optional[str] = Field(
        None, description="Guest information collection type"
    )
    consentLabel: Optional[str] = Field(None, description="Consent checkbox label")

    # Advanced features
    notes: Optional[str] = Field(None, description="Default appointment notes template")
    pixelId: Optional[str] = Field(None, description="Tracking pixel ID")
    calendarCoverImage: Optional[str] = Field(
        None, description="Calendar cover image URL"
    )
    enableRecurring: Optional[bool] = Field(
        None, description="Enable recurring appointments"
    )
    isLivePaymentMode: Optional[bool] = Field(
        None, description="Live payment mode enabled"
    )

    # Group and team configuration
    groupId: Optional[str] = Field(None, description="Calendar group ID")

    # Complex nested objects (stored as generic dicts/lists for flexibility)
    teamMembers: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Team member configurations"
    )
    openHours: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Calendar availability hours"
    )
    availabilities: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Custom availability rules"
    )
    notifications: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="Notification configurations"
    )
    recurring: Optional[Dict[str, Any]] = Field(
        None, description="Recurring appointment settings"
    )
    lookBusyConfig: Optional[Dict[str, Any]] = Field(
        None, description="Look busy configuration"
    )

    # Legacy/deprecated duration field
    eventDuration: Optional[int] = Field(
        None, description="Legacy event duration field"
    )

    # Timestamps - optional since they might not always be present
    createdAt: Optional[Union[datetime, str]] = Field(
        None, description="Creation timestamp"
    )
    updatedAt: Optional[Union[datetime, str]] = Field(
        None, description="Last update timestamp"
    )

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
