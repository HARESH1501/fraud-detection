#!/usr/bin/env python3
"""
SecureGuard AI Application Launcher
Starts both FastAPI backend and Streamlit frontend
"""

import subprocess
import time
import sys
import os
from threading import Thread
import webbrowser

def start_api():
    """Start FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    subprocess.run([sys.executable, "api/app.py"])

def start_streamlit():
    """Start Streamlit frontend"""
    print("🌐 Starting Streamlit frontend...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "web/web_app.py"])

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'streamlit', 'pandas', 
        'numpy', 'scikit-learn', 'lightgbm', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ Packages installed successfully!")

def main():
    print("🛡️ SecureGuard AI - Advanced Fraud Detection System")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Start both services in separate threads
    api_thread = Thread(target=start_api, daemon=True)
    streamlit_thread = Thread(target=start_streamlit, daemon=True)
    
    print("🔄 Starting services...")
    
    # Start API first
    api_thread.start()
    time.sleep(3)  # Give API time to start
    
    # Start Streamlit
    streamlit_thread.start()
    time.sleep(5)  # Give Streamlit time to start
    
    # Open browser
    print("🌐 Opening web browser...")
    webbrowser.open("http://localhost:8501")
    
    print("\n✅ SecureGuard AI is running!")
    print("🌐 Web Interface: http://localhost:8501")
    print("🔧 API Documentation: http://localhost:8000/docs")
    print("📊 Health Check: http://localhost:8000/health")
    print("\n⚠️  Press Ctrl+C to stop all services")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down SecureGuard AI...")
        print("👋 Thank you for using SecureGuard AI!")

if __name__ == "__main__":
    main()