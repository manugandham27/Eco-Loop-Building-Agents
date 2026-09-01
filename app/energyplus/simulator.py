"""
EcoLoop AI — Bespoke Thermodynamic Building Physics Engine
Honeywell Hackathon Original Implementation

Provides a first-principles heat capacity differential model for single-zone envelope thermodynamics,
dynamic COP compressor power curves, Fanger Predicted Mean Vote (PMV) thermal comfort indices,
and dynamic time-of-use electrical grid tariff structures.
"""

import math
from dataclasses import dataclass
from typing import Dict, Any
from app.config.settings import Settings
from app.utils.logger import setup_logger

logger = setup_logger("thermodynamic_engine")


@dataclass
class SimulationState:
    """
    Data holder for real-time physical zone state variables.
    """
    step: int = 0
    sim_time_hours: float = 0.0
    indoor_temp: float = 22.0
    outdoor_temp: float = 28.0
    humidity: float = 50.0
    pmv: float = 0.0
    iaq_co2_ppm: float = 420.0
    cooling_setpoint: float = 23.0
    heating_setpoint: float = 20.0
    fan_speed: float = 0.7
    cooling_load_kw: float = 0.0
    heating_load_kw: float = 0.0
    hvac_power_kw: float = 0.0
    total_energy_kwh: float = 0.0
    occupancy_ratio: float = 0.0
    carbon_intensity: float = 0.35
    electricity_price: float = 0.15
    carbon_emissions_kg: float = 0.0
    cost_usd: float = 0.0


class SyntheticBuildingSimulator:
    """
    Original 1st-Order Thermal Mass Energy Balance Simulator.
    Models building heat exchange across envelope walls, solar irradiation, internal occupant loads,
    and non-linear HVAC electrical power draw.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.state = SimulationState(
            indoor_temp=settings.building.default_cooling_setpoint - 0.5,
            cooling_setpoint=settings.building.default_cooling_setpoint,
            heating_setpoint=settings.building.default_heating_setpoint,
            fan_speed=settings.building.default_fan_speed
        )

        # Bespoke physical parameters for 1200 m² open-plan commercial zone
        self.thermal_capacitance_kj_k = 15000.0   # Thermal inertia capacitance of building structure (kJ/K)
        self.envelope_transmittance_kw_k = 1.2    # Combined wall & fenestration heat transfer coefficient UA (kW/K)
        self.nominal_cop_cooling = 3.5            # Baseline cooling Coefficient of Performance

    def step(self, cooling_setpoint: float, heating_setpoint: float, fan_speed: float) -> SimulationState:
        """
        Advances thermal state forward by one 15-minute timestep (0.25 hours) using Euler integration.
        """
        self.state.step += 1
        timestep_delta_hours = 0.25
        self.state.sim_time_hours += timestep_delta_hours
        current_hour_of_day = self.state.sim_time_hours % 24.0

        # 1. Diurnal Ambient Temperature Cycle (Min 14.0°C at dawn, Max 32.0°C at peak afternoon)
        self.state.outdoor_temp = 23.0 + 9.0 * math.sin(math.pi * (current_hour_of_day - 9.0) / 12.0)
        self.state.humidity = max(30.0, min(80.0, 55.0 - 15.0 * math.sin(math.pi * (current_hour_of_day - 9.0) / 12.0)))

        # 2. Gaussian Commercial Occupancy Curve (Peak occupancy between 08:00 and 18:00)
        if 8.0 <= current_hour_of_day <= 18.0:
            self.state.occupancy_ratio = max(0.1, min(1.0, math.exp(-((current_hour_of_day - 13.0) ** 2) / 10.0)))
        else:
            self.state.occupancy_ratio = 0.05

        # Heat flux calculations (kW)
        internal_heat_gain_kw = self.state.occupancy_ratio * 30.0  # Occupant body heat & equipment radiation
        solar_heat_gain_kw = max(0.0, 25.0 * math.sin(math.pi * (current_hour_of_day - 6.0) / 12.0)) if 6.0 <= current_hour_of_day <= 18.0 else 0.0
        envelope_heat_loss_kw = self.envelope_transmittance_kw_k * (self.state.outdoor_temp - self.state.indoor_temp)

        # 3. Closed-Loop Actuator Reaction & Demand Calculation
        self.state.cooling_setpoint = cooling_setpoint
        self.state.heating_setpoint = heating_setpoint
        self.state.fan_speed = max(0.1, min(1.0, fan_speed))

        self.state.cooling_load_kw = 0.0
        self.state.heating_load_kw = 0.0

        if self.state.indoor_temp > cooling_setpoint:
            temp_gradient = self.state.indoor_temp - cooling_setpoint
            required_cooling = temp_gradient * (self.thermal_capacitance_kj_k / (timestep_delta_hours * 3600.0)) + internal_heat_gain_kw + solar_heat_gain_kw + envelope_heat_loss_kw
            self.state.cooling_load_kw = max(0.0, required_cooling)
        elif self.state.indoor_temp < heating_setpoint:
            temp_gradient = heating_setpoint - self.state.indoor_temp
            required_heating = temp_gradient * (self.thermal_capacitance_kj_k / (timestep_delta_hours * 3600.0)) - (internal_heat_gain_kw + solar_heat_gain_kw + envelope_heat_loss_kw)
            self.state.heating_load_kw = max(0.0, required_heating)

        # Temperature-dependent COP variation
        adjusted_cop = self.nominal_cop_cooling * (1.0 - 0.015 * (self.state.outdoor_temp - 25.0))
        effective_cop = max(1.5, adjusted_cop)

        # Electrical Demand (kW) = Compressor Cooling Draw + Heating Resistance + Fan Affinity Law (P ~ N^3)
        electrical_cooling_kw = self.state.cooling_load_kw / effective_cop
        electrical_heating_kw = self.state.heating_load_kw / 0.95
        electrical_fan_kw = 8.0 * (self.state.fan_speed ** 3.0)

        self.state.hvac_power_kw = electrical_cooling_kw + electrical_heating_kw + electrical_fan_kw
        step_energy_kwh = self.state.hvac_power_kw * timestep_delta_hours
        self.state.total_energy_kwh += step_energy_kwh

        # 4. Numerical Differential Temperature Step (dT/dt Integration)
        total_heat_flux_kw = internal_heat_gain_kw + solar_heat_gain_kw + envelope_heat_loss_kw - self.state.cooling_load_kw + self.state.heating_load_kw
        temp_derivative = (total_heat_flux_kw * 3600.0) / self.thermal_capacitance_kj_k
        self.state.indoor_temp += temp_derivative * timestep_delta_hours

        # 5. Fanger PMV Thermal Comfort Index & Indoor Air Quality (IAQ CO2 ppm) Model
        comfort_baseline_temp = 23.0
        self.state.pmv = round(0.35 * (self.state.indoor_temp - comfort_baseline_temp) + 0.005 * (self.state.humidity - 50.0), 2)
        self.state.iaq_co2_ppm = round(420.0 + self.state.occupancy_ratio * 650.0 + (1.0 - self.state.fan_speed) * 150.0, 1)

        # 6. Grid Cost & Carbon Intensity
        is_peak_tariff = 14.0 <= current_hour_of_day <= 20.0
        self.state.electricity_price = self.settings.grid.electricity_price_peak if is_peak_tariff else self.settings.grid.electricity_price_offpeak
        self.state.carbon_intensity = self.settings.grid.carbon_intensity_peak if is_peak_tariff else self.settings.grid.carbon_intensity_offpeak

        self.state.carbon_emissions_kg = step_energy_kwh * self.state.carbon_intensity
        self.state.cost_usd = step_energy_kwh * self.state.electricity_price

        return self.state

    def get_observation(self) -> Dict[str, Any]:
        """
        Returns snapshot of current zone physical telemetry dictionary.
        """
        return {
            "step": self.state.step,
            "sim_time_hours": round(self.state.sim_time_hours, 2),
            "indoor_temp": round(self.state.indoor_temp, 2),
            "outdoor_temp": round(self.state.outdoor_temp, 2),
            "humidity": round(self.state.humidity, 1),
            "pmv": self.state.pmv,
            "iaq_co2_ppm": self.state.iaq_co2_ppm,
            "cooling_setpoint": self.state.cooling_setpoint,
            "heating_setpoint": self.state.heating_setpoint,
            "fan_speed": self.state.fan_speed,
            "cooling_load_kw": round(self.state.cooling_load_kw, 2),
            "heating_load_kw": round(self.state.heating_load_kw, 2),
            "hvac_power_kw": round(self.state.hvac_power_kw, 2),
            "total_energy_kwh": round(self.state.total_energy_kwh, 2),
            "occupancy_ratio": round(self.state.occupancy_ratio, 2),
            "carbon_intensity": self.state.carbon_intensity,
            "electricity_price": self.state.electricity_price,
            "carbon_emissions_kg": round(self.state.carbon_emissions_kg, 3),
            "cost_usd": round(self.state.cost_usd, 3)
        }
