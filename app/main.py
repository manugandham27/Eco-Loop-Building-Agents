"""
EcoLoop AI — Production FastAPI Server
Exposes enterprise REST API endpoints for remote building telemetry, setpoint overrides,
system health metrics, and OpenAPI/Swagger interactive documentation.
"""

from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config.settings import get_settings
from app.database.models import DatabaseManager
from app.controllers.closed_loop import ClosedLoopController
from app.services.evaluation import EvaluationEngine

# Initialize FastAPI application with OpenAPI metadata
app = FastAPI(
    title="Honeywell EcoLoop AI Platform API",
    description="Production REST API for Physical AI Closed-Loop Building Automation & Energy Optimization.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for enterprise frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()
db_manager = DatabaseManager(settings.db_path)
closed_loop = ClosedLoopController(settings)


class SetpointOverrideRequest(BaseModel):
    cooling_setpoint: float = Field(..., ge=20.0, le=27.0, description="Cooling setpoint in Celsius (20-27)")
    heating_setpoint: float = Field(..., ge=16.0, le=22.0, description="Heating setpoint in Celsius (16-22)")
    fan_speed: float = Field(..., ge=0.1, le=1.0, description="Fan speed ratio (0.1 - 1.0)")
    reasoning: str = Field("Manual Supervisory REST API Override", description="Engineering justification")


class ExecutionStepResponse(BaseModel):
    step: int
    applied_cooling_setpoint: float
    applied_heating_setpoint: float
    applied_fan_speed: float
    status: str


@app.get("/", tags=["Health Check"])
def root_health_check() -> Dict[str, str]:
    """
    Returns core platform status and active physical engine mode.
    """
    return {
        "status": "ONLINE",
        "platform": "Honeywell EcoLoop AI Building Intelligence",
        "engine": "PyEnergyPlus / First-Principles Thermodynamic Fallback",
        "mcp_status": "ACTIVE"
    }


@app.get("/api/v1/telemetry/latest", tags=["Building Telemetry"])
def get_latest_telemetry() -> Dict[str, Any]:
    """
    Returns the latest real-time zone sensor reading (indoor/outdoor temp, PMV, IAQ CO2, grid tariff).
    """
    obs = db_manager.get_latest_observation()
    if not obs:
        raise HTTPException(status_code=444, detail="No simulation telemetry recorded yet.")
    return obs


@app.get("/api/v1/telemetry/history", tags=["Building Telemetry"])
def get_telemetry_history(limit: int = Query(24, ge=1, le=500)) -> List[Dict[str, Any]]:
    """
    Retrieves historical zone telemetry records.
    """
    observations = db_manager.get_all_observations()
    return observations[-limit:] if observations else []


@app.get("/api/v1/metrics/kpis", tags=["Performance Metrics"])
def get_performance_kpis() -> Dict[str, Any]:
    """
    Computes cumulative energy savings %, carbon reduction kg, and comfort preservation scores vs baseline.
    """
    observations = db_manager.get_all_observations()
    return EvaluationEngine.calculate_metrics(observations)


@app.post("/api/v1/control/step", tags=["Autonomous Control"])
def execute_control_step(steps: int = Query(1, ge=1, le=48)) -> Dict[str, Any]:
    """
    Triggers N steps of the autonomous Observe-Reason-Act-Evaluate closed-loop cycle.
    """
    results = closed_loop.run_loop(steps=steps)
    return {
        "executed_steps": len(results),
        "latest_step": results[-1] if results else {}
    }


@app.post("/api/v1/control/override", tags=["Supervisory Overrides"])
def setpoint_override(request: SetpointOverrideRequest) -> ExecutionStepResponse:
    """
    Applies supervisory setpoint overrides to the physical building actuators via MCP tool protocols.
    """
    res = closed_loop.mcp_server.modify_setpoints(
        cooling_setpoint=request.cooling_setpoint,
        heating_setpoint=request.heating_setpoint,
        fan_speed=request.fan_speed,
        reasoning=request.reasoning
    )
    return ExecutionStepResponse(
        step=res.get("step", 0),
        applied_cooling_setpoint=res.get("applied_cooling_setpoint", 23.0),
        applied_heating_setpoint=res.get("applied_heating_setpoint", 20.0),
        applied_fan_speed=res.get("applied_fan_speed", 0.7),
        status="APPLIED"
    )
