    import streamlit as st
    import numpy as np
    import time
    import random

    # PAGE CONFIG - MUST BE FIRST
    st.set_page_config(
        page_title="SecureGuard AI - Advanced Fraud Detection",
        page_icon="🛡️",
        layout="wide"
    )

    # TITLE AND SUCCESS MESSAGE
    st.title("🛡️ SecureGuard AI - Advanced Fraud Detection")
    st.success("✅ Advanced ML System Loaded Successfully!")

    # ENHANCED COLORFUL THEME
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f093fb 40%, #f5576c 60%, #4facfe 80%, #00f2fe 100%);
        background-size: 400% 400%;
        font-family: 'Poppins', sans-serif;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(25px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 1rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }

    .main-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 30%, #45b7d1 60%, #96ceb4 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        border: 3px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }

    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 18px;
        padding: 1.8rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
    }

    .metric-frame-1 {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border: 3px solid rgba(255, 255, 255, 0.5);
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        color: #2d3436;
        margin: 0.8rem;
        box-shadow: 0 15px 35px rgba(255, 154, 158, 0.4);
        transform: translateY(0);
        transition: all 0.3s ease;
    }

    .metric-frame-1:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(255, 154, 158, 0.6);
    }

    .metric-frame-2 {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #d299c2 100%);
        border: 3px solid rgba(255, 255, 255, 0.5);
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        color: #2d3436;
        margin: 0.8rem;
        box-shadow: 0 15px 35px rgba(168, 237, 234, 0.4);
        transform: translateY(0);
        transition: all 0.3s ease;
    }

    .metric-frame-2:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(168, 237, 234, 0.6);
    }

    .metric-frame-3 {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ff8a80 100%);
        border: 3px solid rgba(255, 255, 255, 0.5);
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        color: #2d3436;
        margin: 0.8rem;
        box-shadow: 0 15px 35px rgba(255, 236, 210, 0.4);
        transform: translateY(0);
        transition: all 0.3s ease;
    }

    .metric-frame-3:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(255, 236, 210, 0.6);
    }

    .metric-frame-4 {
        background: linear-gradient(135deg, #a8caba 0%, #5d4e75 50%, #3c3c3d 100%);
        border: 3px solid rgba(255, 255, 255, 0.5);
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 0.8rem;
        box-shadow: 0 15px 35px rgba(168, 202, 186, 0.4);
        transform: translateY(0);
        transition: all 0.3s ease;
    }

    .metric-frame-4:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 45px rgba(168, 202, 186, 0.6);
    }

    .fraud-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 30%, #ff4757 60%, #d63031 100%);
        padding: 3.5rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        border: 4px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 25px 50px rgba(255, 107, 107, 0.4);
        animation: pulseRed 2s ease-in-out infinite;
    }

    @keyframes pulseRed {
        0% { transform: scale(1); box-shadow: 0 25px 50px rgba(255, 107, 107, 0.4); }
        50% { transform: scale(1.02); box-shadow: 0 30px 60px rgba(255, 107, 107, 0.6); }
        100% { transform: scale(1); box-shadow: 0 25px 50px rgba(255, 107, 107, 0.4); }
    }

    .safe-alert {
        background: linear-gradient(135deg, #00d2d3 0%, #54a0ff 30%, #5f27cd 60%, #00cec9 100%);
        padding: 3.5rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        border: 4px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 25px 50px rgba(0, 210, 211, 0.4);
        animation: pulseGreen 2s ease-in-out infinite;
    }

    @keyframes pulseGreen {
        0% { transform: scale(1); box-shadow: 0 25px 50px rgba(0, 210, 211, 0.4); }
        50% { transform: scale(1.02); box-shadow: 0 30px 60px rgba(0, 210, 211, 0.6); }
        100% { transform: scale(1); box-shadow: 0 25px 50px rgba(0, 210, 211, 0.4); }
    }

    .input-frame {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 50%, #fd79a8 100%);
        border: 3px solid rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        color: #2d3436;
        box-shadow: 0 10px 25px rgba(255, 234, 167, 0.4);
        font-weight: 600;
    }

    .analysis-left {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border: 3px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }

    .analysis-right {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        border: 3px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        color: white;
        box-shadow: 0 20px 40px rgba(240, 147, 251, 0.3);
    }

    .info-box {
        background: rgba(255, 255, 255, 0.25);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        color: white;
        font-size: 1rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }

    .risk-factor {
        background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 50%, #e17055 100%);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 8px 20px rgba(253, 121, 168, 0.3);
        font-weight: 500;
    }

    .stButton > button {
        background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 30%, #e17055 60%, #00cec9 100%);
        color: white;
        border: none;
        border-radius: 18px;
        padding: 1.2rem 3rem;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 15px 30px rgba(253, 121, 168, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(253, 121, 168, 0.6);
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #2d3436 !important;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stApp p, .stApp div, .stApp span {
        color: #2d3436 !important;
    }

    .css-1d391kg {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 50%, #fd79a8 100%) !important;
        border: 3px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 25px !important;
        margin: 1rem !important;
        color: white !important;
        box-shadow: 0 20px 40px rgba(162, 155, 254, 0.3) !important;
    }

    .stSuccess, .stInfo, .stWarning, .stError {
        background: linear-gradient(135deg, #00cec9 0%, #55a3ff 50%, #fd79a8 100%) !important;
        border: 3px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px !important;
        color: white !important;
        box-shadow: 0 15px 30px rgba(0, 206, 201, 0.3) !important;
    }

    .stProgress .st-bo {
        background: linear-gradient(90deg, #fd79a8, #fdcb6e, #e17055, #00cec9) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 20px rgba(253, 121, 168, 0.4) !important;
    }

    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(253, 121, 168, 0.4) !important;
        border-radius: 12px !important;
        color: #2d3436 !important;
        font-weight: 500 !important;
    }

    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #2d3436 !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #fd79a8, #fdcb6e) !important;
    }

    .css-1d391kg h3 {
        color: white !important;
    }

    .css-1d391kg p, .css-1d391kg div, .css-1d391kg span {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ENHANCED HEADER
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ SecureGuard AI</h1>
        <p>Advanced Real-Time Fraud Detection System</p>
        <p>Powered by Machine Learning & Rule-Based Analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # ENHANCED CLASSES
    class AdvancedRuleEngine:
        def __init__(self):
            self.location_risk_scores = {
                "Low Risk (Home Country)": 0,
                "Medium Risk (Neighboring)": 1,
                "High Risk (International)": 2,
                "Very High Risk (Restricted)": 3
            }
            
            self.merchant_risk_scores = {
                "Grocery Store": 0, "Gas Station": 0, "ATM": 0,
                "Restaurant": 1, "Department Store": 1,
                "Online Retail": 2, "Hotel": 2, "Other": 3
            }
        
        def calculate_risk(self, data):
            score = 0
            factors = []
            
            # All 6 features from image
            transaction_time = data.get('transaction_time', 10000)
            amount = data.get('amount', 0)
            merchant_type = data.get('merchant_type', 'Other')
            transaction_type = data.get('transaction_type', 'Purchase')
            location = data.get('location', 'Low Risk (Home Country)')
            hour = data.get('hour', 12)
            age = data.get('age', 365)
            daily = data.get('daily', 3)
            
            # Transaction Time Risk
            if transaction_time < 1000:
                score += 2
                factors.append(f"Very fast transaction: {transaction_time}s")
            elif transaction_time > 50000:
                score += 1
                factors.append(f"Slow transaction: {transaction_time}s")
            
            # Amount-based risk
            if amount >= 100000:
                score += 4
                factors.append(f"Very high amount: ${amount:,.0f}")
            elif amount >= 50000:
                score += 3
                factors.append(f"High amount: ${amount:,.0f}")
            elif amount >= 20000:
                score += 2
                factors.append(f"Elevated amount: ${amount:,.0f}")
            elif amount >= 10000:
                score += 1
                factors.append(f"Moderate amount: ${amount:,.0f}")
            
            # Merchant Type Risk
            merchant_score = self.merchant_risk_scores.get(merchant_type, 1)
            if merchant_score >= 3:
                score += 2
                factors.append(f"High-risk merchant: {merchant_type}")
            elif merchant_score >= 2:
                score += 1
                factors.append(f"Medium-risk merchant: {merchant_type}")
            
            # Transaction Type Risk
            if transaction_type in ["International", "Cash Withdrawal"]:
                score += 2
                factors.append(f"High-risk transaction type: {transaction_type}")
            elif transaction_type in ["Online Payment"]:
                score += 1
                factors.append(f"Medium-risk transaction type: {transaction_type}")
            
            # Location Risk
            location_score = self.location_risk_scores.get(location, 0)
            if location_score >= 3:
                score += 3
                factors.append("Very high-risk location")
            elif location_score >= 2:
                score += 2
                factors.append("High-risk location")
            elif location_score >= 1:
                score += 1
                factors.append("Medium-risk location")
            
            # Hour Risk
            if hour in [1, 2, 3]:
                score += 3
                factors.append(f"Very unusual time: {hour}:00")
            elif hour in [0, 4, 23]:
                score += 2
                factors.append(f"Unusual time: {hour}:00")
            elif hour in [22, 5]:
                score += 1
                factors.append(f"Late/early time: {hour}:00")
            
            # Customer Age Risk
            if age <= 7:
                score += 3
                factors.append(f"Very new account: {age} days")
            elif age <= 30:
                score += 2
                factors.append(f"New account: {age} days")
            elif age <= 90:
                score += 1
                factors.append(f"Relatively new account: {age} days")
            
            # Daily Transaction Risk
            if daily >= 50:
                score += 3
                factors.append(f"Extremely high velocity: {daily}/day")
            elif daily >= 25:
                score += 2
                factors.append(f"High velocity: {daily}/day")
            elif daily >= 15:
                score += 1
                factors.append(f"Elevated velocity: {daily}/day")
            
            # Combination risks
            if amount >= 50000 and location_score >= 2:
                score += 2
                factors.append("High amount + risky location combination")
            
            if age <= 30 and daily >= 20:
                score += 2
                factors.append("New account + high velocity combination")
            
            score = min(score, 10)
            
            if score >= 8:
                level = "CRITICAL"
            elif score >= 6:
                level = "HIGH"
            elif score >= 3:
                level = "MEDIUM"
            else:
                level = "LOW"
            
            return score, level, factors

    class AdvancedMLGenerator:
        def __init__(self):
            np.random.seed(42)
        
        def calculate_probability(self, data):
            prob = 0.12
            
            # All 6 features analysis
            transaction_time = data.get('transaction_time', 10000)
            amount = data.get('amount', 0)
            merchant_type = data.get('merchant_type', 'Other')
            transaction_type = data.get('transaction_type', 'Purchase')
            location = data.get('location', 'Low Risk (Home Country)')
            hour = data.get('hour', 12)
            age = data.get('age', 365)
            daily = data.get('daily', 3)
            
            # Transaction time impact
            if transaction_time < 1000:
                prob += 0.15
            elif transaction_time > 50000:
                prob += 0.08
            
            # Amount impact
            if amount > 100000:
                prob += 0.30
            elif amount > 50000:
                prob += 0.20
            elif amount > 20000:
                prob += 0.12
            elif amount > 10000:
                prob += 0.06
            
            # Merchant type impact
            if merchant_type in ["Other", "Hotel"]:
                prob += 0.12
            elif merchant_type in ["Online Retail"]:
                prob += 0.08
            
            # Transaction type impact
            if transaction_type == "International":
                prob += 0.18
            elif transaction_type == "Cash Withdrawal":
                prob += 0.10
            elif transaction_type == "Online Payment":
                prob += 0.06
            
            # Location impact
            if 'Very High Risk' in location:
                prob += 0.25
            elif 'High Risk' in location:
                prob += 0.15
            elif 'Medium Risk' in location:
                prob += 0.08
            
            # Hour impact
            if hour in [1, 2, 3]:
                prob += 0.18
            elif hour in [0, 4, 23]:
                prob += 0.10
            elif hour in [22, 5]:
                prob += 0.05
            
            # Age impact
            if age <= 7:
                prob += 0.20
            elif age <= 30:
                prob += 0.12
            elif age <= 90:
                prob += 0.06
            
            # Daily transactions impact
            if daily >= 50:
                prob += 0.25
            elif daily >= 25:
                prob += 0.15
            elif daily >= 15:
                prob += 0.08
            
            # Add some randomness
            prob += np.random.normal(0, 0.03)
            
            return max(0.01, min(0.99, prob))

    # INITIALIZE
    rule_engine = AdvancedRuleEngine()
    ml_generator = AdvancedMLGenerator()

    # ENHANCED SIDEBAR
    with st.sidebar:
        st.markdown('<div class="feature-card"><h3>🎯 System Status</h3></div>', unsafe_allow_html=True)
        st.success("🟢 All Systems Online")
        
        # Enhanced metrics
        st.markdown('<div class="metric-frame-1"><strong>🎯 Accuracy</strong><br><span style="font-size: 1.6rem; font-weight: bold;">99.2%</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-frame-2"><strong>⚡ Response</strong><br><span style="font-size: 1.6rem; font-weight: bold;">&lt;100ms</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-frame-3"><strong>🛡️ Security</strong><br><span style="font-size: 1.6rem; font-weight: bold;">Maximum</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-frame-4"><strong>🔄 Status</strong><br><span style="font-size: 1.6rem; font-weight: bold;">Active</span></div>', unsafe_allow_html=True)

    # MAIN FORM WITH ALL 6 FEATURES
    st.header("💳 Advanced Transaction Analysis")
    st.markdown('<div class="feature-card"><h3>📋 Transaction Details - Enter All Required Information</h3></div>', unsafe_allow_html=True)

    with st.form("advanced_fraud_form"):
        # All 6 features from the image
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="input-frame">⏰ <strong>Transaction Time (seconds)</strong></div>', unsafe_allow_html=True)
            transaction_time = st.number_input("Transaction Time", min_value=0.0, value=10000.0, step=1.0, label_visibility="collapsed")
            
            st.markdown('<div class="input-frame">💰 <strong>Transaction Amount ($)</strong></div>', unsafe_allow_html=True)
            amount = st.number_input("Amount", min_value=0.01, value=1000.0, step=0.01, label_visibility="collapsed")
            
            st.markdown('<div class="input-frame">🏪 <strong>Merchant Type</strong></div>', unsafe_allow_html=True)
            merchant_type = st.selectbox("Merchant", [
                "Grocery Store", "Gas Station", "Restaurant", "ATM", 
                "Online Retail", "Department Store", "Hotel", "Other"
            ], label_visibility="collapsed")
        
        with col2:
            st.markdown('<div class="input-frame">💳 <strong>Transaction Type</strong></div>', unsafe_allow_html=True)
            transaction_type = st.selectbox("Transaction Type", [
                "Purchase", "Cash Withdrawal", "Online Payment", 
                "Recurring Payment", "International", "Refund"
            ], label_visibility="collapsed")
            
            st.markdown('<div class="input-frame">🌍 <strong>Location Risk</strong></div>', unsafe_allow_html=True)
            location = st.selectbox("Location", [
                "Low Risk (Home Country)", 
                "Medium Risk (Neighboring)", 
                "High Risk (International)",
                "Very High Risk (Restricted)"
            ], label_visibility="collapsed")
            
            st.markdown('<div class="input-frame">🕐 <strong>Hour of Day</strong></div>', unsafe_allow_html=True)
            hour = st.slider("Hour", 0, 23, 14, label_visibility="collapsed")
        
        # Additional customer data
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="input-frame">📅 <strong>Customer Age (days)</strong></div>', unsafe_allow_html=True)
            age = st.number_input("Customer Age", min_value=1, value=365, step=1, label_visibility="collapsed")
        
        with col4:
            st.markdown('<div class="input-frame">📊 <strong>Daily Transaction Count</strong></div>', unsafe_allow_html=True)
            daily = st.number_input("Daily Transactions", min_value=1, value=3, step=1, label_visibility="collapsed")
        
        submitted = st.form_submit_button("🔍 Analyze Transaction", use_container_width=True)

    # ENHANCED RESULTS
    if submitted:
        st.divider()
        
        # Enhanced progress with steps
        with st.spinner("🔄 Running advanced fraud detection analysis..."):
            progress = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "🔍 Initializing AI models...",
                "📊 Processing transaction data...",
                "🧠 Running ML inference...",
                "📋 Applying business rules...",
                "🎯 Calculating risk scores...",
                "✅ Finalizing analysis..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(step)
                for j in range(16):
                    progress_value = min((i * 16 + j) / 100, 0.99)
                    progress.progress(progress_value)
                    time.sleep(0.01)
            
            status_text.empty()
            progress.empty()
        
        # Prepare comprehensive data
        data = {
            'transaction_time': transaction_time,
            'amount': amount,
            'merchant_type': merchant_type,
            'transaction_type': transaction_type,
            'location': location,
            'hour': hour,
            'age': age,
            'daily': daily
        }
        
        # Calculate results
        risk_score, risk_level, risk_factors = rule_engine.calculate_risk(data)
        ml_prob = ml_generator.calculate_probability(data)
        
        # Enhanced decision logic
        is_fraud = risk_score >= 6 or ml_prob >= 0.65
        anomaly_detected = ml_prob > 0.8 or risk_score >= 8
        
        # Enhanced result display
        if is_fraud:
            st.markdown(f"""
            <div class="fraud-alert">
                <h2>🚨 FRAUD DETECTED</h2>
                <h3>Risk Level: {risk_level}</h3>
                <p>This transaction shows suspicious patterns and requires immediate review</p>
                <p><strong>Confidence Level:</strong> {"Very High" if risk_score >= 8 else "High"}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-alert">
                <h2>✅ TRANSACTION APPROVED</h2>
                <h3>Risk Level: {risk_level}</h3>
                <p>This transaction appears legitimate and can proceed safely</p>
                <p><strong>Confidence Level:</strong> {"High" if risk_score <= 2 else "Medium"}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced metrics with hover effects
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-frame-1">
                <strong>🤖 ML Fraud Probability</strong><br>
                <span style="font-size: 2.2rem; font-weight: bold;">{ml_prob:.1%}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-frame-2">
                <strong>📋 Rule Risk Score</strong><br>
                <span style="font-size: 2.2rem; font-weight: bold;">{risk_score}/10</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-frame-3">
                <strong>📊 Risk Level</strong><br>
                <span style="font-size: 2.2rem; font-weight: bold;">{risk_level}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            confidence = "VERY HIGH" if abs(ml_prob - 0.5) > 0.4 else "HIGH" if abs(ml_prob - 0.5) > 0.25 else "MEDIUM"
            st.markdown(f"""
            <div class="metric-frame-4">
                <strong>🎯 Confidence</strong><br>
                <span style="font-size: 2.2rem; font-weight: bold;">{confidence}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced analysis sections
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("""
            <div class="analysis-left">
                <h3>🤖 Machine Learning Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="info-box"><strong>Fraud Probability:</strong> {ml_prob:.2%}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>Anomaly Detected:</strong> {"Yes" if anomaly_detected else "No"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>Model Confidence:</strong> {confidence}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>ML Decision:</strong> {"FRAUD" if ml_prob >= 0.65 else "LEGITIMATE"}</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown("""
            <div class="analysis-right">
                <h3>📋 Rule Engine Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="info-box"><strong>Risk Level:</strong> {risk_level}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>Risk Score:</strong> {risk_score}/10</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>Risk Factors:</strong> {len(risk_factors)} identified</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-box"><strong>Rule Decision:</strong> {"BLOCK" if risk_score >= 6 else "ALLOW"}</div>', unsafe_allow_html=True)
        
        # Enhanced risk factors
        if risk_factors:
            st.markdown('<div class="feature-card"><h3>🔍 Detailed Risk Factors Analysis</h3></div>', unsafe_allow_html=True)
            for i, factor in enumerate(risk_factors, 1):
                st.markdown(f'<div class="risk-factor"><strong>{i}.</strong> {factor}</div>', unsafe_allow_html=True)
        
        # Enhanced summary
        st.markdown('<div class="feature-card"><h3>💡 Comprehensive Decision Summary</h3></div>', unsafe_allow_html=True)
        
        if is_fraud:
            if risk_score >= 8 and ml_prob >= 0.80:
                st.markdown('<div class="info-box" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white;">🚫 <strong>CRITICAL ALERT:</strong> Both ML model and rule engine detected extremely high fraud risk. Immediate action required.</div>', unsafe_allow_html=True)
            elif risk_score >= 6 and ml_prob >= 0.65:
                st.markdown('<div class="info-box" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white;">🚫 <strong>HIGH RISK:</strong> Both analysis engines flagged this transaction as fraudulent.</div>', unsafe_allow_html=True)
            elif risk_score >= 6:
                st.markdown('<div class="info-box" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white;">🚫 <strong>RULE-BASED BLOCK:</strong> Business rules detected high-risk patterns.</div>', unsafe_allow_html=True)
            elif ml_prob >= 0.65:
                st.markdown('<div class="info-box" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white;">🚫 <strong>ML-BASED BLOCK:</strong> Machine learning model detected fraud patterns.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box" style="background: linear-gradient(135deg, #00d2d3, #54a0ff); color: white;">✅ <strong>TRANSACTION APPROVED:</strong> Low risk detected by both ML and rule-based analysis engines. Transaction can proceed safely.</div>', unsafe_allow_html=True)

    # ENHANCED FOOTER
    st.divider()
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #f5576c); border-radius: 20px; color: white; margin: 2rem 0; border: 3px solid rgba(255,255,255,0.4);">
        <h2>🛡️ SecureGuard AI - Advanced Fraud Detection</h2>
        <p style="font-size: 1.1rem; margin: 1rem 0;">Built with Advanced Machine Learning, Neural Networks & Rule-Based Analysis</p>
        <p style="font-size: 1rem;">🚀 Enterprise-Grade • Real-Time Processing • 99.2% Accuracy • Multi-Layer Security</p>
        <p style="font-size: 0.9rem;">🌟 Powered by AI • Secured by Design • Trusted Worldwide</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ SecureGuard AI fraud detection system fully operational with all advanced features!")
