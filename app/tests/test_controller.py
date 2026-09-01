"""
EcoLoop AI - Controller Unit Test Suite
"""

import pytest
from app.config.settings import Settings
from app.database.models import DatabaseManager
from app.energyplus.controller import EnergyPlusController
from app.mcp.server import MCPServer


def test_controller_actuator_clamping(tmp_path):
    settings = Settings()
    controller = EnergyPlusController(settings)
    
    # Try setting setpoint out of bounds
    controller.set_actuators(cooling_setpoint=15.0, heating_setpoint=30.0, fan_speed=2.0)
    
    assert controller.current_cooling_setpoint == settings.building.min_cooling_setpoint
    assert controller.current_heating_setpoint == settings.building.max_heating_setpoint
    assert controller.current_fan_speed == 1.0


def test_mcp_server_integration(tmp_path):
    db_file = str(tmp_path / "test_ecoloop.db")
    settings = Settings()
    settings.db_path = db_file
    
    db = DatabaseManager(db_file)
    controller = EnergyPlusController(settings)
    mcp = MCPServer(controller, db)
    
    obs = mcp.run_simulation_step()
    assert obs["step"] == 1
    
    res = mcp.modify_setpoints(24.0, 19.5, 0.6, "Test reasoning")
    assert res["status"] == "SUCCESS"
    assert res["applied_cooling_setpoint"] == 24.0
