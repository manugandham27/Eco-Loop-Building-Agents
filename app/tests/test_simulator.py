"""
EcoLoop AI - Simulator Unit Test Suite
Verifies physics-based synthetic thermodynamic calculations and PMV indices.
"""

import pytest
from app.config.settings import Settings
from app.energyplus.simulator import SyntheticBuildingSimulator


def test_simulator_step_advancement():
    settings = Settings()
    sim = SyntheticBuildingSimulator(settings)
    
    initial_step = sim.state.step
    state = sim.step(cooling_setpoint=23.0, heating_setpoint=20.0, fan_speed=0.7)
    
    assert state.step == initial_step + 1
    assert state.sim_time_hours == 0.25
    assert 10.0 <= state.outdoor_temp <= 40.0
    assert -3.0 <= state.pmv <= 3.0


def test_simulator_actuator_effect():
    settings = Settings()
    sim = SyntheticBuildingSimulator(settings)
    
    # Run with aggressive cooling
    sim.step(cooling_setpoint=20.0, heating_setpoint=18.0, fan_speed=1.0)
    obs1 = sim.get_observation()
    
    # Run with relaxed cooling
    sim.step(cooling_setpoint=26.0, heating_setpoint=18.0, fan_speed=0.3)
    obs2 = sim.get_observation()
    
    assert obs1["cooling_setpoint"] == 20.0
    assert obs2["cooling_setpoint"] == 26.0
