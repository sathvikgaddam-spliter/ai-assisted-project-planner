# Experiment Results

## Objective
Evaluate planning quality across benchmark project scenarios using the current planner implementation.

## Methodology
The benchmark ran 9 scenarios in fallback mode. Each generated plan was scored with a 1-5 rubric across ten dimensions.

## Aggregate Results
- Average score: 4.58

## Scenario Results
| Scenario | Category | Status | Domain | Score | Sample Output |
| --- | --- | --- | --- | ---: | --- |
| SW-001 | software projects | plan_generated | analytics | 4.4 | evaluation\sample_outputs\SW-001.plan.json |
| AI-001 | AI/RAG projects | plan_generated | software | 4.6 | evaluation\sample_outputs\AI-001.plan.json |
| BI-001 | BI/data projects | plan_generated | analytics | 4.7 | evaluation\sample_outputs\BI-001.plan.json |
| BUS-001 | business workflows | plan_generated | business | 4.5 | evaluation\sample_outputs\BUS-001.plan.json |
| HC-001 | healthcare workflows | plan_generated | healthcare | 4.7 | evaluation\sample_outputs\HC-001.plan.json |
| ACAD-001 | academic planning | plan_generated | academic | 4.5 | evaluation\sample_outputs\ACAD-001.plan.json |
| VAGUE-001 | vague input | clarification_required | unknown | 4.3 | evaluation\sample_outputs\VAGUE-001.plan.json |
| SCOPE-001 | unrealistic scope | plan_generated | healthcare | 4.8 | evaluation\sample_outputs\SCOPE-001.plan.json |
| CONFLICT-001 | conflicting requirements | plan_generated | healthcare | 4.7 | evaluation\sample_outputs\CONFLICT-001.plan.json |

## Findings
- Highest-scoring scenario: SCOPE-001 at 4.8.
- Lowest-scoring scenario: VAGUE-001 at 4.3.
- 1 scenario(s) returned clarification-required output.
- Potential domain or project-understanding mismatches appeared in: SW-001.

## Limitations
- Current scoring uses deterministic heuristics and should be supplemented with human review for academic claims.
- AI planner evaluation depends on provider configuration and may vary across model versions.

## Conclusion
The benchmark establishes a repeatable baseline for comparing fallback and future AI planner behavior.
