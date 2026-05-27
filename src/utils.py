import json
import re
import zipfile
from pathlib import Path
from typing import Any, Dict

from models import ProjectPlan


DEFAULT_OUTPUT_DIR = Path("outputs")
DRAFT_WARNING_TEXT = (
    "This is a draft execution plan generated from incomplete requirements. "
    "Clarification is required before implementation. Assumptions must be validated. "
    "Engineering prompts are provisional. This draft is not production-ready. "
    "Engineer review is required before treating this as implementation-ready."
)


def is_draft_plan(plan: ProjectPlan) -> bool:
    return plan.status == "clarification_required" and bool(plan.phases or plan.engineering_prompts)


def save_json_output(plan: ProjectPlan, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_slugify(plan.project_name)}.plan.json"

    with path.open("w", encoding="utf-8") as file:
        json.dump(_model_to_dict(plan), file, indent=2, default=str)

    return path


def save_markdown_output(plan: ProjectPlan, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{_slugify(plan.project_name)}.plan.md"
    path.write_text(_render_markdown(plan), encoding="utf-8")
    return path


def save_prompt_pack_zip(plan: ProjectPlan, output_dir: str = "outputs") -> str:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    zip_path = output_path / f"{_slugify(plan.project_name)}.prompt_pack.zip"

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("project-plan/project_plan.md", _render_markdown(plan))
        archive.writestr("project-plan/project_plan.json", json.dumps(_model_to_dict(plan), indent=2, default=str))

        for prompt in plan.engineering_prompts:
            archive.writestr(
                f"engineering-prompts/{_slugify(prompt.target_role).replace('-', '_')}_prompt.md",
                _render_engineering_prompt_markdown(prompt),
            )

        if plan.prompt_evaluations:
            archive.writestr("prompt-evaluations/prompt_quality_report.md", _render_prompt_quality_report(plan))

        if is_draft_plan(plan):
            archive.writestr("draft-notes/assumptions.md", _render_draft_assumptions(plan))
            archive.writestr("draft-notes/clarification-questions.md", _render_draft_clarification_questions(plan))
            archive.writestr("draft-notes/draft-warning.md", _render_draft_warning())

    return str(zip_path)


def _model_to_dict(model: ProjectPlan) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        payload = model.model_dump(mode="json")
    else:
        payload = model.dict()
    payload["is_draft"] = is_draft_plan(model)
    payload["requires_clarification"] = model.status == "clarification_required"
    return payload


def _render_markdown(plan: ProjectPlan) -> str:
    lines = [
        f"# {plan.project_name}",
        "",
        "## Summary",
        plan.summary,
        "",
        f"- Domain: {plan.domain}",
        f"- Project type: {plan.project_type}",
        f"- Complexity: {plan.complexity}",
        f"- Status: {plan.status}",
        "",
    ]

    if is_draft_plan(plan):
        lines.extend(
            [
                "## Draft Plan Warning",
                "This is a draft execution plan generated from incomplete requirements.",
                "Clarification is required before implementation.",
                "Assumptions must be validated.",
                "Engineering prompts are provisional.",
                "Engineer review is required before treating this as production-ready.",
                "",
            ]
        )

    if plan.clarification_questions:
        lines.extend(["## Clarification Questions"])
        lines.extend([f"- {question}" for question in plan.clarification_questions])
        lines.append("")

    if plan.warnings:
        lines.extend(["## Warnings"])
        lines.extend([f"- {warning}" for warning in plan.warnings])
        lines.append("")

    if plan.phases:
        lines.append("## Phases")
        for phase in plan.phases:
            lines.extend([f"### {phase.id}: {phase.name}", phase.objective, "", f"Estimated duration: {phase.estimated_duration}", "", "Tasks:"])
            for task in phase.tasks:
                dependency_text = f" Dependencies: {', '.join(task.dependencies)}." if task.dependencies else ""
                lines.append(f"- {task.id}: {task.title} - {task.description}{dependency_text}")
            lines.extend(["", "Deliverables:"])
            lines.extend([f"- {deliverable}" for deliverable in phase.deliverables])
            lines.append("")

    if plan.milestones:
        lines.append("## Milestones")
        lines.extend([f"- {milestone.id}: {milestone.name} ({milestone.target_phase_id})" for milestone in plan.milestones])
        lines.append("")

    if plan.risks:
        lines.append("## Risks")
        lines.extend([f"- {risk.id}: {risk.description} Mitigation: {risk.mitigation}" for risk in plan.risks])
        lines.append("")

    if plan.recommendations:
        lines.append("## Recommendations")
        lines.extend([f"- {item.category}: {item.recommendation}" for item in plan.recommendations])
        lines.append("")

    if plan.assumptions:
        lines.append("## Assumptions")
        lines.extend([f"- {assumption}" for assumption in plan.assumptions])
        lines.append("")

    if plan.engineering_prompts:
        lines.append("## Engineering Prompt Pack")
        for prompt in plan.engineering_prompts:
            lines.extend(
                [
                    f"### {prompt.title}",
                    "",
                    f"**Target Role:** {prompt.target_role}  ",
                    f"**Target Tool:** {prompt.target_tool}  ",
                    f"**Purpose:** {prompt.purpose}",
                    "",
                    "**Related Phases:**",
                ]
            )
            lines.extend(_render_list(prompt.related_phases, "No related phases provided."))
            lines.extend(["", "**Constraints:**"])
            lines.extend(_render_list(prompt.constraints, "No constraints provided."))
            lines.extend(["", "**Acceptance Criteria:**"])
            lines.extend(_render_list(prompt.acceptance_criteria, "No acceptance criteria provided."))
            lines.extend(["", "**Prompt:**", "```text", prompt.prompt_text, "```", ""])

    if plan.prompt_evaluations:
        lines.append("## Prompt Quality Evaluations")
        for evaluation in plan.prompt_evaluations:
            lines.extend(
                [
                    f"### Evaluation for {evaluation.prompt_id}",
                    "",
                    f"- Score: {evaluation.score}/100",
                    f"- Ready to use: {evaluation.ready_to_use}",
                    "",
                    "**Strengths:**",
                ]
            )
            lines.extend(_render_list(evaluation.strengths, "No strengths recorded."))
            lines.extend(["", "**Issues:**"])
            lines.extend(_render_list(evaluation.issues, "No issues recorded."))
            lines.extend(["", "**Improvement Suggestions:**"])
            lines.extend(_render_list(evaluation.improvement_suggestions, "No improvement suggestions recorded."))
            lines.append("")

    return "\n".join(lines)


def _render_list(items: list[str], empty_text: str) -> list[str]:
    values = [item for item in items if item]
    if not values:
        return [f"- {empty_text}"]
    return [f"- {item}" for item in values]


def _render_engineering_prompt_markdown(prompt) -> str:
    lines = [
        f"# {prompt.title}",
        "",
        f"**Target Role:** {prompt.target_role}  ",
        f"**Target Tool:** {prompt.target_tool}  ",
        f"**Purpose:** {prompt.purpose}",
        "",
        "## Related Phases",
        *_render_list(prompt.related_phases, "No related phases provided."),
        "",
        "## Constraints",
        *_render_list(prompt.constraints, "No constraints provided."),
        "",
        "## Acceptance Criteria",
        *_render_list(prompt.acceptance_criteria, "No acceptance criteria provided."),
        "",
        "## Prompt",
        "```text",
        prompt.prompt_text,
        "```",
        "",
    ]
    return "\n".join(lines)


def _render_prompt_quality_report(plan: ProjectPlan) -> str:
    lines = ["# Prompt Quality Report", ""]
    for evaluation in plan.prompt_evaluations:
        lines.extend(
            [
                f"## {evaluation.prompt_id}",
                "",
                f"- Score: {evaluation.score}/100",
                f"- Ready to use: {evaluation.ready_to_use}",
                "",
                "### Strengths",
                *_render_list(evaluation.strengths, "No strengths recorded."),
                "",
                "### Issues",
                *_render_list(evaluation.issues, "No issues recorded."),
                "",
                "### Improvement Suggestions",
                *_render_list(evaluation.improvement_suggestions, "No improvement suggestions recorded."),
                "",
            ]
        )
    return "\n".join(lines)


def _render_draft_assumptions(plan: ProjectPlan) -> str:
    lines = ["# Draft Assumptions", ""]
    lines.extend(_render_list(plan.assumptions, "No assumptions recorded."))
    lines.append("")
    return "\n".join(lines)


def _render_draft_clarification_questions(plan: ProjectPlan) -> str:
    lines = ["# Draft Clarification Questions", ""]
    lines.extend(_render_list(plan.clarification_questions, "No clarification questions recorded."))
    lines.append("")
    return "\n".join(lines)


def _render_draft_warning() -> str:
    return "\n".join(
        [
            "# Draft Plan Warning",
            "",
            DRAFT_WARNING_TEXT,
            "",
            "Do not treat this plan or its engineering prompts as production-ready until requirements are clarified, assumptions are validated, and an engineer reviews the implementation approach.",
            "",
        ]
    )


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "project-plan"
