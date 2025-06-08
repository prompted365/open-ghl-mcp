from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class FormField(BaseModel):
    """Form field definition"""

    id: str
    label: str
    type: str  # text, email, phone, textarea, dropdown, checkbox, radio, file, date, time, number
    required: bool = False
    placeholder: Optional[str] = None
    options: Optional[List[str]] = None  # For dropdown, radio, checkbox
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    pattern: Optional[str] = None


class FormSettings(BaseModel):
    """Form settings configuration"""

    captchaEnabled: Optional[bool] = None
    emailNotifications: Optional[bool] = None
    assignToUser: Optional[str] = None
    redirectUrl: Optional[str] = None
    thankYouMessage: Optional[str] = None


class Form(BaseModel):
    """GoHighLevel Form model"""

    id: str
    name: str
    locationId: str
    description: Optional[str] = None
    isActive: bool = True
    fields: List[FormField] = Field(default_factory=list)
    settings: Optional[FormSettings] = None
    thankYouMessage: Optional[str] = None
    redirectUrl: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class FormList(BaseModel):
    """Response model for form list"""

    forms: List[Form]
    total: Optional[int] = None
    count: Optional[int] = None


class FormSubmissionData(BaseModel):
    """Submission data with dynamic fields"""

    # Standard fields
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None

    # Allow additional fields for custom form fields
    model_config = {"extra": "allow", "populate_by_name": True}


class FormSubmission(BaseModel):
    """GoHighLevel Form Submission model"""

    id: str
    formId: str
    contactId: str
    locationId: str
    data: Dict[str, Any]  # Flexible to handle standard and custom fields
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
    submittedAt: datetime
    attributionSource: Optional[str] = None
    lastAttributionSource: Optional[str] = None

    model_config = {"populate_by_name": True}


class FormSubmissionList(BaseModel):
    """Response model for form submission list"""

    submissions: List[FormSubmission]
    total: Optional[int] = None
    count: Optional[int] = None


class FormSubmitRequest(BaseModel):
    """Request model for form submission"""

    formId: str
    locationId: str

    # Standard fields
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    message: Optional[str] = None

    # Allow custom fields
    customFields: Optional[Dict[str, Any]] = Field(default_factory=dict)

    def to_form_data(self) -> Dict[str, Any]:
        """Convert to format expected by form submit endpoint"""
        data = {"formId": self.formId, "locationId": self.locationId}

        # Add standard fields if provided
        if self.firstName:
            data["firstName"] = self.firstName
        if self.lastName:
            data["lastName"] = self.lastName
        if self.email:
            data["email"] = self.email
        if self.phone:
            data["phone"] = self.phone
        if self.company:
            data["company"] = self.company
        if self.message:
            data["message"] = self.message

        # Add custom fields directly to data
        if self.customFields:
            data.update(self.customFields)

        return data


class FormSubmitResponse(BaseModel):
    """Response model for form submission"""

    success: bool
    submissionId: Optional[str] = None
    contactId: Optional[str] = None
    message: Optional[str] = None
    redirectUrl: Optional[str] = None


class FormFileUploadRequest(BaseModel):
    """Request model for file upload to form field"""

    contactId: str
    locationId: str
    fieldId: str
    fileName: str
    fileContent: str  # Base64 encoded file content
    contentType: Optional[str] = "application/octet-stream"


class FormSearchParams(BaseModel):
    """Parameters for searching forms"""

    locationId: str
    limit: int = Field(default=100, ge=1, le=100)
    skip: int = Field(default=0, ge=0)


class FormSubmissionSearchParams(BaseModel):
    """Parameters for searching form submissions"""

    locationId: str
    formId: Optional[str] = None
    contactId: Optional[str] = None
    startDate: Optional[str] = None  # YYYY-MM-DD format
    endDate: Optional[str] = None  # YYYY-MM-DD format
    limit: int = Field(default=100, ge=1, le=100)
    skip: int = Field(default=0, ge=0)
    page: Optional[int] = None
