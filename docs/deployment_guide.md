# EcoLoop AI Deployment Guide

EcoLoop AI can be deployed in two modes:
1. **Local Development Mode**: Direct Python execution via virtual environment.
2. **Docker Container Mode**: Multi-container Docker deployment for production environments.

---

## 1. Local Deployment
```bash
cd Honeywell
source .venv312/bin/activate
PYTHONPATH=. python3 run.py --mode run --steps 24
streamlit run app/dashboard/dashboard.py
```

---

## 2. Docker Container Deployment

### Single Container Build
```bash
# Build Docker image
docker build -t ecoloop-ai:latest .

# Run dashboard container
docker run -d -p 8501:8501 --name ecoloop_app ecoloop-ai:latest
```
Access dashboard at `http://localhost:8501`.

### Multi-Service Docker Compose
```bash
# Launch both dashboard and headless background engine
docker-compose up -d
```

---

## Environment Variables
- `OPENAI_API_KEY`: API key for LLM endpoint (optional; fallback engineering rule engine activates if not provided).
- `OPENAI_API_BASE`: Target LLM API endpoint URL (default: `https://api.openai.com/v1`).
