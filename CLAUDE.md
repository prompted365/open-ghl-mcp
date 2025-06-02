# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server for the GoHighLevel 2.0 API using FastMCP. The server bridges AI models and the GoHighLevel API.

## GoHighLevel API Documentation
The official API docs are at https://highlevel.stoplight.io/docs/integrations/.

Always use the official API docs at https://highlevel.stoplight.io/docs/integrations/ to understand the API and prefer
this resource over any other documentation.

Only use API v2. Do not use API v1 or refer to API v1 documentation.

## Testing
If you need to test the MCP server with real GoHighLevel accounts, check for TESTING_INSTRUCTIONS.md in the project root. This file contains specific testing accounts and instructions but is not committed to the repository.

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
   - Each endpoint follows the same pattern requiring location tokens for access

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

### Type Definitions
1. Refer to the official API docs at https://highlevel.stoplight.io/docs/integrations/ to understand the API and correctly implement MCP tools and resources.
2. The official API docs define Schemas that should be used as a reference.
3. When adding new MCP tools and resources use the schemas from the API docs to define the types for the MCP server.
4. The schema definitions in the documentation should be considered "best effort" and may not be complete or accurate, but should always be used as a starting point.


## Critical OAuth Implementation Lessons

### Two-Step Authentication Required
- Initial OAuth provides agency/company token
- Must exchange for location token to access contacts: POST `/oauth/locationToken`
- Include both `companyId` (from JWT) and `locationId` in request

### OAuth Endpoints
- Use `/oauth/chooselocation` for authorization (NOT `/oauth/authorize`)
- Token exchange: `https://services.leadconnectorhq.com/oauth/token`
- Add `user_type: "Location"` to token exchange request

### Common Pitfalls to Avoid
- Location token endpoint returns 201 (not 200) - handle both
- Always include `locationId` in API calls even with location token
- Omit `skip` parameter if value is 0 (causes 422 error)
- Extract company ID from JWT dynamically - never hardcode
- Test data needs unique identifiers (use timestamps) to avoid duplicate errors

### MCP Pattern for New Resources
```python
# Tools need location_id parameter
class YourToolParams(BaseModel):
    location_id: str = Field(..., description="The location ID")
    # ... other fields
    access_token: Optional[str] = Field(None, description="Optional access token")

# Client methods need location_id
async def your_method(self, resource_id: str, location_id: str):
    response = await self._request(
        "GET",
        f"/endpoint/{resource_id}",
        location_id=location_id  # This triggers location token usage
    )
```
