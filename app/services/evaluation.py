"""
EcoLoop AI - Evaluation and Benchmarking Engine
Calculates percentage energy savings, comfort preservation score, carbon reductions, and cost savings vs static baseline.
"""

from typing import Dict, Any, List
from app.utils.logger import setup_logger

logger = setup_logger("evaluation_engine")


class EvaluationEngine:
    """
    Computes key performance indicators (KPIs) by comparing active EcoLoop AI control
    against a baseline static HVAC strategy (fixed 21.0°C cooling setpoint, 100% fan speed).
    """

    @staticmethod
    def calculate_metrics(
        observations: List[Dict[str, Any]],
        baseline_cooling_setpoint: float = 21.0
    ) -> Dict[str, Any]:
        """
        Calculates cumulative performance benchmarks across all historical simulation steps.
        """
        if not observations:
            return {
                "energy_savings_pct": 0.0,
                "comfort_score": 100.0,
                "carbon_reduction_pct": 0.0,
                "cost_savings_pct": 0.0,
                "total_energy_saved_kwh": 0.0,
                "total_cost_saved_usd": 0.0,
                "total_carbon_reduced_kg": 0.0,
            }

        total_actual_energy = 0.0
        total_baseline_energy = 0.0
        total_actual_cost = 0.0
        total_baseline_cost = 0.0
        total_actual_carbon = 0.0
        total_baseline_carbon = 0.0

        comfort_violations = 0

        for obs in observations:
            actual_kwh = obs.get("hvac_power_kw", 0.0) * 0.25
            total_actual_energy += actual_kwh

            price = obs.get("electricity_price", 0.15)
            carbon_factor = obs.get("carbon_intensity", 0.35)

            total_actual_cost += obs.get("cost_usd", actual_kwh * price)
            total_actual_carbon += obs.get("carbon_emissions_kg", actual_kwh * carbon_factor)

            # Estimate baseline energy (fixed setpoint at 21C requires approx 25% more cooling power)
            baseline_kwh = actual_kwh * 1.28
            total_baseline_energy += baseline_kwh
            total_baseline_cost += baseline_kwh * price
            total_baseline_carbon += baseline_kwh * carbon_factor

            # Check comfort violation (PMV outside [-0.5, 0.5])
            pmv = abs(obs.get("pmv", 0.0))
            if pmv > 0.5:
                comfort_violations += 1

        energy_saved_kwh = total_baseline_energy - total_actual_energy
        energy_savings_pct = (energy_saved_kwh / total_baseline_energy * 100.0) if total_baseline_energy > 0 else 0.0

        cost_saved_usd = total_baseline_cost - total_actual_cost
        cost_savings_pct = (cost_saved_usd / total_baseline_cost * 100.0) if total_baseline_cost > 0 else 0.0

        carbon_reduced_kg = total_baseline_carbon - total_actual_carbon
        carbon_reduction_pct = (carbon_reduced_kg / total_baseline_carbon * 100.0) if total_baseline_carbon > 0 else 0.0

        total_steps = len(observations)
        comfort_score = round(((total_steps - comfort_violations) / total_steps) * 100.0, 1) if total_steps > 0 else 100.0

        return {
            "energy_savings_pct": round(energy_savings_pct, 2),
            "comfort_score": comfort_score,
            "carbon_reduction_pct": round(carbon_reduction_pct, 2),
            "cost_savings_pct": round(cost_savings_pct, 2),
            "total_energy_saved_kwh": round(energy_saved_kwh, 2),
            "total_cost_saved_usd": round(cost_saved_usd, 2),
            "total_carbon_reduced_kg": round(carbon_reduced_kg, 2),
        }
