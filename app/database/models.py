"""
EcoLoop AI - Database Models & Persistence Engine
Manages SQLite database initialization, schemas, and CRUD operations using SQLAlchemy.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import (
    create_engine, Column, Integer, Float, String, DateTime, Text
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.utils.logger import setup_logger

logger = setup_logger("database")

Base = declarative_base()


class SensorObservationRecord(Base):
    __tablename__ = "sensor_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    step = Column(Integer, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    sim_time_hours = Column(Float, nullable=False, default=0.0)
    indoor_temp = Column(Float, nullable=False)
    outdoor_temp = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pmv = Column(Float, nullable=False)
    iaq_co2_ppm = Column(Float, nullable=False, default=450.0)
    cooling_setpoint = Column(Float, nullable=False, default=23.0)
    heating_setpoint = Column(Float, nullable=False, default=20.0)
    fan_speed = Column(Float, nullable=False, default=0.7)
    cooling_load_kw = Column(Float, nullable=False)
    heating_load_kw = Column(Float, nullable=False)
    hvac_power_kw = Column(Float, nullable=False)
    total_energy_kwh = Column(Float, nullable=False)
    occupancy_ratio = Column(Float, nullable=False)
    carbon_intensity = Column(Float, nullable=False)
    electricity_price = Column(Float, nullable=False)
    carbon_emissions_kg = Column(Float, nullable=False)
    cost_usd = Column(Float, nullable=False)


class AIDecisionRecord(Base):
    __tablename__ = "ai_decisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    step = Column(Integer, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    cooling_setpoint = Column(Float, nullable=False)
    heating_setpoint = Column(Float, nullable=False)
    fan_speed = Column(Float, nullable=False)
    ventilation = Column(String, nullable=False)
    window_strategy = Column(String, nullable=False)
    reasoning = Column(Text, nullable=False)
    action_summary = Column(Text, nullable=True)


class ToolCallRecord(Base):
    __tablename__ = "tool_calls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    step = Column(Integer, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    tool_name = Column(String, nullable=False)
    arguments = Column(Text, nullable=False)
    result = Column(Text, nullable=False)


class SimulationMetricsRecord(Base):
    __tablename__ = "simulation_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    step = Column(Integer, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    energy_saved_kwh = Column(Float, nullable=False)
    baseline_energy_kwh = Column(Float, nullable=False)
    comfort_score = Column(Float, nullable=False)
    carbon_reduction_kg = Column(Float, nullable=False)
    cost_saved_usd = Column(Float, nullable=False)


class DatabaseManager:
    """
    Manages SQLite database creation and provides high-level data access interfaces.
    """

    def __init__(self, db_path: str = "ecoloop.db"):
        self.db_url = f"sqlite:///{db_path}"
        self.engine = create_engine(self.db_url, echo=False, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info(f"Database initialized at {self.db_url}")

    def get_session(self) -> Session:
        return self.SessionLocal()

    def record_observation(self, data: Dict[str, Any]) -> SensorObservationRecord:
        with self.get_session() as session:
            # Filter kwargs to matching columns
            valid_keys = {c.name for c in SensorObservationRecord.__table__.columns}
            filtered_data = {k: v for k, v in data.items() if k in valid_keys}
            record = SensorObservationRecord(**filtered_data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def record_decision(self, data: Dict[str, Any]) -> AIDecisionRecord:
        with self.get_session() as session:
            valid_keys = {c.name for c in AIDecisionRecord.__table__.columns}
            filtered_data = {k: v for k, v in data.items() if k in valid_keys}
            record = AIDecisionRecord(**filtered_data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def record_tool_call(self, step: int, tool_name: str, args: str, result: str) -> ToolCallRecord:
        with self.get_session() as session:
            record = ToolCallRecord(
                step=step,
                tool_name=tool_name,
                arguments=str(args),
                result=str(result)
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def record_metrics(self, data: Dict[str, Any]) -> SimulationMetricsRecord:
        with self.get_session() as session:
            valid_keys = {c.name for c in SimulationMetricsRecord.__table__.columns}
            filtered_data = {k: v for k, v in data.items() if k in valid_keys}
            record = SimulationMetricsRecord(**filtered_data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record

    def get_latest_observation(self) -> Optional[Dict[str, Any]]:
        with self.get_session() as session:
            row = session.query(SensorObservationRecord).order_by(SensorObservationRecord.step.desc()).first()
            if not row:
                return None
            return {c.name: getattr(row, c.name) for c in row.__table__.columns}

    def get_all_observations(self) -> List[Dict[str, Any]]:
        with self.get_session() as session:
            rows = session.query(SensorObservationRecord).order_by(SensorObservationRecord.step.asc()).all()
            return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows]

    def get_all_decisions(self) -> List[Dict[str, Any]]:
        with self.get_session() as session:
            rows = session.query(AIDecisionRecord).order_by(AIDecisionRecord.step.asc()).all()
            return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows]

    def get_all_metrics(self) -> List[Dict[str, Any]]:
        with self.get_session() as session:
            rows = session.query(SimulationMetricsRecord).order_by(SimulationMetricsRecord.step.asc()).all()
            return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows]
