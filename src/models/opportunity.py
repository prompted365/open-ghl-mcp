"""Opportunity models for GoHighLevel API v2"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class OpportunityStatus(str, Enum):
    """Opportunity status values"""

    OPEN = "open"
    WON = "won"
    LOST = "lost"
    ABANDONED = "abandoned"


class OpportunityCreate(BaseModel):
    """Model for creating an opportunity"""

    pipelineId: str = Field(
        ..., description="Pipeline ID where the opportunity will be created"
    )
    locationId: str = Field(..., description="Location ID")
    name: str = Field(..., description="Opportunity name")
    pipelineStageId: str = Field(..., description="Pipeline stage ID")
    status: OpportunityStatus = Field(
        default=OpportunityStatus.OPEN, description="Opportunity status"
    )
    contactId: str = Field(
        ..., description="Contact ID associated with the opportunity"
    )
    monetaryValue: Optional[float] = Field(
        None, description="Monetary value of the opportunity"
    )
    assignedTo: Optional[str] = Field(None, description="User ID of the assigned user")

    # Additional fields
    source: Optional[str] = Field(None, description="Source of the opportunity")
    # NOTE: notes field is not accepted on creation - returns 422 error
    customFields: Optional[List[Dict[str, Any]]] = Field(
        None, description="Custom field values"
    )


class OpportunityUpdate(BaseModel):
    """Model for updating an opportunity"""

    # NOTE: locationId should NOT be in request body - causes 422 error
    name: Optional[str] = Field(None, description="Opportunity name")
    pipelineStageId: Optional[str] = Field(None, description="Pipeline stage ID")
    status: Optional[OpportunityStatus] = Field(None, description="Opportunity status")
    monetaryValue: Optional[float] = Field(
        None, description="Monetary value of the opportunity"
    )
    assignedTo: Optional[str] = Field(None, description="User ID of the assigned user")
    source: Optional[str] = Field(None, description="Source of the opportunity")
    # NOTE: notes field is not accepted on updates - returns 422 error
    customFields: Optional[List[Dict[str, Any]]] = Field(
        None, description="Custom field values"
    )


class Pipeline(BaseModel):
    """Pipeline model"""

    id: str = Field(..., description="Pipeline ID")
    name: str = Field(..., description="Pipeline name")
    # locationId not returned in list response
    stages: Optional[List["PipelineStage"]] = Field(None, description="Pipeline stages")
    dateAdded: Optional[Union[datetime, str]] = Field(
        None, description="Date pipeline was added"
    )
    dateUpdated: Optional[Union[datetime, str]] = Field(
        None, description="Date pipeline was updated"
    )
    originId: Optional[str] = Field(None, description="Origin ID")

    @field_validator("dateAdded", "dateUpdated", mode="before")
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            # Handle GoHighLevel datetime format: "2025-06-08T03:01:58.848Z"
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    # Remove Z and add timezone info
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    # Try standard ISO format
                    return datetime.fromisoformat(v)
                else:
                    # Fallback for other formats
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                # If parsing fails, return None to handle missing/invalid dates
                return None
        return v


class PipelineStage(BaseModel):
    """Pipeline stage model"""

    id: str = Field(..., description="Stage ID")
    name: str = Field(..., description="Stage name")
    position: int = Field(..., description="Stage position in pipeline")
    # pipelineId not returned in nested stages
    originId: Optional[str] = Field(None, description="Origin ID")
    showInFunnel: Optional[bool] = Field(None, description="Show in funnel view")
    showInPieChart: Optional[bool] = Field(None, description="Show in pie chart")


class Attribution(BaseModel):
    """Attribution model for opportunity sources"""

    utmSessionSource: Optional[str] = Field(None, description="UTM session source")
    medium: Optional[str] = Field(None, description="Medium")
    mediumId: Optional[str] = Field(None, description="Medium ID")
    url: Optional[str] = Field(None, description="Attribution URL")
    isFirst: Optional[bool] = Field(None, description="Is first attribution")
    isLast: Optional[bool] = Field(None, description="Is last attribution")


class Relation(BaseModel):
    """Relation model for opportunity associations"""

    associationId: str = Field(..., description="Association ID")
    relationId: str = Field(..., description="Relation ID")
    primary: bool = Field(..., description="Is primary relation")
    objectKey: str = Field(..., description="Object key")
    recordId: str = Field(..., description="Record ID")
    fullName: str = Field(..., description="Full name")
    contactName: str = Field(..., description="Contact name")
    companyName: Optional[str] = Field(None, description="Company name")
    email: str = Field(..., description="Email")
    phone: Optional[str] = Field(None, description="Phone")
    tags: List[str] = Field(default_factory=list, description="Tags")
    attributed: Optional[bool] = Field(None, description="Is attributed")


class Contact(BaseModel):
    """Contact model nested in opportunity"""

    id: str = Field(..., description="Contact ID")
    name: str = Field(..., description="Contact name")
    companyName: Optional[str] = Field(None, description="Company name")
    email: str = Field(..., description="Email")
    phone: Optional[str] = Field(None, description="Phone")
    tags: List[str] = Field(default_factory=list, description="Tags")
    score: List[Any] = Field(default_factory=list, description="Contact score")


class Opportunity(BaseModel):
    """Complete opportunity model from API response"""

    # Core fields
    id: str = Field(..., description="Opportunity ID")
    name: str = Field(..., description="Opportunity name")
    pipelineId: str = Field(..., description="Pipeline ID")
    pipelineStageId: str = Field(..., description="Pipeline stage ID")
    pipelineStageUId: Optional[str] = Field(None, description="Pipeline stage UID")
    assignedTo: Optional[str] = Field(None, description="User ID of assigned user")
    status: OpportunityStatus = Field(..., description="Opportunity status")
    source: Optional[str] = Field(None, description="Source of the opportunity")

    # Timestamps
    lastStatusChangeAt: Optional[Union[datetime, str]] = Field(
        None, description="Last status change timestamp"
    )
    lastStageChangeAt: Optional[Union[datetime, str]] = Field(
        None, description="Last stage change timestamp"
    )
    createdAt: Union[datetime, str] = Field(..., description="Creation timestamp")
    updatedAt: Union[datetime, str] = Field(..., description="Last update timestamp")

    @field_validator(
        "createdAt",
        "updatedAt",
        "lastStatusChangeAt",
        "lastStageChangeAt",
        mode="before",
    )
    @classmethod
    def parse_datetime(cls, v):
        """Parse datetime from string or return as-is if already datetime"""
        if isinstance(v, str):
            # Handle GoHighLevel datetime format: "2025-06-08T03:01:58.848Z"
            from datetime import datetime

            try:
                if v.endswith("Z"):
                    # Remove Z and add timezone info
                    return datetime.fromisoformat(v.replace("Z", "+00:00"))
                elif "T" in v:
                    # Try standard ISO format
                    return datetime.fromisoformat(v)
                else:
                    # Fallback for other formats
                    return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                # If parsing fails, return None to handle missing/invalid dates
                return None
        return v

    # Contact information
    contactId: str = Field(..., description="Associated contact ID")
    contact: Optional[Contact] = Field(None, description="Contact details")

    # Financial information
    monetaryValue: Optional[float] = Field(None, description="Monetary value")

    # Location information
    locationId: str = Field(..., description="Location ID")

    # Notes
    notes: Optional[str] = Field(None, description="Opportunity notes")

    # Additional fields
    indexVersion: Optional[int] = Field(None, description="Index version")
    customFields: List[Dict[str, Any]] = Field(
        default_factory=list, description="Custom field values"
    )
    lostReasonId: Optional[str] = Field(None, description="Lost reason ID")
    followers: List[str] = Field(default_factory=list, description="Follower IDs")
    relations: List[Relation] = Field(
        default_factory=list, description="Related records"
    )
    sort: Optional[List[Any]] = Field(None, description="Sort criteria")
    attributions: List[Attribution] = Field(
        default_factory=list, description="Attribution data"
    )

    # Additional fields from single opportunity response
    isAttribute: Optional[bool] = Field(None, description="Is attribute flag")
    lastActionDate: Optional[Union[datetime, str]] = Field(
        None, description="Last action date"
    )
    internalSource: Optional[Dict[str, Any]] = Field(
        None, description="Internal source information"
    )

    # Pipeline information (populated in responses)
    pipeline: Optional[Pipeline] = Field(None, description="Pipeline details")
    stage: Optional[PipelineStage] = Field(None, description="Current stage details")


class Meta(BaseModel):
    """Pagination metadata"""

    total: int = Field(..., description="Total count of opportunities")
    nextPageUrl: Optional[str] = Field(None, description="URL for next page")
    startAfterId: Optional[str] = Field(
        None, description="ID to start after for pagination"
    )
    startAfter: Optional[int] = Field(
        None, description="Timestamp to start after for pagination"
    )
    currentPage: int = Field(..., description="Current page number")
    nextPage: Optional[str] = Field(None, description="Next page identifier")
    prevPage: Optional[str] = Field(None, description="Previous page identifier")


class Aggregations(BaseModel):
    """Pipeline aggregation data"""

    pipelines: Dict[str, Any] = Field(
        default_factory=dict, description="Pipeline aggregation data"
    )


class OpportunitySearchResult(BaseModel):
    """Result model for opportunity search"""

    opportunities: List[Opportunity] = Field(
        default_factory=list, description="List of opportunities"
    )
    meta: Optional[Meta] = Field(None, description="Pagination metadata")
    aggregations: Optional[Aggregations] = Field(
        None, description="Pipeline aggregations"
    )

    @property
    def total(self) -> Optional[int]:
        """Get total count from meta"""
        return self.meta.total if self.meta else None

    @property
    def count(self) -> int:
        """Get count of opportunities in this response"""
        return len(self.opportunities)


class OpportunitySearchFilters(BaseModel):
    """Search filters for opportunities"""

    pipelineId: Optional[str] = Field(None, description="Filter by pipeline ID")
    pipelineStageId: Optional[str] = Field(
        None, description="Filter by pipeline stage ID"
    )
    assignedTo: Optional[str] = Field(None, description="Filter by assigned user ID")
    status: Optional[OpportunityStatus] = Field(None, description="Filter by status")
    contactId: Optional[str] = Field(None, description="Filter by contact ID")
    startDate: Optional[datetime] = Field(
        None, description="Start date for date range filter"
    )
    endDate: Optional[datetime] = Field(
        None, description="End date for date range filter"
    )
    query: Optional[str] = Field(None, description="Search query for opportunity name")


# Update Pipeline model to resolve forward reference
Pipeline.model_rebuild()
