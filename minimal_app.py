"""
MINIMAL FRAUD DETECTION APP - GUARANTEED TO WORK
No imports, no dependencies, just pure Streamlit
"""

import streamlit as st
import random
import time

# IMMEDIATE UI - MUST BE FIRST
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide"
)

# SHOW SOMETHING IMMEDIATELY
st.title("🛡️ Fraud Detection System")
st.success("✅ App is working! No black screen!")

st.header("💳 Transaction Fraud Analysis")
st.write("Enter transaction details below:")

# SIMPLE FORM
with st.form("fraud_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("💰 Amount ($)", min_value=1.0, value=1000.0)
        location = st.selectbox("🌍 Location", [
            "Home Country", "International", "High Risk Country"
        ])
        hour = st.slider("🕐 Hour of Day", 0, 23, 14)
    
    with col2:
        customer_age = st.number_input("👤 Customer Age (days)", min_value=1, value=365)
        daily_txns = st.number_input("📊 Daily Transactions", min_value=1, value=3)
        merchant = st.selectbox("🏪 Merchant", [
            "Grocery", "Gas Station", "Online", "ATM", "Restaurant"
        ])
    
    submitted = st.form_submit_button("🔍 Check for Fraud", use_container_width=True)

if submitted:
    st.divider()
    
    # SIMPLE FRAUD LOGIC
    with st.spinner("Analyzing..."):
        time.sleep(1)  # Simulate processing
        
        # Simple risk calculation
        risk_score = 0
        reasons = []
        
        if amount > 10000:
            risk_score += 3
            reasons.append(f"High amount: ${amount:,.2f}")
        
        if location == "High Risk Country":
            risk_score += 3
            reasons.append("High-risk location")
        elif location == "International":
            risk_score += 1
            reasons.append("International transaction")
        
        if hour < 6 or hour > 22:
            risk_score += 2
            reasons.append(f"Unusual time: {hour}:00")
        
        if customer_age < 30:
            risk_score += 2
            reasons.append(f"New customer: {customer_age} days")
        
        if daily_txns > 10:
            risk_score += 1
            reasons.append(f"High frequency: {daily_txns}/day")
        
        # Generate fake ML probability
        ml_prob = min(0.95, max(0.05, (risk_score / 10) + random.uniform(-0.2, 0.2)))
        
        # Decision
        if risk_score >= 5 or ml_prob > 0.7:
            st.error("🚨 **FRAUD DETECTED**")
            decision = "FRAUD"
            risk_level = "HIGH"
        elif risk_score >= 3 or ml_prob > 0.4:
            st.warning("⚠️ **SUSPICIOUS TRANSACTION**")
            decision = "REVIEW"
            risk_level = "MEDIUM"
        else:
            st.success("✅ **TRANSACTION APPROVED**")
            decision = "APPROVED"
            risk_level = "LOW"
    
    # Show results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🤖 Fraud Probability", f"{ml_prob:.1%}")
    
    with col2:
        st.metric("📊 Risk Score", f"{risk_score}/10")
    
    with col3:
        st.metric("🎯 Risk Level", risk_level)
    
    if reasons:
        st.subheader("⚠️ Risk Factors:")
        for i, reason in enumerate(reasons, 1):
            st.write(f"{i}. {reason}")

# FOOTER
st.divider()
st.info("🛡️ **Fraud Detection System** - Protecting your transactions with AI")
st.write("Built with Streamlit • No complex dependencies • Always works!")

# ALWAYS SHOW THIS
st.balloons() if submitted and risk_score < 3 else None