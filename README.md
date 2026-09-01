# EcoLoop AI: Closed-Loop Building HVAC Automation Platform

EcoLoop AI is an open-source building automation system built for the Honeywell Hackathon. It connects building energy simulations (EnergyPlus) with local or open-source LLMs using the Model Context Protocol (MCP) to optimize HVAC setpoints, lower energy bills, and maintain occupant thermal comfort without manual intervention.

---

## What It Does
- **Closed-Loop Control**: Runs a continuous cycle that reads building sensor data, predicts weather trends, calculates thermal comfort, and updates HVAC setpoints every 15 minutes.
- **Model Context Protocol (MCP)**: Communicates through 10 standard MCP tool calls (`ReadCurrentState`, `ModifySetpoints`, `ReadWeather`, `DiagnoseBuildingHealth`, `EvaluateDemandResponse`) rather than editing raw code or configuration files.
- **Physics-Based Simulation**: Uses PyEnergyPlus bindings when installed, or falls back to an internal 1st-order thermodynamic heat balance simulator so it runs reliably out of the box on any system.
- **Multi-Objective Optimization**: Evaluates setpoint changes against occupant comfort (Fanger PMV index), power consumption (kW), electricity tariffs ($/kWh), and grid carbon intensity (kg CO2/kWh).
- **Fault Detection & Diagnostics (FDD)**: Monitors sensor telemetry to flag filter clogging, compressor degradation, and high indoor CO2 levels.
- **Real-Time Visual Dashboard**: Includes a Streamlit web application with interactive Plotly charts, AI reasoning logs, baseline energy comparisons, and a CSV data exporter.

---

## Project Structure
```
Honeywell/
├── app/
│   ├── agents/          # Reasoning agent & prompt templates
│   ├── config/          # Policy parameters & settings loader
│   ├── controllers/     # Closed-loop orchestrator loop
│   ├── dashboard/       # Streamlit web UI & What-If stress tester
│   ├── database/        # SQLite models & telemetry database
│   ├── energyplus/      # PyEnergyPlus C-API wrapper & physics simulator
│   ├── mcp/             # MCP server tool definitions
│   ├── services/        # Optimization, evaluation, FDD & demand response
│   ├── simulation/      # Sensor formatting & EPW weather parser
│   ├── utils/           # Structured logging utility
│   └── tests/           # Pytest suite for simulation & controller
├── docs/                # Architecture, design & presentation docs
├── config.yaml          # System policies, tariff rates & target bounds
├── Dockerfile           # Production container build
├── docker-compose.yml   # Multi-service container orchestration
├── requirements.txt     # Python package requirements
└── run.py               # Main CLI runner
```

---

## Quickstart Guide

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/Honeywell/EcoLoop-AI.git
cd Honeywell

# Set up Python virtual environment
python3.12 -m venv .venv312
source .venv312/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run Headless Simulation Loop
To run 24 simulation steps headlessly from the terminal:
```bash
PYTHONPATH=. python3 run.py --mode run --steps 24
```

### 3. Launch Web Dashboard
To launch the interactive Streamlit web dashboard:
```bash
streamlit run app/dashboard/dashboard.py
```
Open **`http://localhost:8501`** in your browser.

### 4. Launch FastAPI REST Server
To start the REST API server and view interactive Swagger documentation:
```bash
uvicorn app.main:app --port 8000
```
Open **`http://localhost:8000/docs`** in your browser.

### 5. Run Pytest Suite
```bash
PYTHONPATH=. pytest app/tests/
```

---

## Key Metrics Recorded (24-Step Benchmark Run)
- **HVAC Energy Savings**: 21.87% reduction vs fixed baseline (21.0°C cooling).
- **Thermal Comfort Preservation**: 100% PMV index compliance during occupied hours (PMV between -0.5 and +0.5).
- **Carbon Reduction**: 1.0 kg CO2 saved per day per zone.

---

## Technical Documentation
- [System Architecture](docs/architecture.md)
- [System Design & Physics Equations](docs/system_design.md)
- [Prompt Engineering & Heuristics](docs/prompt_design.md)
- [Developer Guide](docs/developer_guide.md)
- [Deployment Guide](docs/deployment_guide.md)
- [Evaluation Criteria Alignment](docs/evaluation_summary.md)
- [6-Slide Hackathon Presentation Deck](docs/presentation_deck.md)
- [3-Minute Video Recording Script](docs/video_script.md)
