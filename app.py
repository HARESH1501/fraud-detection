"""
Simple Streamlit App Entry Point for Cloud Deployment
"""

import streamlit as st
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import and run the standalone app
try:
    from web.streamlit_standalone import *
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please check if all required files are present in the repository.")