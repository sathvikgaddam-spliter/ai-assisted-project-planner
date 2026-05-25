# Final Report

## Objective

This project investigates whether an AI-assisted planning system can convert natural-language project descriptions into structured project plans with useful phases, tasks, milestones, dependencies, risks, and recommendations.

## Methodology

The system is evaluated with benchmark scenarios covering software, AI/RAG, BI/data, business, healthcare, academic, vague, unrealistic, and conflicting requirements. Generated `ProjectPlan` objects are scored against a 1-5 rubric for understanding, completeness, task quality, milestones, dependencies, timeline realism, risks, recommendations, hallucination avoidance, and output validity.

## Scenarios Tested

The scenario suite is maintained in `evaluation/scenarios.json`. Each scenario defines the input prompt, expected behavior, and evaluation focus so that fallback and AI planner outputs can be compared consistently.

## Findings

To be completed after running the benchmark and reviewing `reports/experiment_results.md`.

## Limitations

- The current automated evaluator uses transparent heuristics rather than expert human annotation.
- The fallback planner is deterministic and may underrepresent the variability of AI-generated plans.
- Scenario coverage is representative but not exhaustive.
- Academic conclusions should distinguish schema validity from true planning quality.

## Conclusion

Phase 3 adds a repeatable evaluation framework for measuring plan quality, tracking benchmark outputs, and preparing research deliverables. The framework supports current fallback evaluation and can be reused for AI planner comparisons as provider-backed planning matures.
