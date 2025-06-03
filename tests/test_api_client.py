"""Unit tests for GoHighLevel API client"""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from src.api.client import GoHighLevelClient
from src.models.contact import ContactCreate
from src.models.conversation import MessageCreate, MessageType
from src.utils.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    DuplicateResourceError,
)


class TestGoHighLevelClient:
    """Test GoHighLevel API client"""

    @pytest.fixture
    def mock_oauth_service(self):
        """Create mock OAuth service"""
        service = Mock()
        service.get_valid_token = AsyncMock(return_value="agency_token")
        service.get_location_token = AsyncMock(return_value="location_token")
        return service

    @pytest.fixture
    def client(self, mock_oauth_service):
        """Create API client instance"""
        return GoHighLevelClient(mock_oauth_service)

    @pytest.fixture
    def mock_response(self):
        """Create a mock response"""
        response = Mock()
        response.status_code = 200
        response.json = Mock(return_value={})
        response.raise_for_status = Mock()
        return response

    @pytest.mark.asyncio
    async def test_get_headers_agency_token(self, client):
        """Test getting headers with agency token"""
        headers = await client._get_headers()

        assert headers["Authorization"] == "Bearer agency_token"
        assert headers["Version"] == "2021-07-28"
        assert headers["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_get_headers_location_token(self, client):
        """Test getting headers with location token"""
        headers = await client._get_headers("test_location")

        assert headers["Authorization"] == "Bearer location_token"
        client.oauth_service.get_location_token.assert_called_once_with("test_location")

    @pytest.mark.asyncio
    async def test_request_success(self, client, mock_response):
        """Test successful API request"""
        with patch.object(client.client, "request", return_value=mock_response):
            response = await client._request("GET", "/test")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_request_authentication_error(self, client):
        """Test API request with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json = Mock(return_value={"message": "Unauthorized"})

        with patch.object(client.client, "request", return_value=mock_response):
            with pytest.raises(AuthenticationError) as exc_info:
                await client._request("GET", "/test")

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_request_not_found_error(self, client):
        """Test API request with not found error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json = Mock(return_value={"message": "Not found"})

        with patch.object(client.client, "request", return_value=mock_response):
            with pytest.raises(ResourceNotFoundError) as exc_info:
                await client._request("GET", "/test")

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_get_contacts(self, client, mock_contact):
        """Test getting contacts"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(
            return_value={"contacts": [mock_contact.model_dump()], "total": 1}
        )

        with patch.object(client.client, "request", return_value=mock_response):
            result = await client.get_contacts("test_location", limit=10)

        assert len(result.contacts) == 1
        assert result.contacts[0].id == mock_contact.id
        assert result.total == 1

    @pytest.mark.asyncio
    async def test_get_contacts_skip_parameter(self, client):
        """Test skip parameter handling in get_contacts"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={"contacts": [], "total": 0})

        with patch.object(
            client.client, "request", return_value=mock_response
        ) as mock_request:
            # Test with skip=0 (should be omitted)
            await client.get_contacts("test_location", skip=0)
            call_args = mock_request.call_args[1]["params"]
            assert "skip" not in call_args

            # Test with skip>0 (should be included)
            await client.get_contacts("test_location", skip=10)
            call_args = mock_request.call_args[1]["params"]
            assert call_args["skip"] == 10

    @pytest.mark.asyncio
    async def test_create_contact(self, client, mock_contact):
        """Test creating a contact"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json = Mock(return_value={"contact": mock_contact.model_dump()})

        contact_data = ContactCreate(
            locationId="test_location",
            firstName="John",
            lastName="Doe",
            email="john@example.com",
        )

        with patch.object(client.client, "request", return_value=mock_response):
            result = await client.create_contact(contact_data)

        assert result.id == mock_contact.id
        assert result.firstName == "John"

    @pytest.mark.asyncio
    async def test_create_contact_duplicate_error(self, client):
        """Test creating duplicate contact"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json = Mock(
            return_value={"message": "Contact already exists with this email"}
        )

        contact_data = ContactCreate(
            locationId="test_location", email="existing@example.com"
        )

        with patch.object(client.client, "request", return_value=mock_response):
            with pytest.raises(DuplicateResourceError) as exc_info:
                await client.create_contact(contact_data)

        assert "already exists" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_send_message_email(self, client):
        """Test sending email message"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(
            return_value={"conversationId": "conv123", "messageId": "msg123"}
        )

        message_data = MessageCreate(
            type=MessageType.EMAIL,
            conversationId="conv123",
            contactId="contact123",
            html="<p>Test email</p>",
            subject="Test Subject",
            text="Test email",
        )

        with patch.object(
            client.client, "request", return_value=mock_response
        ) as mock_request:
            result = await client.send_message("conv123", message_data, "test_location")

        assert result.conversationId == "conv123"
        assert result.id == "msg123"

        # Verify email fields are sent correctly
        sent_data = mock_request.call_args[1]["json"]
        assert sent_data["html"] == "<p>Test email</p>"
        assert sent_data["subject"] == "Test Subject"
        assert "message" not in sent_data  # Email doesn't use message field

    @pytest.mark.asyncio
    async def test_send_message_sms(self, client):
        """Test sending SMS message"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(
            return_value={"conversationId": "conv123", "messageId": "msg123"}
        )

        message_data = MessageCreate(
            type=MessageType.SMS,
            conversationId="conv123",
            contactId="contact123",
            message="Test SMS",
            phone="+1234567890",
        )

        with patch.object(
            client.client, "request", return_value=mock_response
        ) as mock_request:
            result = await client.send_message("conv123", message_data, "test_location")

        assert result.conversationId == "conv123"
        assert result.id == "msg123"

        # Verify SMS fields are sent correctly
        sent_data = mock_request.call_args[1]["json"]
        assert sent_data["message"] == "Test SMS"
        assert sent_data["phoneNumber"] == "+1234567890"  # API expects phoneNumber
        assert "html" not in sent_data  # SMS doesn't use html field
