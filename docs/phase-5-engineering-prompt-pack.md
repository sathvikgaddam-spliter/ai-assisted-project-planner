# Phase 5: Engineering Prompt Pack Generation and Prompt Quality Evaluation

## Phase Goal

Phase 5 extends AI-Assisted Project Planner from structured project planning into engineering handoff preparation. After a project plan is generated, the system should be able to produce role-based implementation prompts that engineers can copy into AI coding tools and use as starting points for external software implementation work.

This phase does not change the product into an automated website builder, application generator, deployment system, or coding agent. The platform remains a planning and engineering guidance system. Its responsibility is to transform vague assignments into structured plans, technical documentation, implementation workflows, Jira-ready execution tasks, and high-quality prompts for external AI coding tools.

## Product Boundary

AI-Assisted Project Planner does not build or deploy software automatically.

The system should not:

- generate complete applications as a primary product behavior.
- write source code directly into downstream repositories.
- deploy infrastructure or production services.
- claim that generated prompts are sufficient without engineer review.
- replace architecture, security, QA, or release judgment.

The system should:

- preserve the existing project planning workflow.
- generate implementation-ready prompt packs from validated plans.
- keep assumptions and constraints explicit.
- help engineers hand work to AI coding tools in a controlled, reviewable way.
- evaluate prompt quality before presenting prompts as ready to use.

## Why Engineering Prompts Matter

Project plans are useful for understanding scope, sequencing work, and identifying risks, but engineers often need a more direct bridge from plan to implementation. A role-based prompt pack gives each engineering role focused instructions that match its responsibilities while preserving project context and acceptance criteria.

High-quality engineering prompts reduce ambiguity for AI coding tools by specifying:

- the role performing the work.
- the target tool and expected interaction style.
- the relevant phases, tasks, dependencies, and constraints.
- the expected output format.
- acceptance criteria and validation expectations.
- implementation guidance and boundaries.
- explicit instructions about what not to do.

This keeps the planner's output useful without crossing into automatic implementation.

## Supported AI Coding Tools

Phase 5 prompt packs should be designed for engineers using external AI coding tools, including:

- Codex
- Cursor
- Claude Code
- GitHub Copilot
- Lovable
- Bolt

The initial architecture should treat these as target tool labels and prompt-format contexts, not as direct integrations. No provider-specific SDKs or tool APIs are required for this phase.

## Supported Engineering Roles

The planned prompt pack should support these roles:

- Frontend Engineer
- Backend Engineer
- Database Engineer
- QA / Testing Engineer
- DevOps Engineer
- Security Reviewer

Each role prompt should be derived from the existing validated `ProjectPlan` contract rather than from unrelated free-form generation. This preserves deterministic fallback behavior and keeps the prompt pack tied to the same planning artifact used by the CLI, API, frontend, and evaluation framework.

## Planned Prompt Content

Each generated engineering prompt should contain:

- project context.
- target engineering role.
- target AI coding tool.
- technical scope.
- related phases and tasks.
- relevant constraints and assumptions.
- expected output.
- acceptance criteria.
- implementation guidance.
- "do not do" instructions.

The prompt should be specific enough to guide implementation work, but conservative enough to avoid inventing architecture, integrations, credentials, budgets, deadlines, or deployment details that are not present in the plan.

## Prompt Quality Evaluation Goals

Phase 5 should also evaluate generated prompts before presenting them as ready for engineering use.

Prompt evaluation should score:

- clarity.
- specificity.
- technical completeness.
- expected output quality.
- acceptance criteria quality.

Each evaluation should include:

- score out of 100.
- `ready_to_use` boolean.
- strengths.
- issues.
- improvement suggestions.

The goal is not to prove that an external AI tool will implement the software correctly. The goal is to identify whether the generated prompt is clear, bounded, technically useful, and reviewable before an engineer copies it into another tool.

## Implemented Architecture Additions

Phase 5 is implemented as a modular extension after plan generation. It does not replace the planner, analyzer, provider abstraction, or deterministic fallback behavior.

Implemented module responsibilities:

- `src/models.py`: defines `EngineeringPrompt`, `PromptEvaluation`, and prompt-pack fields on `ProjectPlan`.
- `src/prompt_generator.py`: deterministically generates role-based prompt pack objects from a validated `ProjectPlan`.
- `src/prompt_evaluator.py`: deterministically evaluates prompt quality with heuristic scoring rules.
- `src/planner.py`: attaches prompt packs and prompt evaluations to `plan_generated` plans after validation.
- `src/utils.py`: exports prompt pack content in Markdown and ZIP formats.
- `src/main.py`: saves the Prompt Pack ZIP during CLI runs.
- `src/api.py`: exposes `POST /generate-plan-zip` for ZIP downloads.
- `frontend/src/components/ExportActions.jsx`: adds a Prompt Pack ZIP download action in the existing export controls.
- `tests/`: covers schemas, generation, evaluation, planner attachment, exports, CLI, API, and frontend-compatible backend behavior.

The implementation remains deterministic and uses no additional runtime dependencies.

## Implemented Workflow

The implemented workflow is:

1. User submits a project description.
2. Existing planner generates a validated `ProjectPlan`.
3. If the plan status is `plan_generated`, Phase 5 prompt generation receives the validated plan.
4. Role-specific prompts are generated for supported engineering roles.
5. Each prompt is evaluated for quality.
6. The plan includes `engineering_prompts` and `prompt_evaluations`.
7. Markdown export includes Engineering Prompt Pack and Prompt Quality Evaluation sections.
8. ZIP export packages the project plan, role prompt files, and prompt quality report.
9. CLI, API, and frontend flows can save or download the Prompt Pack ZIP.

Clarification-required plans do not receive engineering prompts or prompt evaluations. Their ZIP exports still include the project plan Markdown and JSON files only.

## Compatibility Requirements

Phase 5 preserves:

- deterministic fallback behavior.
- strict Pydantic validation.
- existing planner behavior for description analysis, fallback, and clarification.
- CLI behavior with an added Prompt Pack ZIP export.
- API behavior with the existing `/generate-plan` response preserved and a dedicated `/generate-plan-zip` endpoint added.
- frontend behavior with an added Prompt Pack ZIP download button in the existing export controls.
- current benchmark and unit test compatibility.
- clear separation between planning, prompt generation, and prompt evaluation.

Prompt pack generation depends on validated plan data, not on raw user input alone. This keeps engineering prompts aligned with the same schema and assumptions used throughout the rest of the platform.

## Prompt Pack ZIP Format

The ZIP export uses this structure:

```text
project-plan/
  project_plan.md
  project_plan.json

engineering-prompts/
  frontend_engineer_prompt.md
  backend_engineer_prompt.md
  database_engineer_prompt.md
  qa_testing_engineer_prompt.md
  devops_engineer_prompt.md
  security_reviewer_prompt.md

prompt-evaluations/
  prompt_quality_report.md
```

Prompt files are omitted when a plan requires clarification.

## Future Implementation Principles

Implementation should be incremental:

- Start with deterministic prompt generation from existing plan fields.
- Add strict schemas before exposing prompt packs as formal outputs.
- Add tests for each supported role.
- Add tests for scoring boundaries and `ready_to_use` decisions.
- Keep AI-assisted prompt enhancement optional and behind the existing provider abstraction if introduced later.
- Extend API, frontend, exports, and evaluation reports only through explicit follow-up tasks.

The first working implementation should favor simple, inspectable logic over broad configuration or plugin systems.

## Non-Goals

Phase 5 does not include:

- automatic source code generation.
- repository modification.
- deployment automation.
- direct integrations with Codex, Cursor, Claude Code, GitHub Copilot, Lovable, or Bolt.
- new authentication, persistence, billing, or workspace systems.
- replacing the existing planner with prompt generation.
- changing current API/frontend behavior during documentation initialization.
- adding new runtime dependencies.
- speculative enterprise workflow infrastructure.

## Architectural Safety

This is a safe extension because it can be layered after the existing planner without disrupting the core planning engine. The existing system already produces validated structured plans, which are the correct source artifact for role-specific prompt generation. By keeping Phase 5 modular, deterministic, and schema-driven, future implementation can add engineering prompt packs while preserving the current planner, exports, tests, API behavior, and frontend behavior.
