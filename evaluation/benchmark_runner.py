from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evaluator import evaluate_project_plan
from planner import generate_project_plan


DEFAULT_SCENARIOS_PATH = ROOT_DIR / "evaluation" / "scenarios.json"
DEFAULT_SAMPLE_OUTPUT_DIR = ROOT_DIR / "evaluation" / "sample_outputs"
DEFAULT_REPORT_PATH = ROOT_DIR / "reports" / "experiment_results.md"
DEFAULT_RESULTS_PATH = ROOT_DIR / "evaluation" / "benchmark_results.json"


def run_benchmark(
    scenarios_path: Path = DEFAULT_SCENARIOS_PATH,
    results_path: Path = DEFAULT_RESULTS_PATH,
    report_path: Path = DEFAULT_REPORT_PATH,
    sample_output_dir: Path = DEFAULT_SAMPLE_OUTPUT_DIR,
    use_ai: bool = False,
) -> Dict[str, Any]:
    scenarios = _load_scenarios(scenarios_path)
    sample_output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.parent.mkdir(parents=True, exist_ok=True)

    results: List[Dict[str, Any]] = []
    for scenario in scenarios:
        plan = generate_project_plan(str(scenario["input"]), use_ai=use_ai)
        evaluation = evaluate_project_plan(plan, scenario)
        plan_payload = _model_to_dict(plan)
        sample_path = sample_output_dir / f"{scenario['id']}.plan.json"
        sample_path.write_text(json.dumps(plan_payload, indent=2, default=str), encoding="utf-8")

        results.append(
            {
                "scenario": scenario,
                "plan_summary": {
                    "project_name": plan.project_name,
                    "domain": plan.domain,
                    "project_type": plan.project_type,
                    "complexity": plan.complexity,
                    "status": plan.status,
                    "warnings": plan.warnings,
                },
                "evaluation": evaluation,
                "sample_output": str(sample_path.relative_to(ROOT_DIR)),
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "planner_mode": "ai" if use_ai else "fallback",
        "scenario_count": len(scenarios),
        "average_score": _average([item["evaluation"]["overall_score"] for item in results]),
        "results": results,
    }
    results_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    report_path.write_text(_render_markdown_report(payload), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run benchmark scenarios against the project planner.")
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS_PATH)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS_PATH)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--sample-output-dir", type=Path, default=DEFAULT_SAMPLE_OUTPUT_DIR)
    parser.add_argument("--use-ai", action="store_true", help="Use the configured AI planner instead of deterministic fallback.")
    args = parser.parse_args()

    payload = run_benchmark(
        scenarios_path=args.scenarios,
        results_path=args.results,
        report_path=args.report,
        sample_output_dir=args.sample_output_dir,
        use_ai=args.use_ai,
    )
    print(f"Ran {payload['scenario_count']} scenarios in {payload['planner_mode']} mode.")
    print(f"Average score: {payload['average_score']}")
    print(f"Results: {args.results}")
    print(f"Report: {args.report}")
    return 0


def _load_scenarios(path: Path) -> List[Dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _model_to_dict(model: Any) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json")
    return model.dict()


def _average(values: List[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def _render_markdown_report(payload: Dict[str, Any]) -> str:
    findings = _derive_findings(payload)
    lines = [
        "# Experiment Results",
        "",
        "## Objective",
        "Evaluate planning quality across benchmark project scenarios using the current planner implementation.",
        "",
        "## Methodology",
        f"The benchmark ran {payload['scenario_count']} scenarios in {payload['planner_mode']} mode. Each generated plan was scored with a 1-5 rubric across ten dimensions.",
        "",
        "## Aggregate Results",
        f"- Average score: {payload['average_score']}",
        "",
        "## Scenario Results",
        "| Scenario | Category | Status | Domain | Score | Sample Output |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for item in payload["results"]:
        scenario = item["scenario"]
        plan = item["plan_summary"]
        evaluation = item["evaluation"]
        lines.append(
            f"| {scenario['id']} | {scenario['category']} | {plan['status']} | {plan['domain']} | {evaluation['overall_score']} | {item['sample_output']} |"
        )

    lines.extend(
        [
            "",
            "## Findings",
            *[f"- {finding}" for finding in findings],
            "",
            "## Limitations",
            "- Current scoring uses deterministic heuristics and should be supplemented with human review for academic claims.",
            "- AI planner evaluation depends on provider configuration and may vary across model versions.",
            "",
            "## Conclusion",
            "The benchmark establishes a repeatable baseline for comparing fallback and future AI planner behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def _derive_findings(payload: Dict[str, Any]) -> List[str]:
    results = payload["results"]
    if not results:
        return ["No benchmark results were generated."]

    lowest = min(results, key=lambda item: item["evaluation"]["overall_score"])
    highest = max(results, key=lambda item: item["evaluation"]["overall_score"])
    clarification_count = sum(1 for item in results if item["plan_summary"]["status"] == "clarification_required")
    mismatch_ids = [
        item["scenario"]["id"]
        for item in results
        if item["evaluation"]["scores"]["project_understanding"]["score"] <= 2
    ]

    findings = [
        f"Highest-scoring scenario: {highest['scenario']['id']} at {highest['evaluation']['overall_score']}.",
        f"Lowest-scoring scenario: {lowest['scenario']['id']} at {lowest['evaluation']['overall_score']}.",
        f"{clarification_count} scenario(s) returned clarification-required output.",
    ]
    if mismatch_ids:
        findings.append(f"Potential domain or project-understanding mismatches appeared in: {', '.join(mismatch_ids)}.")
    else:
        findings.append("No severe project-understanding mismatches were detected by the heuristic scorer.")

    return findings


if __name__ == "__main__":
    raise SystemExit(main())
