"""Opportunity parameter classes for MCP tools"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from ...models.opportunity import OpportunityStatus


class GetOpportunitiesParams(BaseModel):
    """Parameters for getting opportunities"""

    location_id: str = Field(..., description="The location ID")
    pipeline_id: Optional[str] = Field(None, description="Filter by pipeline ID")
    pipeline_stage_id: Optional[str] = Field(
        None, description="Filter by pipeline stage ID"
    )
    assigned_to: Optional[str] = Field(None, description="Filter by assigned user ID")
    status: Optional[OpportunityStatus] = Field(None, description="Filter by status")
    contact_id: Optional[str] = Field(None, description="Filter by contact ID")
    query: Optional[str] = Field(None, description="Search query for opportunity name")
    limit: int = Field(100, description="Number of results to return", ge=1, le=100)
    skip: int = Field(0, description="Number of results to skip", ge=0)
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetOpportunityParams(BaseModel):
    """Parameters for getting a single opportunity"""

    opportunity_id: str = Field(..., description="The opportunity ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class CreateOpportunityParams(BaseModel):
    """Parameters for creating an opportunity"""

    location_id: str = Field(..., description="The location ID")
    pipeline_id: str = Field(
        ..., description="Pipeline ID where the opportunity will be created"
    )
    name: str = Field(..., description="Opportunity name")
    pipeline_stage_id: str = Field(..., description="Pipeline stage ID")
    contact_id: str = Field(
        ..., description="Contact ID associated with the opportunity"
    )
    status: Optional[OpportunityStatus] = Field(
        default=OpportunityStatus.OPEN, description="Opportunity status"
    )
    monetary_value: Optional[float] = Field(
        None, description="Monetary value of the opportunity"
    )
    assigned_to: Optional[str] = Field(None, description="User ID of the assigned user")
    source: Optional[str] = Field(None, description="Source of the opportunity")
    notes: Optional[str] = Field(None, description="Notes about the opportunity")
    custom_fields: Optional[Dict[str, Any]] = Field(
        None, description="Custom field values"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class UpdateOpportunityParams(BaseModel):
    """Parameters for updating an opportunity"""

    opportunity_id: str = Field(..., description="The opportunity ID")
    location_id: str = Field(..., description="The location ID")
    name: Optional[str] = Field(None, description="Opportunity name")
    pipeline_stage_id: Optional[str] = Field(None, description="Pipeline stage ID")
    status: Optional[OpportunityStatus] = Field(None, description="Opportunity status")
    monetary_value: Optional[float] = Field(
        None, description="Monetary value of the opportunity"
    )
    assigned_to: Optional[str] = Field(None, description="User ID of the assigned user")
    source: Optional[str] = Field(None, description="Source of the opportunity")
    notes: Optional[str] = Field(None, description="Notes about the opportunity")
    custom_fields: Optional[Dict[str, Any]] = Field(
        None, description="Custom field values"
    )
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class DeleteOpportunityParams(BaseModel):
    """Parameters for deleting an opportunity"""

    opportunity_id: str = Field(..., description="The opportunity ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class UpdateOpportunityStatusParams(BaseModel):
    """Parameters for updating opportunity status"""

    opportunity_id: str = Field(..., description="The opportunity ID")
    location_id: str = Field(..., description="The location ID")
    status: OpportunityStatus = Field(..., description="New status for the opportunity")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetPipelinesParams(BaseModel):
    """Parameters for getting pipelines"""

    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetPipelineParams(BaseModel):
    """Parameters for getting a single pipeline"""

    pipeline_id: str = Field(..., description="The pipeline ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )


class GetPipelineStagesParams(BaseModel):
    """Parameters for getting pipeline stages"""

    pipeline_id: str = Field(..., description="The pipeline ID")
    location_id: str = Field(..., description="The location ID")
    access_token: Optional[str] = Field(
        None, description="Optional access token to use instead of stored token"
    )
