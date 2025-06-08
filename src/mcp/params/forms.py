"""Parameter models for Forms MCP tools"""

from typing import Optional
from pydantic import BaseModel, Field


class GetFormsParams(BaseModel):
    """Parameters for getting forms"""

    location_id: str = Field(..., description="The location ID")
    limit: int = Field(
        default=100, ge=1, le=100, description="Number of results to return"
    )
    skip: int = Field(default=0, ge=0, description="Number of results to skip")
    access_token: Optional[str] = Field(
        None, description="Optional access token override"
    )


class GetAllSubmissionsParams(BaseModel):
    """Parameters for getting all form submissions"""

    location_id: str = Field(..., description="The location ID")
    form_id: Optional[str] = Field(None, description="Filter by specific form")
    contact_id: Optional[str] = Field(None, description="Filter by specific contact")
    start_date: Optional[str] = Field(None, description="Filter from date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="Filter to date (YYYY-MM-DD)")
    limit: int = Field(
        default=100, ge=1, le=100, description="Number of results to return"
    )
    skip: int = Field(default=0, ge=0, description="Number of results to skip")
    access_token: Optional[str] = Field(
        None, description="Optional access token override"
    )


class UploadFormFileParams(BaseModel):
    """Parameters for uploading a file to a form field"""

    contact_id: str = Field(..., description="The contact ID")
    location_id: str = Field(..., description="The location ID")
    field_id: str = Field(..., description="The custom field ID for file upload")
    file_name: str = Field(..., description="Name of the file")
    file_content: str = Field(..., description="Base64 encoded file content")
    content_type: Optional[str] = Field(
        default="application/octet-stream", description="MIME type of the file"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token override"
    )
