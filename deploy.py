#!/usr/bin/env python3
"""
SecureGuard AI Deployment Script
Supports multiple cloud platforms and local deployment
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True):
    """Run shell command with error handling"""
    print(f"🔄 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)
    
    if result.stdout:
        print(result.stdout)
    
    return result

def deploy_local():
    """Deploy locally using Docker"""
    print("🚀 Deploying SecureGuard AI locally...")
    
    # Build Docker image
    run_command("docker build -t secureguard-ai .")
    
    # Stop existing container if running
    run_command("docker stop secureguard-ai", check=False)
    run_command("docker rm secureguard-ai", check=False)
    
    # Run new container
    run_command("""
        docker run -d \
        --name secureguard-ai \
        -p 8000:8000 \
        -p 8501:8501 \
        secureguard-ai
    """)
    
    print("✅ Deployment complete!")
    print("🌐 Web Interface: http://localhost:8501")
    print("🔧 API Docs: http://localhost:8000/docs")

def deploy_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    # Check if Heroku CLI is installed
    result = run_command("heroku --version", check=False)
    if result.returncode != 0:
        print("❌ Heroku CLI not found. Please install it first.")
        return
    
    # Create Procfile for Heroku
    with open("Procfile", "w") as f:
        f.write("web: python api/app.py & streamlit run web/web_app.py --server.port $PORT --server.address 0.0.0.0\n")
    
    # Create runtime.txt
    with open("runtime.txt", "w") as f:
        f.write("python-3.11.0\n")
    
    # Initialize git if needed
    if not Path(".git").exists():
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit"')
    
    # Create Heroku app
    app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
    if app_name:
        run_command(f"heroku create {app_name}")
    else:
        run_command("heroku create")
    
    # Deploy
    run_command("git push heroku main")
    
    print("✅ Heroku deployment complete!")

def deploy_streamlit_cloud():
    """Instructions for Streamlit Cloud deployment"""
    print("🚀 Streamlit Cloud Deployment Instructions:")
    print("""
    1. Push your code to GitHub
    2. Go to https://share.streamlit.io/
    3. Connect your GitHub account
    4. Select your repository
    5. Set main file path: web/web_app.py
    6. Deploy!
    
    Note: For Streamlit Cloud, you'll need to modify the app to work without the FastAPI backend
    or deploy the API separately.
    """)

def deploy_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    
    # Check if Railway CLI is installed
    result = run_command("railway --version", check=False)
    if result.returncode != 0:
        print("❌ Railway CLI not found. Installing...")
        run_command("npm install -g @railway/cli")
    
    # Login and deploy
    run_command("railway login")
    run_command("railway init")
    run_command("railway up")
    
    print("✅ Railway deployment complete!")

def main():
    parser = argparse.ArgumentParser(description="Deploy SecureGuard AI")
    parser.add_argument(
        "platform", 
        choices=["local", "heroku", "streamlit", "railway"],
        help="Deployment platform"
    )
    
    args = parser.parse_args()
    
    print("🛡️ SecureGuard AI Deployment Tool")
    print("=" * 40)
    
    if args.platform == "local":
        deploy_local()
    elif args.platform == "heroku":
        deploy_heroku()
    elif args.platform == "streamlit":
        deploy_streamlit_cloud()
    elif args.platform == "railway":
        deploy_railway()

if __name__ == "__main__":
    main()