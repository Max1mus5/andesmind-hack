"""
Configuration settings for AndesMindHack Backend
"""

import os
from typing import Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "AndesMindHack API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str = "postgresql://neondb_owner:REPLACE_WITH_ACTUAL_PASSWORD@ep-round-wildflower-a8gy0ftu-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000"
    ]
    
    # Email settings (optional for MVP)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    DEFAULT_RATE_LIMIT: str = "100/minute"
    AUTH_RATE_LIMIT: str = "5/minute"
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"]
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        if "REPLACE_WITH_ACTUAL_PASSWORD" in v:
            raise ValueError("Please replace DATABASE_URL with actual credentials")
        return v
    
    @validator('JWT_SECRET_KEY')
    def validate_jwt_secret(cls, v):
        if v == "your-super-secret-jwt-key-change-in-production":
            if os.getenv("ENVIRONMENT") == "production":
                raise ValueError("Please change JWT_SECRET_KEY in production")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()