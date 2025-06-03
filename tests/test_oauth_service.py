"""Unit tests for OAuth service"""

import pytest
from unittest.mock import Mock, patch
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.services.oauth import OAuthService, OAuthSettings
from src.models.auth import TokenResponse, StoredToken


class TestOAuthService:
    """Test OAuth service functionality"""

    @pytest.fixture
    def oauth_settings(self, tmp_path):
        """Create OAuth settings with test values"""
        return OAuthSettings(
            ghl_client_id="test_client_id",
            ghl_client_secret="test_client_secret",
            token_storage_path=str(tmp_path / "tokens.json"),
        )

    @pytest.fixture
    def oauth_service(self, oauth_settings):
        """Create OAuth service instance"""
        with patch("src.services.oauth.OAuthSettings", return_value=oauth_settings):
            return OAuthService()

    @pytest.fixture
    def valid_stored_token(self):
        """Create a valid stored token"""
        return StoredToken(
            access_token="valid_token",
            refresh_token="refresh_token",
            token_type="Bearer",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            scope="contacts.read contacts.write",
            user_type="Location",
        )

    @pytest.fixture
    def expired_stored_token(self):
        """Create an expired stored token"""
        return StoredToken(
            access_token="expired_token",
            refresh_token="refresh_token",
            token_type="Bearer",
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
            scope="contacts.read contacts.write",
            user_type="Location",
        )

    @pytest.mark.asyncio
    async def test_load_token_no_file(self, oauth_service):
        """Test loading token when file doesn't exist"""
        token = await oauth_service.load_token()
        assert token is None

    @pytest.mark.asyncio
    async def test_load_token_success(
        self, oauth_service, valid_stored_token, oauth_settings
    ):
        """Test loading token from file"""
        # Create token file
        token_path = Path(oauth_settings.token_storage_path)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w") as f:
            json.dump(valid_stored_token.model_dump(mode="json"), f)

        token = await oauth_service.load_token()
        assert token is not None
        assert token.access_token == valid_stored_token.access_token

    @pytest.mark.asyncio
    async def test_save_token(self, oauth_service, valid_stored_token, oauth_settings):
        """Test saving token to file"""
        await oauth_service.save_token(valid_stored_token)

        # Verify file was created
        token_path = Path(oauth_settings.token_storage_path)
        assert token_path.exists()

        # Verify content
        with open(token_path) as f:
            data = json.load(f)
            assert data["access_token"] == valid_stored_token.access_token

    @pytest.mark.asyncio
    async def test_get_valid_token_cached(self, oauth_service, valid_stored_token):
        """Test getting valid token from cache"""
        # Mock load_token to return valid token
        with patch.object(oauth_service, "load_token", return_value=valid_stored_token):
            token = await oauth_service.get_valid_token()
            assert token == valid_stored_token.access_token

    @pytest.mark.asyncio
    async def test_get_valid_token_expired_refresh(
        self, oauth_service, expired_stored_token
    ):
        """Test refreshing expired token"""
        # Mock refresh_token method
        new_token = StoredToken(
            access_token="new_token",
            refresh_token="new_refresh",
            token_type="Bearer",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            scope="contacts.read contacts.write",
            user_type="Location",
        )

        with patch.object(
            oauth_service, "load_token", return_value=expired_stored_token
        ):
            with patch.object(oauth_service, "refresh_token", return_value=new_token):
                token = await oauth_service.get_valid_token()
                assert token == "new_token"

    @pytest.mark.asyncio
    async def test_get_valid_token_no_token_authenticates(
        self, oauth_service, valid_stored_token
    ):
        """Test that get_valid_token calls authenticate when no token exists"""
        with patch.object(oauth_service, "load_token", return_value=None):
            with patch.object(
                oauth_service, "authenticate", return_value=valid_stored_token
            ):
                token = await oauth_service.get_valid_token()
                assert token == valid_stored_token.access_token
                oauth_service.authenticate.assert_called_once()

    @pytest.mark.asyncio
    async def test_exchange_code_for_token(self, oauth_service):
        """Test exchanging authorization code for token"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json = Mock(
            return_value={
                "access_token": "test_token",
                "refresh_token": "test_refresh",
                "expires_in": 3600,
                "token_type": "Bearer",
                "scope": "contacts.read",
                "userType": "Location",
            }
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            token = await oauth_service._exchange_code_for_token("test_code")

        assert isinstance(token, TokenResponse)
        assert token.access_token == "test_token"

    @pytest.mark.asyncio
    async def test_refresh_token(self, oauth_service):
        """Test token refresh"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json = Mock(
            return_value={
                "access_token": "refreshed_token",
                "refresh_token": "new_refresh",
                "expires_in": 3600,
                "token_type": "Bearer",
                "scope": "contacts.read",
                "userType": "Location",
            }
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with patch.object(oauth_service, "save_token") as mock_save:
                token = await oauth_service.refresh_token("old_refresh")

        assert isinstance(token, StoredToken)
        assert token.access_token == "refreshed_token"
        mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_location_token_cached(self, oauth_service, valid_stored_token):
        """Test getting cached location token"""
        location_id = "test_location"
        # Location tokens should be StoredToken objects
        oauth_service._location_tokens = {location_id: valid_stored_token}

        token = await oauth_service.get_location_token(location_id)
        assert token == valid_stored_token.access_token

    @pytest.mark.asyncio
    async def test_get_location_token_new(self, oauth_service, valid_stored_token):
        """Test getting new location token"""
        location_id = "test_location"

        # Create a properly formatted mock JWT token
        import base64
        import json

        payload = json.dumps({"authClassId": "test_company"})
        encoded_payload = base64.b64encode(payload.encode()).decode().rstrip("=")
        mock_jwt = f"header.{encoded_payload}.signature"

        # Mock the agency token and load_token
        with patch.object(oauth_service, "get_valid_token", return_value=mock_jwt):
            with patch.object(
                oauth_service, "load_token", return_value=valid_stored_token
            ):
                # Mock the API response
                mock_response = Mock()
                mock_response.status_code = 201
                mock_response.json = Mock(
                    return_value={
                        "access_token": "location_token",
                        "token_type": "Bearer",
                        "expires_in": 86400,
                        "scope": "contacts.read",
                        "userId": "user_id",
                        "userType": "Location",
                        "locationId": location_id,
                    }
                )

                with patch("httpx.AsyncClient.post", return_value=mock_response):
                    token = await oauth_service.get_location_token(location_id)

        assert token == "location_token"
        # Check that token was cached as a StoredToken
        assert location_id in oauth_service._location_tokens
        assert (
            oauth_service._location_tokens[location_id].access_token == "location_token"
        )
