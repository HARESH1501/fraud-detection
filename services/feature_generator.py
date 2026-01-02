"""
Feature Generation Service
Converts user-friendly inputs to V1-V28 PCA features for the trained model
"""
import numpy as np
import pandas as pd
from typing import Dict, Any
import hashlib
import math


class FeatureGenerator:
    """Generates V1-V28 features from user-friendly transaction inputs"""
    
    def __init__(self):
        # Mapping dictionaries for categorical features
        self.merchant_type_map = {
            "Online Retail": 0, "Gas Station": 1, "Restaurant": 2, "ATM": 3,
            "Grocery Store": 4, "Department Store": 5, "Hotel": 6, "Other": 7
        }
        
        self.transaction_type_map = {
            "Purchase": 0, "Cash Withdrawal": 1, "Online Payment": 2,
            "Recurring Payment": 3, "International": 4, "Refund": 5
        }
        
        self.location_risk_map = {
            "Low Risk (Home Country)": 0, "Medium Risk (Neighboring)": 1,
            "High Risk (International)": 2, "Very High Risk (Restricted)": 3
        }
        
        # Initialize random seed for consistent feature generation
        np.random.seed(42)
        
        # Base fraud probability - start lower for more realistic results
        self.base_fraud_probability = 0.15  # 15% base probability
    
    def generate_v_features(self, transaction_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Generate V1-V28 features from user-friendly transaction data
        
        Args:
            transaction_data: Dictionary containing user-friendly transaction fields
            
        Returns:
            Dictionary with V1-V28 features
        """
        # Extract basic features
        time_val = transaction_data.get('Time', 0)
        amount = transaction_data.get('Amount', 0)
        merchant_type = transaction_data.get('merchant_type', 'Other')
        transaction_type = transaction_data.get('transaction_type', 'Purchase')
        location_risk = transaction_data.get('location_risk', 'Low Risk (Home Country)')
        hour_of_day = transaction_data.get('hour_of_day', 12)
        customer_age_days = transaction_data.get('customer_age_days', 365)
        daily_transactions = transaction_data.get('daily_transactions', 3)
        
        # Convert categorical to numerical
        merchant_code = self.merchant_type_map.get(merchant_type, 7)
        txn_type_code = self.transaction_type_map.get(transaction_type, 0)
        location_code = self.location_risk_map.get(location_risk, 0)
        
        # Create a deterministic seed based on transaction characteristics
        seed_string = f"{amount}_{merchant_code}_{txn_type_code}_{location_code}_{hour_of_day}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16) % (2**32)
        np.random.seed(seed)
        
        # Generate V features using realistic patterns
        v_features = {}
        
        # V1-V5: Amount-based features (log transformations, ratios)
        log_amount = math.log(max(amount, 0.01))
        v_features['V1'] = log_amount * np.random.normal(0.1, 0.05)
        v_features['V2'] = (amount / 1000) * np.random.normal(0.05, 0.02)
        v_features['V3'] = math.sqrt(amount) * np.random.normal(0.02, 0.01)
        v_features['V4'] = (amount ** 0.3) * np.random.normal(0.03, 0.015)
        v_features['V5'] = (1 / (1 + amount/100)) * np.random.normal(0.1, 0.03)
        
        # V6-V10: Time-based features
        time_normalized = time_val / 86400  # Convert to days
        v_features['V6'] = time_normalized * np.random.normal(0.02, 0.01)
        v_features['V7'] = math.sin(hour_of_day * 2 * math.pi / 24) * np.random.normal(0.1, 0.02)
        v_features['V8'] = math.cos(hour_of_day * 2 * math.pi / 24) * np.random.normal(0.1, 0.02)
        v_features['V9'] = (hour_of_day / 24) * np.random.normal(0.05, 0.01)
        v_features['V10'] = math.log(max(customer_age_days, 1)) * np.random.normal(0.03, 0.01)
        
        # V11-V15: Merchant and transaction type features
        v_features['V11'] = merchant_code * np.random.normal(0.1, 0.02)
        v_features['V12'] = txn_type_code * np.random.normal(0.08, 0.02)
        v_features['V13'] = (merchant_code * txn_type_code) * np.random.normal(0.05, 0.01)
        v_features['V14'] = (merchant_code / 8) * np.random.normal(0.1, 0.03)
        v_features['V15'] = (txn_type_code / 6) * np.random.normal(0.08, 0.02)
        
        # V16-V20: Location and risk features
        v_features['V16'] = location_code * np.random.normal(0.15, 0.03)
        v_features['V17'] = (location_code ** 2) * np.random.normal(0.05, 0.02)
        v_features['V18'] = (location_code * merchant_code) * np.random.normal(0.03, 0.01)
        v_features['V19'] = math.exp(-location_code) * np.random.normal(0.1, 0.02)
        v_features['V20'] = (1 / (1 + location_code)) * np.random.normal(0.12, 0.03)
        
        # V21-V25: Customer behavior features
        txn_frequency = daily_transactions / 10  # Normalize
        v_features['V21'] = txn_frequency * np.random.normal(0.08, 0.02)
        v_features['V22'] = math.log(max(daily_transactions, 1)) * np.random.normal(0.06, 0.015)
        v_features['V23'] = (customer_age_days / 365) * np.random.normal(0.04, 0.01)
        v_features['V24'] = (daily_transactions * amount / 1000) * np.random.normal(0.02, 0.005)
        v_features['V25'] = math.sqrt(customer_age_days) * np.random.normal(0.03, 0.01)
        
        # V26-V28: Complex interaction features
        interaction1 = amount * location_code * merchant_code
        interaction2 = hour_of_day * txn_type_code * daily_transactions
        interaction3 = customer_age_days * amount * location_code
        
        v_features['V26'] = math.log(max(interaction1, 1)) * np.random.normal(0.01, 0.005)
        v_features['V27'] = math.log(max(interaction2, 1)) * np.random.normal(0.015, 0.005)
        v_features['V28'] = math.log(max(interaction3, 1)) * np.random.normal(0.008, 0.003)
        
        # Add some realistic noise and ensure reasonable ranges
        for key in v_features:
            # Add small random noise
            v_features[key] += np.random.normal(0, 0.001)
            # Clip to reasonable ranges (typical PCA features range)
            v_features[key] = np.clip(v_features[key], -5.0, 5.0)
            # Round to 6 decimal places
            v_features[key] = round(v_features[key], 6)
        
        return v_features
        
    def generate_realistic_ml_probability(self, transaction_data: Dict[str, Any]) -> float:
        """
        Generate a more realistic ML fraud probability based on transaction characteristics
        This simulates what a real trained model might output
        """
        # Base probability
        prob = self.base_fraud_probability
        
        # Amount influence
        amount = transaction_data.get('Amount', 0)
        if amount > 100000:
            prob += 0.25
        elif amount > 50000:
            prob += 0.15
        elif amount > 20000:
            prob += 0.08
        elif amount > 10000:
            prob += 0.03
        elif amount < 100:
            prob -= 0.05
        
        # Location influence
        location_risk = transaction_data.get('location_risk', 'Low Risk (Home Country)')
        if 'Very High Risk' in location_risk:
            prob += 0.20
        elif 'High Risk' in location_risk:
            prob += 0.12
        elif 'Medium Risk' in location_risk:
            prob += 0.05
        else:
            prob -= 0.03
        
        # Time influence
        hour = transaction_data.get('hour_of_day', 12)
        if hour in [1, 2, 3]:
            prob += 0.15
        elif hour in [0, 4, 23]:
            prob += 0.08
        elif 9 <= hour <= 17:
            prob -= 0.05
        
        # Customer age influence
        customer_age = transaction_data.get('customer_age_days', 365)
        if customer_age <= 7:
            prob += 0.18
        elif customer_age <= 30:
            prob += 0.10
        elif customer_age <= 90:
            prob += 0.03
        elif customer_age >= 365:
            prob -= 0.05
        
        # Velocity influence
        daily_txns = transaction_data.get('daily_transactions', 3)
        if daily_txns >= 50:
            prob += 0.20
        elif daily_txns >= 25:
            prob += 0.12
        elif daily_txns >= 15:
            prob += 0.06
        elif daily_txns <= 2:
            prob -= 0.03
        
        # Add some randomness to simulate model uncertainty
        prob += np.random.normal(0, 0.05)
        
        # Ensure probability is within valid range
        prob = max(0.01, min(0.99, prob))
        
        return prob
    
    def convert_user_friendly_to_standard(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert user-friendly transaction data to standard format with V1-V28 features
        
        Args:
            user_data: User-friendly transaction data
            
        Returns:
            Standard transaction data with V1-V28 features
        """
        # Generate V features
        v_features = self.generate_v_features(user_data)
        
        # Create standard format
        standard_data = {
            'Time': user_data.get('Time', 0),
            'Amount': user_data.get('Amount', 0),
            **v_features
        }
        
        # Add threshold if provided
        if 'threshold' in user_data:
            standard_data['threshold'] = user_data['threshold']
        
        return standard_data


# Global instance
feature_generator = FeatureGenerator()