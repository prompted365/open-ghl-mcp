"""
Standard Mode Setup Wizard for GoHighLevel MCP Server
"""

import os
import webbrowser
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

import httpx
from pydantic import BaseModel


class SetupResponse(BaseModel):
    """Response from token validation"""
    valid: bool
    config: Optional[dict] = None
    message: str
    error: Optional[str] = None


class StandardModeSetup:
    """Handles Standard Mode setup wizard"""

    def __init__(self):
        self.config_dir = Path("./config")
        self.env_file = Path(".env")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def check_auth_status(self) -> Tuple[bool, str]:
        """Check if we have valid authentication configured"""
        # Check for existing .env file
        if not self.env_file.exists():
            return False, "No configuration found"

        # Check for setup token in .env
        try:
            with open(self.env_file, 'r') as f:
                content = f.read()

            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('SETUP_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    if token and token.startswith('bm_ghl_mcp_'):
                        return True, "Authentication configured"

        except Exception:
            pass

        return False, "Invalid or missing setup token"

    async def validate_token(self, token: str) -> SetupResponse:
        """Validate setup token with Basic Machines API"""
        if not token or not token.startswith('bm_ghl_mcp_'):
            return SetupResponse(
                valid=False,
                error="invalid_format",
                message="Token must start with 'bm_ghl_mcp_'"
            )

        try:
            response = await self.client.post(
                "https://egigkzfowimxfavnjvpe.supabase.co/functions/v1/get-setup-token",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return SetupResponse(**data)
            else:
                try:
                    error_data = response.json()
                    return SetupResponse(
                        valid=False,
                        error=error_data.get("error", "unknown"),
                        message=error_data.get("message", f"HTTP {response.status_code}")
                    )
                except:
                    return SetupResponse(
                        valid=False,
                        error="http_error",
                        message=f"HTTP {response.status_code}: {response.text[:100]}"
                    )

        except httpx.TimeoutException:
            return SetupResponse(
                valid=False,
                error="timeout",
                message="Request timed out. Please check your internet connection."
            )
        except Exception as e:
            return SetupResponse(
                valid=False,
                error="network_error",
                message=f"Network error: {str(e)}"
            )

    def save_token_to_config(self, token: str) -> None:
        """Save validated token to .env file"""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)

        # Create .env content
        env_content = f"""# Basic Machines GoHighLevel MCP Server Configuration
# Generated on {datetime.now().isoformat()}

# Authentication mode
AUTH_MODE=standard

# Basic Machines setup token
SETUP_TOKEN={token}

# Supabase configuration (managed by Basic Machines)
SUPABASE_URL=https://egigkzfowimxfavnjvpe.supabase.co
SUPABASE_ACCESS_KEY={token}

# Marketplace app configuration
MARKETPLACE_APP_ID=ghl-mcp-server
"""

        # Write to .env file
        with open(self.env_file, 'w') as f:
            f.write(env_content)

    async def interactive_setup(self) -> bool:
        """Run interactive setup wizard"""
        print("\n🚀 GoHighLevel MCP Server - Standard Mode Setup\n")

        print("Welcome! This setup wizard will help you connect your MCP server")
        print("to GoHighLevel using Basic Machines' standard authentication.\n")

        print("📋 Setup Steps:")
        print("1. Install the Basic Machines app in your GoHighLevel account")
        print("2. Copy your setup token from the installation success page")
        print("3. Paste the token here to complete setup\n")

        # Open marketplace automatically
        marketplace_url = "https://marketplace.gohighlevel.com/oauth/chooselocation?response_type=code&redirect_uri=https%3A%2F%2Fegigkzfowimxfavnjvpe.supabase.co%2Ffunctions%2Fv1%2Foauth-callback&client_id=683d23275f311ae4ccf17876-mbeko6sk&scope=conversations.readonly+conversations.write+conversations%2Fmessage.readonly+conversations%2Fmessage.write+conversations%2Freports.readonly+conversations%2Flivechat.write+contacts.readonly+contacts.write"
        print(f"🌐 Opening GoHighLevel Marketplace...")
        print(f"   {marketplace_url}")
        print("\nIf the browser doesn't open automatically, please visit the URL above.\n")

        try:
            webbrowser.open(marketplace_url)
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("Please manually visit the marketplace URL above.\n")

        # Wait for user to complete installation
        print("📱 Please:")
        print("   • Install or reinstall the 'Basic Machines' app")
        print("   • Complete the authorization process")
        print("   • Copy your setup token from the success page")
        print("   • Return here and paste the token below\n")

        # Token input loop
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                token = input("🔑 Paste your setup token here: ").strip()

                if not token:
                    print("❌ Please enter a token.\n")
                    continue

                print("🔍 Validating token...")

                validation = await self.validate_token(token)

                if validation.valid:
                    print("✅ Token validated successfully!")
                    print("💾 Saving configuration...")

                    self.save_token_to_config(token)

                    print("🎉 Setup complete!")
                    print("   Your MCP server is now configured for Standard mode.")
                    print("   Configuration saved to .env file.\n")
                    return True

                else:
                    remaining = max_attempts - attempt - 1
                    print(f"❌ Token validation failed: {validation.message}")

                    if validation.error == "token_expired":
                        print("   Please reinstall the Basic Machines app to get a new token.")
                    elif validation.error == "invalid_format":
                        print("   Make sure you copied the complete token.")
                    elif validation.error in ["timeout", "network_error"]:
                        print("   Please check your internet connection and try again.")

                    if remaining > 0:
                        print(f"   You have {remaining} attempt{'s' if remaining > 1 else ''} remaining.\n")
                        continue
                    else:
                        print("\n❌ Maximum attempts reached. Setup cancelled.")
                        return False

            except KeyboardInterrupt:
                print("\n\n⏹️  Setup cancelled by user.")
                return False
            except Exception as e:
                print(f"\n❌ Unexpected error during setup: {e}")
                return False

        return False

    async def validate_existing_config(self) -> bool:
        """Validate existing configuration"""
        auth_valid, _ = self.check_auth_status()
        if not auth_valid:
            return False

        # Load token from .env
        try:
            with open(self.env_file, 'r') as f:
                content = f.read()

            token = None
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('SETUP_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    break

            if not token:
                return False

            # Validate token with API
            validation = await self.validate_token(token)
            return validation.valid

        except Exception:
            return False
