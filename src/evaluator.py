from __future__ import annotations

from typing import Dict, List

from models import ProjectPlan
from scorer import (
    ScoreResult,
    average_score,
    score_completeness,
    score_dependency_correctness,
    score_hallucination_avoidance,
    score_milestone_usefulness,
    score_output_validity,
    score_project_understanding,
    score_recommendation_quality,
    score_risk_awareness,
    score_task_quality,
    score_timeline_realism,
    scores_to_dict,
)


SCORERS = [
    score_project_understanding,
    score_completeness,
    score_task_quality,
    score_milestone_usefulness,
    score_dependency_correctness,
    score_timeline_realism,
    score_risk_awareness,
    score_recommendation_quality,
    score_hallucination_avoidance,
    score_output_validity,
]


def evaluate_project_plan(plan: ProjectPlan, scenario: Dict[str, object]) -> Dict[str, object]:
    scores: List[ScoreResult] = [scorer(plan, scenario) for scorer in SCORERS]
    return {
        "scenario_id": scenario.get("id"),
        "category": scenario.get("category"),
        "status": plan.status,
        "domain": plan.domain,
        "complexity": plan.complexity,
        "overall_score": average_score(scores),
        "scores": scores_to_dict(scores),
    }
