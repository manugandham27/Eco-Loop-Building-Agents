# EcoLoop AI System Architecture

## System Overview

EcoLoop AI is a physical building automation platform designed to control HVAC setpoints dynamically based on weather forecasts, occupancy, electricity prices, and carbon intensity.

```
                      +-----------------------------+
                      |    Streamlit Dashboard UI   |
                      +--------------+--------------+
                                     |
                                     v
                      +--------------+--------------+
                      |   SQLite Database Storage   |
                      +--------------+--------------+
                                     ^
                                     |
+---------------------+      +-------+-------+      +---------------------+
| PyEnergyPlus /      | <--->|  MCP Server   |<---> | LangGraph / LLM     |
| Physics Simulator   |      | Tool Provider |      | Reasoning Agent     |
+---------------------+      +---------------+      +---------------------+
```

## Subsystem Breakdown

1. **Simulation Subsystem (`app/energyplus/`)**
   - Binds dynamically to PyEnergyPlus C-API libraries when present on the system.
   - Includes a fallback 1st-order zone heat balance simulator (modeling thermal mass, HVAC COP curves, occupant heat gains, and PMV index) so the project runs on any development environment without dependency crashes.

2. **Sensor Stream (`app/simulation/sensors.py`)**
   - Formats raw simulation output into validated Pydantic observation models (indoor/outdoor temperature, relative humidity, PMV comfort index, CO2 PPM levels, active power draw, grid tariffs, and carbon factors).

3. **MCP Tool Server (`app/mcp/server.py`)**
   - Standardizes operational tools for the AI agent: `ReadCurrentState`, `ModifySetpoints`, `RunSimulationStep`, `SaveMetrics`, `ReadWeather`, `DiagnoseBuildingHealth`, and `EvaluateDemandResponse`.

4. **Reasoning Agent (`app/agents/`)**
   - Prompts the LLM as a senior building energy engineer. Receives telemetry data, evaluates energy vs. comfort trade-offs, and outputs structured JSON setpoint recommendations.

5. **Optimization & Evaluation Engines (`app/services/`)**
   - Evaluates multi-objective scalar loss functions balancing energy, comfort, electricity costs, and grid carbon footprint. Computes cumulative performance metrics against fixed-setpoint baselines.

---

## Technical Design Rationale

### 1. Tool-Calling Isolation (MCP Standard)
The reasoning agent cannot directly edit files or source code. All control actions pass through validated MCP tools (`ModifySetpoints`). The controller enforces safety limits before applying setpoint changes (e.g. cooling setpoints are strictly bounded between 20.0°C and 27.0°C).

### 2. Prompt Engineering
The agent prompt enforces structured JSON output with quantitative explanations. The prompt requires the model to cite occupancy ratios, outdoor temperatures, price tiers, and expected PMV impact in its reasoning log.

### 3. Latency Management
To prevent LLM API delays from stalling the 15-minute simulation loop:
- Weather and tariff data are batched into a single 6-hour forecast payload per iteration.
- If API calls time out, the system uses an internal engineering rule engine to keep timesteps running without disruption.

### 4. Time-Series Data Handling
EnergyPlus runs produce high-frequency data. EcoLoop AI manages this by:
- Storing full step histories in SQLite indexed by `step` and `sim_time_hours`.
- Passing a compact sliding window of recent telemetry steps to the LLM agent, keeping token usage under 2,000 tokens per call.
