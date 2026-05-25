import json
import re
from pathlib import Path
from typing import Any, Dict

from models import ProjectPlan


DEFAULT_OUTPUT_DIR = Path("outputs")


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


def _model_to_dict(model: ProjectPlan) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json")
    return model.dict()


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

    return "\n".join(lines)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "project-plan"
