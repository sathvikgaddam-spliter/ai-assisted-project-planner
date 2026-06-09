import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import EngineeringPrompt, ProjectPlan, PromptEvaluation


def test_project_plan_defaults_include_empty_prompt_pack_fields():
    plan = ProjectPlan(
        project_name="Test Plan",
        description="Build a test planning tool.",
        domain="software",
        project_type="software application",
        complexity="medium",
        status="plan_generated",
        summary="A test project plan.",
    )

    assert plan.engineering_prompts == []
    assert plan.prompt_evaluations == []


def test_engineering_prompt_schema_accepts_role_oriented_prompt():
    prompt = EngineeringPrompt(
        id="EP1",
        title="Backend implementation prompt",
        target_role="Backend Engineer",
        target_tool="Codex",
        purpose="Guide backend implementation for the validated project plan.",
        related_phases=["P2", "P3"],
        prompt_text="You are a senior backend engineer responsible for building the API layer.",
        acceptance_criteria=["API endpoints are implemented and tested."],
        constraints=["Do not deploy production infrastructure."],
    )

    assert prompt.target_tool == "Codex"
    assert prompt.related_phases == ["P2", "P3"]


def test_prompt_evaluation_score_is_bounded_to_100():
    evaluation = PromptEvaluation(
        prompt_id="EP1",
        score=92,
        ready_to_use=True,
        strengths=["Clear role and scope."],
        issues=[],
        improvement_suggestions=[],
    )

    assert evaluation.score == 92

    with pytest.raises(ValidationError):
        PromptEvaluation(
            prompt_id="EP1",
            score=101,
            ready_to_use=False,
        )


def test_new_prompt_models_forbid_extra_fields():
    with pytest.raises(ValidationError):
        EngineeringPrompt(
            id="EP1",
            title="Frontend prompt",
            target_role="Frontend Engineer",
            target_tool="Cursor",
            purpose="Guide frontend implementation.",
            prompt_text="You are a senior frontend engineer responsible for implementing the UI.",
            unsupported_field=True,
        )


def test_project_plan_accepts_nested_prompt_pack_data():
    plan = ProjectPlan(
        project_name="Prompt Pack Plan",
        description="Build a planner.",
        domain="software",
        project_type="software application",
        complexity="medium",
        status="plan_generated",
        summary="A plan with prompt pack schema data.",
        engineering_prompts=[
            EngineeringPrompt(
                id="EP1",
                title="QA prompt",
                target_role="QA / Testing Engineer",
                target_tool="Claude Code",
                purpose="Guide test planning.",
                related_phases=["P4"],
                prompt_text="You are a senior QA engineer responsible for validating the release.",
                acceptance_criteria=["Critical workflows have test coverage."],
                constraints=["Do not change product requirements."],
            )
        ],
        prompt_evaluations=[
            PromptEvaluation(
                prompt_id="EP1",
                score=88,
                ready_to_use=True,
                strengths=["Specific acceptance criteria."],
                issues=[],
                improvement_suggestions=["Add more edge cases later."],
            )
        ],
    )

    assert plan.engineering_prompts[0].target_role == "QA / Testing Engineer"
    assert plan.prompt_evaluations[0].prompt_id == "EP1"
