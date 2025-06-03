[![Automated Tests](https://github.com/basicmachines-co/open-ghl-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/basicmachines-co/open-ghl-mcp/actions/workflows/test.yml)
# GoHighLevel MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with the GoHighLevel API v2. This server enables AI assistants to interact with GoHighLevel's CRM functionality, starting with comprehensive contact management.

## Features

- 🔐 **OAuth 2.0 Authentication**: Full OAuth flow with automatic token management
- 🏢 **Multi-location Support**: Works with agency accounts to manage multiple locations
- 👥 **Contact Management**: Complete CRUD operations for contacts
- 💬 **Conversations**: Search conversations, view messages, and manage messaging
- 🏷️ **Tag Management**: Add and remove tags from contacts
- 🔄 **Automatic Token Refresh**: Handles token expiration seamlessly
- 🛠️ **MCP Tools & Resources**: Both tools and resources for flexible integration

## Prerequisites

- Python 3.8+
- GoHighLevel OAuth App credentials
- `uv` package manager (or pip)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/open-ghl-mcp.git
cd open-ghl-mcp
```

2. Create a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your GoHighLevel OAuth credentials
```

## Configuration

Create a `.env` file with your GoHighLevel OAuth App credentials:

```env
# GoHighLevel OAuth Configuration
GHL_CLIENT_ID=your-client-id
GHL_CLIENT_SECRET=your-client-secret
```

## OAuth Setup

1. Create an OAuth app in your GoHighLevel account
2. Set the redirect URL to: `http://localhost:8080/oauth/callback`
3. Copy your Client ID and Client Secret to the `.env` file

## Usage

### Running the MCP Server

```bash
python src/main.py
```

The server will start on port 8000 by default.

### First-time Authentication

On first run, the server will:
1. Open your browser for GoHighLevel authorization
2. Ask you to select a location (sub-account)
3. Store the tokens locally for future use

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
- Supports Python 3.9, 3.10, 3.11, and 3.12
- Includes linting, type checking, and test coverage
- Coverage reports are uploaded to Codecov (if configured)

## Architecture

The server follows a modular architecture:

- **OAuth Service**: Handles authentication and token management
- **API Client**: Manages communication with GoHighLevel API
- **MCP Server**: FastMCP-based server exposing tools and resources
- **Models**: Pydantic models for data validation

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and feature requests, please use the GitHub issues tracker.
