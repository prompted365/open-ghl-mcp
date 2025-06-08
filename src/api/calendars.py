"""Calendar and appointment management client for GoHighLevel API v2"""

from typing import Optional
from datetime import datetime, date

from .base import BaseGoHighLevelClient
from ..models.calendar import (
    Appointment,
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentList,
    Calendar,
    CalendarList,
    FreeSlot,
    FreeSlotsResult,
)


class CalendarsClient(BaseGoHighLevelClient):
    """Client for calendar and appointment endpoints"""

    # Appointment Methods

    async def get_appointments(
        self,
        calendar_id: str,
        location_id: str,
        limit: int = 100,
        skip: int = 0,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        user_id: Optional[str] = None,
    ) -> AppointmentList:
        """Get appointments for a calendar"""
        params = {"locationId": location_id, "calendarId": calendar_id, "limit": limit}

        if skip > 0:
            params["skip"] = skip
        if start_date:
            params["startTime"] = start_date.isoformat()
        if end_date:
            params["endTime"] = end_date.isoformat()
        if user_id:
            params["userId"] = user_id

        response = await self._request(
            "GET",
            "/calendars/events",
            params=params,
            location_id=location_id,
        )
        data = response.json()
        return AppointmentList(
            appointments=[Appointment(**a) for a in data.get("events", [])],
            count=len(data.get("events", [])),
            total=data.get("total"),
        )

    async def get_appointment(
        self, appointment_id: str, location_id: str
    ) -> Appointment:
        """Get a specific appointment"""
        response = await self._request(
            "GET",
            f"/calendars/events/appointments/{appointment_id}",
            location_id=location_id,
        )
        data = response.json()
        return Appointment(**data.get("appointment", data))

    async def create_appointment(self, appointment: AppointmentCreate) -> Appointment:
        """Create a new appointment"""
        # Convert datetime objects to ISO strings for the API
        appointment_data = appointment.model_dump(exclude_none=True)

        # Handle datetime serialization
        if "startTime" in appointment_data and isinstance(
            appointment_data["startTime"], datetime
        ):
            appointment_data["startTime"] = appointment_data["startTime"].isoformat()
        if "endTime" in appointment_data and isinstance(
            appointment_data["endTime"], datetime
        ):
            appointment_data["endTime"] = appointment_data["endTime"].isoformat()

        response = await self._request(
            "POST",
            "/calendars/events/appointments",
            json=appointment_data,
            location_id=appointment.locationId,
        )
        data = response.json()
        return Appointment(**data.get("appointment", data))

    async def update_appointment(
        self, appointment_id: str, updates: AppointmentUpdate, location_id: str
    ) -> Appointment:
        """Update an existing appointment"""
        # Convert datetime objects to ISO strings for the API
        update_data = updates.model_dump(exclude_none=True)

        # Handle datetime serialization
        if "startTime" in update_data and isinstance(
            update_data["startTime"], datetime
        ):
            update_data["startTime"] = update_data["startTime"].isoformat()
        if "endTime" in update_data and isinstance(update_data["endTime"], datetime):
            update_data["endTime"] = update_data["endTime"].isoformat()

        response = await self._request(
            "PUT",
            f"/calendars/events/appointments/{appointment_id}",
            json=update_data,
            location_id=location_id,
        )
        data = response.json()
        return Appointment(**data.get("appointment", data))

    async def delete_appointment(self, appointment_id: str, location_id: str) -> bool:
        """Delete an appointment"""
        response = await self._request(
            "DELETE", f"/calendars/events/{appointment_id}", location_id=location_id
        )
        return response.status_code == 200

    # Calendar Methods

    async def get_calendars(self, location_id: str) -> CalendarList:
        """Get all calendars for a location"""
        response = await self._request(
            "GET",
            "/calendars/",
            params={"locationId": location_id},
            location_id=location_id,
        )
        data = response.json()
        return CalendarList(
            calendars=[Calendar(**c) for c in data.get("calendars", [])],
            count=len(data.get("calendars", [])),
            total=data.get("total"),
        )

    async def get_calendar(self, calendar_id: str, location_id: str) -> Calendar:
        """Get a specific calendar"""
        response = await self._request(
            "GET", f"/calendars/{calendar_id}", location_id=location_id
        )
        data = response.json()
        return Calendar(**data.get("calendar", data))

    async def get_free_slots(
        self,
        calendar_id: str,
        location_id: str,
        start_date: date,
        end_date: Optional[date] = None,
        timezone: Optional[str] = None,
    ) -> FreeSlotsResult:
        """Get available time slots for a calendar"""
        params = {
            "calendarId": calendar_id,
            "startDate": start_date.isoformat(),
        }

        if end_date:
            params["endDate"] = end_date.isoformat()
        if timezone:
            params["timezone"] = timezone

        response = await self._request(
            "GET",
            f"/calendars/{calendar_id}/free-slots",
            params=params,
            location_id=location_id,
        )
        data = response.json()
        return FreeSlotsResult(
            slots=[FreeSlot(**s) for s in data.get("slots", [])],
            date=data.get("date", start_date.isoformat()),
            timezone=data.get("timezone"),
        )
