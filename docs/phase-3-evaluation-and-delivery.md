# Phase 3: Evaluation and Delivery

## Phase Goal

Evaluate whether the planner produces useful, domain-aware, and trustworthy plans before presenting it as a finished product. Phase 3 focuses on prompt experiments, quality metrics, hallucination detection, final reporting, demo preparation, and the roadmap for a later UI.

## Prompt Comparison Experiments

Prompt experiments should compare different orchestration strategies:

- Single-step planning versus separate understanding and planning.
- Few-shot examples versus schema-only prompts.
- Domain-specific prompt templates versus one general prompt.
- Strict clarification threshold versus permissive planning.
- Different provider and model combinations.
- Response repair prompt versus direct retry.

Each experiment should record:

- prompt version.
- provider and model.
- scenario input.
- output plan.
- validation result.
- quality scores.
- observed failure modes.

## Evaluation Framework

The evaluation framework should measure both structural correctness and reasoning quality.

Evaluation sources:

- automated schema validation.
- deterministic rule checks.
- scenario-specific expected behavior.
- human review rubric.
- optional AI-assisted critique with strict rubric.

The evaluation should produce a report per scenario and an aggregate summary across domains.

## Sample Project Scenarios

Evaluation should use the scenarios in `docs/test-scenarios.md`, including:

- software MVPs.
- AI systems.
- BI and ETL workflows.
- business campaigns.
- academic research workflows.
- healthcare scheduling workflow.
- vague and invalid inputs.
- unrealistic and conflicting constraints.
- provider and configuration failures.

The purpose is to test whether the system selects the right planning style for the project, not just whether it returns valid JSON.

## Quality Metrics

Recommended metrics:

- Domain classification accuracy.
- Project type classification accuracy.
- Clarification appropriateness.
- Plan completeness.
- Dependency correctness.
- Milestone relevance.
- Timeline realism.
- Risk identification quality.
- Recommendation usefulness.
- Assumption discipline.
- Schema validity.
- Export consistency.
- Hallucination rate.

Each scenario should include pass/fail validation criteria and optional numeric ratings.

## Hallucination Detection Strategy

The planner should be evaluated for unsupported claims and invented details.

Detection checks:

- Does the plan introduce tools, teams, budgets, deadlines, or stakeholders not provided or clearly marked as assumptions?
- Does it claim integrations or data sources that were not mentioned?
- Does it skip clarification when the input is too vague?
- Does it create impossible timelines without warning?
- Does it recommend regulated workflows without acknowledging compliance risk?
- Does it produce dependencies that reference missing tasks?

Plans should clearly separate:

- known facts from user input.
- reasonable assumptions.
- risks.
- recommendations.
- unknowns requiring clarification.

## Final Report Planning

The final report should include:

- project vision and architecture summary.
- implementation phase summary.
- AI orchestration design.
- provider abstraction explanation.
- validation strategy.
- test scenario coverage.
- prompt experiment results.
- quality metric results.
- known limitations.
- future UI roadmap.
- demo instructions.

The report should include concrete examples of good and bad planner behavior.

## Demo Preparation

The demo should show:

- A clear software project generating a domain-appropriate plan.
- A BI dashboard project generating analytics phases.
- A vague prompt returning clarification questions.
- An unrealistic timeline being flagged.
- JSON and Markdown exports.
- A validation failure or malformed provider response handled safely.

The demo should use CLI commands so the backend-first strategy remains clear.

## UI Roadmap for Future Phase

UI development should begin only after backend planning behavior is reliable.

Future UI capabilities:

- project description intake form.
- guided clarification flow.
- plan preview.
- editable assumptions.
- phase and task review.
- export controls.
- plan comparison view.
- provider and prompt experiment dashboard for internal use.

The UI should consume backend contracts rather than reimplementing planning logic.
