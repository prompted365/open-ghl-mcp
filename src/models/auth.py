from typing import Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, field_serializer


class TokenResponse(BaseModel):
    """OAuth token response from GoHighLevel"""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: str
    scope: str
    userType: str
    userId: Optional[str] = None


class LocationTokenResponse(BaseModel):
    """Location token response from GoHighLevel"""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str
    userId: str
    userType: str = "Location"
    locationId: str


class StoredToken(BaseModel):
    """Token storage model with metadata"""

    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    scope: str
    user_type: str

    @field_serializer("expires_at")
    def serialize_expires_at(self, expires_at: datetime, _info):
        """Serialize datetime to ISO format"""
        return expires_at.isoformat()

    @classmethod
    def from_token_response(cls, response: TokenResponse) -> "StoredToken":
        """Create StoredToken from OAuth response"""
        expires_at = datetime.now(timezone.utc).timestamp() + response.expires_in
        return cls(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            token_type=response.token_type,
            expires_at=datetime.fromtimestamp(expires_at, timezone.utc),
            scope=response.scope,
            user_type=response.userType,
        )

    def is_expired(self) -> bool:
        """Check if the token is expired"""
        now = datetime.now(timezone.utc)
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return now >= expires_at

    def needs_refresh(self, buffer_seconds: int = 300) -> bool:
        """Check if token needs refresh (with 5-minute buffer by default)"""
        # Ensure we're always comparing timezone-aware datetimes
        now = datetime.now(timezone.utc)
        buffer_time = now + timedelta(seconds=buffer_seconds)

        # Make sure expires_at is timezone-aware
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        return buffer_time >= expires_at
