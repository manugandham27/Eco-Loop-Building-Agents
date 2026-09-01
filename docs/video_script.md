# EcoLoop AI — 3-Minute Video Script (Simple Everyday Language)

**Target Duration**: 3 Minutes (180 Seconds)  
**Execution Step**: Set sidebar steps counter to 15  
**URL**: `http://localhost:8501`  

---

## 🕒 Video Narration Script

### 💥 0:00 - 0:25 | The Problem & Simple Concept (25 Seconds)
- **Visual**: Show Streamlit Dashboard top header (`http://localhost:8501`).
- **Voiceover**:
  > *"Think about how air conditioning works in most office buildings today. It usually runs on a basic timer, blasting cold air at 21 degrees all day long—whether the building is full of people or completely empty, or even when power prices double in the afternoon. That wastes massive amounts of energy and money!
  > We created **EcoLoop AI** to fix this. It acts like a smart co-pilot for the building. It constantly checks indoor room temperatures, weather forecasts, and power prices, and automatically adjusts the thermostat so you save energy without anyone sweating."*

---

### 🧠 0:25 - 0:55 | How It Works (Analogy: Safe Digital Remote) (30 Seconds)
- **Visual**: Click to **🛡️ FDD & Enterprise REST API** tab, showing registered MCP tools.
- **Voiceover**:
  > *"How does the AI safely control the building's AC? Through something called the **Model Context Protocol**, or **MCP**. 
  > Think of MCP like a secure digital remote control. Instead of letting the AI touch complex raw code or physical wiring, the AI uses standard buttons on this remote—like 'Read Room Temperature', 'Check Weather Forecast', or 'Adjust Thermostat'. That way, every action is safe, predictable, and transparent."*

---

### 🕹️ 0:55 - 1:55 | Live 15-Step Example (Real Afternoon Heat & Price Spike) (60 Seconds)
- **Visual**: In Sidebar ➔ Set **Steps to Execute** to `15` ➔ Click **▶️ Run Autonomous Step(s)**. Show live Plotly charts updating.
- **Voiceover**:
  > *"Let me show you a real-life example over 15 simulation steps. I'll set our step counter to 15 and hit run.
  > Watch the line chart as the day progresses:
  > In the morning, as employees arrive, the AI keeps rooms nice and comfortable at 23 degrees.
  > But look at 2 PM in the afternoon—outdoor temperatures climb, and grid electricity prices jump to peak rates of 28 cents per unit. The AI sees this price surge coming on its weather forecast, so it gently eases the cooling setpoint from 23 to 25 degrees and dials back fan speeds. People inside stay comfortable, but the power bill drops immediately!
  > If you look at the **Reasoning Log**, the AI explains the exact plain-English logic behind every single adjustment it makes."*

---

### 🚀 1:55 - 2:35 | Stress Testing (Extreme 42°C Days & Diagnostics) (40 Seconds)
- **Visual**: Click **🧪 What-If Stress Tester** tab ➔ Drag Heatwave slider to 42°C ➔ Click Inject.
- **Voiceover**:
  > *"What happens on an extreme 42-degree summer heatwave? On our What-If tab, we can drag the outdoor heat slider to 42 degrees, and the system self-corrects instantly to prevent rooms from overheating.
  > On top of that, our system continuously monitors equipment health—just like a car checking its engine light—alerting facility managers if an air filter gets clogged or a compressor loses efficiency.
  > For IT teams, we also built a complete **FastAPI REST API** so engineers can monitor building health remotely from anywhere."*

---

### 🏆 2:35 - 3:00 | Results & Extra Features Summary (25 Seconds)
- **Visual**: Switch to Top KPI Cards showing 21.87% Energy Savings and click CSV Export button.
- **Voiceover**:
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
