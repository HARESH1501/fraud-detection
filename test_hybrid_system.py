#!/usr/bin/env python3
"""
Test script to demonstrate the hybrid fraud detection system
Shows how ML and rule-based systems work together
"""

import requests
import json
from datetime import datetime

def test_transaction(description, transaction_data):
    """Test a single transaction and display results"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {description}")
    print(f"{'='*60}")
    
    # Display input data
    print("📋 Transaction Details:")
    for key, value in transaction_data.items():
        print(f"  {key}: {value}")
    
    try:
        # Send request to API
        response = requests.post(
            "http://127.0.0.1:8000/predict/friendly",
            json=transaction_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Display results
            print(f"\n🎯 DECISION: {result['final_decision']}")
            print(f"📊 Combined Risk: {result.get('combined_risk_score', 'N/A')}")
            print(f"🤖 ML Probability: {result['fraud_probability']:.1%}")
            print(f"📋 Rule Risk Score: {result.get('rule_risk_score', 0)}/10")
            print(f"🔍 Anomaly Detected: {result['anomaly_detected']}")
            print(f"💡 Confidence: {result.get('confidence', 'N/A')}")
            print(f"🔍 Reason: {result.get('decision_reason', 'N/A')}")
            
            # Show risk factors
            risk_factors = result.get('rule_risk_factors', [])
            if risk_factors:
                print(f"\n⚠️  Risk Factors ({len(risk_factors)}):")
                for i, factor in enumerate(risk_factors[:5], 1):
                    print(f"  {i}. {factor}")
            
            # Show explanation
            print(f"\n💬 Explanation:")
            print(f"  {result.get('explanation', 'No explanation available')}")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")

def main():
    print("🛡️ SecureGuard AI - Hybrid Fraud Detection System Test")
    print("Testing ML + Rule-Based Decision Engine")
    
    # Test Case 1: Normal transaction (should be approved)
    test_transaction(
        "Normal Transaction - Should be APPROVED",
        {
            "Time": 10000.0,
            "Amount": 150.00,
            "merchant_type": "Grocery Store",
            "transaction_type": "Purchase",
            "location_risk": "Low Risk (Home Country)",
            "hour_of_day": 14,
            "customer_age_days": 365,
            "daily_transactions": 3
        }
    )
    
    # Test Case 2: High amount + risky location (should be flagged)
    test_transaction(
        "High Risk Transaction - Should be FRAUD",
        {
            "Time": 15000.0,
            "Amount": 25000.00,
            "merchant_type": "Online Retail",
            "transaction_type": "International",
            "location_risk": "Very High Risk (Restricted)",
            "hour_of_day": 2,
            "customer_age_days": 15,
            "daily_transactions": 15
        }
    )
    
    # Test Case 3: Medium risk (rule engine catches it)
    test_transaction(
        "Medium Risk - Rule Engine Should Catch",
        {
            "Time": 20000.0,
            "Amount": 8000.00,
            "merchant_type": "ATM",
            "transaction_type": "Cash Withdrawal",
            "location_risk": "High Risk (International)",
            "hour_of_day": 1,
            "customer_age_days": 45,
            "daily_transactions": 12
        }
    )
    
    # Test Case 4: New customer, high velocity (should be flagged)
    test_transaction(
        "New Customer High Velocity - Should be FRAUD",
        {
            "Time": 25000.0,
            "Amount": 5000.00,
            "merchant_type": "Hotel",
            "transaction_type": "Purchase",
            "location_risk": "Medium Risk (Neighboring)",
            "hour_of_day": 23,
            "customer_age_days": 7,
            "daily_transactions": 25
        }
    )
    
    # Test Case 5: Edge case - moderate signals
    test_transaction(
        "Edge Case - Moderate Signals",
        {
            "Time": 30000.0,
            "Amount": 3500.00,
            "merchant_type": "Department Store",
            "transaction_type": "Purchase",
            "location_risk": "Low Risk (Home Country)",
            "hour_of_day": 22,
            "customer_age_days": 90,
            "daily_transactions": 8
        }
    )
    
    print(f"\n{'='*60}")
    print("🎉 Test Complete!")
    print("The hybrid system combines:")
    print("  🤖 ML Model (LightGBM + Isolation Forest)")
    print("  📋 Rule Engine (Business Logic)")
    print("  🎯 Smart Decision Logic")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()