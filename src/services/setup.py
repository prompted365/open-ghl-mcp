"""
Standard Mode Setup Wizard for GoHighLevel MCP Server
"""

import json
import sys
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
        # Use absolute path based on the module location
        base_dir = Path(__file__).parent.parent.parent  # Goes up to project root
        self.config_dir = base_dir / "config"
        self.env_file = base_dir / ".env"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def is_first_run(self) -> bool:
        """Check if this is the first time running the server"""
        # Check for any configuration files
        standard_config = self.config_dir / "standard_config.json"
        first_run_marker = self.config_dir / ".first_run_complete"

        return not (
            standard_config.exists()
            or self.env_file.exists()
            or first_run_marker.exists()
        )

    def mark_first_run_complete(self) -> None:
        """Mark that first-run setup is complete"""
        self.config_dir.mkdir(exist_ok=True)
        marker_file = self.config_dir / ".first_run_complete"
        marker_file.touch()

    def save_custom_mode_choice(self) -> None:
        """Save that user chose custom mode (for incomplete setups)"""
        self.config_dir.mkdir(exist_ok=True)
        marker_file = self.config_dir / ".custom_mode_chosen"
        marker_file.touch()

    def was_custom_mode_chosen(self) -> bool:
        """Check if user previously chose custom mode"""
        marker_file = self.config_dir / ".custom_mode_chosen"
        return marker_file.exists()

    def clear_custom_mode_choice(self) -> None:
        """Clear custom mode choice marker (when setup is complete)"""
        marker_file = self.config_dir / ".custom_mode_chosen"
        if marker_file.exists():
            marker_file.unlink()

    def check_auth_status(self) -> Tuple[bool, str]:
        """Check if we have valid authentication configured"""
        # Check for standard mode config
        standard_config = self.config_dir / "standard_config.json"
        if standard_config.exists():
            try:
                with open(standard_config, "r") as f:
                    config_data = json.load(f)
                token = config_data.get("setup_token")
                if token and token.startswith("bm_ghl_mcp_"):
                    return True, "Standard mode configured"
            except Exception:
                pass

        # Check for custom mode (.env file)
        if self.env_file.exists():
            try:
                with open(self.env_file, "r") as f:
                    content = f.read()
                if "GHL_CLIENT_ID=" in content and "GHL_CLIENT_SECRET=" in content:
                    return True, "Custom mode configured"
            except Exception:
                pass

        return False, "No valid configuration found"

    async def validate_token(self, token: str) -> SetupResponse:
        """Validate setup token with Basic Machines API"""
        if not token or not token.startswith("bm_ghl_mcp_"):
            return SetupResponse(
                valid=False,
                error="invalid_format",
                message="Token must start with 'bm_ghl_mcp_'",
            )

        try:
            response = await self.client.post(
                "https://egigkzfowimxfavnjvpe.supabase.co/functions/v1/get-setup-token",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=10.0,
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
                        message=error_data.get(
                            "message", f"HTTP {response.status_code}"
                        ),
                    )
                except Exception:
                    return SetupResponse(
                        valid=False,
                        error="http_error",
                        message=f"HTTP {response.status_code}: {response.text[:100]}",
                    )

        except httpx.TimeoutException:
            return SetupResponse(
                valid=False,
                error="timeout",
                message="Request timed out. Please check your internet connection.",
            )
        except Exception as e:
            return SetupResponse(
                valid=False, error="network_error", message=f"Network error: {str(e)}"
            )

    def save_token_to_config(self, token: str) -> None:
        """Save validated token to config file"""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)

        # Save token to config file (JSON format)
        config_data = {
            "auth_mode": "standard",
            "setup_token": token,
            "created_at": datetime.now().isoformat(),
            "supabase_url": "https://egigkzfowimxfavnjvpe.supabase.co",
        }

        # Write to standard_config.json file
        config_file = self.config_dir / "standard_config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

    def choose_auth_mode(self) -> str:
        """Let user choose between Standard and Custom authentication mode"""
        print("\n🚀 Welcome to GoHighLevel MCP Server!\n")
        print("Setting up in Custom Mode Authentication...")
        print("\n🔧 Custom Mode Setup")
        print("   • Use your own GoHighLevel Marketplace App")
        print("   • Full control over OAuth settings\n")

        # Automatically return custom mode for early release
        return "custom"

        # while True:
        #     choice = input("Enter 1 for Standard or 2 for Custom [1]: ").strip()
        #     if choice == "" or choice == "1":
        #         return "standard"
        #     elif choice == "2":
        #         return "custom"
        #     else:
        #         print("Please enter 1 or 2.")

    async def interactive_custom_setup(self) -> bool:
        """Interactive setup for custom mode"""

        # Ask if they have created their marketplace app
        print("⚠️ GoHighLevel Marketplace App Required")
        print("   Custom mode requires your own GoHighLevel Marketplace App.\n")

        while True:
            has_app = (
                input("Have you already created a GoHighLevel Marketplace App? (y/n): ")
                .strip()
                .lower()
            )
            if has_app in ["y", "yes"]:
                return await self._collect_custom_credentials()
            elif has_app in ["n", "no"]:
                self._show_marketplace_app_instructions()
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    async def _collect_custom_credentials(self) -> bool:
        """Collect custom credentials and complete OAuth flow"""
        print("\n📋 Enter Your Marketplace App Credentials\n")

        try:
            # Collect credentials
            client_id = input("Enter your GHL_CLIENT_ID: ").strip()
            if not client_id:
                print("❌ Client ID cannot be empty.")
                return False

            client_secret = input("Enter your GHL_CLIENT_SECRET: ").strip()
            if not client_secret:
                print("❌ Client Secret cannot be empty.")
                return False

            # Create .env file content
            env_content = f"""# GoHighLevel MCP Server - Custom Mode Configuration
AUTH_MODE=custom
GHL_CLIENT_ID={client_id}
GHL_CLIENT_SECRET={client_secret}

# OAuth settings (modify if needed)
OAUTH_REDIRECT_URI=http://localhost:8080/oauth/callback
OAUTH_SERVER_PORT=8080
"""

            # Write .env file
            with open(self.env_file, "w") as f:
                f.write(env_content)

            print("✅ Configuration saved to .env file!")

            # Now run the OAuth flow to get tokens
            print("\n🔐 Starting OAuth authorization...")
            print("📱 Please:")
            print("   • Authorize the app in the browser window that opens")
            print("   • Complete the authorization process")
            print("   • Return here when done\n")

            # Import here to avoid circular imports
            from ..services.oauth import OAuthService

            # Initialize OAuth service (it will read the .env file we just created)
            oauth_service = OAuthService()

            # Run the OAuth flow
            stored_token = await oauth_service.authenticate()

            if stored_token:
                print("✅ OAuth authorization successful!")
                print("💾 Access tokens saved!")
                print("🎉 Custom mode setup complete!")
                return True
            else:
                print("❌ OAuth authorization failed.")
                print("   Please check your credentials and try again.")
                return False

        except KeyboardInterrupt:
            print("\n\n⏹️  Setup cancelled by user.")
            return False
        except Exception as e:
            print(f"\n❌ Error during OAuth setup: {e}")
            print("   Please check your credentials and try again.")
            return False

    def _show_marketplace_app_instructions(self) -> None:
        """Show instructions for creating a marketplace app"""
        print("\n📋 How to Create a GoHighLevel Marketplace App\n")

        print("1. 🌐 Visit: https://marketplace.gohighlevel.com/")
        print("2. 🔐 Sign in to your GHL account")
        print("3. 🔧 Go to 'Developer' → 'My Apps' → 'Create App'")
        print("4. 📝 Fill out your app details")
        print("5. 🔗 Set redirect URL to: http://localhost:8080/oauth/callback")
        print("6. 💾 Save your app and note the Client ID and Client Secret\n")

        print("📋 Required Scopes (select these when creating your app):")
        print("   • contacts.readonly")
        print("   • contacts.write")
        print("   • conversations.readonly")
        print("   • conversations.write")
        print("   • conversations/message.readonly")
        print("   • conversations/message.write")
        print("   • locations.readonly")

        print("💡 Need help? Check the README for detailed instructions.")
        print("🔗 https://github.com/basicmachines-co/open-ghl-mcp/blob/main/README.md")
        print(
            "\n🔄 After creating your app, run this command again and select 'y' when asked."
        )
        print("   python -m src.main\n")

    async def interactive_setup(self) -> bool:
        """Run interactive setup wizard"""
        print("📋 Setup Steps:")
        print("1. Install the Basic Machines app in your GoHighLevel account")
        print("2. Copy your setup token from the installation success page")
        print("3. Paste the token here to complete setup\n")

        # Show marketplace URL and wait for user confirmation
        marketplace_url = (
            "https://app.gohighlevel.com/integration/683d23275f311ae4ccf17876"
        )
        print("🌐 We'll open the GoHighLevel Marketplace to install the app:")
        print(f"   {marketplace_url}\n")

        input("Press Enter to open the marketplace in your browser...")

        print("\n🌐 Opening GoHighLevel Marketplace...")

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
                    self.mark_first_run_complete()

                    print("🎉 Setup complete!")
                    print("   Your MCP server is now configured for Standard mode.")
                    print("   Configuration saved successfully.\n")
                    return True

                else:
                    remaining = max_attempts - attempt - 1
                    print(f"❌ Token validation failed: {validation.message}")

                    if validation.error == "token_expired":
                        print(
                            "   Please reinstall the Basic Machines app to get a new token."
                        )
                    elif validation.error == "invalid_format":
                        print("   Make sure you copied the complete token.")
                    elif validation.error in ["timeout", "network_error"]:
                        print("   Please check your internet connection and try again.")

                    if remaining > 0:
                        print(
                            f"   You have {remaining} attempt{'s' if remaining > 1 else ''} remaining.\n"
                        )
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
        auth_valid, message = self.check_auth_status()
        if not auth_valid:
            return False

        # Check if we're in custom mode
        if self.env_file.exists():
            # Custom mode - just check that .env file has required fields
            try:
                with open(self.env_file, "r") as f:
                    content = f.read()
                if "GHL_CLIENT_ID=" in content and "GHL_CLIENT_SECRET=" in content:
                    return True
                else:
                    print("DEBUG: .env file missing required fields", file=sys.stderr)
                    return False
            except Exception as e:
                print(f"DEBUG: Error reading .env file: {e}", file=sys.stderr)
                return False

        # Standard mode - validate token with API
        try:
            config_file = self.config_dir / "standard_config.json"
            with open(config_file, "r") as f:
                config_data = json.load(f)

            token = config_data.get("setup_token")
            if not token:
                print("DEBUG: No setup_token found in config", file=sys.stderr)
                return False

            # Validate token with API
            validation = await self.validate_token(token)
            if not validation.valid:
                print(
                    f"DEBUG: Token validation failed: {validation.message}",
                    file=sys.stderr,
                )
            return validation.valid

        except Exception as e:
            print(
                f"DEBUG: Exception during validation: {type(e).__name__}: {str(e)}",
                file=sys.stderr,
            )
            import traceback

            traceback.print_exc(file=sys.stderr)
            return False

    def show_claude_desktop_instructions(self) -> None:
        """Show Claude Desktop configuration instructions"""
        import os

        print("\n" + "=" * 60)
        print("🎯 Next Step: Configure Claude Desktop")
        print("=" * 60)

        # Check for virtual environment
        venv_path = Path(os.getcwd()) / ".venv"
        if venv_path.exists():
            python_path = str(venv_path / "bin" / "python")
        else:
            python_path = "python"
            print("\n⚠️  Warning: No .venv directory found.")
            print("   Make sure you have installed requirements:")
            print("   python -m venv .venv")
            print(
                "   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate"
            )
            print("   pip install -r requirements.txt")

        print("\n📋 Add this server to Claude Desktop:")
        print("\n1. Open Claude Desktop settings")
        print("2. Navigate to 'Developer' → 'Edit Config'")
        print("3. Add the following to your mcpServers configuration:")
        print(
            f"""
{{
  "mcpServers": {{
    "ghl-mcp-server": {{
      "command": "{python_path}",
      "args": [
        "-m",
        "src.main"
      ],
      "cwd": "{os.getcwd()}",
      "env": {{
        "PYTHONPATH": "{os.getcwd()}"
      }}
    }}
  }}
}}
"""
        )
        print("4. Save the configuration and restart Claude Desktop")
        print("\n✅ Your GoHighLevel MCP server is now configured!")
