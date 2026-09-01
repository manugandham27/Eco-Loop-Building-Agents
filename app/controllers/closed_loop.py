"""
EcoLoop AI - Closed-Loop Control Orchestrator
Executes the continuous physical control cycle:
Observe (Simulation) -> Reason (LLM Agent) -> Act (MCP Actuator) -> Evaluate (Metrics) -> Repeat
"""

import time
from typing import Dict, Any, List
from app.config.settings import Settings
from app.database.models import DatabaseManager
from app.energyplus.controller import EnergyPlusController
from app.mcp.server import MCPServer
from app.agents.reasoning import ReasoningAgent
from app.utils.logger import setup_logger

logger = setup_logger("closed_loop_orchestrator")


class ClosedLoopController:
    """
    Autonomous physical AI orchestrator operating the closed-loop building automation lifecycle.
    Runs without human intervention.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.db_manager = DatabaseManager(settings.db_path)
        self.ep_controller = EnergyPlusController(settings)
        self.mcp_server = MCPServer(self.ep_controller, self.db_manager)
        self.agent = ReasoningAgent(settings, self.mcp_server)

    def run_step(self) -> Dict[str, Any]:
        """
        Executes one full iteration of the autonomous Observe-Reason-Act-Evaluate loop.
        """
        logger.info("=== Starting Closed-Loop Autonomous Control Timestep ===")

        # Step 1: Advance simulation & observe physical parameters via MCP
        observation = self.mcp_server.run_simulation_step()
        step_num = observation.get("step", 0)

        # Step 2 & 3: Reason using LLM Agent & Actuate setpoints via MCP tool
        reasoning_result = self.agent.reason_and_act()

        # Step 4: Evaluate performance & compute cumulative metrics
        metrics = self.mcp_server.save_metrics()

        logger.info(
            f"=== Completed Step {step_num} | Energy Savings: {metrics['energy_savings_pct']}% | "
            f"Comfort Score: {metrics['comfort_score']}% | Carbon Reduced: {metrics['total_carbon_reduced_kg']} kg ==="
        )

        return {
            "step": step_num,
            "observation": observation,
            "decision": reasoning_result["decision"],
            "metrics": metrics
        }

    def run_loop(self, steps: int = 24, sleep_interval_sec: float = 0.0) -> List[Dict[str, Any]]:
        """
        Executes continuous closed-loop control for N timesteps.
        """
        logger.info(f"Initiating autonomous closed-loop execution for {steps} steps...")
        results = []
        for i in range(steps):
            res = self.run_step()
            results.append(res)
            if sleep_interval_sec > 0:
                time.sleep(sleep_interval_sec)
        logger.info(f"Successfully completed {steps} steps of autonomous closed-loop control.")
        return results
