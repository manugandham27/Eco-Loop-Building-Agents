"""
EcoLoop AI - EnergyPlus API Wrapper
Provides standard dynamic binding interface for official PyEnergyPlus API.
Handles state creation, handle registration, variable extraction, and actuator setting.
"""

import sys
import os
from typing import Optional, Any, Callable
from app.utils.logger import setup_logger

logger = setup_logger("energyplus_api")


class EnergyPlusAPIWrapper:
    """
    Wrapper for official PyEnergyPlus library calls.
    Gracefully detects installed EnergyPlus versions and loads dynamic C-API bindings.
    """

    def __init__(self, energyplus_install_path: Optional[str] = None):
        self.api: Optional[Any] = None
        self.is_available: bool = False
        self._init_api(energyplus_install_path)

    def _init_api(self, path: Optional[str] = None) -> None:
        """
        Attempts to import pyenergyplus from standard install paths or sys.path.
        """
        search_paths = []
        if path:
            search_paths.append(path)

        # Standard macOS & Linux EnergyPlus installation paths
        search_paths.extend([
            "/Applications/EnergyPlus-23-2-0",
            "/Applications/EnergyPlus-23-1-0",
            "/Applications/EnergyPlus-22-2-0",
            "/usr/local/EnergyPlus-23-2-0",
            "/usr/local/EnergyPlus-23-1-0"
        ])

        for p in search_paths:
            if os.path.exists(p) and p not in sys.path:
                sys.path.append(p)

        try:
            from pyenergyplus.api import EnergyPlusAPI
            self.api = EnergyPlusAPI()
            self.is_available = True
            logger.info("Successfully bound PyEnergyPlus C-API interface.")
        except ImportError:
            self.is_available = False
            logger.info("PyEnergyPlus library not detected on system path. Enabling High-Fidelity Synthetic Simulation fallback.")

    def create_state(self) -> Optional[Any]:
        if not self.is_available or not self.api:
            return None
        return self.api.state_manager.new_state()

    def run_simulation(self, state: Any, command_line_args: list) -> int:
        if not self.is_available or not self.api:
            return -1
        return self.api.runtime.run_energyplus(state, command_line_args)

    def register_callback_begin_timestep(self, state: Any, func: Callable) -> None:
        if self.is_available and self.api:
            self.api.runtime.callback_begin_zone_timestep_before_init_heat_balance(state, func)

    def get_variable_handle(self, state: Any, name: str, key: str) -> int:
        if not self.is_available or not self.api:
            return -1
        return self.api.exchange.get_variable_handle(state, name, key)

    def get_variable_value(self, state: Any, handle: int) -> float:
        if not self.is_available or not self.api or handle == -1:
            return 0.0
        return self.api.exchange.get_variable_value(state, handle)

    def get_actuator_handle(self, state: Any, component_type: str, control_type: str, unique_key: str) -> int:
        if not self.is_available or not self.api:
            return -1
        return self.api.exchange.get_actuator_handle(state, component_type, control_type, unique_key)

    def set_actuator_value(self, state: Any, handle: int, value: float) -> None:
        if self.is_available and self.api and handle != -1:
            self.api.exchange.set_actuator_value(state, handle, value)
