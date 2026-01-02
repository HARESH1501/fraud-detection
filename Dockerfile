# Multi-stage Dockerfile for SecureGuard AI
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Create startup script
RUN echo '#!/bin/bash\n\
python api/app.py &\n\
streamlit run web/web_app.py --server.port 8501 --server.address 0.0.0.0\n\
wait' > start.sh && chmod +x start.sh

# Start both services
CMD ["./start.sh"]