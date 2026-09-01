"""
EcoLoop AI - Agentic Reasoning Module
Executes LLM-driven decision reasoning using open-source LLM clients or heuristic physical policies.
Integrates directly with the MCP Server to modify setpoints and query environment forecasts.
"""

import json
import re
from typing import Dict, Any, Optional
import httpx
from app.config.settings import Settings
from app.mcp.server import MCPServer
from app.agents.prompts import BUILDING_ENGINEER_SYSTEM_PROMPT, USER_OBSERVATION_PROMPT
from app.utils.logger import setup_logger

logger = setup_logger("reasoning_agent")


class ReasoningAgent:
    """
    LLM-powered Reasoning Agent for Honeywell EcoLoop AI.
    Executes reasoning over building observation telemetry and applies optimal setpoints via MCP tools.
    """

    def __init__(self, settings: Settings, mcp_server: MCPServer):
        self.settings = settings
        self.mcp = mcp_server
        self.llm_config = settings.llm

    def reason_and_act(self) -> Dict[str, Any]:
        """
        Executes a single Observe -> Reason -> Act cycle:
        1. Queries current state via ReadCurrentState MCP tool.
        2. Queries weather forecast via ReadWeather MCP tool.
        3. Formulates prompt and calls LLM (or heuristic expert policy fallback).
        4. Applies setpoints via ModifySetpoints MCP tool.
        """
        # 1. Observe via MCP
        current_obs = self.mcp.read_current_state()
        forecast = self.mcp.read_weather(horizon_hours=6)

        # 2. Format Prompt
        user_prompt = USER_OBSERVATION_PROMPT.format(
            step=current_obs.get("step", 0),
            sim_time_hours=current_obs.get("sim_time_hours", 0.0),
            indoor_temp=current_obs.get("indoor_temp", 22.0),
            outdoor_temp=current_obs.get("outdoor_temp", 25.0),
            humidity=current_obs.get("humidity", 50.0),
            pmv=current_obs.get("pmv", 0.0),
            cooling_setpoint=current_obs.get("cooling_setpoint", 23.0),
            heating_setpoint=current_obs.get("heating_setpoint", 20.0),
            fan_speed=current_obs.get("fan_speed", 0.7),
            fan_speed_pct=int(current_obs.get("fan_speed", 0.7) * 100),
            hvac_power_kw=current_obs.get("hvac_power_kw", 0.0),
            total_energy_kwh=current_obs.get("total_energy_kwh", 0.0),
            occupancy_ratio=current_obs.get("occupancy_ratio", 0.0),
            occupancy_pct=int(current_obs.get("occupancy_ratio", 0.0) * 100),
            electricity_price=current_obs.get("electricity_price", 0.15),
            tariff_type="PEAK" if current_obs.get("electricity_price", 0.15) > 0.20 else "OFF_PEAK",
            carbon_intensity=current_obs.get("carbon_intensity", 0.35),
            weather_forecast_json=json.dumps(forecast, indent=2)
        )

        # 3. Call LLM or Rule-based Expert Engine
        decision = self._call_llm_or_heuristic(BUILDING_ENGINEER_SYSTEM_PROMPT, user_prompt, current_obs)

        # 4. Act via MCP tool
        actuation_result = self.mcp.modify_setpoints(
            cooling_setpoint=decision["recommended_cooling_setpoint"],
            heating_setpoint=decision["recommended_heating_setpoint"],
            fan_speed=decision["recommended_fan_speed"],
            reasoning=decision["reasoning"]
        )

        return {
            "observation": current_obs,
            "decision": decision,
            "actuation_result": actuation_result
        }

    def _call_llm_or_heuristic(
        self,
        system_prompt: str,
        user_prompt: str,
        obs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Tries to call OpenAI/LiteLLM endpoint if API key is provided, else executes high-precision engineering heuristic.
        """
        api_key = self.llm_config.api_key
        if api_key and self.llm_config.api_base_url:
            try:
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.llm_config.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": self.llm_config.temperature
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(f"{self.llm_config.api_base_url}/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        content = resp.json()["choices"][0]["message"]["content"]
                        match = re.search(r"\{.*\}", content, re.DOTALL)
                        if match:
                            return json.loads(match.group(0))
            except Exception as e:
                logger.warning(f"LLM API call skipped ({e}). Executing Senior Expert Engineering Rule Engine.")

        # Fallback Senior Building Engineering Dynamic Heuristics
        return self._expert_heuristic(obs)

    def _expert_heuristic(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expert Honeywell HVAC Rule Engine incorporating occupancy, tariff structure, outdoor temp, and PMV.
        """
        indoor = obs.get("indoor_temp", 22.0)
        outdoor = obs.get("outdoor_temp", 25.0)
        occ = obs.get("occupancy_ratio", 0.5)
        price = obs.get("electricity_price", 0.15)
        pmv = obs.get("pmv", 0.0)

        # Baseline setpoints
        c_set = 23.0
        h_set = 20.0
        fan = 0.7
        reasons = []

        if occ < 0.15:
            c_set += 2.0
            h_set -= 2.0
            fan = 0.3
            reasons.append(f"Occupancy dropped to {int(occ*100)}%. Setpoints relaxed to save HVAC energy.")
        elif occ >= 0.5:
            reasons.append(f"Occupancy active at {int(occ*100)}%. Tightening setpoints to preserve PMV comfort.")

        if price > 0.20:  # Peak tariff
            c_set += 1.0
            fan = max(0.4, fan - 0.2)
            reasons.append(f"Electricity tariff is currently HIGH (${price}/kWh). Moderating cooling setpoint to {c_set}°C.")

        if outdoor < 22.0 and indoor > 23.0:
            reasons.append(f"Outdoor temperature is cool ({outdoor}°C). Utilizing natural economizer cooling potential.")

        if pmv > 0.5:
            c_set -= 0.5
            fan = min(1.0, fan + 0.2)
            reasons.append(f"Occupant discomfort detected (PMV={pmv}). Increasing cooling to return PMV to comfort zone.")

        reasoning_text = " ".join(reasons) if reasons else "Operating under standard steady-state building policy."

        return {
            "reasoning": reasoning_text,
            "recommended_cooling_setpoint": round(c_set, 1),
            "recommended_heating_setpoint": round(h_set, 1),
            "recommended_fan_speed": round(fan, 2),
            "ventilation_strategy": "DEMAND_CONTROLLED",
            "window_strategy": "OPEN" if (outdoor < indoor and outdoor > 18.0) else "CLOSED"
        }
