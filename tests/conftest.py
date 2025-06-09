"""Pytest configuration and shared fixtures"""

import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta, timezone

from src.models.auth import TokenResponse, LocationTokenResponse
from src.models.contact import Contact
from src.models.conversation import Conversation, Message, MessageStatus


@pytest.fixture
def mock_token_response():
    """Mock OAuth token response"""
    return TokenResponse(
        access_token="mock_access_token",
        token_type="Bearer",
        expires_in=3600,
        refresh_token="mock_refresh_token",
        scope="contacts.read contacts.write",
        userId="mock_user_id",
        userType="Location",
    )


@pytest.fixture
def mock_location_token_response():
    """Mock location token response"""
    return LocationTokenResponse(
        access_token="mock_location_token",
        token_type="Bearer",
        expires_in=86400,
        refresh_token="mock_location_refresh_token",
        scope="contacts.read contacts.write",
        userId="mock_user_id",
        userType="Location",
        locationId="mock_location_id",
    )


@pytest.fixture
def mock_jwt_payload():
    """Mock JWT payload with company ID"""
    return {
        "companyId": "mock_company_id",
        "userId": "mock_user_id",
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
    }


@pytest.fixture
def mock_contact():
    """Mock contact object"""
    return Contact(
        id="mock_contact_id",
        locationId="mock_location_id",
        firstName="John",
        lastName="Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        tags=["test", "mock"],
        source="API Test",
        dateAdded="2024-01-01T00:00:00Z",
        dateUpdated="2024-01-01T00:00:00Z",
    )


@pytest.fixture
def mock_conversation():
    """Mock conversation object"""
    return Conversation(
        id="mock_conversation_id",
        locationId="mock_location_id",
        contactId="mock_contact_id",
        lastMessageDate="2024-01-01T00:00:00Z",
        type="SMS",
        unreadCount=0,
        starred=False,
        dateAdded="2024-01-01T00:00:00Z",
        dateUpdated="2024-01-01T00:00:00Z",
    )


@pytest.fixture
def mock_message():
    """Mock message object"""
    return Message(
        id="mock_message_id",
        conversationId="mock_conversation_id",
        locationId="mock_location_id",
        contactId="mock_contact_id",
        type=1,
        messageType="TYPE_SMS",
        direction="outgoing",
        status=MessageStatus.SENT,
        body="Test message",
        dateAdded="2024-01-01T00:00:00Z",
    )


@pytest.fixture
def mock_httpx_client():
    """Mock httpx client for API calls"""
    client = AsyncMock()
    response = AsyncMock()
    response.status_code = 200
    response.json = AsyncMock(return_value={})
    response.raise_for_status = Mock()
    client.request = AsyncMock(return_value=response)
    return client


@pytest.fixture
def mock_oauth_service(
    mock_token_response, mock_location_token_response, mock_jwt_payload
):
    """Mock OAuth service"""
    service = Mock()
    service.has_valid_token = Mock(return_value=True)
    service.get_token = Mock(return_value=mock_token_response)
    service.get_location_token = AsyncMock(return_value=mock_location_token_response)
    service._decode_jwt = Mock(return_value=mock_jwt_payload)
    service.token = mock_token_response
    service.location_tokens = {"mock_location_id": mock_location_token_response}
    return service
