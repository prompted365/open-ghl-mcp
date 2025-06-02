# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server for the GoHighLevel 2.0 API using FastMCP. The server bridges AI models and the GoHighLevel API.

- **Framework**: FastMCP (Python)
- **Target API**: GoHighLevel 2.0
- **Primary Language**: Python

## Common Commands

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Start the MCP server
python src/main.py
```

## Architecture

The MCP server follows a modular architecture:

1. **OAuth Service** (`src/services/oauth.py`):
   - Handles OAuth 2.0 flow with GoHighLevel
   - Manages agency and location token exchange
   - Automatic token refresh and caching
   - Browser-based authorization flow

2. **API Client** (`src/api/client.py`):
   - Async HTTP client for GoHighLevel API v2
   - Automatic location token usage for contact operations
   - Consistent error handling and response parsing

3. **MCP Server** (`src/main.py`):
   - FastMCP-based implementation
   - Tools for CRUD operations on contacts
   - Resources for listing and viewing contacts
   - Support for custom access tokens per request

4. **Models** (`src/models/`):
   - Pydantic models for contacts and authentication
   - Request/response validation
   - Type safety throughout the codebase

## Key Implementation Details

### Authentication Flow
1. Agency-level OAuth provides company access
2. Location tokens are obtained for specific sub-accounts
3. Contact operations require location-specific tokens
4. Tokens are cached and refreshed automatically

### API Quirks
- Location token endpoint returns 201 (not 200)
- Contact endpoints require locationId even with location token
- Skip parameter should be omitted if 0
- Duplicate contacts return 400 with details

### Adding New Endpoints
1. Add models to `src/models/`
2. Add client methods to `src/api/client.py` (remember location_id parameter)
3. Add MCP tools/resources to `src/main.py`
4. Test with both agency and location tokens