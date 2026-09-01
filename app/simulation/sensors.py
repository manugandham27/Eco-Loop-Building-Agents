"""
EcoLoop AI - Sensor Stream Converter
Converts raw simulation states into structured JSON telemetry observations.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class TelemetryObservation(BaseModel):
    step: int
    sim_time_hours: float
    indoor_temp: float = Field(..., description="Indoor temperature in Celsius")
    outdoor_temp: float = Field(..., description="Outdoor temperature in Celsius")
    humidity: float = Field(..., description="Indoor relative humidity percentage")
    pmv: float = Field(..., description="Predicted Mean Vote comfort index (-3 to +3)")
    iaq_co2_ppm: float = Field(450.0, description="Indoor Air Quality CO2 concentration in PPM")
    cooling_setpoint: float
    heating_setpoint: float
    fan_speed: float
    cooling_load_kw: float
    heating_load_kw: float
    hvac_power_kw: float
    total_energy_kwh: float
    occupancy_ratio: float = Field(..., description="Occupancy percentage ratio (0.0 - 1.0)")
    carbon_intensity: float = Field(..., description="kg CO2 / kWh grid factor")
    electricity_price: float = Field(..., description="$/kWh grid tariff")
    carbon_emissions_kg: float
    cost_usd: float


class SensorStream:
    """
    Transforms raw simulation observations into validated TelemetryObservation objects.
    """

    @staticmethod
    def process(raw_data: Dict[str, Any]) -> TelemetryObservation:
        return TelemetryObservation(**raw_data)
