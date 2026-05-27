import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from models import ProjectPlan


DEFAULT_OUTPUT_DIR = Path("outputs")
PLANNER_VERSION = "0.1.0"
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
    manifest = _build_manifest(plan)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("project-summary.md", _render_project_summary(plan, manifest))
        archive.writestr("manifest.json", json.dumps(manifest, indent=2, default=str))
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


def _build_manifest(plan: ProjectPlan) -> Dict[str, Any]:
    task_count = sum(len(phase.tasks) for phase in plan.phases)
    return {
        "planner_version": PLANNER_VERSION,
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "project": {
            "title": plan.project_name,
            "domain": plan.domain,
            "project_type": plan.project_type,
            "complexity": plan.complexity,
            "status": plan.status,
            "is_draft": is_draft_plan(plan),
            "requires_clarification": plan.status == "clarification_required",
        },
        "metrics": {
            "phase_count": len(plan.phases),
            "task_count": task_count,
            "engineering_prompt_count": len(plan.engineering_prompts),
            "prompt_evaluation_count": len(plan.prompt_evaluations),
            "assumption_count": len(plan.assumptions),
            "risk_count": len(plan.risks),
            "recommendation_count": len(plan.recommendations),
            "clarification_question_count": len(plan.clarification_questions),
        },
        "warnings": plan.warnings,
        "clarification_questions": plan.clarification_questions,
        "generated_artifacts": _build_artifact_list(plan),
    }


def _build_artifact_list(plan: ProjectPlan) -> list[str]:
    artifacts = [
        "project-summary.md",
        "manifest.json",
        "project-plan/project_plan.md",
        "project-plan/project_plan.json",
    ]
    artifacts.extend(
        f"engineering-prompts/{_slugify(prompt.target_role).replace('-', '_')}_prompt.md"
        for prompt in plan.engineering_prompts
    )
    if plan.prompt_evaluations:
        artifacts.append("prompt-evaluations/prompt_quality_report.md")
    if is_draft_plan(plan):
        artifacts.extend(
            [
                "draft-notes/assumptions.md",
                "draft-notes/clarification-questions.md",
                "draft-notes/draft-warning.md",
            ]
        )
    return artifacts


def _render_project_summary(plan: ProjectPlan, manifest: Dict[str, Any]) -> str:
    project = manifest["project"]
    metrics = manifest["metrics"]
    lines = [
        f"# {plan.project_name} Export Summary",
        "",
        "## Overview",
        f"- Project title: {project['title']}",
        f"- Detected domain: {project['domain']}",
        f"- Project type: {project['project_type']}",
        f"- Complexity: {project['complexity']}",
        f"- Planner version: {manifest['planner_version']}",
        f"- Export timestamp: {manifest['export_timestamp']}",
        "",
        "## Status",
        f"- Planner status: {project['status']}",
        f"- Draft status: {project['is_draft']}",
        f"- Clarification required: {project['requires_clarification']}",
    ]

    if project["is_draft"]:
        lines.extend(
            [
                "",
                "## DRAFT PLAN — REQUIREMENTS INCOMPLETE",
                "Assumptions were used to create this draft execution plan.",
                "Clarification is required before implementation.",
                "Engineering review is required before treating this as production-ready.",
            ]
        )
    elif not project["requires_clarification"]:
        lines.extend(["", "This plan is implementation-ready based on the available requirements."])

    lines.extend(
        [
            "",
            "## Planning Metrics",
            f"- Number of phases: {metrics['phase_count']}",
            f"- Number of tasks: {metrics['task_count']}",
            f"- Number of engineering prompts: {metrics['engineering_prompt_count']}",
            f"- Number of prompt evaluations: {metrics['prompt_evaluation_count']}",
            f"- Number of assumptions: {metrics['assumption_count']}",
            f"- Number of risks: {metrics['risk_count']}",
            f"- Number of recommendations: {metrics['recommendation_count']}",
            f"- Number of clarification questions: {metrics['clarification_question_count']}",
            "",
            "## Generated Artifacts",
            *_render_list(manifest["generated_artifacts"], "No generated artifacts recorded."),
        ]
    )

    if plan.warnings:
        lines.extend(["", "## Warnings", *_render_list(plan.warnings, "No warnings recorded.")])

    if plan.clarification_questions:
        lines.extend(
            [
                "",
                "## Clarification Questions",
                *_render_list(plan.clarification_questions, "No clarification questions recorded."),
            ]
        )

    lines.append("")
    return "\n".join(lines)


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
