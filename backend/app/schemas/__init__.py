"""
AccessAI Pydantic Schemas
Request and response models for API endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class ProcessingStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Language(str, Enum):
    """Supported output languages"""
    ENGLISH = "en"
    HINDI = "hi"
    KANNADA = "kn"


# ==================== Document Schemas ====================

class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    session_id: str
    document_id: str
    file_name: str
    file_size: int
    status: ProcessingStatus
    message: str


class DocumentStatusResponse(BaseModel):
    """Document processing status"""
    session_id: str
    document_id: str
    status: ProcessingStatus
    ocr_confidence: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ==================== Analysis Schemas ====================

class AnalysisRequest(BaseModel):
    """Request for medical analysis"""
    session_id: str
    document_id: str
    language: Language = Language.ENGLISH
    user_context: Optional[Dict[str, Any]] = None


class ExplanationSection(BaseModel):
    """Section of the medical explanation"""
    title: str
    content: str
    type: str = "general"  # general, warning, info


class AnalysisResponse(BaseModel):
    """Response for medical analysis"""
    session_id: str
    document_id: str
    explanation: str
    explanation_sections: List[ExplanationSection] = []
    confidence: int
    ocr_confidence: float
    questions: List[str]
    language: Language
    model: str
    processing_time_ms: int


# ==================== Scheme Schemas ====================

class SchemeMatchRequest(BaseModel):
    """Request for scheme matching"""
    state: str = Field(..., description="User's state")
    income_range: str = Field(..., description="Income range (below-1l, 1l-3l, 3l-5l, above-5l)")
    age: int = Field(..., ge=0, le=150, description="User's age")
    is_bpl: bool = Field(default=False, description="BPL card holder")
    conditions: Optional[List[str]] = Field(default=None, description="Medical conditions")


class SchemeInfo(BaseModel):
    """Government scheme information"""
    id: str
    name: str
    type: str
    coverage: str
    eligibility: List[str]
    documents_required: List[str]
    benefits: List[str]
    state: str
    match_reason: str
    apply_link: Optional[str] = None


class SchemeMatchResponse(BaseModel):
    """Response for scheme matching"""
    schemes: List[SchemeInfo]
    count: int


# ==================== Audio Schemas ====================

class AudioRequest(BaseModel):
    """Request for text-to-speech synthesis"""
    text: str = Field(..., min_length=1, max_length=5000)
    language: Language = Language.HINDI
    session_id: Optional[str] = None


class AudioResponse(BaseModel):
    """Response for audio synthesis"""
    audio_url: str
    audio_key: str
    voice_id: str
    language: Language
    expires_at: datetime


# ==================== Health Check ====================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    environment: str
    services: Dict[str, str]
    timestamp: datetime
