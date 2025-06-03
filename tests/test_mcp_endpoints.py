"""Unit tests for MCP endpoints"""

import pytest
from unittest.mock import AsyncMock, patch, Mock

from src.utils.exceptions import (
    AuthenticationError,
    DuplicateResourceError,
)


class TestMCPEndpoints:
    """Test MCP server endpoints"""

    @pytest.mark.asyncio
    async def test_create_contact_success(self, mock_contact):
        """Test successful contact creation"""
        from src.main import create_contact, CreateContactParams

        mock_client = AsyncMock()
        mock_client.create_contact = AsyncMock(return_value=mock_contact)

        params = CreateContactParams(
            location_id="test_location",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
        )

        with patch("src.main.get_client", return_value=mock_client):
            result = await create_contact(params)

        assert result["success"] is True
        assert result["contact"]["id"] == mock_contact.id
        mock_client.create_contact.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_contact_duplicate_error(self):
        """Test contact creation with duplicate error"""
        from src.main import create_contact, CreateContactParams

        mock_client = AsyncMock()
        mock_client.create_contact = AsyncMock(
            side_effect=DuplicateResourceError("Contact already exists", 400)
        )

        params = CreateContactParams(
            location_id="test_location", email="existing@example.com"
        )

        with patch("src.main.get_client", return_value=mock_client):
            with pytest.raises(DuplicateResourceError):
                await create_contact(params)

    @pytest.mark.asyncio
    async def test_get_contact_success(self, mock_contact):
        """Test successful contact retrieval"""
        from src.main import get_contact, GetContactParams

        mock_client = AsyncMock()
        mock_client.get_contact = AsyncMock(return_value=mock_contact)

        params = GetContactParams(
            contact_id="test_contact", location_id="test_location"
        )

        with patch("src.main.get_client", return_value=mock_client):
            result = await get_contact(params)

        assert result["success"] is True
        assert result["contact"]["id"] == mock_contact.id

    @pytest.mark.asyncio
    async def test_list_contacts_resource(self, mock_contact):
        """Test list contacts resource"""
        from src.main import list_contacts_resource

        mock_client = AsyncMock()
        mock_client.get_contacts = AsyncMock(
            return_value=Mock(contacts=[mock_contact], total=1, count=1)
        )

        with patch("src.main.ghl_client", mock_client):
            result = await list_contacts_resource("test_location")

        assert isinstance(result, str)
        assert "Total contacts: 1" in result
        assert "John Doe" in result
        assert mock_contact.id in result

    @pytest.mark.asyncio
    async def test_send_message_email(self):
        """Test sending email message"""
        from src.main import send_message, SendMessageParams

        mock_client = AsyncMock()
        mock_message = Mock()
        mock_message.id = "msg123"
        mock_message.conversationId = "conv123"
        mock_message.model_dump = Mock(
            return_value={"id": "msg123", "conversationId": "conv123"}
        )
        mock_client.send_message = AsyncMock(return_value=mock_message)

        params = SendMessageParams(
            location_id="test_location",
            conversation_id="conv123",
            contact_id="contact123",
            message_type="Email",
            html="<p>Test</p>",
            subject="Test Subject",
        )

        with patch("src.main.get_client", return_value=mock_client):
            result = await send_message(params)

        assert result["success"] is True
        assert result["message"]["id"] == "msg123"

    @pytest.mark.asyncio
    async def test_authentication_error_handling(self):
        """Test that authentication errors are properly propagated"""
        from src.main import get_contact, GetContactParams

        mock_client = AsyncMock()
        mock_client.get_contact = AsyncMock(
            side_effect=AuthenticationError("Invalid token", 401)
        )

        params = GetContactParams(contact_id="test", location_id="test")

        with patch("src.main.get_client", return_value=mock_client):
            with pytest.raises(AuthenticationError) as exc_info:
                await get_contact(params)

            assert exc_info.value.status_code == 401
