[![Automated Tests](https://github.com/basicmachines-co/open-ghl-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/basicmachines-co/open-ghl-mcp/actions/workflows/test.yml)
# GoHighLevel MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with the GoHighLevel API v2. This server enables AI assistants to interact with GoHighLevel's CRM functionality, starting with comprehensive contact management.

## Features

- 🔐 **OAuth 2.0 Authentication**: Full OAuth flow with automatic token management by default
- 🌟 **Custom Authentication**: Manual authentication with your own Marketplace App credentials available as an option
- 🏢 **Multi-location Support**: Works with agency accounts to manage multiple sub-accounts
- 👥 **Contact Management**: Complete CRUD operations for contacts
- 💬 **Conversations**: Search conversations, view messages, and manage messaging
- 🏷️ **Tag Management**: Add and remove tags from contacts
- 🔄 **Automatic Token Refresh**: Handles token expiration seamlessly
- 🛠️ **MCP Tools & Resources**: Both tools and resources for flexible integration

## Prerequisites

- Python 3.12+
- `uv` package manager (or pip)
- One of the following:
  - **Standard Mode Configuration**: Access via our hosted GoHighLevel app (recommended)
  - **Custom Mode Configuration**: Your own GoHighLevel Marketplace App credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/open-ghl-mcp.git
cd open-ghl-mcp
```
2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Start the server:
```bash
python src/main.py
```

## Configuration

This MCP server supports two authentication modes:

### Option 1: Standard Mode (Recommended)

Use our hosted GoHighLevel app without exposing credentials:

1. Install our app from the GoHighLevel Marketplace
2. Complete the OAuth flow to get your access key
3. Return to this MCP server and paste your access key
4. Configure your LLM to use the MCP server

### Option 2: Custom Mode

Use your own GoHighLevel Marketplace App:

1. Create your own GoHighLevel Marketplace App
2. Set the redirect URL to: `http://localhost:8080/oauth/callback`
3. Configure your `.env` file:

```env
AUTH_MODE=custom
GHL_CLIENT_ID=your-client-id
GHL_CLIENT_SECRET=your-client-secret
```

4. Start the server:
```bash
python src/main.py
```
5. Configure your LLM to use the MCP server

## Usage

### Running the MCP Server

```bash
python src/main.py
```

The server will start on port 8000 by default.

### First-time Authentication

#### Standard Mode
1. The server will prompt you to install the Basic Machines Marketplace App
2. Follow the provided link to complete OAuth through the Marketplace App
3. Security Tokens are managed automatically by Basic Machines

#### Custom Mode
1. The server will read the .env file and use the credentials to authenticate with GoHighLevel

### Available MCP Tools

#### Contact Management
- `create_contact` - Create a new contact
- `update_contact` - Update existing contact
- `delete_contact` - Delete a contact
- `get_contact` - Get a single contact
- `search_contacts` - Search contacts with filters
- `add_contact_tags` - Add tags to a contact
- `remove_contact_tags` - Remove tags from a contact

#### Conversation Management
- `get_conversations` - Search and list conversations
- `get_conversation` - Get a single conversation
- `get_messages` - Get messages from a conversation
- `send_message` - Send messages (SMS ✅, Email ✅, WhatsApp, IG, FB, Custom, Live_Chat)
- `update_message_status` - Update message delivery status

#### Available Resources
- `contacts://{location_id}` - List all contacts for a location
- `contact://{location_id}/{contact_id}` - Get a single contact details
- `conversations://{location_id}` - List all conversations for a location
- `conversation://{location_id}/{conversation_id}` - Get conversation with messages

## Development

### Testing

For local testing with real GoHighLevel accounts, create a `TESTING_INSTRUCTIONS.md` file in the project root with your specific testing accounts and guidelines. This file is gitignored and should not be committed to the repository.

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_api_client.py -v
```

### Code Quality

This project uses automated code quality tools. Before committing changes:

```bash
# Format code with Black
uv run black src/ tests/

# Check linting with flake8
uv run flake8 src/ tests/

# Run type checking with mypy
uv run mypy src/ --ignore-missing-imports

# Run all checks at once
uv run black src/ tests/ && uv run flake8 src/ tests/ && uv run mypy src/ --ignore-missing-imports
```

### Pre-commit Hook (optional)

To automatically format code before commits:

```bash
# Create a git pre-commit hook
echo '#!/bin/sh
uv run black src/ tests/
uv run flake8 src/ tests/
' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Continuous Integration

The project uses GitHub Actions for CI/CD:
- Tests run automatically on all pushes and pull requests
- Tested with Python 3.12 and 3.13
- Includes linting, type checking, and test coverage
- Coverage reports are uploaded to Codecov (if configured)

## Architecture

The server follows a modular architecture:

- **OAuth Service**: Handles authentication and token management
- **API Client**: Manages communication with GoHighLevel API
- **MCP Server**: FastMCP-based server exposing tools and resources
- **Data Models**: Pydantic models for data validation

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and feature requests, please use the GitHub issues tracker.
