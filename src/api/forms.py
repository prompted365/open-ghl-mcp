"""Forms client for GoHighLevel API v2"""

from typing import Optional, Dict, Any
import base64

from .base import BaseGoHighLevelClient
from ..models.form import (
    FormList,
    FormSubmissionList,
    FormFileUploadRequest,
)


class FormsClient(BaseGoHighLevelClient):
    """Client for forms-related endpoints of GoHighLevel API v2"""

    async def get_forms(
        self, location_id: str, limit: int = 100, skip: int = 0
    ) -> FormList:
        """Get all forms for a location

        Args:
            location_id: The location ID
            limit: Number of results to return (max 100)
            skip: Number of results to skip

        Returns:
            FormList with forms
        """
        params = {"locationId": location_id, "limit": limit}
        if skip > 0:
            params["skip"] = skip

        response = await self._request(
            "GET", "/forms/", params=params, location_id=location_id
        )

        data = response.json()
        return FormList(**data)

    # NOTE: GET /forms/{id} is not supported by the API
    # Returns 401: "This route is not yet supported by the IAM Service"

    # NOTE: GET /forms/{id}/submissions is not supported by the API
    # Returns 404 Not Found

    async def get_all_submissions(
        self,
        location_id: str,
        form_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        skip: int = 0,
    ) -> FormSubmissionList:
        """Get all form submissions for a location

        Args:
            location_id: The location ID
            form_id: Filter by specific form
            contact_id: Filter by specific contact
            start_date: Filter from date (YYYY-MM-DD)
            end_date: Filter to date (YYYY-MM-DD)
            limit: Number of results to return
            skip: Number of results to skip

        Returns:
            FormSubmissionList with submissions
        """
        params = {"locationId": location_id, "limit": limit}
        if skip > 0:
            params["skip"] = skip
        if form_id:
            params["formId"] = form_id
        if contact_id:
            params["contactId"] = contact_id
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = await self._request(
            "GET", "/forms/submissions", params=params, location_id=location_id
        )

        data = response.json()
        return FormSubmissionList(**data)

    # NOTE: Form submission endpoints have been removed
    # POST /forms/submit returns 401 Unauthorized and needs further investigation
    # The authenticated endpoint also doesn't work as expected

    async def upload_form_file(
        self, file_upload: FormFileUploadRequest
    ) -> Dict[str, Any]:
        """Upload a file to a form's custom field

        Args:
            file_upload: File upload request with base64 content

        Returns:
            Upload response
        """
        # Decode base64 file content
        file_content = base64.b64decode(file_upload.fileContent)

        # Prepare multipart form data
        files = {
            "file": (file_upload.fileName, file_content, file_upload.contentType),
        }
        data = {
            "fieldId": file_upload.fieldId,
        }

        # Override headers to remove Content-Type (httpx will set it with boundary)
        headers = await self._get_headers(file_upload.locationId)
        headers.pop("Content-Type", None)

        response = await self.client.post(
            f"{self.API_BASE_URL}/forms/upload-custom-files",
            params={
                "contactId": file_upload.contactId,
                "locationId": file_upload.locationId,
            },
            files=files,
            data=data,
            headers=headers,
        )

        if response.status_code >= 400:
            from ..utils.exceptions import handle_api_error

            handle_api_error(response)

        return response.json()
