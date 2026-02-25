"""
AccessAI Document API Endpoints
Handles document upload and processing
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import uuid
import logging
from datetime import datetime

from app.schemas import DocumentUploadResponse, ProcessingStatus
from app.services.aws_service import aws_service
from app.services.knowledge_retrieval import knowledge_service

logger = logging.getLogger(__name__)
router = APIRouter()


# In-memory session storage (in production, use Redis or database)
sessions_store = {}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a medical document for processing.
    
    Supported formats: PDF, JPG, PNG, TIFF
    """
    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/tiff"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Validate file size (max 10MB)
    file_size = 0
    file_content = b""
    chunk = await file.read(1024 * 1024)  # 1MB chunks
    while chunk:
        file_content += chunk
        file_size += len(chunk)
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")
        chunk = await file.read(1024 * 1024)
    
    # Generate session and document IDs
    session_id = str(uuid.uuid4())
    document_id = str(uuid.uuid4())
    
    # Store session info
    sessions_store[session_id] = {
        "document_id": document_id,
        "file_name": file.filename,
        "file_size": file_size,
        "status": ProcessingStatus.PENDING,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "s3_info": None,
        "ocr_result": None,
        "analysis_result": None
    }
    
    # Upload to S3 in background
    try:
        s3_info = await aws_service.upload_document(
            file_content=file_content,
            file_name=file.filename,
            session_id=session_id
        )
        sessions_store[session_id]["s3_info"] = s3_info
        sessions_store[session_id]["status"] = ProcessingStatus.PENDING
        sessions_store[session_id]["updated_at"] = datetime.now()
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        sessions_store[session_id]["status"] = ProcessingStatus.FAILED
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    # Start OCR processing in background
    background_tasks.add_task(
        process_document,
        session_id=session_id,
        file_content=file_content,
        file_name=file.filename
    )
    
    return DocumentUploadResponse(
        session_id=session_id,
        document_id=document_id,
        file_name=file.filename,
        file_size=file_size,
        status=ProcessingStatus.PENDING,
        message="Document uploaded successfully. Processing started."
    )


async def process_document(session_id: str, file_content: bytes, file_name: str):
    """Background task to process document with Textract"""
    try:
        sessions_store[session_id]["status"] = ProcessingStatus.PROCESSING
        sessions_store[session_id]["updated_at"] = datetime.now()
        
        # Run OCR
        ocr_result = await aws_service.extract_text(file_content, file_name)
        
        sessions_store[session_id]["ocr_result"] = ocr_result
        sessions_store[session_id]["status"] = ProcessingStatus.COMPLETED
        sessions_store[session_id]["updated_at"] = datetime.now()
        
        logger.info(f"Document {session_id} processed successfully")
    except Exception as e:
        logger.error(f"Processing error for {session_id}: {str(e)}")
        sessions_store[session_id]["status"] = ProcessingStatus.FAILED
        sessions_store[session_id]["error_message"] = str(e)


@router.get("/status/{session_id}")
async def get_document_status(session_id: str):
    """Get the processing status of a document"""
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions_store[session_id]
    
    return {
        "session_id": session_id,
        "document_id": session["document_id"],
        "status": session["status"],
        "file_name": session["file_name"],
        "ocr_confidence": session.get("ocr_result", {}).get("confidence"),
        "created_at": session["created_at"],
        "updated_at": session["updated_at"]
    }


@router.get("/result/{session_id}")
async def get_document_result(session_id: str):
    """Get the OCR result of a processed document"""
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions_store[session_id]
    
    if session["status"] != ProcessingStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Document not ready. Current status: {session['status']}"
        )
    
    return {
        "session_id": session_id,
        "document_id": session["document_id"],
        "text": session.get("ocr_result", {}).get("text"),
        "confidence": session.get("ocr_result", {}).get("confidence"),
        "blocks_count": session.get("ocr_result", {}).get("blocks_count")
    }


@router.delete("/{session_id}")
async def delete_document(session_id: str):
    """Delete a document and its associated data"""
    if session_id not in sessions_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete from S3 if exists
    s3_info = sessions_store[session_id].get("s3_info")
    if s3_info:
        try:
            await aws_service.delete_document(s3_info["s3_key"])
        except Exception as e:
            logger.warning(f"Failed to delete S3 object: {str(e)}")
    
    # Remove from memory
    del sessions_store[session_id]
    
    return {"message": "Document deleted successfully"}
