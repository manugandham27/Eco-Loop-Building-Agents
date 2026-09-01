"""
EcoLoop AI — Demand Response & Peak Shaving Subsystem
Handles automated grid Demand Response (DR) signals, shedding non-critical HVAC loads
during electrical grid emergency events or critical peak pricing windows.
"""

from typing import Dict, Any
from app.utils.logger import setup_logger

logger = setup_logger("demand_response")


class DemandResponseController:
    """
    Automated Demand Response & Peak Shaving Controller.
    Interprets utility grid curtailment events and overrides setpoints to prevent grid blackouts.
    """

    def __init__(self):
        self.dr_active = False
        self.curtailment_target_kw = 0.0

    def evaluate_grid_event(self, electricity_price: float, hvac_power_kw: float) -> Dict[str, Any]:
        """
        Detects critical grid price events ($0.40/kWh threshold) and triggers peak shedding mode.
        """
        if electricity_price >= 0.40:
            self.dr_active = True
            self.curtailment_target_kw = hvac_power_kw * 0.35  # Request 35% load shedding
            logger.warning(f"CRITICAL GRID EVENT DETECTED (${electricity_price}/kWh). Triggering Automated Demand Response!")
            return {
                "dr_active": True,
                "event_type": "CRITICAL_PEAK_SHEDDING",
                "recommended_cooling_setpoint_offset": +2.5,
                "recommended_fan_limit": 0.3,
                "target_curtailment_kw": round(self.curtailment_target_kw, 2)
            }

        self.dr_active = False
        self.curtailment_target_kw = 0.0
        return {
            "dr_active": False,
            "event_type": "NORMAL_GRID_OPERATION",
            "recommended_cooling_setpoint_offset": 0.0,
            "recommended_fan_limit": 1.0,
            "target_curtailment_kw": 0.0
        }
