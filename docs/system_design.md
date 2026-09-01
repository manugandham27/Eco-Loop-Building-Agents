# EcoLoop AI System Design & Physics Models

This document details the thermodynamic equations, comfort models, and loss functions used in the EcoLoop AI platform.

---

## 1. Zone Heat Balance Equation

Zone indoor temperature $T_{\text{indoor}}$ is calculated using a 1st-order thermal mass differential equation:

$$C_{\text{zone}} \frac{dT_{\text{indoor}}}{dt} = Q_{\text{occ}} + Q_{\text{solar}} + UA (T_{\text{outdoor}} - T_{\text{indoor}}) - Q_{\text{cooling}} + Q_{\text{heating}}$$

Where:
- $C_{\text{zone}} = 15,000 \text{ kJ/K}$ (Zone heat capacity for 1,200 m² floor area)
- $UA = 1.2 \text{ kW/K}$ (Envelope heat transmittance)
- $Q_{\text{occ}} = \text{Occupancy Ratio} \times 30.0 \text{ kW}$ (Internal body & equipment heat gains)
- $Q_{\text{solar}} = 25.0 \text{ kW} \times \sin(\pi (t - 6)/12)$ (Diurnal solar radiation)

---

## 2. Occupant Thermal Comfort (Fanger PMV Model)

Thermal comfort is computed using Predicted Mean Vote (PMV):

$$\text{PMV} \approx 0.35 \cdot (T_{\text{indoor}} - 23.0) + 0.005 \cdot (RH - 50.0)$$

- **Target Range**: $-0.5 \le \text{PMV} \le +0.5$ (Optimal comfort per ISO 7730 / ASHRAE 55)
- **Discomfort Penalty**: Applied whenever $| \text{PMV} | > 0.5$ during occupied hours.

---

## 3. HVAC Compressor COP Model

The Coefficient of Performance (COP) varies dynamically with outdoor ambient temperature:

$$\text{COP}_{\text{actual}} = \text{COP}_{\text{nominal}} \cdot \left(1.0 - 0.015 \cdot (T_{\text{outdoor}} - 25.0)\right)$$

Where $\text{COP}_{\text{nominal}} = 3.5$.

---

## 4. Multi-Objective Optimization Loss Function

The controller evaluates candidate setpoints against a weighted loss function $J$:

$$J = w_{\text{energy}} \cdot S_{\text{energy}} + w_{\text{comfort}} \cdot S_{\text{comfort}} + w_{\text{cost}} \cdot S_{\text{cost}} + w_{\text{carbon}} \cdot S_{\text{carbon}}$$

Default policy weights:
- $w_{\text{energy}} = 0.35$ (Power draw reduction)
- $w_{\text{comfort}} = 0.35$ (PMV comfort preservation)
- $w_{\text{cost}} = 0.15$ (Time-of-use tariff reduction)
- $w_{\text{carbon}} = 0.15$ (Grid emissions reduction)
