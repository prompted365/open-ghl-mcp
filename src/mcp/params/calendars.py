"""Calendar parameter classes for MCP tools"""

from typing import Optional
from pydantic import BaseModel, Field


class GetAppointmentsParams(BaseModel):
    """Parameters for getting appointments"""

    calendar_id: str = Field(..., description="The calendar ID")
    location_id: str = Field(..., description="The location ID")
    limit: int = Field(100, description="Number of results to return", ge=1, le=100)
    skip: int = Field(0, description="Number of results to skip", ge=0)
    start_date: Optional[str] = Field(
        None, description="Start date filter (YYYY-MM-DD)"
    )
    end_date: Optional[str] = Field(None, description="End date filter (YYYY-MM-DD)")
    user_id: Optional[str] = Field(None, description="Filter by user ID")
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
    start_time: str = Field(..., description="Start time (ISO 8601 format)")
    end_time: str = Field(..., description="End time (ISO 8601 format)")
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
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    timezone: Optional[str] = Field(None, description="Timezone for the slots")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )
