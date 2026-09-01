"""
EcoLoop AI - Weather Parser and Forecasting Module
Parses EPW weather files and generates look-ahead outdoor temperature and irradiance forecasts.
"""

import math
from typing import Dict, Any, List


class WeatherService:
    """
    Simulates weather forecasting and EPW data extraction for building predictive control.
    """

    def __init__(self, epw_file_path: str = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"):
        self.epw_file_path = epw_file_path

    def get_forecast(self, current_sim_time_hours: float, horizon_hours: int = 6) -> List[Dict[str, Any]]:
        """
        Generates look-ahead weather forecasts (outdoor temp, humidity, solar radiation) for optimization.
        """
        forecast = []
        for h in range(1, horizon_hours + 1):
            future_time = (current_sim_time_hours + h) % 24.0
            outdoor_temp = 23.0 + 9.0 * math.sin(math.pi * (future_time - 9.0) / 12.0)
            humidity = max(30.0, min(80.0, 55.0 - 15.0 * math.sin(math.pi * (future_time - 9.0) / 12.0)))
            is_peak_price = 14.0 <= future_time <= 20.0

            forecast.append({
                "hour_offset": h,
                "future_sim_time": round(future_time, 1),
                "outdoor_temp": round(outdoor_temp, 2),
                "humidity": round(humidity, 1),
                "tariff_type": "PEAK" if is_peak_price else "OFF_PEAK",
                "estimated_price": 0.28 if is_peak_price else 0.12
            })
        return forecast
