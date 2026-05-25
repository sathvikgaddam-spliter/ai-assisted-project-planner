# Scoring Rubric

Use a 1-5 score for each dimension. Scores should reflect the generated plan itself, not the intent of the scenario.

## 1. Project Understanding

- 1: Misclassifies the domain or core objective.
- 2: Captures a few keywords but misses the main project context.
- 3: Identifies the broad domain and deliverable with generic framing.
- 4: Correctly captures domain, users, deliverable, and constraints.
- 5: Demonstrates precise understanding of domain, stakeholders, constraints, and success criteria.

## 2. Completeness

- 1: Missing most required plan sections.
- 2: Includes a partial plan with major omissions.
- 3: Includes core phases, tasks, risks, and recommendations.
- 4: Covers all major sections with useful detail.
- 5: Covers all sections comprehensively, including assumptions, warnings, and validation needs.

## 3. Task Quality

- 1: Tasks are vague, duplicative, or not actionable.
- 2: Some tasks are actionable but many lack owners, effort, or acceptance criteria.
- 3: Most tasks are actionable and assigned to sensible roles.
- 4: Tasks are specific, sequenced, and include clear acceptance criteria.
- 5: Tasks are highly actionable, measurable, role-aware, and tailored to the scenario.

## 4. Milestone Usefulness

- 1: No milestones or unusable milestones.
- 2: Milestones exist but do not map cleanly to delivery progress.
- 3: Milestones summarize phase completion.
- 4: Milestones create useful decision or review gates.
- 5: Milestones are measurable, stakeholder-relevant, and aligned to risk reduction.

## 5. Dependency Correctness

- 1: Dependencies are absent when needed or reference invalid tasks.
- 2: Dependencies exist but are mostly generic or inconsistent.
- 3: Dependencies are valid and broadly sequential.
- 4: Dependencies capture important task order and cross-phase prerequisites.
- 5: Dependencies are valid, complete, and clearly explain delivery constraints.

## 6. Timeline Realism

- 1: Timeline is impossible or ignores explicit constraints.
- 2: Timeline is optimistic and lacks scope warnings.
- 3: Timeline is plausible for a generic MVP or workflow.
- 4: Timeline is realistic for the stated scope and includes validation gates.
- 5: Timeline explicitly reconciles scope, risks, resources, and staged delivery.

## 7. Risk Awareness

- 1: No meaningful risks.
- 2: Generic risks only.
- 3: Includes common delivery risks.
- 4: Includes domain-specific risks and mitigations.
- 5: Identifies domain, compliance, scope, data, and adoption risks with strong mitigations.

## 8. Recommendation Quality

- 1: Recommendations are absent or irrelevant.
- 2: Recommendations are generic and not tied to scenario risks.
- 3: Recommendations provide reasonable next steps.
- 4: Recommendations are specific, prioritized, and tied to constraints.
- 5: Recommendations materially improve feasibility, safety, and research or delivery quality.

## 9. Hallucination Avoidance

- 1: Invents unsupported facts, tools, integrations, or guarantees.
- 2: Makes several unsupported assumptions without labeling them.
- 3: Uses some assumptions but labels them or keeps them low-risk.
- 4: Avoids unsupported claims and asks for clarification where needed.
- 5: Explicitly separates known input from assumptions and refuses unsafe over-specific planning.

## 10. Output Validity

- 1: Output cannot be parsed or does not match the schema.
- 2: Output is parseable but violates major schema or consistency expectations.
- 3: Output is valid and includes required top-level fields.
- 4: Output is valid and internally consistent.
- 5: Output is valid, internally consistent, and ready for downstream reporting.
