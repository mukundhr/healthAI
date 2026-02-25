from fastapi import APIRouter, HTTPException
import logging

from app.schemas import SchemeMatchRequest, SchemeMatchResponse
from app.services.knowledge_retrieval import knowledge_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Scheme application links (in production, fetch from database)
SCHEME_LINKS = {
    "scheme_001": "https://pmjay.gov.in",
    "scheme_002": "https://arogya.karnataka.gov.in",
    "scheme_003": "https://www.jtyogya.in",
    "scheme_004": "https://www.tn.gov.in",
    "scheme_005": "https://nhm.gov.in",
    "scheme_006": "https://pmsma.nhp.gov.in"
}


@router.post("/match", response_model=SchemeMatchResponse)
async def match_schemes(request: SchemeMatchRequest):

    try:
        # Initialize knowledge service if needed
        knowledge_service.initialize()
        
        # Find matching schemes
        schemes = await knowledge_service.match_schemes(
            state=request.state,
            income_range=request.income_range,
            age=request.age,
            is_bpl=request.is_bpl,
            conditions=request.conditions
        )
        
        # Add application links
        for scheme in schemes:
            scheme["apply_link"] = SCHEME_LINKS.get(scheme["id"])
        
        return SchemeMatchResponse(
            schemes=schemes,
            count=len(schemes)
        )
    except Exception as e:
        logger.error(f"Scheme matching error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scheme matching failed: {str(e)}")


@router.get("/search")
async def search_schemes(
    state: str = None,
    query: str = None,
    scheme_type: str = None
):

    try:
        knowledge_service.initialize()
        
        # For now, return all schemes filtered
        all_schemes = knowledge_service.schemes_metadata
        
        # Filter by state
        if state:
            state_normalized = state.lower().replace(" ", "_")
            all_schemes = [
                s for s in all_schemes
                if s["state"] == "all_india" or s["state"] == state_normalized
            ]
        
        # Filter by type
        if scheme_type:
            all_schemes = [s for s in all_schemes if s["type"] == scheme_type]
        
        # Filter by query
        if query:
            query_lower = query.lower()
            all_schemes = [
                s for s in all_schemes
                if query_lower in s["name"].lower() or
                   any(query_lower in kw for kw in s.get("keywords", []))
            ]
        
        # Add links
        for scheme in all_schemes:
            scheme["apply_link"] = SCHEME_LINKS.get(scheme["id"])
        
        return {
            "schemes": all_schemes,
            "count": len(all_schemes)
        }
    except Exception as e:
        logger.error(f"Scheme search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/{scheme_id}")
async def get_scheme_details(scheme_id: str):
    try:
        knowledge_service.initialize()
        
        # Find scheme by ID
        for scheme in knowledge_service.schemes_metadata:
            if scheme["id"] == scheme_id:
                scheme_copy = dict(scheme)
                scheme_copy["apply_link"] = SCHEME_LINKS.get(scheme_id)
                return scheme_copy
        
        raise HTTPException(status_code=404, detail="Scheme not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scheme details error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
