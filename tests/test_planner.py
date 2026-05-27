import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import generate_project_plan


def test_generate_software_project_plan():
    plan = generate_project_plan("Build an expense tracker app for college students to track spending and budgets.", use_ai=False)

    assert plan.status == "plan_generated"
    assert plan.domain == "software"
    assert len(plan.phases) >= 4
    assert any("Architecture" in phase.name for phase in plan.phases)
    assert plan.dependencies
    assert len(plan.engineering_prompts) == 6
    assert len(plan.prompt_evaluations) == 6


def test_prompt_evaluations_reference_existing_prompt_ids():
    plan = generate_project_plan("Build an expense tracker app for college students to track spending and budgets.", use_ai=False)

    prompt_ids = {prompt.id for prompt in plan.engineering_prompts}
    evaluation_prompt_ids = {evaluation.prompt_id for evaluation in plan.prompt_evaluations}

    assert evaluation_prompt_ids == prompt_ids


def test_generate_analytics_project_plan():
    plan = generate_project_plan("Create a Power BI dashboard for sales managers showing revenue and regional trends.", use_ai=False)

    assert plan.status == "plan_generated"
    assert plan.domain == "analytics"
    assert any("KPI" in phase.name for phase in plan.phases)
    assert any("Data quality" in risk.description for risk in plan.risks)


def test_vague_input_returns_clarification_plan():
    plan = generate_project_plan("I want to build something for students.", use_ai=False)

    assert plan.status == "clarification_required"
    assert plan.domain == "unknown"
    assert plan.phases == []
    assert len(plan.clarification_questions) >= 4
    assert plan.engineering_prompts == []
    assert plan.prompt_evaluations == []


def test_short_meaningful_request_generates_draft_plan_and_prompts():
    plan = generate_project_plan("Build a racing game", use_ai=False)

    assert plan.status == "clarification_required"
    assert plan.phases
    assert plan.clarification_questions
    assert any("draft execution plan" in warning for warning in plan.warnings)
    assert len(plan.engineering_prompts) == 6
    assert len(plan.prompt_evaluations) == 6
    assert "requirements are incomplete" in plan.engineering_prompts[0].prompt_text.lower()
    assert "production-ready" in plan.engineering_prompts[0].prompt_text.lower()


def test_meaningful_general_project_requests_generate_prompt_packs():
    descriptions = [
        "Build a portfolio website",
        "Build a restaurant ordering app",
        "Build a logistics tracking system",
        "Build a food delivery analytics dashboard",
    ]

    for description in descriptions:
        plan = generate_project_plan(description, use_ai=False)

        assert plan.phases, description
        assert len(plan.engineering_prompts) == 6, description
        assert len(plan.prompt_evaluations) == 6, description


def test_meaningless_inputs_do_not_generate_prompts():
    for description in ["hi", "test", "app", "build something"]:
        try:
            plan = generate_project_plan(description, use_ai=False)
        except ValueError:
            continue

        assert plan.status == "clarification_required"
        assert plan.phases == []
        assert plan.engineering_prompts == []
        assert plan.prompt_evaluations == []


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        generate_project_plan("")


def test_unrealistic_scope_adds_warning_and_scope_recommendation():
    plan = generate_project_plan(
        "Build a full e-commerce marketplace with payments, inventory, seller dashboards, mobile apps, and analytics in one week.",
        use_ai=False,
    )

    assert plan.status == "plan_generated"
    assert plan.complexity == "high"
    assert plan.warnings
    assert any(recommendation.category == "Scope" for recommendation in plan.recommendations)
