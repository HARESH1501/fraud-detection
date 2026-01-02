import streamlit as st

st.title("🛡️ Fraud Detection Test")
st.success("✅ SUCCESS! App is working!")

amount = st.number_input("Amount", value=1000)
if st.button("Check"):
    if amount > 5000:
        st.error("🚨 FRAUD")
    else:
        st.success("✅ SAFE")

st.write("If you see this, the deployment is working!")