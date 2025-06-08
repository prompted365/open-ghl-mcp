"""Opportunity and pipeline management client for GoHighLevel API v2"""

from typing import List, Optional

from .base import BaseGoHighLevelClient
from ..models.opportunity import (
    Opportunity,
    OpportunityCreate,
    OpportunityUpdate,
    OpportunitySearchResult,
    OpportunitySearchFilters,
    Pipeline,
    PipelineStage,
)


class OpportunitiesClient(BaseGoHighLevelClient):
    """Client for opportunity and pipeline endpoints"""

    async def get_opportunities(
        self,
        location_id: str,
        limit: int = 100,
        skip: int = 0,
        filters: Optional[OpportunitySearchFilters] = None,
    ) -> OpportunitySearchResult:
        """Get opportunities for a location"""
        params = {"location_id": location_id, "limit": limit}

        if skip > 0:
            params["skip"] = skip

        if filters:
            filter_data = filters.model_dump(exclude_none=True)
            for key, value in filter_data.items():
                if key in ["startDate", "endDate"] and value:
                    params[key] = value.isoformat()
                elif value is not None:
                    params[key] = value

        response = await self._request(
            "GET", "/opportunities/search", params=params, location_id=location_id
        )
        data = response.json()
        return OpportunitySearchResult(
            opportunities=[Opportunity(**o) for o in data.get("opportunities", [])],
            meta=data.get("meta"),
            aggregations=data.get("aggregations"),
        )

    async def get_opportunity(
        self, opportunity_id: str, location_id: str
    ) -> Opportunity:
        """Get a specific opportunity"""
        response = await self._request(
            "GET",
            f"/opportunities/{opportunity_id}",
            params={"locationId": location_id},
            location_id=location_id,
        )
        data = response.json()
        return Opportunity(**data.get("opportunity", data))

    async def create_opportunity(self, opportunity: OpportunityCreate) -> Opportunity:
        """Create a new opportunity"""
        response = await self._request(
            "POST",
            "/opportunities",
            json=opportunity.model_dump(exclude_none=True),
            location_id=opportunity.locationId,
        )
        data = response.json()
        return Opportunity(**data.get("opportunity", data))

    async def update_opportunity(
        self, opportunity_id: str, updates: OpportunityUpdate, location_id: str
    ) -> Opportunity:
        """Update an existing opportunity"""
        response = await self._request(
            "PUT",
            f"/opportunities/{opportunity_id}",
            json=updates.model_dump(exclude_none=True),
            location_id=location_id,
        )
        data = response.json()
        return Opportunity(**data.get("opportunity", data))

    async def delete_opportunity(self, opportunity_id: str, location_id: str) -> bool:
        """Delete an opportunity"""
        response = await self._request(
            "DELETE",
            f"/opportunities/{opportunity_id}",
            params={"locationId": location_id},
            location_id=location_id,
        )
        return response.status_code == 200

    async def update_opportunity_status(
        self, opportunity_id: str, status: str, location_id: str
    ) -> Opportunity:
        """Update opportunity status"""
        response = await self._request(
            "PUT",
            f"/opportunities/{opportunity_id}/status",
            json={"locationId": location_id, "status": status},
            location_id=location_id,
        )
        data = response.json()
        return Opportunity(**data.get("opportunity", data))

    async def get_pipelines(self, location_id: str) -> List[Pipeline]:
        """Get all pipelines for a location"""
        response = await self._request("GET", "/pipelines", location_id=location_id)
        data = response.json()
        return [Pipeline(**p) for p in data.get("pipelines", [])]

    async def get_pipeline(self, pipeline_id: str, location_id: str) -> Pipeline:
        """Get a specific pipeline"""
        response = await self._request(
            "GET", f"/pipelines/{pipeline_id}", location_id=location_id
        )
        data = response.json()
        return Pipeline(**data.get("pipeline", data))

    async def get_pipeline_stages(
        self, pipeline_id: str, location_id: str
    ) -> List[PipelineStage]:
        """Get stages for a specific pipeline"""
        response = await self._request(
            "GET", f"/pipelines/{pipeline_id}/stages", location_id=location_id
        )
        data = response.json()
        return [PipelineStage(**s) for s in data.get("stages", [])]
