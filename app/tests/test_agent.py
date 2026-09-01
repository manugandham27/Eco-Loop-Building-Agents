"""
EcoLoop AI - Agentic Loop Unit Test Suite
"""

import pytest
from app.config.settings import Settings
from app.controllers.closed_loop import ClosedLoopController


def test_closed_loop_execution(tmp_path):
    db_file = str(tmp_path / "test_loop.db")
    settings = Settings()
    settings.db_path = db_file
    
    loop_controller = ClosedLoopController(settings)
    results = loop_controller.run_loop(steps=2)
    
    assert len(results) == 2
    assert results[0]["step"] == 1
    assert "observation" in results[0]
    assert "decision" in results[0]
    assert "metrics" in results[0]
    assert "reasoning" in results[0]["decision"]
