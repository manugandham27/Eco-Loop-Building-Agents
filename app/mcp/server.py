"""
EcoLoop AI - Model Context Protocol (MCP) Server
Exposes standardized MCP operational tools allowing LLM agents to observe state, adjust actuators,
read forecasts, query health diagnostics, evaluate grid demand response, and query performance metrics safely.
"""

import json
from typing import Dict, Any, List, Optional
from app.config.settings import get_settings
from app.database.models import DatabaseManager
from app.energyplus.controller import EnergyPlusController
from app.simulation.weather import WeatherService
from app.services.evaluation import EvaluationEngine
from app.services.fdd import FaultDetectionDiagnostics
from app.services.demand_response import DemandResponseController
from app.utils.logger import setup_logger

logger = setup_logger("mcp_server")


class MCPServer:
    """
    Model Context Protocol operational interface for EcoLoop AI.
    Integrates database, simulation controller, weather forecaster, FDD diagnostics, and metrics recorder.
    """

    def __init__(self, controller: EnergyPlusController, db_manager: DatabaseManager):
        self.settings = get_settings()
        self.controller = controller
        self.db = db_manager
        self.weather_service = WeatherService(self.settings.simulation.epw_weather_file)
        self.dr_controller = DemandResponseController()

    def read_current_state(self) -> Dict[str, Any]:
        """
        [MCP Tool: ReadCurrentState]
        Returns the latest real-time building observation (indoor temp, outdoor temp, PMV, IAQ CO2, power, tariffs).
        """
        obs = self.db.get_latest_observation()
        if not obs:
            obs = self.controller.step()
        logger.info("[MCP Tool Executed] ReadCurrentState")
        return obs

    def read_simulation_log(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        [MCP Tool: ReadSimulationLog]
        Retrieves recent telemetry observations from the SQLite database log.
        """
        obs_list = self.db.get_all_observations()
        logger.info(f"[MCP Tool Executed] ReadSimulationLog (limit={limit})")
        return obs_list[-limit:] if obs_list else []

    def modify_setpoints(
        self,
        cooling_setpoint: float,
        heating_setpoint: float,
        fan_speed: float,
        reasoning: str
    ) -> Dict[str, Any]:
        """
        [MCP Tool: ModifySetpoints]
        Updates building HVAC setpoints, fan speeds, and logs the agent's explicit engineering reasoning.
        """
        self.controller.set_actuators(
            cooling_setpoint=cooling_setpoint,
            heating_setpoint=heating_setpoint,
            fan_speed=fan_speed
        )

        # Log decision into database
        obs = self.read_current_state()
        step = obs.get("step", 0)

        decision_record = self.db.record_decision({
            "step": step,
            "cooling_setpoint": self.controller.current_cooling_setpoint,
            "heating_setpoint": self.controller.current_heating_setpoint,
            "fan_speed": self.controller.current_fan_speed,
            "ventilation": "AUTO_DEMAND_CONTROLLED",
            "window_strategy": "CLOSED" if obs.get("outdoor_temp", 25.0) > 24.0 else "NATURAL_VENTILATION",
            "reasoning": reasoning,
            "action_summary": f"Set Cooling: {cooling_setpoint}°C, Heating: {heating_setpoint}°C, Fan: {fan_speed*100:.0f}%"
        })

        logger.info(f"[MCP Tool Executed] ModifySetpoints -> Cooling={cooling_setpoint}°C, Heating={heating_setpoint}°C")
        return {
            "status": "SUCCESS",
            "step": step,
            "applied_cooling_setpoint": self.controller.current_cooling_setpoint,
            "applied_heating_setpoint": self.controller.current_heating_setpoint,
            "applied_fan_speed": self.controller.current_fan_speed,
            "decision_id": decision_record.id
        }

    def run_simulation_step(self) -> Dict[str, Any]:
        """
        [MCP Tool: RunSimulationStep]
        Advances the building simulation by 1 timestep and records observation to DB.
        """
        raw_obs = self.controller.step()
        record = self.db.record_observation(raw_obs)
        logger.info(f"[MCP Tool Executed] RunSimulationStep -> Advanced to Step {record.step}")
        return raw_obs

    def save_metrics(self) -> Dict[str, Any]:
        """
        [MCP Tool: SaveMetrics]
        Calculates cumulative performance metrics vs baseline and saves to database.
        """
        observations = self.db.get_all_observations()
        metrics = EvaluationEngine.calculate_metrics(observations)

        latest_obs = observations[-1] if observations else {}
        step = latest_obs.get("step", 0)

        self.db.record_metrics({
            "step": step,
            "energy_saved_kwh": metrics["total_energy_saved_kwh"],
            "baseline_energy_kwh": metrics["total_energy_saved_kwh"] * 1.25,
            "comfort_score": metrics["comfort_score"],
            "carbon_reduction_kg": metrics["total_carbon_reduced_kg"],
            "cost_saved_usd": metrics["total_cost_saved_usd"]
        })

        logger.info("[MCP Tool Executed] SaveMetrics")
        return metrics

    def read_weather(self, horizon_hours: int = 6) -> List[Dict[str, Any]]:
        """
        [MCP Tool: ReadWeather]
        Fetches look-ahead weather forecast data for predictive setpoint adjustment.
        """
        current_obs = self.read_current_state()
        sim_time = current_obs.get("sim_time_hours", 0.0)
        forecast = self.weather_service.get_forecast(sim_time, horizon_hours)
        logger.info(f"[MCP Tool Executed] ReadWeather (horizon={horizon_hours}h)")
        return forecast

    def diagnose_building_health(self) -> Dict[str, Any]:
        """
        [MCP Tool: DiagnoseBuildingHealth]
        Executes automated Fault Detection & Diagnostics (FDD) to detect component degradation or airflow issues.
        """
        current_obs = self.read_current_state()
        history = self.read_simulation_log(limit=10)
        diagnostics = FaultDetectionDiagnostics.analyze_health(current_obs, history)
        logger.info(f"[MCP Tool Executed] DiagnoseBuildingHealth -> Status: {diagnostics['health_status']}")
        return diagnostics

    def evaluate_demand_response(self) -> Dict[str, Any]:
        """
        [MCP Tool: EvaluateDemandResponse]
        Checks for smart grid Peak Load Shaving events and calculates load shedding recommendations.
        """
        current_obs = self.read_current_state()
        price = current_obs.get("electricity_price", 0.15)
        hvac_power = current_obs.get("hvac_power_kw", 0.0)
        dr_event = self.dr_controller.evaluate_grid_event(price, hvac_power)
        logger.info(f"[MCP Tool Executed] EvaluateDemandResponse -> DR Active: {dr_event['dr_active']}")
        return dr_event

    def read_historical_data(self) -> Dict[str, Any]:
        """
        [MCP Tool: ReadHistoricalData]
        Retrieves all recorded observations, decisions, and system metrics for long-term trend analysis.
        """
        logger.info("[MCP Tool Executed] ReadHistoricalData")
        return {
            "observations": self.db.get_all_observations(),
            "decisions": self.db.get_all_decisions(),
            "metrics": self.db.get_all_metrics()
        }

    def generate_dashboard(self) -> Dict[str, Any]:
        """
        [MCP Tool: GenerateDashboard]
        Returns a summary payload ready for visual rendering in the Streamlit UI dashboard.
        """
        observations = self.db.get_all_observations()
        decisions = self.db.get_all_decisions()
        kpis = EvaluationEngine.calculate_metrics(observations)

        logger.info("[MCP Tool Executed] GenerateDashboard")
        return {
            "total_steps": len(observations),
            "latest_observation": observations[-1] if observations else {},
            "latest_decision": decisions[-1] if decisions else {},
            "kpis": kpis
        }
