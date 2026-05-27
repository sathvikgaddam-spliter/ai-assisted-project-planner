import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models import EngineeringPrompt, Phase, ProjectPlan, PromptEvaluation, Task
from planner import generate_project_plan
from prompt_evaluator import evaluate_engineering_prompt, evaluate_engineering_prompts, validate_prompt_quality
from prompt_generator import generate_engineering_prompts


def test_evaluate_engineering_prompt_returns_prompt_evaluation():
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)
    prompt = generate_engineering_prompts(plan)[0]

    evaluation = evaluate_engineering_prompt(prompt)

    assert isinstance(evaluation, PromptEvaluation)
    assert evaluation.prompt_id == prompt.id


def test_evaluation_score_is_between_zero_and_100():
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)
    prompt = generate_engineering_prompts(plan)[0]

    evaluation = evaluate_engineering_prompt(prompt)

    assert 0 <= evaluation.score <= 100
    assert 0 <= evaluation.quality_score <= 100


def test_strong_generated_prompts_are_ready_to_use():
    plan = generate_project_plan("Build a hospital appointment scheduling system for patients.", use_ai=False)

    evaluations = evaluate_engineering_prompts(generate_engineering_prompts(plan))

    assert evaluations
    assert all(evaluation.ready_to_use for evaluation in evaluations)
    assert all(evaluation.score >= 75 for evaluation in evaluations)
    assert all(evaluation.quality_score >= 75 for evaluation in evaluations)
    assert all(not evaluation.missing_sections for evaluation in evaluations)


def test_weak_prompt_receives_lower_score():
    weak_prompt = _weak_prompt()

    evaluation = evaluate_engineering_prompt(weak_prompt)

    assert evaluation.score < 75
    assert evaluation.quality_score < 75
    assert evaluation.ready_to_use is False


def test_missing_sections_create_issues_and_suggestions():
    weak_prompt = _weak_prompt()

    evaluation = evaluate_engineering_prompt(weak_prompt)
    issue_text = " ".join(evaluation.issues)
    suggestion_text = " ".join(evaluation.improvement_suggestions)

    assert "missing required sections" in issue_text
    assert "Acceptance Criteria" in issue_text
    assert "Add" in suggestion_text


def test_validate_prompt_quality_identifies_missing_sections():
    result = validate_prompt_quality(_weak_prompt())

    assert result["quality_score"] < 75
    assert "Acceptance Criteria" in result["missing_sections"]
    assert "Constraints" in result["missing_sections"]
    assert result["warnings"]
    assert any("Engineer review recommended" in note for note in result["review_notes"])


def test_prompt_evaluation_includes_quality_gate_metadata():
    evaluation = evaluate_engineering_prompt(_weak_prompt())

    assert evaluation.missing_sections
    assert evaluation.warnings
    assert evaluation.review_notes
    assert "Acceptance Criteria" in evaluation.missing_sections


def test_draft_plan_prompts_include_stronger_review_warnings():
    plan = generate_project_plan("Build a racing game", use_ai=False)

    evaluations = evaluate_engineering_prompts(plan.engineering_prompts)
    warning_text = " ".join(warning for evaluation in evaluations for warning in evaluation.warnings)
    review_text = " ".join(note for evaluation in evaluations for note in evaluation.review_notes)

    assert "requirements are incomplete" in warning_text.lower()
    assert "validate assumptions" in review_text.lower()


def test_batch_evaluator_returns_one_evaluation_per_prompt():
    plan = generate_project_plan("Create a Power BI dashboard for sales managers.", use_ai=False)
    prompts = generate_engineering_prompts(plan)

    evaluations = evaluate_engineering_prompts(prompts)

    assert len(evaluations) == len(prompts)
    assert [evaluation.prompt_id for evaluation in evaluations] == [prompt.id for prompt in prompts]


def test_prompt_evaluator_does_not_modify_plan():
    plan = _base_plan_without_prompt_pack()
    prompts = generate_engineering_prompts(plan)

    evaluations = evaluate_engineering_prompts(prompts)

    assert evaluations
    assert plan.engineering_prompts == []
    assert plan.prompt_evaluations == []


def _weak_prompt() -> EngineeringPrompt:
    return EngineeringPrompt(
        id="EP-WEAK",
        title="Weak prompt",
        target_role="Backend Engineer",
        target_tool="Codex",
        purpose="Build backend work.",
        related_phases=[],
        prompt_text="Build the backend.",
        acceptance_criteria=[],
        constraints=[],
    )


def _base_plan_without_prompt_pack() -> ProjectPlan:
    return ProjectPlan(
        project_name="Manual Plan",
        description="Build an expense tracker app for college students.",
        domain="software",
        project_type="software application",
        complexity="medium",
        status="plan_generated",
        summary="A manual plan for prompt evaluator isolation tests.",
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
                        description="Implement the core expense tracking workflow.",
                        owner_role="Backend Engineer",
                        estimated_effort="2 days",
                        acceptance_criteria=["Workflow is reviewed and tested."],
                    )
                ],
                deliverables=["working workflow"],
            )
        ],
    )
