from fastapi import APIRouter, HTTPException
import logging
from datetime import datetime, timedelta

from app.schemas import AudioRequest, AudioResponse, Language
from app.services.aws_service import aws_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/synthesize", response_model=AudioResponse)
async def synthesize_speech(request: AudioRequest):

    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long. Maximum 5000 characters")
    
    try:
        result = await aws_service.synthesize_speech(
            text=request.text,
            language=request.language.value
        )
        
        return AudioResponse(
            audio_url=result["audio_url"],
            audio_key=result["audio_key"],
            voice_id=result["voice_id"],
            language=Language(request.language),
            expires_at=datetime.now() + timedelta(hours=1)
        )
    except Exception as e:
        logger.error(f"Speech synthesis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")


@router.post("/synthesize-explanation")
async def synthesize_explanation(
    explanation: str,
    language: str = "hi"
):
    if not explanation:
        raise HTTPException(status_code=400, detail="Explanation cannot be empty")
    
    # Truncate if too long (Polly has limits)
    if len(explanation) > 3000:
        explanation = explanation[:3000] + "..."
    
    try:
        result = await aws_service.synthesize_speech(
            text=explanation,
            language=language
        )
        
        return {
            "audio_url": result["audio_url"],
            "voice_id": result["voice_id"],
            "language": language,
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
        }
    except Exception as e:
        logger.error(f"Explanation synthesis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
