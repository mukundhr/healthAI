from fastapi import APIRouter, HTTPException
import logging
from datetime import datetime, timedelta

from app.schemas import AudioRequest, AudioResponse, Language
from app.services.aws_service import aws_service
from app.services.session_store import audio_cache

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/synthesize", response_model=AudioResponse)
async def synthesize_speech(request: AudioRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long. Maximum 5000 characters")

    # Check cache
    cached = audio_cache.get(request.text, request.language.value)
    if cached:
        logger.info("Returning cached audio")
        return AudioResponse(**cached)

    try:
        result = await aws_service.synthesize_speech(
            text=request.text,
            language=request.language.value,
        )

        # Rough duration estimate: ~150 words/minute for Indian languages
        word_count = len(request.text.split())
        duration_estimate = (word_count / 150) * 60

        response_data = {
            "audio_url": result["audio_url"],
            "audio_key": result["audio_key"],
            "voice_id": result["voice_id"],
            "language": Language(request.language),
            "duration_estimate_seconds": round(duration_estimate, 1),
            "expires_at": datetime.now() + timedelta(hours=1),
        }

        # Cache the result
        audio_cache.set(request.text, request.language.value, response_data)

        return AudioResponse(**response_data)

    except Exception as e:
        logger.error(f"Speech synthesis error: {e}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")


@router.post("/synthesize-explanation")
async def synthesize_explanation(explanation: str, language: str = "hi"):
    if not explanation:
        raise HTTPException(status_code=400, detail="Explanation cannot be empty")

    if len(explanation) > 3000:
        explanation = explanation[:3000] + "..."

    # Check cache
    cached = audio_cache.get(explanation, language)
    if cached:
        return cached

    try:
        result = await aws_service.synthesize_speech(
            text=explanation,
            language=language,
        )

        response = {
            "audio_url": result["audio_url"],
            "voice_id": result["voice_id"],
            "language": language,
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
        }

        audio_cache.set(explanation, language, response)
        return response

    except Exception as e:
        logger.error(f"Explanation synthesis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
