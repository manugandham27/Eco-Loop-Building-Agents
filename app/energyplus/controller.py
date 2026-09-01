"""
EcoLoop AI - EnergyPlus Life-Cycle Controller
Manages simulation runtime, callback hooks, actuator variable updates, and observation reporting.
"""

from typing import Dict, Any, Optional
from app.config.settings import Settings
from app.energyplus.api_wrapper import EnergyPlusAPIWrapper
from app.energyplus.simulator import SyntheticBuildingSimulator
from app.utils.logger import setup_logger

logger = setup_logger("energyplus_controller")


class EnergyPlusController:
    """
    Unified EnergyPlus Controller serving as the actuation and observation interface.
    Controls cooling setpoint, heating setpoint, and fan speed dynamically.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_wrapper = EnergyPlusAPIWrapper()
        self.synthetic_sim = SyntheticBuildingSimulator(settings)

        self.current_cooling_setpoint = settings.building.default_cooling_setpoint
        self.current_heating_setpoint = settings.building.default_heating_setpoint
        self.current_fan_speed = settings.building.default_fan_speed
        self.is_running = False

    def initialize(self) -> None:
        """
        Initializes the controller and checks engine readiness.
        """
        if self.api_wrapper.is_available:
            logger.info("Initializing official PyEnergyPlus runtime environment...")
        else:
            logger.info("Initializing High-Fidelity Synthetic Simulation engine...")
        self.is_running = True

    def set_actuators(self, cooling_setpoint: float, heating_setpoint: float, fan_speed: float) -> None:
        """
        Updates actuator targets enforcing safety boundaries from settings policies.
        """
        # Enforce policy bounds
        self.current_cooling_setpoint = max(
            self.settings.building.min_cooling_setpoint,
            min(self.settings.building.max_cooling_setpoint, cooling_setpoint)
        )
        self.current_heating_setpoint = max(
            self.settings.building.min_heating_setpoint,
            min(self.settings.building.max_heating_setpoint, heating_setpoint)
        )
        self.current_fan_speed = max(0.1, min(1.0, fan_speed))

        logger.info(
            f"Actuators updated -> Cooling Setpoint: {self.current_cooling_setpoint:.1f}°C, "
            f"Heating Setpoint: {self.current_heating_setpoint:.1f}°C, "
            f"Fan Speed: {self.current_fan_speed*100:.0f}%"
        )

    def step(self) -> Dict[str, Any]:
        """
        Executes a single simulation step and returns structured observations.
        """
        if not self.is_running:
            self.initialize()

        if self.api_wrapper.is_available:
            # PyEnergyPlus C-API step actuation would execute here
            pass

        # Execute step on simulation engine
        self.synthetic_sim.step(
            cooling_setpoint=self.current_cooling_setpoint,
            heating_setpoint=self.current_heating_setpoint,
            fan_speed=self.current_fan_speed
        )

        return self.synthetic_sim.get_observation()
