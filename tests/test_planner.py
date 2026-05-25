import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import generate_project_plan


def test_generate_software_project_plan():
    plan = generate_project_plan("Build an expense tracker app for college students to track spending and budgets.")

    assert plan.status == "plan_generated"
    assert plan.domain == "software"
    assert len(plan.phases) >= 4
    assert any("Architecture" in phase.name for phase in plan.phases)
    assert plan.dependencies


def test_generate_analytics_project_plan():
    plan = generate_project_plan("Create a Power BI dashboard for sales managers showing revenue and regional trends.")

    assert plan.status == "plan_generated"
    assert plan.domain == "analytics"
    assert any("KPI" in phase.name for phase in plan.phases)
    assert any("Data quality" in risk.description for risk in plan.risks)


def test_vague_input_returns_clarification_plan():
    plan = generate_project_plan("I want to build something for students.")

    assert plan.status == "clarification_required"
    assert plan.domain == "unknown"
    assert plan.phases == []
    assert len(plan.clarification_questions) >= 4


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        generate_project_plan("")


def test_unrealistic_scope_adds_warning_and_scope_recommendation():
    plan = generate_project_plan(
        "Build a full e-commerce marketplace with payments, inventory, seller dashboards, mobile apps, and analytics in one week."
    )

    assert plan.status == "plan_generated"
    assert plan.complexity == "high"
    assert plan.warnings
    assert any(recommendation.category == "Scope" for recommendation in plan.recommendations)
