import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import EngineeringPrompt, Phase, ProjectPlan, Task
from planner import generate_project_plan
from prompt_generator import generate_engineering_prompts


def test_generate_engineering_prompts_returns_six_schema_objects():
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    prompts = generate_engineering_prompts(plan)

    assert len(prompts) == 6
    assert all(isinstance(prompt, EngineeringPrompt) for prompt in prompts)


def test_generate_engineering_prompts_includes_all_supported_roles():
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    prompts = generate_engineering_prompts(plan)
    roles = {prompt.target_role for prompt in prompts}

    assert roles == {
        "Frontend Engineer",
        "Backend Engineer",
        "Database Engineer",
        "QA / Testing Engineer",
        "DevOps Engineer",
        "Security Reviewer",
    }


def test_each_prompt_has_required_framing_and_sections():
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    prompts = generate_engineering_prompts(plan)

    for prompt in prompts:
        assert prompt.prompt_text.startswith("You are a senior")
        assert "## Project Context" in prompt.prompt_text
        assert "## Acceptance Criteria" in prompt.prompt_text
        assert "## Do Not Do" in prompt.prompt_text
        assert "The planner itself must not build, deploy, or modify software." in prompt.prompt_text


def test_prompt_related_phases_are_populated_from_plan_phases():
    plan = generate_project_plan("Create a Power BI dashboard for sales managers.", use_ai=False)
    phase_ids = [phase.id for phase in plan.phases]

    prompts = generate_engineering_prompts(plan)

    assert phase_ids
    assert all(prompt.related_phases == phase_ids for prompt in prompts)


def test_prompt_generator_does_not_modify_plan():
    plan = _base_plan_without_prompt_pack()

    prompts = generate_engineering_prompts(plan)

    assert prompts
    assert plan.engineering_prompts == []
    assert plan.prompt_evaluations == []


def _base_plan_without_prompt_pack() -> ProjectPlan:
    return ProjectPlan(
        project_name="Manual Plan",
        description="Build a hospital appointment scheduling system for patients.",
        domain="healthcare",
        project_type="healthcare workflow improvement",
        complexity="medium",
        status="plan_generated",
        summary="A manual plan for prompt generator isolation tests.",
        phases=[
            Phase(
                id="P1",
                name="Implementation",
                objective="Build the planned workflow.",
                estimated_duration="1 week",
                tasks=[
                    Task(
                        id="T1",
                        title="Build workflow",
                        description="Implement the core scheduling workflow.",
                        owner_role="Backend Engineer",
                        estimated_effort="2 days",
                        acceptance_criteria=["Workflow is reviewed and tested."],
                    )
                ],
                deliverables=["working workflow"],
            )
        ],
    )
