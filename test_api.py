#!/usr/bin/env python3
"""
Quick API test to check if the hybrid system is working
"""

import requests
import json

def test_api():
    """Test the new friendly API endpoint"""
    
    # Test data
    test_transaction = {
        "Time": 10000.0,
        "Amount": 1000.0,
        "merchant_type": "Grocery Store",
        "transaction_type": "Purchase", 
        "location_risk": "Low Risk (Home Country)",
        "hour_of_day": 14,
        "customer_age_days": 365,
        "daily_transactions": 3
    }
    
    print("🧪 Testing API endpoint...")
    print(f"📋 Test data: {json.dumps(test_transaction, indent=2)}")
    
    try:
        # Test health endpoint first
        health_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        print(f"✅ Health check: {health_response.status_code}")
        
        # Test friendly prediction endpoint
        response = requests.post(
            "http://127.0.0.1:8000/predict/friendly",
            json=test_transaction,
            timeout=10
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API is working!")
            print(f"🎯 Decision: {result.get('final_decision', 'N/A')}")
            print(f"🤖 ML Probability: {result.get('fraud_probability', 0):.1%}")
            print(f"📋 Rule Risk Score: {result.get('rule_risk_score', 0)}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_api()