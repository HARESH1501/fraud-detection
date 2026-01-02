"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class UserFriendlyTransactionRequest(BaseModel):
    """User-friendly transaction request model"""
    Time: float = Field(..., ge=0, description="Transaction time (seconds from first transaction)")
    Amount: float = Field(..., ge=0, description="Transaction amount")
    
    # User-friendly fields
    merchant_type: str = Field(..., description="Type of merchant")
    transaction_type: str = Field(..., description="Type of transaction")
    location_risk: str = Field(..., description="Location risk level")
    hour_of_day: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    customer_age_days: int = Field(..., ge=1, description="Customer account age in days")
    daily_transactions: int = Field(..., ge=1, description="Average daily transactions")
    
    # Optional threshold override
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Custom fraud threshold")
    
    @validator('Amount')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v


class TransactionRequest(BaseModel):
    """Single transaction request model (legacy support)"""
    Time: float = Field(..., ge=0, description="Transaction time (seconds from first transaction)")
    Amount: float = Field(..., ge=0, description="Transaction amount")
    
    # PCA Features V1-V28
    V1: float = Field(default=0.0, description="PCA component 1")
    V2: float = Field(default=0.0, description="PCA component 2")
    V3: float = Field(default=0.0, description="PCA component 3")
    V4: float = Field(default=0.0, description="PCA component 4")
    V5: float = Field(default=0.0, description="PCA component 5")
    V6: float = Field(default=0.0, description="PCA component 6")
    V7: float = Field(default=0.0, description="PCA component 7")
    V8: float = Field(default=0.0, description="PCA component 8")
    V9: float = Field(default=0.0, description="PCA component 9")
    V10: float = Field(default=0.0, description="PCA component 10")
    V11: float = Field(default=0.0, description="PCA component 11")
    V12: float = Field(default=0.0, description="PCA component 12")
    V13: float = Field(default=0.0, description="PCA component 13")
    V14: float = Field(default=0.0, description="PCA component 14")
    V15: float = Field(default=0.0, description="PCA component 15")
    V16: float = Field(default=0.0, description="PCA component 16")
    V17: float = Field(default=0.0, description="PCA component 17")
    V18: float = Field(default=0.0, description="PCA component 18")
    V19: float = Field(default=0.0, description="PCA component 19")
    V20: float = Field(default=0.0, description="PCA component 20")
    V21: float = Field(default=0.0, description="PCA component 21")
    V22: float = Field(default=0.0, description="PCA component 22")
    V23: float = Field(default=0.0, description="PCA component 23")
    V24: float = Field(default=0.0, description="PCA component 24")
    V25: float = Field(default=0.0, description="PCA component 25")
    V26: float = Field(default=0.0, description="PCA component 26")
    V27: float = Field(default=0.0, description="PCA component 27")
    V28: float = Field(default=0.0, description="PCA component 28")
    
    # Optional threshold override
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Custom fraud threshold")
    
    @validator('Amount')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v


class BatchTransactionRequest(BaseModel):
    """Batch transaction request model"""
    transactions: List[TransactionRequest] = Field(..., min_items=1, max_items=1000)
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Custom fraud threshold for all transactions")


class PredictionResponse(BaseModel):
    """Fraud prediction response model"""
    fraud_probability: float = Field(..., description="Probability of fraud (0-1)")
    anomaly_detected: bool = Field(..., description="Whether anomaly was detected")
    risk_score: str = Field(..., description="Risk level: LOW, MEDIUM, HIGH, CRITICAL")
    threshold_used: float = Field(..., description="Threshold used for decision")
    final_decision: str = Field(..., description="FRAUD or LEGITIMATE")
    confidence: str = Field(..., description="Prediction confidence: LOW, MEDIUM, HIGH")
    explanation: str = Field(..., description="Human-readable explanation")
    timestamp: str = Field(..., description="Prediction timestamp (ISO format)")


class HybridPredictionResponse(BaseModel):
    """Enhanced fraud prediction response model with hybrid analysis"""
    fraud_probability: float = Field(..., description="ML fraud probability (0-1)")
    anomaly_detected: bool = Field(..., description="Whether anomaly was detected")
    rule_risk_score: int = Field(..., description="Rule-based risk score (0-10)")
    rule_risk_level: str = Field(..., description="Rule risk level: LOW, MEDIUM, HIGH, CRITICAL")
    rule_risk_factors: List[str] = Field(..., description="List of detected risk factors")
    combined_risk_score: str = Field(..., description="Combined risk level: LOW, MEDIUM, HIGH, CRITICAL")
    threshold_used: float = Field(..., description="ML threshold used for decision")
    final_decision: str = Field(..., description="FRAUD or LEGITIMATE")
    decision_reason: str = Field(..., description="Reason for the decision")
    confidence: str = Field(..., description="Decision confidence: LOW, MEDIUM, HIGH")
    explanation: str = Field(..., description="Comprehensive explanation")
    ml_analysis: Dict[str, Any] = Field(..., description="ML model analysis details")
    rule_analysis: Dict[str, Any] = Field(..., description="Rule engine analysis details")
    timestamp: str = Field(..., description="Prediction timestamp (ISO format)")


class BatchPredictionResponse(BaseModel):
    """Batch prediction response model"""
    results: List[PredictionResponse] = Field(..., description="Individual prediction results")
    summary: Dict[str, Any] = Field(..., description="Batch processing summary")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    models_loaded: Dict[str, bool] = Field(..., description="Model loading status")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: str = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")