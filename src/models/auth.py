from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """OAuth token response from GoHighLevel"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: str
    scope: str
    userType: str
    
    
class StoredToken(BaseModel):
    """Token storage model with metadata"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    scope: str
    user_type: str
    
    @classmethod
    def from_token_response(cls, response: TokenResponse) -> "StoredToken":
        """Create StoredToken from OAuth response"""
        expires_at = datetime.now().timestamp() + response.expires_in
        return cls(
            access_token=response.access_token,
            refresh_token=response.refresh_token,
            token_type=response.token_type,
            expires_at=datetime.fromtimestamp(expires_at),
            scope=response.scope,
            user_type=response.userType
        )
    
    def is_expired(self) -> bool:
        """Check if the token is expired"""
        return datetime.now() >= self.expires_at
    
    def needs_refresh(self, buffer_seconds: int = 300) -> bool:
        """Check if token needs refresh (with 5-minute buffer by default)"""
        buffer_time = datetime.now().timestamp() + buffer_seconds
        return datetime.fromtimestamp(buffer_time) >= self.expires_at