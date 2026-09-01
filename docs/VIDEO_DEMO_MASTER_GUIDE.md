# EcoLoop AI — 3-Minute PoC Video Recording Master Guide

This guide gives you the exact **screen-share actions**, **simple everyday narration**, **timeline**, and **relatable real-life examples** to record your 3-minute video demo.

---

## 📋 Pre-Recording Setup (Do This First)

1. Open **Terminal** and activate the environment:
   ```bash
   source .venv312/bin/activate
   streamlit run app/dashboard/dashboard.py
   ```
2. Open your browser to **`http://localhost:8501`** (Streamlit Dashboard).
3. In a second browser tab, open **`http://localhost:8000/docs`** (FastAPI Swagger UI).
4. Set screen recording resolution to **1920x1080** and make sure your microphone is clear.

---

## 🎬 Video Timeline & Screen-Sharing Overview

```
+------------------------------------------------------------------------------------+
| Timeline   | Screen to Share            | Action to Perform                        |
+------------+----------------------------+------------------------------------------+
| 0:00-0:25  | Streamlit Home (Tab 1)    | Mouse hover over top 5 KPI Cards         |
| 0:25-0:55  | Tab 5 (FDD & MCP)          | Highlight 10 MCP Tools JSON list         |
| 0:55-1:55  | Sidebar & Tab 1 / Tab 2    | Set steps = 15 -> Click Run -> Show charts|
| 1:55-2:35  | Tab 4 (What-If) + Swagger | Drag Heatwave to 42°C -> Show API docs   |
| 2:35-3:00  | Tab 3 (Baseline Compare)   | Highlight Extra Features & CSV Export    |
+------------------------------------------------------------------------------------+
```

---

### SCENE 1 | 0:00 - 0:25 (25s) — Everyday Problem & Simple Concept

- **🖥️ What to Share**: Streamlit Dashboard header (`http://localhost:8501`) showing top KPI cards.
- **🖱️ What to Do**: Slowly move mouse over top metrics (**21.87% Energy Savings**, **100% Comfort Score**).
- **🎙️ What to Say (Everyday Language)**:
  > *"Think about how air conditioning works in most office buildings today. It usually runs on a basic timer, blasting cold air at 21 degrees all day long—whether the building is full of people or completely empty, or even when power prices double in the afternoon. That wastes massive amounts of energy and money!
  > We created **EcoLoop AI** to fix this. It acts like a smart co-pilot for the building. It constantly checks indoor room temperatures, weather forecasts, and power prices, and automatically adjusts the thermostat so you save energy without anyone sweating."*

---

### SCENE 2 | 0:25 - 0:55 (30s) — How It Works (Analogy: Safe Digital Remote)

- **🖥️ What to Share**: Click **Tab 5: 🛡️ FDD & Enterprise REST API**.
- **🖱️ What to Do**: Highlight the **Registered MCP Tool Primitives** JSON list on the right.
- **🎙️ What to Say (Everyday Language)**:
  > *"How does the AI safely control the building's AC? Through something called the **Model Context Protocol**, or **MCP**. 
  > Think of MCP like a secure digital remote control. Instead of letting the AI touch complex raw code or physical wiring, the AI uses standard buttons on this remote—like 'Read Room Temperature', 'Check Weather Forecast', or 'Adjust Thermostat'. That way, every action is safe, predictable, and transparent."*

---

### SCENE 3 | 0:55 - 1:55 (60s) — Live 15-Step Example (Real Afternoon Heat & Price Spike)

- **🖥️ What to Share**: Sidebar Control Panel on the left ➔ **Tab 1** ➔ **Tab 2**.
- **🖱️ What to Do**: 
  1. Change **Steps to Execute** in the sidebar from `4` to **`15`**.
  2. Click the red **▶️ Run Autonomous Step(s)** button.
  3. Watch live line charts update on **Tab 1: 📈 Real-Time Telemetry**.
  4. Click **Tab 2: 🤖 AI Reasoning Timeline** and expand the latest decision log.
- **🎙️ What to Say (Everyday Language)**:
  > *"Let's see a real-life example in action over 15 simulation steps. I'll set our step counter to 15 and hit run.
  > Watch the line chart as the day progresses:
  > In the morning, as employees arrive, the AI keeps rooms nice and comfortable at 23 degrees.
  > But look at 2 PM in the afternoon—outdoor temperatures climb, and grid electricity prices jump to peak rates of 28 cents per unit. The AI sees this price surge coming on its weather forecast, so it gently eases the cooling setpoint from 23 to 25 degrees and dials back fan speeds. People inside stay comfortable, but the power bill drops immediately!
  > If you look at the **Reasoning Log**, the AI explains the exact plain-English logic behind every single adjustment it makes."*

---

### SCENE 4 | 1:55 - 2:35 (40s) — Stress Testing (Extreme 42°C Days & Smart Diagnostics)

- **🖥️ What to Share**: Click **Tab 4: 🧪 What-If Stress Tester**, then switch to browser tab 2 (`http://localhost:8000/docs`).
- **🖱️ What to Do**: 
  1. Drag the **Outdoor Ambient Heatwave** slider up to **`42°C`**.
  2. Click **🚀 Inject Stress Scenario & Run Step**.
  3. Switch to the FastAPI Swagger UI tab (`/docs`) and scroll through endpoints.
- **🎙️ What to Say (Everyday Language)**:
  > *"What happens on an extreme 42-degree summer heatwave? On our What-If tab, we can drag the outdoor heat slider to 42 degrees, and the system self-corrects instantly to prevent rooms from overheating.
  > On top of that, our system continuously monitors equipment health—just like a car checking its engine light—alerting facility managers if an air filter gets clogged or a compressor loses efficiency.
  > For IT teams, we also built a complete **FastAPI REST API** so engineers can monitor building health remotely from anywhere."*

---

### SCENE 5 | 2:35 - 3:00 (25s) — Results & Extra Features Summary

- **🖥️ What to Share**: Click **Tab 3: ⚖️ Baseline Comparison**.
- **🖱️ What to Do**: Hover over the green vs blue energy bar chart, then click the blue **📥 Export Full Telemetry CSV Report** button.
- **🎙️ What to Say (Everyday Language)**:
  > *"The results speak for themselves: EcoLoop AI cut overall HVAC energy use by **21.87%** while keeping occupant thermal comfort at a perfect **100%**. 
  > On top of the core project, we added **5 extra features**: automatic maintenance diagnostics, grid power-saving modes, a live REST API, automated GitHub testing pipelines, and one-click CSV report downloads.
  > Thank you!"*

---

## 🌟 Extra Enterprise Features Breakdown (Simple Everyday Terms)

1. **⚡ Production FastAPI REST API (`app/main.py`)**:
   - Like a secure web link allowing facility engineers to check building status or change settings from a mobile app (`http://localhost:8000/docs`).
2. **🛠️ Automatic Maintenance & Fault Diagnostics (`app/services/fdd.py`)**:
   - Acts like a car check-engine light, warning managers if AC filters are dirty or cooling coils need servicing before a breakdown occurs.
3. **📉 Smart Grid Power-Saving Mode (`app/services/demand_response.py`)**:
   - Automatically sheds 35% AC power draw when the power grid issues emergency peak pricing alerts ($\ge \$0.40/\text{kWh}$).
4. **🧪 What-If Heatwave Simulator (`app/dashboard/dashboard.py`)**:
   - Interactive sliders to test how the building handles extreme 45°C heatwaves or crowded office events.
5. **⚙️ Automated Testing Pipeline (`.github/workflows/ci.yml`)**:
   - Continuous GitHub testing checks that automatically verify every line of code works smoothly before deployment.
