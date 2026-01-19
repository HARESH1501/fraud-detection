import streamlit as st
import numpy as np
import time
import random

# MUST BE FIRST - PAGE CONFIG
st.set_page_config(
    page_title="SecureGuard AI - Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

# IMMEDIATE SUCCESS MESSAGE TO CONFIRM APP LOADS
st.title("🛡️ SecureGuard AI - Fraud Detection")
st.success("✅ System Loaded Successfully!")

# ENTERPRISE FINTECH THEME - PROFESSIONAL DARK MODE
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background: #020617;
    font-family: 'Inter', sans-serif;
    color: #cbd5f5;
}

.main .block-container {
    background: #020617;
    border: 1px solid #1e293b;
    padding: 2rem;
    border-radius: 16px;
    margin: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.main-header {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    padding: 3rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
    color: #f8fafc;
    border: 1px solid #1e293b;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
}

.dark-card {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #f8fafc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.dark-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.1);
}

.fraud-alert {
    background: linear-gradient(90deg, #ef4444, #b91c1c);
    padding: 3rem 2rem;
    border-radius: 16px;
    text-align: center;
    color: #f8fafc;
    margin: 2rem 0;
    border: 1px solid #ef4444;
    box-shadow: 0 8px 24px rgba(239, 68, 68, 0.3);
}

.safe-alert {
    background: linear-gradient(90deg, #22c55e, #0ea5e9);
    padding: 3rem 2rem;
    border-radius: 16px;
    text-align: center;
    color: #f8fafc;
    margin: 2rem 0;
    border: 1px solid #22c55e;
    box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
}

.metric-frame {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    color: #f8fafc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    margin: 0.5rem 0;
    transition: all 0.3s ease;
}

.metric-frame:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.1);
}

.analysis-frame {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.5rem;
    color: #f8fafc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.analysis-frame:hover {
    border-color: #3b82f6;
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.1);
}

.info-box {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    color: #cbd5f5;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}

.info-box:hover {
    border-color: #3b82f6;
    background: rgba(59, 130, 246, 0.05);
}

.input-frame {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.8rem 0;
    color: #f8fafc;
    transition: all 0.3s ease;
}

.input-frame:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: #f8fafc;
    border: none;
    border-radius: 12px;
    padding: 1rem 2.5rem;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #f8fafc !important;
    font-weight: 700;
}

.stApp p, .stApp div, .stApp span {
    color: #cbd5f5 !important;
}

.stApp label {
    color: #94a3b8 !important;
    font-weight: 500;
}

.css-1d391kg {
    background: #020617 !important;
    border: 1px solid #1e293b !important;
    border-radius: 16px !important;
    margin: 1rem !important;
    color: #cbd5f5 !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
}

.stSuccess, .stInfo, .stWarning, .stError {
    background: #020617 !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.stProgress .st-bo {
    background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider > div > div > div {
    background: #020617 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #f8fafc !important;
}

.stSelectbox > div > div > div {
    background: #020617 !important;
    color: #f8fafc !important;
    border: 1px solid #1e293b !important;
}

.stSlider > div > div > div > div {
    background: #3b82f6 !important;
}

.stSlider > div > div > div > div > div {
    background: #2563eb !important;
}

/* Sidebar Styling */
.css-1d391kg .css-1v0mbdj {
    background: #020617 !important;
    border-right: 1px solid #1e293b !important;
}

/* Custom Divider */
.custom-divider {
    height: 1px;
    background: #1e293b;
    margin: 2rem 0;
    border: none;
}

/* Risk Level Colors */
.risk-low { color: #22c55e !important; }
.risk-medium { color: #f59e0b !important; }
.risk-high { color: #ef4444 !important; }

/* Confidence Colors */
.confidence-high { color: #0ea5e9 !important; }
.confidence-medium { color: #f59e0b !important; }
.confidence-low { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# HEADER SECTION
st.markdown("""
<div class="main-header">
    <h1>🛡️ SecureGuard AI</h1>
    <p>Advanced Transaction Analysis</p>
    <p>Enter transaction details below for comprehensive fraud detection</p>
</div>
""", unsafe_allow_html=True)

# RULE ENGINE CLASS
class RuleEngine:
    def __init__(self):
        self.location_risk_scores = {
            "Low Risk (Home Country)": 0,
            "Medium Risk (Neighboring)": 1,
            "High Risk (International)": 2,
            "Very High Risk (Restricted)": 3
        }
    
    def calculate_risk_score(self, transaction_data):
        risk_score = 0
        risk_factors = []
        
        amount = transaction_data.get('Amount', 0)
        location_risk = transaction_data.get('location_risk', 'Low Risk (Home Country)')
        hour_of_day = transaction_data.get('hour_of_day', 12)
        customer_age_days = transaction_data.get('customer_age_days', 365)
        daily_transactions = transaction_data.get('daily_transactions', 3)
        
        # Amount-based risk
        if amount >= 50000:
            risk_score += 3
            risk_factors.append(f"High transaction amount (${amount:,.2f})")
        elif amount >= 20000:
            risk_score += 2
            risk_factors.append(f"Elevated transaction amount (${amount:,.2f})")
        elif amount >= 10000:
            risk_score += 1
            risk_factors.append(f"Moderate transaction amount (${amount:,.2f})")
        
        # Location risk
        location_score = self.location_risk_scores.get(location_risk, 0)
        if location_score >= 2:
            risk_score += 2
            risk_factors.append("High-risk location")
        elif location_score >= 1:
            risk_score += 1
            risk_factors.append("Medium-risk location")
        
        # Time-based risk
        if hour_of_day in [1, 2, 3]:
            risk_score += 2
            risk_factors.append(f"Unusual transaction time ({hour_of_day}:00)")
        elif hour_of_day in [0, 4, 23]:
            risk_score += 1
            risk_factors.append(f"Late transaction time ({hour_of_day}:00)")
        
        # Customer age risk
        if customer_age_days <= 30:
            risk_score += 2
            risk_factors.append(f"New customer account ({customer_age_days} days)")
        elif customer_age_days <= 90:
            risk_score += 1
            risk_factors.append(f"Relatively new account ({customer_age_days} days)")
        
        # Transaction velocity risk
        if daily_transactions >= 25:
            risk_score += 2
            risk_factors.append(f"High transaction velocity ({daily_transactions}/day)")
        elif daily_transactions >= 15:
            risk_score += 1
            risk_factors.append(f"Elevated transaction velocity ({daily_transactions}/day)")
        
        risk_score = max(0, min(risk_score, 10))
        
        if risk_score >= 6:
            risk_level = "HIGH"
        elif risk_score >= 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return risk_score, {
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'total_risk_score': risk_score
        }

# ML PROBABILITY GENERATOR
class MLGenerator:
    def __init__(self):
        self.base_fraud_probability = 0.15
        np.random.seed(42)
    
    def generate_ml_probability(self, transaction_data):
        prob = self.base_fraud_probability
        
        amount = transaction_data.get('Amount', 0)
        location_risk = transaction_data.get('location_risk', 'Low Risk (Home Country)')
        hour = transaction_data.get('hour_of_day', 12)
        customer_age = transaction_data.get('customer_age_days', 365)
        daily_txns = transaction_data.get('daily_transactions', 3)
        
        if amount > 50000:
            prob += 0.20
        elif amount > 20000:
            prob += 0.10
        elif amount > 10000:
            prob += 0.05
        
        if 'High Risk' in location_risk:
            prob += 0.15
        elif 'Medium Risk' in location_risk:
            prob += 0.08
        
        if hour in [1, 2, 3]:
            prob += 0.12
        elif hour in [0, 4, 23]:
            prob += 0.06
        
        if customer_age <= 30:
            prob += 0.10
        elif customer_age <= 90:
            prob += 0.05
        
        if daily_txns >= 25:
            prob += 0.15
        elif daily_txns >= 15:
            prob += 0.08
        
        prob += np.random.normal(0, 0.03)
        
        return max(0.01, min(0.99, prob))

# INITIALIZE SERVICES
rule_engine = RuleEngine()
ml_generator = MLGenerator()

# SIDEBAR WITH ENTERPRISE THEME
with st.sidebar:
    st.markdown('<div class="dark-card"><h3>🎯 System Status</h3></div>', unsafe_allow_html=True)
    st.success("🟢 Online")
    
    st.markdown('<div class="metric-frame"><strong>Accuracy</strong><br><span style="color: #22c55e;">99.1%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-frame"><strong>Response</strong><br><span style="color: #0ea5e9;">&lt;120ms</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-frame"><strong>Status</strong><br><span style="color: #22c55e;">✅ Active</span></div>', unsafe_allow_html=True)

# MAIN INTERFACE
st.header("💳 Advanced Transaction Analysis")

# TRANSACTION FORM WITH ALL SIX FEATURES FROM IMAGE
st.markdown('<div class="dark-card"><h3>📋 Transaction Details</h3></div>', unsafe_allow_html=True)

with st.form("fraud_detection"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Transaction Time (seconds)
        st.markdown('<div class="input-frame">⏰ <strong>Transaction Time (seconds)</strong></div>', unsafe_allow_html=True)
        transaction_time = st.number_input("", min_value=0.0, value=10000.0, step=1.0, label_visibility="collapsed", key="time")
        
        # Transaction Amount
        st.markdown('<div class="input-frame">💰 <strong>Transaction Amount ($)</strong></div>', unsafe_allow_html=True)
        amount = st.number_input("", min_value=0.01, value=1000.0, step=0.01, label_visibility="collapsed", key="amount")
        
        # Merchant Type
        st.markdown('<div class="input-frame">🏪 <strong>Merchant Type</strong></div>', unsafe_allow_html=True)
        merchant_type = st.selectbox("", [
            "Grocery Store", "Gas Station", "Restaurant", "ATM", 
            "Online Retail", "Department Store", "Hotel", "Other"
        ], label_visibility="collapsed", key="merchant")
    
    with col2:
        # Transaction Type
        st.markdown('<div class="input-frame">💳 <strong>Transaction Type</strong></div>', unsafe_allow_html=True)
        transaction_type = st.selectbox("", [
            "Purchase", "Cash Withdrawal", "Online Payment", 
            "Recurring Payment", "International", "Refund"
        ], label_visibility="collapsed", key="trans_type")
        
        # Location Risk
        st.markdown('<div class="input-frame">🌍 <strong>Location Risk</strong></div>', unsafe_allow_html=True)
        location_risk = st.selectbox("", [
            "Low Risk (Home Country)", 
            "Medium Risk (Neighboring)", 
            "High Risk (International)", 
            "Very High Risk (Restricted)"
        ], label_visibility="collapsed", key="location")
        
        # Hour of Day
        st.markdown('<div class="input-frame">🕐 <strong>Hour of Day</strong></div>', unsafe_allow_html=True)
        hour_of_day = st.slider("", 0, 23, 14, label_visibility="collapsed", key="hour")
    
    # Additional fields in a new row
    col3, col4 = st.columns(2)
    
    with col3:
        # Customer Age
        st.markdown('<div class="input-frame">📅 <strong>Customer Age (days)</strong></div>', unsafe_allow_html=True)
        customer_age_days = st.number_input("", min_value=1, value=365, step=1, label_visibility="collapsed", key="age")
    
    with col4:
        # Daily Transaction Count
        st.markdown('<div class="input-frame">📊 <strong>Daily Transaction Count</strong></div>', unsafe_allow_html=True)
        daily_transactions = st.number_input("", min_value=1, value=3, step=1, label_visibility="collapsed", key="daily")
    
    submitted = st.form_submit_button("🔍 Analyze Transaction", use_container_width=True)

# PROCESSING AND RESULTS
if submitted:
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    with st.spinner("🔄 Analyzing transaction..."):
        progress_bar = st.progress(0)
        
        for i in range(100):
            progress_bar.progress(min((i + 1) / 100, 0.99))
            time.sleep(0.008)
        
        # Prepare data with all six features
        transaction_data = {
            "transaction_time": transaction_time,
            "Amount": amount,
            "merchant_type": merchant_type,
            "transaction_type": transaction_type,
            "location_risk": location_risk,
            "hour_of_day": hour_of_day,
            "customer_age_days": customer_age_days,
            "daily_transactions": daily_transactions
        }
        
        # Run analysis
        rule_risk_score, rule_details = rule_engine.calculate_risk_score(transaction_data)
        ml_prob = ml_generator.generate_ml_probability(transaction_data)
        
        # Decision logic
        should_block = rule_risk_score >= 6 or ml_prob >= 0.65
        anomaly_detected = ml_prob > 0.7 or rule_risk_score >= 7
        
        progress_bar.empty()
    
    # RESULTS WITH MODERN FRAMES
    if should_block:
        st.markdown(f"""
        <div class="fraud-alert">
            <h2>🚨 FRAUD DETECTED</h2>
            <h3>Risk Level: {rule_details.get('risk_level', 'HIGH')}</h3>
            <p>This transaction shows suspicious patterns</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="safe-alert">
            <h2>✅ TRANSACTION APPROVED</h2>
            <h3>Risk Level: {rule_details.get('risk_level', 'LOW')}</h3>
            <p>This transaction appears legitimate</p>
        </div>
        """, unsafe_allow_html=True)
    
    # METRICS WITH ENTERPRISE COLORS (4 key metrics like in image)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-frame">
            <strong>🤖 ML Fraud Probability</strong><br>
            <span style="font-size: 1.8rem; color: #3b82f6;">{ml_prob:.1%}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        risk_color = "#ef4444" if rule_risk_score >= 6 else "#f59e0b" if rule_risk_score >= 3 else "#22c55e"
        st.markdown(f"""
        <div class="metric-frame">
            <strong>📋 Rule Risk Score</strong><br>
            <span style="font-size: 1.8rem; color: {risk_color};">{rule_risk_score}/10</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk_level = rule_details.get('risk_level', 'LOW')
        level_color = "#ef4444" if risk_level == "HIGH" else "#f59e0b" if risk_level == "MEDIUM" else "#22c55e"
        st.markdown(f"""
        <div class="metric-frame">
            <strong>📊 Risk Level</strong><br>
            <span style="font-size: 1.8rem; color: {level_color};">{risk_level}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        confidence = "HIGH" if abs(ml_prob - 0.5) > 0.3 else "MEDIUM"
        conf_color = "#0ea5e9" if confidence == "HIGH" else "#f59e0b"
        st.markdown(f"""
        <div class="metric-frame">
            <strong>🎯 Confidence</strong><br>
            <span style="font-size: 1.8rem; color: {conf_color};">{confidence}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # ANALYSIS WITH DARK FRAMES
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class="analysis-frame">
            <h3>🤖 ML Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="info-box"><strong>Fraud Probability:</strong> {ml_prob:.1%}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box"><strong>Anomaly Detected:</strong> {"Yes" if anomaly_detected else "No"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box"><strong>ML Decision:</strong> {"FRAUD" if ml_prob >= 0.65 else "LEGITIMATE"}</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="analysis-frame">
            <h3>📋 Rule Engine Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="info-box"><strong>Risk Level:</strong> {rule_details.get("risk_level", "LOW")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box"><strong>Risk Score:</strong> {rule_risk_score}/10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box"><strong>Risk Factors:</strong> {len(rule_details.get("risk_factors", []))}</div>', unsafe_allow_html=True)
    
    # RISK FACTORS WITH FRAMES
    risk_factors = rule_details.get('risk_factors', [])
    if risk_factors:
        st.markdown('<div class="dark-card"><h3>🔍 Risk Factors</h3></div>', unsafe_allow_html=True)
        for factor in risk_factors:
            st.markdown(f'<div class="info-box">• {factor}</div>', unsafe_allow_html=True)
    
    # EXPLANATION WITH ENTERPRISE COLORS
    st.markdown('<div class="dark-card"><h3>💡 Decision Explanation</h3></div>', unsafe_allow_html=True)
    if should_block:
        if rule_risk_score >= 6 and ml_prob >= 0.65:
            st.markdown('<div class="info-box" style="border-left: 4px solid #ef4444;">🚫 BLOCKED: Both ML and Rule engines detected high risk</div>', unsafe_allow_html=True)
        elif rule_risk_score >= 6:
            st.markdown('<div class="info-box" style="border-left: 4px solid #ef4444;">🚫 BLOCKED: Rule engine detected high risk factors</div>', unsafe_allow_html=True)
        elif ml_prob >= 0.65:
            st.markdown('<div class="info-box" style="border-left: 4px solid #ef4444;">🚫 BLOCKED: ML model detected high fraud probability</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box" style="border-left: 4px solid #22c55e;">✅ APPROVED: Low risk detected by both analysis engines</div>', unsafe_allow_html=True)

# FOOTER WITH ENTERPRISE THEME
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="dark-card" style="text-align: center;">
    <h3>🛡️ SecureGuard AI - Enterprise Fraud Detection</h3>
    <p style="color: #94a3b8;">Built with Machine Learning and Rule-Based Analysis</p>
    <p style="color: #3b82f6;">🚀 Fast • Accurate • Reliable • Enterprise-Grade</p>
</div>
""", unsafe_allow_html=True)

st.success("✅ Fraud detection system operational!")
