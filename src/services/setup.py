"""
Standard Mode Setup Wizard for GoHighLevel MCP Server
"""

import json
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
        custom_env = Path(".env")
        first_run_marker = self.config_dir / ".first_run_complete"

        return not (standard_config.exists() or custom_env.exists() or first_run_marker.exists())

    def mark_first_run_complete(self) -> None:
        """Mark that first-run setup is complete"""
        self.config_dir.mkdir(exist_ok=True)
        marker_file = self.config_dir / ".first_run_complete"
        marker_file.touch()

    def check_auth_status(self) -> Tuple[bool, str]:
        """Check if we have valid authentication configured"""
        # Check for standard mode config
        standard_config = self.config_dir / "standard_config.json"
        if standard_config.exists():
            try:
                with open(standard_config, 'r') as f:
                    config_data = json.load(f)
                token = config_data.get('setup_token')
                if token and token.startswith('bm_ghl_mcp_'):
                    return True, "Standard mode configured"
            except Exception:
                pass

        # Check for custom mode (.env file)
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                if 'GHL_CLIENT_ID=' in content and 'GHL_CLIENT_SECRET=' in content:
                    return True, "Custom mode configured"
            except Exception:
                pass

        return False, "No valid configuration found"

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
        """Save validated token to config file"""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)

        # Save token to config file (JSON format)
        config_data = {
            "auth_mode": "standard",
            "setup_token": token,
            "created_at": datetime.now().isoformat(),
            "supabase_url": "https://egigkzfowimxfavnjvpe.supabase.co"
        }

        # Write to standard_config.json file
        config_file = self.config_dir / "standard_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    def choose_auth_mode(self) -> str:
        """Let user choose between Standard and Custom authentication mode"""
        print("\n🚀 Welcome to GoHighLevel MCP Server!\n")
        print("Choose your authentication mode:\n")

        print("📋 1. Standard Mode (Recommended)")
        print("   • Zero configuration required")
        print("   • Uses Basic Machines' hosted app")
        print("   • Quick setup through marketplace")
        print("   • Automatically managed authentication\n")

        print("🔧 2. Custom Mode (Advanced)")
        print("   • Use your own GoHighLevel Marketplace App")
        print("   • Requires creating app in GHL Developer Portal")
        print("   • Manual configuration with .env file")
        print("   • Full control over OAuth settings\n")

        while True:
            choice = input("Enter 1 for Standard or 2 for Custom [1]: ").strip()
            if choice == "" or choice == "1":
                return "standard"
            elif choice == "2":
                return "custom"
            else:
                print("Please enter 1 or 2.")

    def show_custom_mode_instructions(self) -> None:
        """Show instructions for setting up custom mode"""
        print("\n🔧 Custom Mode Setup Instructions\n")

        print("📋 Step 1: Create a GoHighLevel Marketplace App")
        print("   1. Visit: https://marketplace.gohighlevel.com/")
        print("   2. Sign in to your GHL account")
        print("   3. Go to 'Developer' > 'My Apps' > 'Create App'")
        print("   4. Set redirect URL to: http://localhost:8080/oauth/callback")
        print("   5. Note your Client ID and Client Secret\n")

        print("📋 Step 2: Create .env file")
        print("   Create a .env file in this directory with:")
        print("   ")
        print("   AUTH_MODE=custom")
        print("   GHL_CLIENT_ID=your-client-id-here")
        print("   GHL_CLIENT_SECRET=your-client-secret-here")
        print("   \n")

        print("📋 Step 3: Restart the server")
        print("   After creating the .env file, run:")
        print("   python -m src.main\n")

        print("💡 Need help? Check the README for detailed instructions.")
        print("🔗 https://github.com/basicmachines-co/open-ghl-mcp/blob/main/README.md\n")

    async def interactive_setup(self) -> bool:
        """Run interactive setup wizard"""
        print("📋 Setup Steps:")
        print("1. Install the Basic Machines app in your GoHighLevel account")
        print("2. Copy your setup token from the installation success page")
        print("3. Paste the token here to complete setup\n")

        # Show marketplace URL and wait for user confirmation
        marketplace_url = "https://app.gohighlevel.com/integration/683d23275f311ae4ccf17876"
        print(f"🌐 We'll open the GoHighLevel Marketplace to install the app:")
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

        # Load token from standard_config.json
        try:
            config_file = self.config_dir / "standard_config.json"
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            token = config_data.get('setup_token')
            if not token:
                print(f"DEBUG: No setup_token found in config", file=sys.stderr)
                return False

            # Validate token with API
            validation = await self.validate_token(token)
            if not validation.valid:
                print(f"DEBUG: Token validation failed: {validation.message}", file=sys.stderr)
            return validation.valid

        except Exception as e:
            print(f"DEBUG: Exception during validation: {type(e).__name__}: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return False
