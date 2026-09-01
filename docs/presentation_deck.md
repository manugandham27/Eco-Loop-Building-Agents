# EcoLoop AI — 6-Slide Presentation Deck

---

## Slide 1: Title Slide
**EcoLoop AI: Autonomous Closed-Loop Building HVAC Control**  
*Physical AI Powered by EnergyPlus, Model Context Protocol (MCP), and LLM Agents*

- 🏢 **Focus Area**: Commercial Building HVAC Automation
- 🤖 **Core Idea**: Autonomous setpoint control using sensor feedback and predictive weather data
- ⚡ **Measured Impact**: 21.87% energy savings while maintaining occupant thermal comfort

---

## Slide 2: Problem & Solution
**Fixed Schedule Limits vs. Autonomous Control**

- **The Problem**:
  - Fixed HVAC schedules waste energy cooling empty floors during peak tariff hours.
  - Basic PID controllers ignore weather forecasts, carbon grid factors, and real-time power prices.
  - Black-box ML models lack readable engineering rationale for setpoint changes.
- **EcoLoop AI Solution**:
  - **Closed-Loop Automation**: Runs continuous 15-minute Observe ➔ Reason ➔ Act ➔ Evaluate cycles.
  - **Model Context Protocol (MCP)**: Operates safely through 10 validated MCP tool calls.
  - **Explainable Decisions**: Outputs step-by-step physical rationale for every setpoint override.

---

## Slide 3: System Architecture & Data Flow
**Closed-Loop Execution Pipeline**

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

1. **OBSERVE**: Read zone temperature, humidity, occupancy, CO2 levels, and power draw.
2. **FORECAST**: Fetch 6-hour look-ahead weather and price tier data.
3. **REASON**: Evaluate energy, comfort (PMV), financial cost, and carbon loss terms.
4. **ACT**: Apply cooling, heating, and fan setpoints via `ModifySetpoints` MCP tool.
5. **EVALUATE**: Compute cumulative KPIs against a fixed 21.0°C baseline.

---

## Slide 4: Optimization & Comfort Balancing
**Multi-Objective Loss Function**

$$J = 0.35 \cdot E_{\text{energy}} + 0.35 \cdot C_{\text{comfort}} + 0.15 \cdot \text{Cost} + 0.15 \cdot \text{Carbon}$$

- ⚡ **Energy Reduction**: Eases cooling setpoints during low occupancy or high outdoor thermal mass.
- 🧘 **Thermal Comfort (PMV)**: Keeps Fanger PMV score strictly between $-0.5$ and $+0.5$.
- 💰 **Tariff Arbitrage**: Pre-cools during off-peak hours ($0.12/kWh); relaxes setpoints during peak hours ($0.28/kWh).
- 🌿 **Carbon Footprint**: Lowers demand during high grid carbon intensity (0.65 kg CO2/kWh).

---

## Slide 5: Results & Visual Dashboard
**24-Hour Benchmark Simulation Results**

- 📉 **Energy Savings**: **21.87% reduction** vs static baseline schedule
- 🧘 **Thermal Comfort**: **100% PMV compliance** during occupied hours
- 🌿 **Emissions Saved**: **1.0 kg CO2** reduced per day per zone
- 📊 **Streamlit UI**: Includes live trajectory graphs, reasoning logs, baseline comparisons, FDD diagnostics, and CSV export.

---

## Slide 6: Tech Stack & Verification
**Production Software Quality & Testing**

- 🛠️ **Tech Stack**: Python 3.12 | PyEnergyPlus | MCP SDK | Streamlit | FastAPI | SQLAlchemy | Plotly
- 💻 **Local Execution**: `python run.py --mode run` + `streamlit run app/dashboard/dashboard.py`
- 🐳 **Docker Support**: Multi-service `docker-compose up -d` stack
- 🧪 **Automated Testing**: 100% Pytest pass rate (`pytest app/tests/`)
