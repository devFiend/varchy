"""Tests for the deterministic 100-point validation scoring engine."""

from varchy.core.models.common import RiskLevel, Severity
from varchy.core.models.planning import Task
from varchy.core.models.project import Assumption
from varchy.core.validator.engine import ValidationEngine
from varchy.providers.mock import MockAIProvider


def test_complete_blueprint_passes_validation():
    bp = MockAIProvider.generate_mock_blueprint()
    validator = ValidationEngine()
    report = validator.evaluate(bp)

    assert report.total_score >= 80.0
    assert report.passed is True
    assert len(report.critical_blockers) == 0


def test_circular_dependency_triggers_critical_blocker():
    bp = MockAIProvider.generate_mock_blueprint()
    # Introduce circular dependency: TASK-001 -> TASK-002 -> TASK-001
    bp.planning.tasks = [
        Task(
            id="TASK-001",
            phase_id="PHASE-1",
            title="Task 1",
            description="First task",
            dependencies=["TASK-002"],
        ),
        Task(
            id="TASK-002",
            phase_id="PHASE-1",
            title="Task 2",
            description="Second task",
            dependencies=["TASK-001"],
        ),
    ]

    validator = ValidationEngine()
    report = validator.evaluate(bp)

    assert report.passed is False
    assert len(report.critical_blockers) > 0
    circular_issues = [b for b in report.critical_blockers if "Circular dependency" in b.message]
    assert len(circular_issues) == 1


def test_unconfirmed_high_risk_assumption_blocks_blueprint():
    bp = MockAIProvider.generate_mock_blueprint()
    bp.assumptions.append(
        Assumption(
            id="ASM-999",
            statement="Cloud provider grants free unbounded GPU compute.",
            category="Infrastructure",
            risk_level=RiskLevel.HIGH,
            confirmed=False,
        )
    )

    validator = ValidationEngine()
    report = validator.evaluate(bp)

    assert report.passed is False
    high_risk_blockers = [b for b in report.critical_blockers if "ASM-999" == b.entity_id]
    assert len(high_risk_blockers) == 1

