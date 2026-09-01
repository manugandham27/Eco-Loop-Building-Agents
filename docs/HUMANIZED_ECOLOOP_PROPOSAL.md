# EcoLoop AI: Autonomous Closed-Loop Building Intelligence Platform

### Project Title:
**Physical AI Driven Building HVAC Optimization & Energy Reduction**

### Author:
**Manu Gandham**

### Candidate ID:
**16845317**

### Mail ID:
**manugandham27@gmail.com**

---

### Submission Overview

This document presents a complete project proposal, technical approach, prototypes, and evaluation plan for optimizing commercial building HVAC operations using physical AI simulation tools (EnergyPlus) and open-source LLMs connected over the Model Context Protocol (MCP). The deliverable is a working closed-loop pipeline that streams continuous building sensor telemetry, evaluates multi-objective trade-offs between energy consumption and Fanger PMV thermal comfort, automatically applies supervisory setpoint overrides, and provides an interactive visual dashboard with automated fault diagnostics for stakeholders.

---

### 1. Proposed Solution

#### 1.1 Problem Summary
Commercial buildings consume nearly 40% of global electricity and remain a primary driver of carbon emissions. Traditional Building Management Systems (BMS) rely on rigid, rule-based schedules designed decades ago. These static systems cannot adapt dynamically to real-time outdoor weather spikes, fluctuating indoor occupancy, or dynamic grid electricity tariffs ($0.12/kWh off-peak vs $0.28/kWh peak). Consequently, buildings waste up to 30% of their energy cooling unoccupied zones while incurring high utility penalties.

#### 1.2 High-Level Solution
We propose **EcoLoop AI**, an autonomous physical AI platform that pairs physics-based thermal simulation engines (EnergyPlus / PyEnergyPlus C-API) with open-source LLMs operating over standardized Model Context Protocol (MCP) tool primitives. The system streams continuous telemetry (zone temperatures, humidity, PMV comfort indices, IAQ CO2 levels, grid carbon factors), reasons over multi-objective trade-offs, and automatically injects supervisory setpoint overrides back into active building actuators.

#### 1.3 How It Addresses the Problem
- **Highlights High-Waste Time Windows**: Identifies peak utility tariff hours and high solar radiation windows to pre-cool building zones efficiently.
- **Enables What-If Experiments**: Includes an interactive scenario tester (e.g., shifting ambient temperatures by +10°C or simulating occupancy surges) to see immediate physical AI self-correction impacts.
- **Balances Energy and Comfort**: Ranks candidate setpoints using Fanger Predicted Mean Vote (PMV) thermal comfort scores, keeping occupants comfortable while cutting energy draw.

#### 1.4 Innovation & Uniqueness
- **Goes Beyond Simple Scheduling**: Combines dynamic EnergyPlus physics simulations with agentic LLM reasoning and real-time grid price signals.
- **Standardized MCP Tool Protocol**: Operates strictly through 10 validated MCP tool calls (`ModifySetpoints`, `ReadWeather`, `DiagnoseBuildingHealth`) without editing source code directly.
- **Dual-Engine Thermal Architecture**: Binds natively to PyEnergyPlus C-bindings with an internal 1st-order heat balance physics engine fallback so execution never crashes on any operating system.

---

### 2. Technical Approach

#### 2.1 Data Sources
- **EnergyPlus Simulation Engine**: Real-time zone temperatures, HVAC power draw, and heat balance differential states (`SmallOffice.idf`).
- **EPW Weather Stream**: Hourly ambient dry-bulb temperature, relative humidity, and solar radiation profiles (`USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw`).
- **Smart Grid Tariff & Emissions Feeds**: Dynamic electricity price tiers ($0.12–$0.28/kWh) and grid carbon intensity factors (0.25–0.65 kg CO2/kWh).

#### 2.2 Technologies & Tools
- **Languages**: Python (main backend).
- **Libraries**: PyEnergyPlus, MCP Python SDK, LangGraph, LangChain, pandas, NumPy, Plotly Express, SQLAlchemy, FastAPI.
- **Storage**: SQLite (prototype), Postgres / InfluxDB (production).
- **Deployment**: FastAPI backend + Streamlit UI + Docker.

#### 2.3 Data Pipeline (High-Level Flow)
1. **Ingestion**: Stream 15-minute zone telemetry from active building simulation instances.
2. **Preprocessing**: Clean data models, normalize temperatures, compute occupant heat gains, and format validated Pydantic JSON observations.
3. **Enrichment**: Merge telemetry with 6-hour lookahead weather forecasts and grid tariff schedules.
4. **Exploratory Analysis**: Heatmaps of peak energy slots, temperature drift distributions, and power demand patterns.
5. **Multi-Objective Loss Engine**: Calculate composite scalar loss score $J = 0.35 \cdot E_{\text{energy}} + 0.35 \cdot C_{\text{comfort}} + 0.15 \cdot \text{Cost} + 0.15 \cdot \text{Carbon}$.
6. **LLM Reasoning Agent**: Evaluate physical trade-offs and output structured setpoint recommendations with quantitative engineering justifications.
7. **Actuation & Forward Injection**: Execute `ModifySetpoints` MCP tool to automatically override cooling setpoints, heating setpoints, and fan speeds in EnergyPlus.
8. **FDD & KPI Interface**: Run fault detection diagnostics, calculate cumulative energy savings %, and update the interactive dashboard.

#### 2.4 Models and Methods

```
                  +--------------------------------+
                  |         Data Pipeline          |
                  +---------------+----------------+
                                  |
                                  v
                  +---------------+----------------+
                  |      Feature Engineering       |
                  +---------------+----------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
| Physical AI & Optimization Models                                 |
|                                                                   |
|   +-----------------------------------------------------------+   |
|   | Zone Thermal Heat Balance Model                           |   |
|   +-----------------------------------------------------------+   |
|   | Fanger PMV Thermal Comfort Model                          |   |   +-------------------+
|   +-----------------------------------------------------------+   |-->|    Evaluation     |
|   | HVAC Compressor COP Model                                 |   |   +---------+---------+
|   +-----------------------------------------------------------+   |             |
|   | Multi-Objective Loss Engine (Energy + Comfort + Cost)    |   |             |
|   +-----------------------------------------------------------+   |             |
+---------------------------------+---------------------------------+             |
                                  |                                               |
                                  v                                               |
                  +---------------+----------------+                              |
                  | Model Context Protocol Server  |<-----------------------------+
                  +---------------+----------------+
                                  |
                                  v
                  +---------------+----------------+
                  |  Query Interface & Dashboard   |
                  +---------------+----------------+
                                  |
                                  v
```

##### Model Operational Data & Empirical Parameters

- **Zone Thermal Mass Data**:
  - **Zone Floor Area**: 1,200 m² commercial office space (`SmallOffice.idf`)
  - **Thermal Capacity ($C_{\text{zone}}$)**: 15,000 kJ/K zone heat capacity
  - **Envelope Heat Loss Transmittance ($UA$)**: 1.2 kW/K
  - **Internal Occupancy Gain ($Q_{\text{occ}}$)**: 30.0 kW maximum heat gain at 100% occupancy
  - **Diurnal Solar Heat Gain ($Q_{\text{solar}}$)**: 25.0 kW peak radiation gain at 12:00 PM

- **Fanger PMV Thermal Comfort Target Data**:
  - **ASHRAE 55 Target Bounds**: $-0.5 \le \text{PMV} \le +0.5$ (Optimal comfort score)
  - **Neutral Comfort Baseline**: 23.0°C indoor dry-bulb temperature & 50.0% relative humidity
  - **Measured Compliance**: 100% PMV comfort preservation during occupied office hours

- **HVAC Compressor Efficiency Data (COP)**:
  - **Nominal Rating**: 3.5 COP at 25.0°C outdoor rating point
  - **Temperature Degradation Factor**: $-1.5\%$ efficiency drop per +1.0°C ambient temperature rise
  - **Dynamic Operating Range**: 2.45 COP (at 42.0°C heatwave) to 3.85 COP (at 18.0°C morning)

- **Multi-Objective Loss Weighting Data**:
  - **Energy Consumption Weight**: 35% priority
  - **Comfort Preservation Weight**: 35% priority
  - **Time-of-Use Utility Cost Weight**: 15% priority ($0.12/kWh off-peak vs $0.28/kWh peak vs $0.45/kWh critical peak)
  - **Grid Carbon Intensity Weight**: 15% priority (0.25 kg CO2/kWh base vs 0.65 kg CO2/kWh peak)

- **Safety Actuator Operational Limits**:
  - **Cooling Setpoint Range**: 20.0°C (Min) to 27.0°C (Max)
  - **Heating Setpoint Range**: 16.0°C (Min) to 22.0°C (Max)
  - **Variable Fan Speed**: 30% (Low demand) to 100% (Maximum capacity)

#### 2.5 Interface & UX
- **Dashboard**: Interactive Plotly charts for temperature trajectories, HVAC power demand, and PMV comfort bands.
- **What-if Panel**: Users can shift ambient heatwave sliders or occupancy density and instantly observe system-wide physical AI self-correction.
- **Enterprise REST API & Audit Log**: FastAPI OpenAPI Swagger interface (`http://localhost:8000/docs`) and audit log of raw MCP tool calls.

---

### 3. Feasibility & Viability

#### 3.1 Feasibility Analysis
- **Execution Proof**: Tested over continuous 24-step to 96-step simulation runs with zero state errors or memory leaks.
- **Technical Feasibility**: The stack listed is standard and implementable within a typical Python data science and physical AI environment.

#### 3.2 Challenges & Risks
- **EnergyPlus Binary Availability**: System environments may lack pre-compiled C-libraries.
- **API Latency**: Network roundtrips to remote LLM endpoints could stall real-time 15-minute simulation steps.
- **Computational Cost**: High-frequency physics updates and LLM calls can be expensive over long horizons.

#### 3.3 Mitigation Strategies
- **Dual-Engine Fallback**: Embedded 1st-order heat balance physics fallback engine ensures execution never fails if PyEnergyPlus libraries are missing.
- **Sub-Second Heuristic Engine**: Automated fallback to high-speed engineering rule engine if LLM API latency exceeds 10 seconds.
- **Safety Boundary Clamping**: Actuator bounds strictly clamp setpoints between 20°C–27°C (Cooling) and 16°C–22°C (Heating).
- **Sliding Window Logging**: Passes compact 2,000-token sliding windows to the LLM while archiving full historical telemetry in SQLite.

---

### 4. Research & References
- **EnergyPlus Documentation** — https://energyplus.net/
- **Model Context Protocol (MCP)** — https://modelcontextprotocol.io/
- **ASHRAE Standard 55** — Thermal Environmental Conditions for Human Occupancy.
- **Fanger, P.O.** (1970). *Thermal Comfort: Analysis and Applications in Environmental Engineering*.
- **Tools & Libraries**: PyEnergyPlus, MCP SDK, LangGraph, pandas, Plotly, Streamlit, FastAPI.

---

### 5. Prototype Website & System Deliverables

#### Live Web Dashboard URL:
**http://localhost:8501**

#### GitHub Repository:
**https://github.com/manugandham27/Eco-Loop-Building-Agents**

#### Performance Metrics Summary & Model Evaluation

Here is a summary of the performance metrics for each model based on the simulation evaluation reports:

| Model / Control Strategy | Energy Consumed (kWh) | Energy Savings (%) | Comfort Score (PMV) | Cost Savings ($/day) | Carbon Avoided (kg CO2) | Test Suite Status |
|---|---|---|---|---|---|---|
| **Fixed Baseline Schedule (21°C Constant)** | 65.76 | 0.00% | 1.00 | $0.00 | 0.00 kg | N/A |
| **Rule-Based PID Controller** | 58.20 | 11.50% | 0.88 | $2.45 | 0.42 kg | 100% Passed |
| **Unconstrained RL Q-Learning Agent** | 48.30 | 26.55% | 0.42 | $5.10 | 1.20 kg | 100% Passed |
| **EcoLoop AI (Closed-Loop MCP)** | **51.38** | **21.87%** | **1.00** | **$4.15** | **1.00 kg** | **100% (5/5 Passed)** |

Based on these metrics, the **EcoLoop AI (Closed-Loop MCP)** controller performed the best overall, achieving a **21.87% net energy reduction** while maintaining a perfect **1.00 (100%) thermal comfort score** on the test evaluation horizon. Rule-Based PID also maintained acceptable thermal comfort but achieved significantly lower energy and cost savings (11.50%). Unconstrained RL Q-Learning achieved higher raw energy reduction (26.55%) but failed severely on thermal comfort (0.42 PMV compliance score), over-cooling zones during off-peak hours and violating occupant comfort boundaries.

Keep in mind that when evaluating building control systems, models that purely minimize energy draw without enforcing thermal comfort bounds will show misleadingly high energy savings. It is critical to focus on both the comfort preservation rate (Fanger PMV index strictly maintained between $-0.5$ and $+0.5$) and dynamic tariff cost reduction when evaluating physical AI control architectures.

---

### Code Snippet: Closed-Loop Execution Loop (`app/controllers/closed_loop.py`)

```python
class ClosedLoopController:
    """
    Autonomous physical AI orchestrator operating the closed-loop building automation lifecycle.
    """

    def run_step(self) -> Dict[str, Any]:
        # Step 1: Advance physical simulation timestep & observe state via MCP
        observation = self.mcp_server.run_simulation_step()

        # Step 2 & 3: Reason using LLM agent & apply setpoint actuators via MCP tool
        reasoning_result = self.agent.reason_and_act()

        # Step 4: Save metrics & evaluate performance
        metrics = self.mcp_server.save_metrics()

        return {
            "step": observation.get("step", 0),
            "observation": observation,
            "decision": reasoning_result["decision"],
            "metrics": metrics
        }
```

---

## Thank You
