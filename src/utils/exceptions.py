"""Custom exceptions for GoHighLevel MCP Server"""

from typing import Optional, Dict, Any
import httpx


class GoHighLevelError(Exception):
    """Base exception for GoHighLevel API errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(GoHighLevelError):
    """Raised when authentication fails"""

    pass


class RateLimitError(GoHighLevelError):
    """Raised when rate limit is exceeded"""

    pass


class ResourceNotFoundError(GoHighLevelError):
    """Raised when a resource is not found"""

    pass


class ValidationError(GoHighLevelError):
    """Raised when request validation fails"""

    pass


class DuplicateResourceError(GoHighLevelError):
    """Raised when attempting to create a duplicate resource"""

    pass


def handle_api_error(response: httpx.Response) -> None:
    """Convert HTTP errors to appropriate exceptions

    This preserves the original error details from the API while
    providing structured exception types for better handling.
    """
    try:
        error_data = response.json()
    except Exception:
        error_data = {"message": response.text}

    status_code = response.status_code
    message = error_data.get("message", f"API error: {status_code}")

    # Map status codes to specific exceptions
    if status_code == 401:
        raise AuthenticationError(message, status_code, error_data)
    elif status_code == 403:
        raise AuthenticationError(f"Forbidden: {message}", status_code, error_data)
    elif status_code == 404:
        raise ResourceNotFoundError(message, status_code, error_data)
    elif status_code == 422:
        raise ValidationError(message, status_code, error_data)
    elif status_code == 429:
        raise RateLimitError(message, status_code, error_data)
    elif status_code == 400:
        # Check for duplicate contact error
        if "duplicate" in message.lower() or "already exists" in message.lower():
            raise DuplicateResourceError(message, status_code, error_data)
        raise ValidationError(message, status_code, error_data)
    else:
        raise GoHighLevelError(message, status_code, error_data)
