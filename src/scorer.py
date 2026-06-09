from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Set

from models import ProjectPlan


RUBRIC_DIMENSIONS = [
    "project_understanding",
    "completeness",
    "task_quality",
    "milestone_usefulness",
    "dependency_correctness",
    "timeline_realism",
    "risk_awareness",
    "recommendation_quality",
    "hallucination_avoidance",
    "output_validity",
]


@dataclass(frozen=True)
class ScoreResult:
    dimension: str
    score: int
    evidence: str


def clamp_score(value: int) -> int:
    return max(1, min(5, value))


def score_project_understanding(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    expected_domain = _expected_domain(str(scenario.get("category", "")), str(scenario.get("input", "")))
    score = 3
    evidence = f"Plan domain is {plan.domain}."

    if plan.status == "clarification_required":
        score = 4 if expected_domain == "unknown" else 3
        evidence = "Plan asks for clarification instead of over-specifying unclear input."
    elif expected_domain != "unknown" and plan.domain == expected_domain:
        score = 4
        evidence = f"Plan correctly identifies the {expected_domain} domain."
    elif expected_domain == "unknown":
        score = 3
    else:
        score = 2
        evidence = f"Expected {expected_domain}, but plan classified {plan.domain}."

    focus_text = " ".join(_as_string_list(scenario.get("evaluation_focus", []))).lower()
    plan_text = _plan_text(plan)
    if expected_domain in plan_text and any(token in plan_text for token in _keywords(str(scenario.get("input", "")))):
        score += 1
        evidence += " Scenario-specific terms appear in the plan."
    if "conflict" in focus_text and (plan.warnings or plan.clarification_questions):
        score += 1
        evidence += " Conflicts or uncertainty are surfaced."

    return ScoreResult("project_understanding", clamp_score(score), evidence)


def score_completeness(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    if plan.status == "clarification_required":
        score = 4 if plan.clarification_questions else 2
        return ScoreResult("completeness", score, "Clarification plan includes questions instead of execution sections.")

    present = sum(
        bool(value)
        for value in [
            plan.phases,
            _all_tasks(plan),
            plan.milestones,
            plan.dependencies,
            plan.risks,
            plan.recommendations,
            plan.assumptions or plan.warnings,
        ]
    )
    score = 1 + min(4, present // 2)
    if present >= 6:
        score = 4
    if present == 7 and len(plan.phases) >= 4:
        score = 5

    return ScoreResult("completeness", clamp_score(score), f"{present} major plan sections contain content.")


def score_task_quality(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    tasks = _all_tasks(plan)
    if not tasks:
        score = 4 if plan.status == "clarification_required" else 1
        return ScoreResult("task_quality", score, "No execution tasks are expected only for clarification plans.")

    actionable = [
        task
        for task in tasks
        if task.title and task.description and task.owner_role and task.estimated_effort and task.acceptance_criteria
    ]
    ratio = len(actionable) / len(tasks)
    score = 2 + round(ratio * 2)
    if len(tasks) >= 6 and ratio == 1:
        score = 5

    return ScoreResult("task_quality", clamp_score(score), f"{len(actionable)} of {len(tasks)} tasks include core execution details.")


def score_milestone_usefulness(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    if plan.status == "clarification_required":
        return ScoreResult("milestone_usefulness", 4, "Milestones are deferred because clarification is required.")
    if not plan.milestones:
        return ScoreResult("milestone_usefulness", 1, "No milestones are present.")

    phase_ids = {phase.id for phase in plan.phases}
    valid = [milestone for milestone in plan.milestones if milestone.target_phase_id in phase_ids]
    score = 3 if valid else 2
    if len(valid) == len(plan.phases) and len(valid) == len(plan.milestones):
        score = 4
    if any("review" in milestone.description.lower() or "complete" in milestone.description.lower() for milestone in valid):
        score += 1

    return ScoreResult("milestone_usefulness", clamp_score(score), f"{len(valid)} milestones map to valid phases.")


def score_dependency_correctness(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    if plan.status == "clarification_required":
        return ScoreResult("dependency_correctness", 4, "Dependencies are deferred because clarification is required.")

    task_ids = {task.id for task in _all_tasks(plan)}
    task_dependency_ids = [dependency for task in _all_tasks(plan) for dependency in task.dependencies]
    explicit_dependency_pairs = [(item.source_task_id, item.target_task_id) for item in plan.dependencies]
    invalid = [
        pair
        for pair in explicit_dependency_pairs
        if pair[0] not in task_ids or pair[1] not in task_ids or pair[0] == pair[1]
    ]

    if invalid:
        score = 1
        evidence = f"{len(invalid)} dependencies reference invalid task ids."
    elif not task_dependency_ids and not plan.dependencies:
        score = 2
        evidence = "No dependencies are present."
    elif len(explicit_dependency_pairs) >= len(task_dependency_ids):
        score = 5
        evidence = "Task dependencies are represented in the explicit dependency list."
    else:
        score = 3
        evidence = "Dependencies exist but are not fully represented as explicit relationships."

    return ScoreResult("dependency_correctness", score, evidence)


def score_timeline_realism(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    input_text = str(scenario.get("input", "")).lower()
    plan_text = _plan_text(plan)
    has_aggressive_timeline = any(term in input_text for term in ["one week", "1 week", "two weeks", "2 weeks"])
    has_scope_warning = bool(plan.warnings) or any("scope" in risk.description.lower() for risk in plan.risks)

    if plan.status == "clarification_required":
        score = 4
        evidence = "Timeline is deferred until missing information is clarified."
    elif has_aggressive_timeline and has_scope_warning:
        score = 5
        evidence = "Aggressive timeline is paired with warnings or scope risk."
    elif has_aggressive_timeline:
        score = 2
        evidence = "Aggressive timeline is not clearly challenged."
    elif any(term in plan_text for term in ["week", "weeks", "semester", "month"]):
        score = 4
        evidence = "Plan includes phase-level duration estimates."
    else:
        score = 2
        evidence = "Timeline detail is sparse."

    return ScoreResult("timeline_realism", score, evidence)


def score_risk_awareness(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    risk_text = " ".join([risk.description + " " + risk.mitigation for risk in plan.risks]).lower()
    focus_text = " ".join(_as_string_list(scenario.get("evaluation_focus", []))).lower()
    domain_terms = ["privacy", "compliance", "hipaa", "data quality", "scope", "hallucination", "validation"]
    hits = sum(1 for term in domain_terms if term in risk_text)

    if not plan.risks and plan.status != "clarification_required":
        score = 1
    elif plan.status == "clarification_required":
        score = 4
    else:
        score = 3 + min(2, hits)
    if "privacy" in focus_text and "privacy" not in risk_text and "compliance" not in risk_text:
        score -= 1

    return ScoreResult("risk_awareness", clamp_score(score), f"{len(plan.risks)} risks are present; {hits} domain risk terms found.")


def score_recommendation_quality(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    if not plan.recommendations and plan.status != "clarification_required":
        return ScoreResult("recommendation_quality", 1, "No recommendations are present.")
    if plan.status == "clarification_required":
        return ScoreResult("recommendation_quality", 4, "Clarification questions are the appropriate next recommendation.")

    useful = [item for item in plan.recommendations if item.recommendation and item.rationale]
    score = 3 if useful else 2
    if any(item.category.lower() in {"scope", "planning", "delivery"} for item in useful):
        score += 1
    if plan.warnings and any("scope" in item.category.lower() for item in useful):
        score += 1

    return ScoreResult("recommendation_quality", clamp_score(score), f"{len(useful)} recommendations include rationale.")


def score_hallucination_avoidance(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    input_text = str(scenario.get("input", "")).lower()
    focus_text = " ".join(_as_string_list(scenario.get("evaluation_focus", []))).lower()
    is_vague_or_conflicted = "vague" in str(scenario.get("category", "")).lower() or "conflict" in focus_text

    if is_vague_or_conflicted and plan.status == "clarification_required":
        score = 5
        evidence = "Plan asks for clarification on vague or conflicting input."
    elif is_vague_or_conflicted and (plan.warnings or plan.assumptions):
        score = 4
        evidence = "Plan labels uncertainty through warnings or assumptions."
    elif is_vague_or_conflicted:
        score = 2
        evidence = "Plan may over-specify uncertain input."
    else:
        score = 4 if plan.assumptions else 3
        evidence = "Plan includes assumptions or keeps claims generic."

    unsafe_terms = ["guaranteed", "perfect", "fully compliant", "zero risk"]
    if any(term in _plan_text(plan) for term in unsafe_terms) and not any(term in input_text for term in unsafe_terms):
        score -= 2
        evidence += " Unsupported certainty language appears."

    return ScoreResult("hallucination_avoidance", clamp_score(score), evidence)


def score_output_validity(plan: ProjectPlan, scenario: Dict[str, object]) -> ScoreResult:
    task_ids = {task.id for task in _all_tasks(plan)}
    phase_ids = {phase.id for phase in plan.phases}
    invalid_milestones = [milestone for milestone in plan.milestones if milestone.target_phase_id not in phase_ids]
    invalid_dependencies = [
        dependency
        for dependency in plan.dependencies
        if dependency.source_task_id not in task_ids or dependency.target_task_id not in task_ids
    ]

    if invalid_milestones or invalid_dependencies:
        score = 2
        evidence = f"{len(invalid_milestones)} invalid milestones and {len(invalid_dependencies)} invalid dependencies found."
    elif plan.status == "clarification_required" and plan.clarification_questions:
        score = 5
        evidence = "Clarification plan is schema-valid and internally consistent."
    elif plan.phases and task_ids:
        score = 5
        evidence = "Generated plan is schema-valid and internally consistent."
    else:
        score = 3
        evidence = "Plan is schema-valid but sparse."

    return ScoreResult("output_validity", score, evidence)


def average_score(scores: Sequence[ScoreResult]) -> float:
    if not scores:
        return 0.0
    return round(sum(item.score for item in scores) / len(scores), 2)


def scores_to_dict(scores: Sequence[ScoreResult]) -> Dict[str, Dict[str, object]]:
    return {item.dimension: {"score": item.score, "evidence": item.evidence} for item in scores}


def _all_tasks(plan: ProjectPlan):
    return [task for phase in plan.phases for task in phase.tasks]


def _plan_text(plan: ProjectPlan) -> str:
    parts: List[str] = [
        plan.project_name,
        plan.description,
        plan.domain,
        plan.project_type,
        plan.summary,
        " ".join(plan.assumptions),
        " ".join(plan.warnings),
        " ".join(plan.clarification_questions),
    ]
    for phase in plan.phases:
        parts.extend([phase.name, phase.objective, phase.estimated_duration, " ".join(phase.deliverables)])
        for task in phase.tasks:
            parts.extend([task.title, task.description, task.owner_role, task.estimated_effort])
    for risk in plan.risks:
        parts.extend([risk.description, risk.mitigation])
    for recommendation in plan.recommendations:
        parts.extend([recommendation.category, recommendation.recommendation, recommendation.rationale])
    return " ".join(parts).lower()


def _expected_domain(category: str, input_text: str) -> str:
    text = f"{category} {input_text}".lower()
    if "healthcare" in text or "clinic" in text or "patient" in text or "hipaa" in text:
        return "healthcare"
    if "bi/" in text or "dashboard" in text or "power bi" in text or "data" in text:
        return "analytics"
    if "business" in text or "go-to-market" in text or "campaign" in text:
        return "business"
    if "academic" in text or "independent study" in text or "research" in text:
        return "academic"
    if "software" in text or "app" in text or "rag" in text or "assistant" in text:
        return "software"
    if "vague" in text:
        return "unknown"
    return "unknown"


def _keywords(text: str) -> Set[str]:
    words = {word.strip(".,:;!?()[]").lower() for word in text.split()}
    return {word for word in words if len(word) > 5}


def _as_string_list(value: object) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    return []
