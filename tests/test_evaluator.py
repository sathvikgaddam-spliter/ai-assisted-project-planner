import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from evaluator import evaluate_project_plan
from planner import generate_project_plan


def test_evaluator_scores_generated_plan():
    scenario = {
        "id": "SW-TEST",
        "category": "software projects",
        "input": "Build an expense tracker app for college students to track spending and budgets.",
        "expected_behavior": "Generate a software MVP plan.",
        "evaluation_focus": ["domain classification", "task sequencing"],
    }
    plan = generate_project_plan(scenario["input"], use_ai=False)
    result = evaluate_project_plan(plan, scenario)

    assert result["scenario_id"] == "SW-TEST"
    assert result["overall_score"] >= 3
    assert len(result["scores"]) == 10
    assert result["scores"]["output_validity"]["score"] == 5


def test_scenarios_have_required_fields():
    scenarios_path = Path(__file__).resolve().parents[1] / "evaluation" / "scenarios.json"
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))

    assert len(scenarios) >= 9
    for scenario in scenarios:
        assert scenario["id"]
        assert scenario["category"]
        assert scenario["input"]
        assert scenario["expected_behavior"]
        assert scenario["evaluation_focus"]
