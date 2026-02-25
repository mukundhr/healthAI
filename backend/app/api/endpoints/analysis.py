"""
AccessAI Analysis API Endpoints
Handles medical report analysis using AI
"""

from fastapi import APIRouter, HTTPException
import logging
import time

from app.schemas import AnalysisResponse, AnalysisRequest, Language, ProcessingStatus
from app.services.aws_service import aws_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Import sessions store from documents endpoint
# In production, use a shared database/Redis
sessions_store = {}


@router.post("/explain", response_model=AnalysisResponse)
async def analyze_medical_report(request: AnalysisRequest):
    """
    Analyze a medical report and generate simplified explanation.
    
    Uses Amazon Bedrock (Claude) to provide:
    - Plain language explanation
    - Doctor questions
    - Confidence scores
    """
    # Get session
    session = sessions_store.get(request.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("status") != ProcessingStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Document not ready for analysis. Status: {session.get('status')}"
        )
    
    # Get extracted text
    ocr_result = session.get("ocr_result", {})
    extracted_text = ocr_result.get("text", "")
    
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text extracted from document")
    
    start_time = time.time()
    
    try:
        # Generate AI explanation using Bedrock
        analysis_result = await aws_service.generate_medical_explanation(
            extracted_text=extracted_text,
            language=request.language.value,
            user_context=request.user_context
        )
        
        # Store analysis result
        session["analysis_result"] = analysis_result
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return AnalysisResponse(
            session_id=request.session_id,
            document_id=request.document_id,
            explanation=analysis_result["explanation"],
            explanation_sections=[],  # Could be parsed from explanation
            confidence=analysis_result["confidence"],
            ocr_confidence=ocr_result.get("confidence", 0),
            questions=analysis_result["questions"],
            language=Language(request.language),
            model=analysis_result["model"],
            processing_time_ms=processing_time_ms
        )
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/result/{session_id}")
async def get_analysis_result(session_id: str):
    """Get cached analysis result"""
    session = sessions_store.get(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    analysis_result = session.get("analysis_result")
    
    if not analysis_result:
        raise HTTPException(status_code=404, detail="No analysis result found")
    
    return analysis_result
