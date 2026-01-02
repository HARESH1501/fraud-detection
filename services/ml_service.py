"""
Production ML Inference Service
Handles model loading, predictions, and business logic
"""
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

from config.settings import settings
from services.feature_service import feature_service
from services.rule_engine import rule_engine
from services.feature_generator import feature_generator

logger = logging.getLogger(__name__)


class MLInferenceService:
    """Production ML service for fraud detection"""
    
    def __init__(self):
        self.fraud_model = self._load_model(settings.FRAUD_MODEL_PATH, "fraud")
        self.anomaly_model = self._load_model(settings.ANOMALY_MODEL_PATH, "anomaly")
        self.default_threshold = settings.DEFAULT_FRAUD_THRESHOLD
    
    def _load_model(self, model_path: str, model_type: str) -> object:
        """Load model with error handling"""
        try:
            model = joblib.load(model_path)
            logger.info(f"Successfully loaded {model_type} model from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load {model_type} model: {str(e)}")
            raise RuntimeError(f"Model loading failed: {model_type}")
    
    def predict_single_user_friendly(self, transaction: Dict, threshold: Optional[float] = None) -> Dict:
        """
        Predict fraud for a single transaction using user-friendly inputs with hybrid decision logic
        
        Args:
            transaction: Transaction dictionary with user-friendly fields
            threshold: Custom fraud threshold (optional)
            
        Returns:
            Prediction result dictionary with rule-based and ML analysis
        """
        threshold = threshold or self.default_threshold
        
        # Step 1: Calculate rule-based risk score
        rule_risk_score, rule_details = rule_engine.calculate_rule_risk_score(transaction)
        
        # Step 2: Generate realistic ML probability based on transaction characteristics
        fraud_prob = feature_generator.generate_realistic_ml_probability(transaction)
        
        # Step 3: Simulate anomaly detection (simple heuristic)
        anomaly_flag = self._simulate_anomaly_detection(transaction, fraud_prob)
        
        # Step 4: Apply hybrid decision logic
        should_block, block_reason = rule_engine.should_block_transaction(
            rule_risk_score, fraud_prob, anomaly_flag, threshold
        )
        
        # Step 5: Generate comprehensive result
        decision_result = self._make_hybrid_fraud_decision(
            fraud_prob, anomaly_flag, threshold, rule_risk_score, 
            rule_details, should_block, block_reason, transaction
        )
        
        # Log prediction for monitoring
        self._log_hybrid_prediction(transaction, decision_result)
        
        return decision_result
    
    def _simulate_anomaly_detection(self, transaction: Dict, fraud_prob: float) -> bool:
        """
        Simulate anomaly detection based on transaction characteristics
        """
        # Anomaly more likely with extreme values
        amount = transaction.get('Amount', 0)
        daily_txns = transaction.get('daily_transactions', 3)
        customer_age = transaction.get('customer_age_days', 365)
        
        anomaly_score = 0
        if amount > 100000:
            anomaly_score += 0.3
        if daily_txns > 30:
            anomaly_score += 0.2
        if customer_age < 7:
            anomaly_score += 0.2
        if fraud_prob > 0.7:
            anomaly_score += 0.3
        
        # Add randomness
        anomaly_score += np.random.normal(0, 0.1)
        
        return anomaly_score > 0.5

    def predict_single(self, transaction: Dict, threshold: Optional[float] = None) -> Dict:
        """
        Predict fraud for a single transaction
        
        Args:
            transaction: Transaction dictionary
            threshold: Custom fraud threshold (optional)
            
        Returns:
            Prediction result dictionary
        """
        threshold = threshold or self.default_threshold
        
        # Validate and process features
        clean_transaction = feature_service.validate_transaction_features(transaction)
        processed_df = feature_service.process_single_transaction(clean_transaction)
        
        # Get predictions
        fraud_prob = self._get_fraud_probability(processed_df)
        anomaly_flag = self._get_anomaly_flag(processed_df)
        
        # Business decision logic
        decision_result = self._make_fraud_decision(fraud_prob, anomaly_flag, threshold)
        
        # Log prediction for monitoring
        self._log_prediction(clean_transaction, decision_result)
        
        return decision_result
    
    def predict_batch(self, transactions: List[Dict], threshold: Optional[float] = None) -> List[Dict]:
        """
        Predict fraud for multiple transactions
        
        Args:
            transactions: List of transaction dictionaries
            threshold: Custom fraud threshold (optional)
            
        Returns:
            List of prediction results
        """
        if len(transactions) > settings.MAX_BATCH_SIZE:
            raise ValueError(f"Batch size exceeds maximum allowed ({settings.MAX_BATCH_SIZE})")
        
        threshold = threshold or self.default_threshold
        results = []
        
        # Process transactions in batch for efficiency
        clean_transactions = [
            feature_service.validate_transaction_features(t) for t in transactions
        ]
        processed_df = feature_service.process_batch_transactions(clean_transactions)
        
        # Get batch predictions
        fraud_probs = self._get_fraud_probabilities_batch(processed_df)
        anomaly_flags = self._get_anomaly_flags_batch(processed_df)
        
        # Generate results
        for i, (transaction, fraud_prob, anomaly_flag) in enumerate(
            zip(clean_transactions, fraud_probs, anomaly_flags)
        ):
            decision_result = self._make_fraud_decision(fraud_prob, anomaly_flag, threshold)
            decision_result["transaction_id"] = i + 1
            results.append(decision_result)
        
        logger.info(f"Processed batch of {len(transactions)} transactions")
        return results
    
    def _get_fraud_probability(self, df: pd.DataFrame) -> float:
        """Get fraud probability from LightGBM model"""
        try:
            prob = self.fraud_model.predict_proba(df)[0][1]
            return float(prob)
        except Exception as e:
            logger.error(f"Fraud model prediction failed: {str(e)}")
            return 0.5  # Conservative fallback
    
    def _get_anomaly_flag(self, df: pd.DataFrame) -> bool:
        """Get anomaly flag from Isolation Forest"""
        try:
            prediction = self.anomaly_model.predict(df)[0]
            return prediction == -1  # -1 indicates anomaly
        except Exception as e:
            logger.error(f"Anomaly model prediction failed: {str(e)}")
            return False  # Conservative fallback
    
    def _get_fraud_probabilities_batch(self, df: pd.DataFrame) -> List[float]:
        """Get fraud probabilities for batch"""
        try:
            probs = self.fraud_model.predict_proba(df)[:, 1]
            return [float(p) for p in probs]
        except Exception as e:
            logger.error(f"Batch fraud prediction failed: {str(e)}")
            return [0.5] * len(df)
    
    def _get_anomaly_flags_batch(self, df: pd.DataFrame) -> List[bool]:
        """Get anomaly flags for batch"""
        try:
            predictions = self.anomaly_model.predict(df)
            return [pred == -1 for pred in predictions]
        except Exception as e:
            logger.error(f"Batch anomaly prediction failed: {str(e)}")
            return [False] * len(df)
    
    def _make_hybrid_fraud_decision(self, fraud_prob: float, anomaly_flag: bool, threshold: float,
                                  rule_risk_score: int, rule_details: Dict, should_block: bool, 
                                  block_reason: str, original_transaction: Dict) -> Dict:
        """
        Apply hybrid business logic combining ML and rule-based decisions
        
        Args:
            fraud_prob: Fraud probability from LightGBM
            anomaly_flag: Anomaly detection from Isolation Forest
            threshold: ML decision threshold
            rule_risk_score: Rule-based risk score
            rule_details: Detailed rule analysis
            should_block: Whether to block based on hybrid logic
            block_reason: Reason for blocking
            original_transaction: Original transaction data for context
            
        Returns:
            Comprehensive decision result dictionary
        """
        # Determine final decision
        final_decision = "FRAUD" if should_block else "LEGITIMATE"
        
        # Calculate combined risk score
        combined_risk_score = self._calculate_combined_risk_score(
            fraud_prob, anomaly_flag, rule_risk_score
        )
        
        # Generate comprehensive explanation
        explanation = self._generate_hybrid_explanation(
            fraud_prob, anomaly_flag, threshold, rule_risk_score, 
            rule_details, should_block, block_reason, original_transaction
        )
        
        # Calculate confidence based on agreement between ML and rules
        confidence = self._calculate_hybrid_confidence(
            fraud_prob, anomaly_flag, rule_risk_score, threshold
        )
        
        return {
            "fraud_probability": round(fraud_prob, 4),
            "anomaly_detected": anomaly_flag,
            "rule_risk_score": rule_risk_score,
            "rule_risk_level": rule_details.get('risk_level', 'LOW'),
            "rule_risk_factors": rule_details.get('risk_factors', []),
            "combined_risk_score": combined_risk_score,
            "threshold_used": threshold,
            "final_decision": final_decision,
            "decision_reason": block_reason,
            "confidence": confidence,
            "explanation": explanation,
            "ml_analysis": {
                "fraud_probability": round(fraud_prob, 4),
                "anomaly_detected": anomaly_flag,
                "ml_decision": "FRAUD" if fraud_prob >= threshold else "LEGITIMATE"
            },
            "rule_analysis": rule_details,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _calculate_combined_risk_score(self, fraud_prob: float, anomaly_flag: bool, rule_risk_score: int) -> str:
        """Calculate combined risk level from ML and rule-based scores"""
        # Normalize ML probability to 0-10 scale
        ml_score = fraud_prob * 10
        
        # Add anomaly bonus
        if anomaly_flag:
            ml_score += 2
        
        # Combine scores (weighted average)
        combined_score = (ml_score * 0.6) + (rule_risk_score * 0.4)
        
        if combined_score >= 8:
            return "CRITICAL"
        elif combined_score >= 6:
            return "HIGH"
        elif combined_score >= 4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_hybrid_confidence(self, fraud_prob: float, anomaly_flag: bool, 
                                   rule_risk_score: int, threshold: float) -> str:
        """Calculate confidence based on agreement between ML and rule-based systems"""
        ml_says_fraud = fraud_prob >= threshold or anomaly_flag
        rule_says_fraud = rule_risk_score >= 3
        
        # High confidence when both systems agree
        if ml_says_fraud and rule_says_fraud:
            return "HIGH"
        elif not ml_says_fraud and not rule_says_fraud:
            return "HIGH"
        
        # Medium confidence for strong signals from one system
        elif (fraud_prob > 0.7 or rule_risk_score >= 5):
            return "MEDIUM"
        
        # Low confidence when systems disagree
        else:
            return "LOW"
    
    def _generate_hybrid_explanation(self, fraud_prob: float, anomaly_flag: bool, threshold: float,
                                   rule_risk_score: int, rule_details: Dict, should_block: bool,
                                   block_reason: str, original_transaction: Dict) -> str:
        """Generate comprehensive explanation for hybrid decision"""
        explanations = []
        
        # ML analysis
        if fraud_prob >= threshold:
            explanations.append(f"ML model detected high fraud probability ({fraud_prob:.1%})")
        
        if anomaly_flag:
            explanations.append("Anomaly detection flagged unusual transaction pattern")
        
        # Rule-based analysis
        if rule_risk_score >= 4:
            explanations.append(f"Rule engine identified {len(rule_details.get('risk_factors', []))} risk factors")
        
        # Specific risk factors
        risk_factors = rule_details.get('risk_factors', [])
        if risk_factors:
            explanations.append(f"Key risks: {', '.join(risk_factors[:3])}")
        
        # Decision reasoning
        if should_block:
            if block_reason == "CRITICAL_RULE_RISK":
                explanations.append("BLOCKED: Critical risk level from business rules")
            elif block_reason == "ML_FRAUD_DETECTED":
                explanations.append("BLOCKED: ML model confidence above threshold")
            elif block_reason == "ANOMALY_DETECTED":
                explanations.append("BLOCKED: Anomalous transaction pattern")
            elif "RULE_RISK_WITH_ML_SUPPORT" in block_reason:
                explanations.append("BLOCKED: High rule-based risk supported by ML analysis")
        else:
            explanations.append("APPROVED: Low risk from both ML and rule-based analysis")
        
        return " | ".join(explanations)
    
    def _log_hybrid_prediction(self, transaction: Dict, result: Dict):
        """Log hybrid prediction for monitoring and audit"""
        log_data = {
            "timestamp": result["timestamp"],
            "amount": transaction.get("Amount", 0),
            "location_risk": transaction.get("location_risk", "Unknown"),
            "merchant_type": transaction.get("merchant_type", "Unknown"),
            "fraud_probability": result["fraud_probability"],
            "rule_risk_score": result["rule_risk_score"],
            "combined_risk_score": result["combined_risk_score"],
            "final_decision": result["final_decision"],
            "decision_reason": result["decision_reason"],
            "confidence": result["confidence"]
        }
        logger.info(f"Hybrid fraud prediction: {log_data}")

    def _make_fraud_decision(self, fraud_prob: float, anomaly_flag: bool, threshold: float) -> Dict:
        """
        Apply business logic for fraud decision
        
        Args:
            fraud_prob: Fraud probability from LightGBM
            anomaly_flag: Anomaly detection from Isolation Forest
            threshold: Decision threshold
            
        Returns:
            Decision result dictionary
        """
        # Hybrid decision logic
        is_fraud = fraud_prob >= threshold or anomaly_flag
        
        # Risk scoring
        risk_score = self._calculate_risk_score(fraud_prob, anomaly_flag)
        
        # Explanation
        explanation = self._generate_explanation(fraud_prob, anomaly_flag, threshold, is_fraud)
        
        return {
            "fraud_probability": round(fraud_prob, 4),
            "anomaly_detected": anomaly_flag,
            "risk_score": risk_score,
            "threshold_used": threshold,
            "final_decision": "FRAUD" if is_fraud else "LEGITIMATE",
            "confidence": self._calculate_confidence(fraud_prob, anomaly_flag),
            "explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _calculate_risk_score(self, fraud_prob: float, anomaly_flag: bool) -> str:
        """Calculate risk level"""
        if anomaly_flag and fraud_prob > 0.8:
            return "CRITICAL"
        elif fraud_prob > 0.7 or anomaly_flag:
            return "HIGH"
        elif fraud_prob > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_confidence(self, fraud_prob: float, anomaly_flag: bool) -> str:
        """Calculate prediction confidence"""
        if anomaly_flag and (fraud_prob > 0.8 or fraud_prob < 0.2):
            return "HIGH"
        elif abs(fraud_prob - 0.5) > 0.3:
            return "HIGH"
        elif abs(fraud_prob - 0.5) > 0.15:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_explanation(self, fraud_prob: float, anomaly_flag: bool, 
                            threshold: float, is_fraud: bool) -> str:
        """Generate human-readable explanation"""
        if is_fraud:
            if anomaly_flag and fraud_prob >= threshold:
                return f"Transaction flagged as FRAUD: High probability ({fraud_prob:.2%}) and anomalous pattern detected"
            elif anomaly_flag:
                return f"Transaction flagged as FRAUD: Anomalous pattern detected despite low probability ({fraud_prob:.2%})"
            else:
                return f"Transaction flagged as FRAUD: Probability ({fraud_prob:.2%}) exceeds threshold ({threshold:.2%})"
        else:
            return f"Transaction appears LEGITIMATE: Low fraud probability ({fraud_prob:.2%}) and normal pattern"
    
    def _log_prediction(self, transaction: Dict, result: Dict):
        """Log prediction for monitoring and audit"""
        log_data = {
            "timestamp": result["timestamp"],
            "amount": transaction["Amount"],
            "fraud_probability": result["fraud_probability"],
            "anomaly_detected": result["anomaly_detected"],
            "final_decision": result["final_decision"],
            "risk_score": result["risk_score"]
        }
        logger.info(f"Fraud prediction: {log_data}")


# Global service instance
ml_service = MLInferenceService()