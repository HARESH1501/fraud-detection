"""
Rule-Based Risk Engine
Implements business logic for fraud detection based on transaction characteristics
"""
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class RuleBasedRiskEngine:
    """
    Rule-based risk assessment engine that evaluates transaction risk
    based on business logic and domain expertise
    """
    
    def __init__(self):
        # Risk scoring thresholds
        self.high_amount_threshold = 20000
        self.very_high_amount_threshold = 50000
        self.new_customer_days = 60
        self.very_new_customer_days = 30
        self.high_velocity_threshold = 10
        self.very_high_velocity_threshold = 20
        
        # Risk hours (late night/early morning)
        self.risky_hours = [0, 1, 2, 3, 4, 23]
        self.very_risky_hours = [1, 2, 3]
        
        # Location risk mapping
        self.location_risk_scores = {
            "Low Risk (Home Country)": 0,
            "Medium Risk (Neighboring)": 1,
            "High Risk (International)": 2,
            "Very High Risk (Restricted)": 3
        }
        
        # Merchant risk mapping
        self.merchant_risk_scores = {
            "ATM": 0,
            "Grocery Store": 0,
            "Gas Station": 0,
            "Restaurant": 1,
            "Department Store": 1,
            "Online Retail": 2,
            "Hotel": 2,
            "Other": 3
        }
        
        # Transaction type risk mapping
        self.transaction_type_risk_scores = {
            "Recurring Payment": 0,
            "Purchase": 1,
            "Online Payment": 2,
            "Cash Withdrawal": 2,
            "International": 3,
            "Refund": 1
        }
    
    def calculate_rule_risk_score(self, transaction_data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        Calculate rule-based risk score and return detailed risk factors
        Uses industry-standard tiered scoring with both positive and negative risk factors
        
        Args:
            transaction_data: Dictionary containing transaction details
            
        Returns:
            Tuple of (risk_score, risk_details)
        """
        risk_score = 0
        risk_factors = []
        risk_details = {}
        
        # Extract transaction details
        amount = transaction_data.get('Amount', 0)
        location_risk = transaction_data.get('location_risk', 'Low Risk (Home Country)')
        hour_of_day = transaction_data.get('hour_of_day', 12)
        customer_age_days = transaction_data.get('customer_age_days', 365)
        daily_transactions = transaction_data.get('daily_transactions', 3)
        merchant_type = transaction_data.get('merchant_type', 'Other')
        transaction_type = transaction_data.get('transaction_type', 'Purchase')
        
        # 1. Amount-based risk assessment (TIERED)
        if amount >= 100000:  # Very high amounts
            risk_score += 4
            risk_factors.append(f"Very high transaction amount (${amount:,.2f})")
            risk_details['amount_risk'] = 'VERY_HIGH'
        elif amount >= 50000:  # High amounts
            risk_score += 3
            risk_factors.append(f"High transaction amount (${amount:,.2f})")
            risk_details['amount_risk'] = 'HIGH'
        elif amount >= 20000:  # Elevated amounts
            risk_score += 2
            risk_factors.append(f"Elevated transaction amount (${amount:,.2f})")
            risk_details['amount_risk'] = 'MEDIUM'
        elif amount >= 10000:  # Moderate amounts
            risk_score += 1
            risk_factors.append(f"Moderate transaction amount (${amount:,.2f})")
            risk_details['amount_risk'] = 'MEDIUM'
        elif amount < 100:  # Very low amounts (reduce risk)
            risk_score -= 1
            risk_details['amount_risk'] = 'LOW'
        else:
            risk_details['amount_risk'] = 'LOW'
        
        # 2. Location risk assessment
        location_score = self.location_risk_scores.get(location_risk, 0)
        if location_score >= 3:
            risk_score += 3
            risk_factors.append("Very high-risk location (restricted)")
        elif location_score >= 2:
            risk_score += 2
            risk_factors.append("High-risk location (international)")
        elif location_score >= 1:
            risk_score += 1
            risk_factors.append("Medium-risk location (neighboring)")
        else:
            risk_score -= 1  # Home country reduces risk
        
        risk_details['location_risk_score'] = location_score
        
        # 3. Time-based risk assessment (MORE RESTRICTIVE)
        if hour_of_day in [1, 2, 3]:  # Only very late hours
            risk_score += 2
            risk_factors.append(f"Very unusual transaction time ({hour_of_day}:00)")
            risk_details['time_risk'] = 'VERY_HIGH'
        elif hour_of_day in [0, 4, 23]:  # Slightly unusual
            risk_score += 1
            risk_factors.append(f"Unusual transaction time ({hour_of_day}:00)")
            risk_details['time_risk'] = 'HIGH'
        elif 9 <= hour_of_day <= 17:  # Business hours reduce risk
            risk_score -= 1
            risk_details['time_risk'] = 'LOW'
        else:
            risk_details['time_risk'] = 'MEDIUM'
        
        # 4. Customer age risk assessment (MORE BALANCED)
        if customer_age_days <= 7:  # Very new
            risk_score += 3
            risk_factors.append(f"Very new customer account ({customer_age_days} days)")
            risk_details['customer_age_risk'] = 'VERY_HIGH'
        elif customer_age_days <= 30:  # New
            risk_score += 2
            risk_factors.append(f"New customer account ({customer_age_days} days)")
            risk_details['customer_age_risk'] = 'HIGH'
        elif customer_age_days <= 90:  # Somewhat new
            risk_score += 1
            risk_factors.append(f"Relatively new customer account ({customer_age_days} days)")
            risk_details['customer_age_risk'] = 'MEDIUM'
        elif customer_age_days >= 365:  # Established customer reduces risk
            risk_score -= 1
            risk_details['customer_age_risk'] = 'LOW'
        else:
            risk_details['customer_age_risk'] = 'MEDIUM'
        
        # 5. Transaction velocity risk assessment (MORE RESTRICTIVE)
        if daily_transactions >= 50:  # Extremely high
            risk_score += 3
            risk_factors.append(f"Extremely high transaction velocity ({daily_transactions}/day)")
            risk_details['velocity_risk'] = 'VERY_HIGH'
        elif daily_transactions >= 25:  # Very high
            risk_score += 2
            risk_factors.append(f"Very high transaction velocity ({daily_transactions}/day)")
            risk_details['velocity_risk'] = 'VERY_HIGH'
        elif daily_transactions >= 15:  # High
            risk_score += 1
            risk_factors.append(f"High transaction velocity ({daily_transactions}/day)")
            risk_details['velocity_risk'] = 'HIGH'
        elif daily_transactions <= 2:  # Low velocity reduces risk
            risk_score -= 1
            risk_details['velocity_risk'] = 'LOW'
        else:
            risk_details['velocity_risk'] = 'MEDIUM'
        
        # 6. Merchant type risk assessment (REDUCED IMPACT)
        merchant_score = self.merchant_risk_scores.get(merchant_type, 1)
        if merchant_score >= 3 and amount >= 5000:  # Only for high amounts
            risk_score += 1
            risk_factors.append(f"High-risk merchant type with significant amount ({merchant_type})")
        elif merchant_score == 0:  # Low-risk merchants reduce risk
            risk_score -= 1
        risk_details['merchant_risk_score'] = merchant_score
        
        # 7. Transaction type risk assessment (REDUCED IMPACT)
        txn_type_score = self.transaction_type_risk_scores.get(transaction_type, 1)
        if txn_type_score >= 3:
            risk_score += 1
            risk_factors.append(f"High-risk transaction type ({transaction_type})")
        elif txn_type_score == 0:  # Low-risk types reduce risk
            risk_score -= 1
        risk_details['transaction_type_risk_score'] = txn_type_score
        
        # 8. Combination risk factors (ONLY FOR EXTREME CASES)
        if (amount >= 50000 and location_score >= 3):
            risk_score += 2
            risk_factors.append("Very high amount + restricted location combination")
        
        if (customer_age_days <= 7 and daily_transactions >= 25):
            risk_score += 2
            risk_factors.append("Brand new customer + very high velocity combination")
        
        if (hour_of_day in [1, 2, 3] and amount >= 20000):
            risk_score += 1
            risk_factors.append("Very late hour + high amount combination")
        
        # Ensure risk score stays within reasonable bounds
        risk_score = max(0, min(risk_score, 10))
        
        # Calculate overall risk level
        if risk_score >= 8:
            risk_level = "CRITICAL"
        elif risk_score >= 6:
            risk_level = "HIGH"
        elif risk_score >= 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        risk_details.update({
            'total_risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'risk_factor_count': len(risk_factors)
        })
        
        logger.info(f"Rule-based risk assessment: Score={risk_score}, Level={risk_level}, Factors={len(risk_factors)}")
        
        return risk_score, risk_details
    
    def should_block_transaction(self, rule_risk_score: int, ml_fraud_prob: float, 
                                anomaly_detected: bool, ml_threshold: float = 0.35) -> Tuple[bool, str]:
        """
        Determine if transaction should be blocked using industry-standard decision logic
        
        Args:
            rule_risk_score: Rule-based risk score (0-10)
            ml_fraud_prob: ML model fraud probability (0-1)
            anomaly_detected: Whether anomaly was detected
            ml_threshold: ML fraud threshold
            
        Returns:
            Tuple of (should_block, reason)
        """
        # Convert ML probability to percentage for easier logic
        ml_prob_pct = ml_fraud_prob * 100
        
        # CRITICAL RISK: Always block (8+ rule score OR very high ML)
        if rule_risk_score >= 8:
            return True, "CRITICAL_RULE_RISK"
        
        if ml_prob_pct >= 80:
            return True, "CRITICAL_ML_RISK"
        
        # HIGH RISK: Block with combined evidence
        if rule_risk_score >= 6 and ml_prob_pct >= 40:
            return True, "HIGH_COMBINED_RISK"
        
        if ml_prob_pct >= 70:
            return True, "HIGH_ML_RISK"
        
        # MEDIUM RISK: Block only with strong ML support
        if rule_risk_score >= 4 and ml_prob_pct >= 60:
            return True, "MEDIUM_RULE_WITH_HIGH_ML"
        
        # ANOMALY: Block only if combined with other risk factors
        if anomaly_detected and (rule_risk_score >= 3 or ml_prob_pct >= 50):
            return True, "ANOMALY_WITH_RISK_FACTORS"
        
        # STANDARD ML THRESHOLD: Only if no negative risk factors
        if ml_prob_pct >= (ml_threshold * 100) and rule_risk_score >= 0:
            return True, "ML_THRESHOLD_EXCEEDED"
        
        # DEFAULT: Allow transaction
        return False, "APPROVED"


# Global instance
rule_engine = RuleBasedRiskEngine()