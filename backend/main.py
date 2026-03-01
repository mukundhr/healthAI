from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.endpoints import documents, analysis, schemes, audio
from app.api.endpoints import notifications
from app.core import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AccessAI Backend...")
    logger.info(f"Environment: {config.settings.ENVIRONMENT}")
    
    # Initialize AWS services on startup
    from app.services import aws_service
    aws_service.initialize_services()
    
    yield
    
    logger.info("Shutting down AccessAI Backend...")


# Create FastAPI application
app = FastAPI(
    title="AccessAI API",
    description="Medical Report Analysis API with OCR, AI Explanation, and Text-to-Speech",
    version="1.0.0",
    docs_url="/docs" if config.settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if config.settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    documents.router,
    prefix="/api/v1/documents",
    tags=["Documents"]
)
app.include_router(
    analysis.router,
    prefix="/api/v1/analysis",
    tags=["Analysis"]
)
app.include_router(
    schemes.router,
    prefix="/api/v1/schemes",
    tags=["Schemes"]
)
app.include_router(
    audio.router,
    prefix="/api/v1/audio",
    tags=["Audio"]
)
app.include_router(
    notifications.router,
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AccessAI API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": config.settings.ENVIRONMENT
    }
