# EcoLoop AI Developer Guide

## Local Setup
1. Clone the repository and navigate to the project root:
   ```bash
   cd Honeywell
   ```
2. Create and activate a Python 3.12 virtual environment:
   ```bash
   python3.12 -m venv .venv312
   source .venv312/bin/activate
   ```
3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Platform
- **Headless Mode** (Runs N closed-loop simulation steps from CLI):
  ```bash
  PYTHONPATH=. python3 run.py --mode run --steps 24
  ```
- **Web Dashboard** (Launches interactive Streamlit UI):
  ```bash
  streamlit run app/dashboard/dashboard.py
  ```
- **FastAPI REST Server** (Launches API server with Swagger docs):
  ```bash
  uvicorn app.main:app --port 8000
  ```

## Running Unit & Integration Tests
Run pytest to verify simulation, controller, database, and agent modules:
```bash
PYTHONPATH=. pytest app/tests/
```
