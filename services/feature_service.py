"""
Production Feature Engineering Service
Centralized feature processing for consistency across all endpoints
"""
import pandas as pd
import numpy as np
import joblib
from typing import Dict, List, Union, Optional
from config.settings import settings


class FeatureEngineeringService:
    """Centralized feature engineering for fraud detection"""
    
    def __init__(self):
        self.scaler = self._load_scaler()
    
    def _load_scaler(self) -> Optional[object]:
        """Load the trained scaler"""
        try:
            return joblib.load(settings.SCALER_PATH)
        except FileNotFoundError:
            return None
    
    def process_single_transaction(self, transaction: Dict) -> pd.DataFrame:
        """
        Process a single transaction for inference
        
        Args:
            transaction: Dictionary with transaction features
            
        Returns:
            Processed DataFrame ready for model inference
        """
        df = pd.DataFrame([transaction])
        return self._apply_feature_engineering(df)
    
    def process_batch_transactions(self, transactions: List[Dict]) -> pd.DataFrame:
        """
        Process multiple transactions for batch inference
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Processed DataFrame ready for model inference
        """
        df = pd.DataFrame(transactions)
        return self._apply_feature_engineering(df)
    
    def _apply_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply consistent feature engineering transformations
        
        Args:
            df: Raw transaction DataFrame
            
        Returns:
            Engineered DataFrame
        """
        df = df.copy()
        
        # Log transform Amount (handle zero/negative values)
        df["Amount_log"] = np.log1p(np.maximum(df["Amount"], 0))
        
        # Scale Amount
        if self.scaler is not None:
            df["Amount_scaled"] = self.scaler.transform(df[["Amount"]])
        else:
            # Fallback: normalize Amount manually
            df["Amount_scaled"] = (df["Amount"] - df["Amount"].mean()) / df["Amount"].std()
        
        # Drop raw Amount (models expect this)
        df = df.drop(columns=["Amount"])
        
        return df
    
    def validate_transaction_features(self, transaction: Dict) -> Dict:
        """
        Validate and clean transaction features
        
        Args:
            transaction: Raw transaction dictionary
            
        Returns:
            Validated transaction dictionary
        """
        required_features = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
        
        # Ensure all required features are present
        for feature in required_features:
            if feature not in transaction:
                transaction[feature] = 0.0
        
        # Type conversion and bounds checking
        transaction["Time"] = max(0.0, float(transaction["Time"]))
        transaction["Amount"] = max(0.0, float(transaction["Amount"]))
        
        # Validate PCA features (V1-V28)
        for i in range(1, 29):
            v_key = f"V{i}"
            transaction[v_key] = float(transaction.get(v_key, 0.0))
        
        return transaction


# Global service instance
feature_service = FeatureEngineeringService()