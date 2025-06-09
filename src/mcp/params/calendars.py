"""Calendar parameter classes for MCP tools"""

from typing import Optional
from pydantic import BaseModel, Field


class GetAppointmentsParams(BaseModel):
    """Parameters for getting appointments for a contact"""

    contact_id: str = Field(..., description="The contact ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetAppointmentParams(BaseModel):
    """Parameters for getting a single appointment"""

    appointment_id: str = Field(..., description="The appointment ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class CreateAppointmentParams(BaseModel):
    """Parameters for creating an appointment"""

    location_id: str = Field(..., description="The location ID")
    calendar_id: str = Field(..., description="The calendar ID")
    contact_id: str = Field(..., description="The contact ID")
    start_time: str = Field(
        ...,
        description="Start time in timezone-aware ISO 8601 format (e.g., '2025-06-09T11:00:00-05:00' for 11 AM Central Time). Include timezone offset to avoid 'slot no longer available' errors",
    )
    end_time: str = Field(
        ...,
        description="End time in timezone-aware ISO 8601 format (e.g., '2025-06-09T11:30:00-05:00' for 11:30 AM Central Time). Include timezone offset to avoid 'slot no longer available' errors",
    )
    title: Optional[str] = Field(None, description="Appointment title")
    appointment_status: Optional[str] = Field(None, description="Appointment status")
    assigned_user_id: Optional[str] = Field(None, description="Assigned user ID")
    notes: Optional[str] = Field(None, description="Appointment notes")
    address: Optional[str] = Field(None, description="Appointment address")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class UpdateAppointmentParams(BaseModel):
    """Parameters for updating an appointment"""

    appointment_id: str = Field(..., description="The appointment ID")
    location_id: str = Field(..., description="The location ID")
    start_time: Optional[str] = Field(None, description="Start time (ISO 8601 format)")
    end_time: Optional[str] = Field(None, description="End time (ISO 8601 format)")
    title: Optional[str] = Field(None, description="Appointment title")
    appointment_status: Optional[str] = Field(None, description="Appointment status")
    assigned_user_id: Optional[str] = Field(None, description="Assigned user ID")
    notes: Optional[str] = Field(None, description="Appointment notes")
    address: Optional[str] = Field(None, description="Appointment address")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class DeleteAppointmentParams(BaseModel):
    """Parameters for deleting an appointment"""

    appointment_id: str = Field(..., description="The appointment ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetCalendarsParams(BaseModel):
    """Parameters for getting calendars"""

    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetCalendarParams(BaseModel):
    """Parameters for getting a single calendar"""

    calendar_id: str = Field(..., description="The calendar ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetFreeSlotsParams(BaseModel):
    """Parameters for getting free time slots"""

    calendar_id: str = Field(..., description="The calendar ID")
    location_id: str = Field(..., description="The location ID")
    start_date: str = Field(
        ..., description="Start date (YYYY-MM-DD). Example: '2025-06-09'"
    )
    end_date: Optional[str] = Field(
        None,
        description="End date (YYYY-MM-DD). IMPORTANT: Provide end_date for better results - without it, the API may return limited or no slots. Example: '2025-06-10'",
    )
    timezone: Optional[str] = Field(
        None,
        description="Timezone for the slots (e.g., 'America/Chicago'). If not provided, uses the calendar's default timezone",
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )
