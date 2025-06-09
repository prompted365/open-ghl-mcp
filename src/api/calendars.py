"""Calendar and appointment management client for GoHighLevel API v2"""

from typing import Optional, Dict, Any
from datetime import datetime, date, timedelta
import pytz

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

    @staticmethod
    def format_datetime_with_timezone(
        dt: datetime, timezone_name: str = "America/Chicago"
    ) -> str:
        """Helper to format datetime with proper timezone for GoHighLevel API

        Args:
            dt: Datetime object (can be naive or aware)
            timezone_name: IANA timezone name (default: America/Chicago for Central Time)

        Returns:
            ISO format string with timezone offset (e.g., '2025-06-09T11:00:00-05:00')

        Common timezones:
        - 'America/Chicago' (Central)
        - 'America/New_York' (Eastern)
        - 'America/Los_Angeles' (Pacific)
        - 'America/Denver' (Mountain)
        """
        tz = pytz.timezone(timezone_name)
        if dt.tzinfo is None:
            # Naive datetime - localize it
            dt_aware = tz.localize(dt)
        else:
            # Already aware - convert to target timezone
            dt_aware = dt.astimezone(tz)
        return dt_aware.isoformat()

    # Appointment Methods

    async def get_appointments(
        self,
        contact_id: str,
        location_id: str,
    ) -> AppointmentList:
        """Get appointments for a contact

        Note: Appointments belong to contacts, not calendars.
        """
        response = await self._request(
            "GET",
            f"/contacts/{contact_id}/appointments",
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

        # The API returns a minimal response when creating appointments
        # We need to merge it with the original request data to create a complete Appointment object
        if "id" in data:
            # Successful creation - merge the response with request data
            complete_data = {
                **appointment_data,  # Original request data
                **data,  # Response data (overwrites any conflicts)
                "locationId": appointment.locationId,  # Ensure locationId is present
                "appointmentStatus": data.get(
                    "appoinmentStatus",
                    appointment_data.get("appointmentStatus", "confirmed"),
                ),  # Handle typo in API
            }
            # Remove the misspelled field if present
            complete_data.pop("appoinmentStatus", None)
            return Appointment(**complete_data)
        else:
            # If no ID in response, just return what we got (error case)
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
        # Convert dates to millisecond timestamps
        start_timestamp = int(
            datetime.combine(start_date, datetime.min.time()).timestamp() * 1000
        )

        params: Dict[str, Any] = {
            "startDate": start_timestamp,
        }

        if end_date:
            end_timestamp = int(
                datetime.combine(end_date, datetime.min.time()).timestamp() * 1000
            )
            params["endDate"] = end_timestamp
        if timezone:
            params["timezone"] = timezone

        # Note: Do NOT include locationId in params - it uses the token's location
        response = await self._request(
            "GET",
            f"/calendars/{calendar_id}/free-slots",
            params=params,
            location_id=location_id,  # This is for token selection, not query params
        )
        data = response.json()

        # The response format is different - it's organized by date
        # Example: {"2025-06-10": {"slots": [...]}}
        all_slots = []
        for date_key, date_data in data.items():
            if (
                date_key != "traceId"
                and isinstance(date_data, dict)
                and "slots" in date_data
            ):
                for slot_time in date_data.get("slots", []):
                    # Each slot is just a timestamp string like "2025-06-10T11:00:00-05:00"
                    # We need to create start and end times (assuming 30-minute slots)
                    slot_dt = datetime.fromisoformat(slot_time.replace("Z", "+00:00"))
                    end_dt = slot_dt + timedelta(minutes=30)
                    all_slots.append(
                        FreeSlot(
                            startTime=slot_time,
                            endTime=end_dt.isoformat(),
                            available=True,
                        )
                    )

        return FreeSlotsResult(
            slots=all_slots,
            date=start_date.isoformat(),
            timezone=timezone,
        )
