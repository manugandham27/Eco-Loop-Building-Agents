"""
EcoLoop AI - Multi-Objective Optimization Engine
Calculates multi-objective penalty and efficiency scores across Energy, Comfort, Cost, and Carbon Footprint.
Ensures trade-off optimization rather than single-objective sub-optimization.
"""

from typing import Dict, Any
from app.config.settings import Settings, OptimizationWeights
from app.utils.logger import setup_logger

logger = setup_logger("optimization_engine")


class MultiObjectiveOptimizer:
    """
    Evaluates setpoint candidates and computes composite loss score J:
    J = w_energy * E + w_comfort * C_comfort + w_cost * Cost + w_carbon * Carbon
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.weights: OptimizationWeights = settings.optimization

    def evaluate_candidate(
        self,
        indoor_temp: float,
        pmv: float,
        hvac_power_kw: float,
        electricity_price: float,
        carbon_intensity: float
    ) -> Dict[str, float]:
        """
        Computes composite scalar penalty score for a given setpoint candidate state.
        Lower score indicates higher overall performance across all objectives.
        """
        # 1. Energy Penalty (Normalized against 25 kW max HVAC capacity)
        energy_score = min(1.0, hvac_power_kw / 25.0)

        # 2. Comfort Penalty (Fanger PMV deviation score: 0 = perfect comfort, > 0.5 = discomfort)
        comfort_penalty = abs(pmv)
        if comfort_penalty < 0.2:
            comfort_score = 0.0
        elif comfort_penalty <= 0.5:
            comfort_score = (comfort_penalty - 0.2) / 0.3
        else:
            comfort_score = min(2.0, 1.0 + (comfort_penalty - 0.5) * 2.0)

        # 3. Financial Cost Score (Normalized against peak price $0.28/kWh)
        cost_rate_usd_hr = hvac_power_kw * electricity_price
        cost_score = min(1.0, cost_rate_usd_hr / 7.0)

        # 4. Carbon Footprint Score (Normalized against peak grid factor 0.65 kg/kWh)
        carbon_rate_kg_hr = hvac_power_kw * carbon_intensity
        carbon_score = min(1.0, carbon_rate_kg_hr / 16.0)

        # Composite Loss Function calculation
        composite_score = (
            self.weights.energy * energy_score +
            self.weights.comfort * comfort_score +
            self.weights.cost * cost_score +
            self.weights.carbon * carbon_score
        )

        return {
            "composite_score": round(composite_score, 4),
            "energy_score": round(energy_score, 4),
            "comfort_score": round(comfort_score, 4),
            "cost_score": round(cost_score, 4),
            "carbon_score": round(carbon_score, 4),
        }
