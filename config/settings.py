"""
Production Configuration Management
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    API_TITLE: str = "Production Fraud Detection API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Enterprise-grade fraud detection system for financial institutions"
    
    # Model Paths
    MODEL_DIR: str = "models"
    FRAUD_MODEL_PATH: str = "models/fraud_model.pkl"
    ANOMALY_MODEL_PATH: str = "models/anomaly_model.pkl"
    SCALER_PATH: str = "models/scaler.pkl"
    
    # Business Logic
    DEFAULT_FRAUD_THRESHOLD: float = 0.35
    MAX_BATCH_SIZE: int = 1000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Performance
    REQUEST_TIMEOUT: int = 30
    MAX_WORKERS: int = 4
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()