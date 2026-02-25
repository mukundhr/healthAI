from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):

    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Common dev server
        "http://127.0.0.1:5173",
    ]
    
    # AWS Configuration
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""  # Set via environment
    AWS_SECRET_ACCESS_KEY: str = ""  # Set via environment
    
    # AWS Services
    AWS_S3_BUCKET: str = "accessai-documents"
    AWS_TEXTTRACT_ROLE_ARN: str = ""  # Cross-account role for Textract
    AWS_BEDROCK_MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    AWS_POLLY_VOICE_ID_HINDI: str = "Aditi"
    AWS_POLLY_VOICE_ID_KANNADA: str = "Kajal"
    
    # Storage
    TEMP_UPLOAD_DIR: str = "/tmp/accessai/uploads"
    
    # API Keys (for alternative/LLM providers if needed)
    OPENAI_API_KEY: str = ""  # Fallback if Bedrock unavailable
    
    # Security
    API_KEY_HEADER: str = "X-API-Key"
    ENCRYPTION_KEY: str = ""  # For encrypting sensitive data
    
    # Session
    SESSION_TIMEOUT_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Global settings instance
settings = get_settings()
