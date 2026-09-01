"""
EcoLoop AI - Honeywell Hackathon Main Entrypoint
CLI application to run autonomous physical building control loops or launch the Streamlit dashboard.
"""

import sys
import argparse
import subprocess
from app.config.settings import get_settings
from app.controllers.closed_loop import ClosedLoopController
from app.utils.logger import setup_logger

logger = setup_logger("ecoloop_main")


def run_headless(steps: int):
    """
    Executes N steps of closed-loop building control headlessly.
    """
    logger.info(f"Launching EcoLoop AI Headless Controller for {steps} steps...")
    settings = get_settings()
    controller = ClosedLoopController(settings)
    results = controller.run_loop(steps=steps)
    logger.info(f"Headless execution finished successfully. Recorded {len(results)} timesteps.")


def launch_dashboard():
    """
    Launches the Streamlit Web Application.
    """
    logger.info("Launching EcoLoop AI Streamlit Interactive Dashboard...")
    cmd = ["streamlit", "run", "app/dashboard/dashboard.py"]
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="EcoLoop AI - Autonomous Physical Building Intelligence")
    parser.add_argument("--mode", choices=["run", "dashboard"], default="run", help="Execution mode: run or dashboard")
    parser.add_argument("--steps", type=int, default=12, help="Number of simulation timesteps to execute")

    args = parser.parse_args()

    if args.mode == "dashboard":
        launch_dashboard()
    else:
        run_headless(args.steps)


if __name__ == "__main__":
    main()
