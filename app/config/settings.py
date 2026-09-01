"""
EcoLoop AI - Configuration and Policy Management Module
Provides strongly typed Pydantic models for platform parameters, grid tariffs, and optimization policy weights.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import os
import yaml
from pydantic import BaseModel, Field


class BuildingConfig(BaseModel):
    name: str = "Honeywell HQ - Innovation Tower Zone 1"
    floor_area_sqm: float = 1200.0
    target_pmv_min: float = -0.5
    target_pmv_max: float = 0.5
    default_cooling_setpoint: float = 23.0
    default_heating_setpoint: float = 20.0
    default_fan_speed: float = 0.7
    min_cooling_setpoint: float = 20.0
    max_cooling_setpoint: float = 27.0
    min_heating_setpoint: float = 16.0
    max_heating_setpoint: float = 22.0


class GridConfig(BaseModel):
    electricity_price_peak: float = 0.28
    electricity_price_offpeak: float = 0.12
    carbon_intensity_peak: float = 0.65
    carbon_intensity_offpeak: float = 0.25


class OptimizationWeights(BaseModel):
    energy: float = 0.35
    comfort: float = 0.35
    cost: float = 0.15
    carbon: float = 0.15


class LLMConfig(BaseModel):
    provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.2
    api_base_url: Optional[str] = "https://api.openai.com/v1"
    api_key: Optional[str] = None


class SimulationConfig(BaseModel):
    timesteps_per_hour: int = 4
    duration_days: int = 7
    epw_weather_file: str = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
    idf_building_file: str = "SmallOffice.idf"


class MCPConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class Settings(BaseModel):
    building: BuildingConfig = Field(default_factory=BuildingConfig)
    grid: GridConfig = Field(default_factory=GridConfig)
    optimization: OptimizationWeights = Field(default_factory=OptimizationWeights)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    simulation: SimulationConfig = Field(default_factory=SimulationConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    db_path: str = "ecoloop.db"

    @classmethod
    def load_from_yaml(cls, yaml_path: str = "config.yaml") -> "Settings":
        """
        Loads configuration settings from a YAML file. Falls back to defaults if file is missing.
        """
        file_path = Path(yaml_path)
        if not file_path.exists():
            return cls()

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            # Read env variables for LLM key
            api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
            if api_key and "llm" in data:
                data["llm"]["api_key"] = api_key

            return cls(
                building=BuildingConfig(**data.get("building", {})),
                grid=GridConfig(**data.get("grid", {})),
                optimization=OptimizationWeights(**data.get("optimization", {}).get("weights", {})),
                llm=LLMConfig(**data.get("llm", {})),
                simulation=SimulationConfig(**data.get("simulation", {})),
                mcp=MCPConfig(**data.get("mcp", {})),
            )
        except Exception as e:
            print(f"Warning: Failed to load config.yaml ({e}). Using default settings.")
            return cls()


# Singleton instance for platform configuration
get_settings = Settings.load_from_yaml
