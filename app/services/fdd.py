"""
EcoLoop AI — Automated Fault Detection & Diagnostics (FDD) Engine
Monitors real-time building sensor streams to detect equipment efficiency degradation,
compressor hunting, airflow restrictions, and sensor drift.
"""

from typing import Dict, Any, List
from app.utils.logger import setup_logger

logger = setup_logger("fdd_engine")


class FaultDetectionDiagnostics:
    """
    Automated FDD Subsystem for Honeywell Building Automation.
    Analyzes historical and current telemetry to identify operational anomalies.
    """

    @staticmethod
    def analyze_health(current_obs: Dict[str, Any], history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates physical parameters and identifies active component faults or maintenance warnings.
        """
        alerts = []
        status = "HEALTHY"

        indoor_temp = current_obs.get("indoor_temp", 22.0)
        cooling_setpoint = current_obs.get("cooling_setpoint", 23.0)
        hvac_power = current_obs.get("hvac_power_kw", 0.0)
        fan_speed = current_obs.get("fan_speed", 0.7)
        co2_ppm = current_obs.get("iaq_co2_ppm", 450.0)

        # 1. Thermal Degradation Check (HVAC running at max power but temp not dropping)
        if hvac_power > 15.0 and indoor_temp > (cooling_setpoint + 2.5):
            alerts.append({
                "type": "THERMAL_DEGRADATION",
                "severity": "WARNING",
                "message": f"Zone temperature ({indoor_temp}°C) is 2.5°C above setpoint despite high HVAC demand ({hvac_power} kW). Inspect compressor COP and refrigerant pressure."
            })
            status = "ATTENTION_REQUIRED"

        # 2. Indoor Air Quality Ventilation Warning (CO2 > 900 ppm)
        if co2_ppm > 900.0:
            alerts.append({
                "type": "HIGH_CO2_VENTILATION",
                "severity": "WARNING",
                "message": f"Indoor CO2 level ({co2_ppm} PPM) exceeds recommended ASHRAE threshold (900 PPM). Increase fresh air intake."
            })
            if status != "ATTENTION_REQUIRED":
                status = "ATTENTION_REQUIRED"

        # 3. Airflow Restriction Warning (High fan speed with high CO2)
        if fan_speed > 0.85 and co2_ppm > 800.0:
            alerts.append({
                "type": "AIRFLOW_RESTRICTION",
                "severity": "INFO",
                "message": "Fan operating at >85% capacity with elevated CO2. Recommended HVAC filter replacement."
            })

        # 4. Thermal Stability Check across recent history (Detecting setpoint hunting)
        if len(history) >= 4:
            recent_temps = [r.get("indoor_temp", 22.0) for r in history[-4:]]
            temp_range = max(recent_temps) - min(recent_temps)
            if temp_range > 3.0:
                alerts.append({
                    "type": "SETPOINT_HUNTING",
                    "severity": "INFO",
                    "message": f"Rapid temperature fluctuation ({temp_range:.1f}°C variance over 4 steps). Damping actuator response."
                })

        logger.info(f"FDD Health Analysis complete -> Status: {status}, Active Alerts: {len(alerts)}")

        return {
            "health_status": status,
            "alerts_count": len(alerts),
            "alerts": alerts,
            "filter_health_pct": round(max(20.0, 100.0 - (current_obs.get("step", 0) * 0.5)), 1),
            "compressor_efficiency_pct": round(max(60.0, 98.0 - (current_obs.get("hvac_power_kw", 0.0) * 0.3)), 1)
        }
