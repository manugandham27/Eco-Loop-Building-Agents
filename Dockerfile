# EcoLoop AI - Production Dockerfile
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies (build essentials & sqlite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sqlite3 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose Streamlit dashboard port
EXPOSE 8501

# Default command: launch Streamlit Dashboard
CMD ["streamlit", "run", "app/dashboard/dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
