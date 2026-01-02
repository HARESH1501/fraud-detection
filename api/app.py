
"""
Production Fraud Detection API
Enterprise-grade FastAPI application for real-time fraud detection
"""
import sys
import os
import time
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import uvicorn

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from api.models import (
    TransactionRequest, UserFriendlyTransactionRequest, BatchTransactionRequest, 
    PredictionResponse, HybridPredictionResponse, BatchPredictionResponse, HealthResponse, ErrorResponse
)
from services.ml_service import ml_service
from services.feature_generator import feature_generator

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application startup time
startup_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Fraud Detection API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Models loaded successfully")
    yield
    logger.info("Shutting down Fraud Detection API...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID for tracking"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="ValidationError",
            message=str(exc),
            timestamp=datetime.utcnow().isoformat(),
            request_id=getattr(request.state, 'request_id', None)
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            timestamp=datetime.utcnow().isoformat(),
            request_id=getattr(request.state, 'request_id', None)
        ).dict()
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring and load balancers
    """
    try:
        # Test model availability
        models_status = {
            "fraud_model": ml_service.fraud_model is not None,
            "anomaly_model": ml_service.anomaly_model is not None,
            "feature_service": True
        }
        
        uptime = time.time() - startup_time
        
        return HealthResponse(
            status="healthy" if all(models_status.values()) else "degraded",
            timestamp=datetime.utcnow().isoformat(),
            version=settings.API_VERSION,
            models_loaded=models_status,
            uptime_seconds=uptime
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_friendly": "/predict/friendly",
            "predict_batch": "/predict/batch",
            "docs": "/docs"
        }
    }


# Single transaction prediction (legacy)
@app.post("/predict", response_model=PredictionResponse)
async def predict_transaction(transaction: TransactionRequest, request: Request):
    """
    Predict fraud for a single transaction (legacy endpoint with V1-V28 features)
    
    - **Time**: Transaction time (seconds from first transaction)
    - **Amount**: Transaction amount (must be positive)
    - **V1-V28**: PCA-transformed features (optional, default to 0.0)
    - **threshold**: Custom fraud threshold (optional, overrides default)
    """
    try:
        logger.info(f"Processing single transaction prediction - Request ID: {request.state.request_id}")
        
        # Convert to dictionary for processing
        transaction_dict = transaction.dict()
        custom_threshold = transaction_dict.pop('threshold', None)
        
        # Get prediction
        result = ml_service.predict_single(transaction_dict, custom_threshold)
        
        logger.info(f"Prediction completed - Decision: {result['final_decision']}")
        return PredictionResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Validation error in prediction: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction service error")


# User-friendly transaction prediction
@app.post("/predict/friendly", response_model=HybridPredictionResponse)
async def predict_user_friendly_transaction(transaction: UserFriendlyTransactionRequest, request: Request):
    """
    Predict fraud for a single transaction using user-friendly inputs
    
    - **Time**: Transaction time (seconds from first transaction)
    - **Amount**: Transaction amount (must be positive)
    - **merchant_type**: Type of merchant (e.g., "Online Retail", "Gas Station")
    - **transaction_type**: Type of transaction (e.g., "Purchase", "Cash Withdrawal")
    - **location_risk**: Location risk level (e.g., "Low Risk (Home Country)")
    - **hour_of_day**: Hour when transaction occurred (0-23)
    - **customer_age_days**: Days since customer account creation
    - **daily_transactions**: Average number of transactions per day
    - **threshold**: Custom fraud threshold (optional, overrides default)
    """
    try:
        logger.info(f"Processing user-friendly transaction prediction - Request ID: {request.state.request_id}")
        
        # Convert user-friendly data to standard format with V1-V28 features
        user_data = transaction.dict()
        standard_data = feature_generator.convert_user_friendly_to_standard(user_data)
        
        # Extract threshold
        custom_threshold = user_data.pop('threshold', None)
        
        # Get hybrid prediction (ML + Rule-based)
        result = ml_service.predict_single_user_friendly(user_data, custom_threshold)
        
        logger.info(f"User-friendly prediction completed - Decision: {result['final_decision']}")
        return HybridPredictionResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Validation error in user-friendly prediction: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"User-friendly prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction service error")


# Batch transaction prediction
@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch_transactions(batch_request: BatchTransactionRequest, request: Request):
    """
    Predict fraud for multiple transactions
    
    - **transactions**: List of transactions (max 1000)
    - **threshold**: Custom fraud threshold for all transactions (optional)
    """
    try:
        logger.info(f"Processing batch prediction - {len(batch_request.transactions)} transactions")
        
        # Convert transactions to dictionaries
        transactions = []
        for txn in batch_request.transactions:
            txn_dict = txn.dict()
            txn_dict.pop('threshold', None)  # Remove individual thresholds
            transactions.append(txn_dict)
        
        # Get batch predictions
        results = ml_service.predict_batch(transactions, batch_request.threshold)
        
        # Generate summary
        fraud_count = sum(1 for r in results if r['final_decision'] == 'FRAUD')
        summary = {
            "total_transactions": len(results),
            "fraud_detected": fraud_count,
            "legitimate_transactions": len(results) - fraud_count,
            "fraud_rate": round(fraud_count / len(results), 4),
            "processing_timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Batch processing completed - {fraud_count}/{len(results)} flagged as fraud")
        
        return BatchPredictionResponse(
            results=[PredictionResponse(**r) for r in results],
            summary=summary
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in batch prediction: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Batch prediction service error")


# CSV upload endpoint for batch processing
@app.post("/predict/upload")
async def predict_csv_upload(file: UploadFile = File(...)):
    """
    Upload CSV file for batch fraud prediction
    
    Expected CSV columns: Time, Amount, V1-V28
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read CSV
        content = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(content.decode('utf-8')))
        
        # Validate required columns
        required_cols = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_cols}"
            )
        
        # Convert to transaction list
        transactions = df[required_cols].to_dict('records')
        
        if len(transactions) > settings.MAX_BATCH_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File contains {len(transactions)} transactions, maximum allowed is {settings.MAX_BATCH_SIZE}"
            )
        
        # Process batch
        results = ml_service.predict_batch(transactions)
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Return as JSON (could be extended to return CSV)
        fraud_count = sum(1 for r in results if r['final_decision'] == 'FRAUD')
        
        return {
            "filename": file.filename,
            "total_transactions": len(results),
            "fraud_detected": fraud_count,
            "results": results
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        logger.error(f"CSV upload error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="CSV processing error")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.MAX_WORKERS
    )
