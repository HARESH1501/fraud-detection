"""
Streamlit Cloud Deployment Entry Point
This file is required for Streamlit Cloud deployment
"""

# Import the standalone web application (works without FastAPI)
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the standalone Streamlit app
from web.streamlit_standalone import *

# Note: Streamlit Cloud will automatically run this file