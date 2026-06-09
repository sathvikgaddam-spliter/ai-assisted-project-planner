from typing import List

from models import EngineeringPrompt, ProjectPlan


TARGET_TOOLS = "Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt"

ROLE_CONFIGS = [
    {
        "id": "EP1",
        "role": "Frontend Engineer",
        "senior_framing": "You are a senior frontend engineer responsible for implementing the user-facing experience.",
        "goal": "Implement the frontend experience for the planned project while preserving the validated project scope.",
        "scope": "UI workflows, client-side validation, accessibility, responsive behavior, and integration points with backend APIs.",
    },
    {
        "id": "EP2",
        "role": "Backend Engineer",
        "senior_framing": "You are a senior backend engineer responsible for building the application services and API layer.",
        "goal": "Implement backend services that support the planned workflows, validation rules, and task sequencing.",
        "scope": "API contracts, service logic, validation, error handling, integrations, and backend test coverage.",
    },
    {
        "id": "EP3",
        "role": "Database Engineer",
        "senior_framing": "You are a senior database engineer responsible for designing the data model and persistence approach.",
        "goal": "Define storage structures that support the project requirements without inventing unsupported data sources.",
        "scope": "Entities, relationships, indexes, migrations, data quality checks, retention needs, and backup assumptions.",
    },
    {
        "id": "EP4",
        "role": "QA / Testing Engineer",
        "senior_framing": "You are a senior QA engineer responsible for validating the implementation against the plan.",
        "goal": "Create a practical test strategy for the project phases, risks, acceptance criteria, and release workflow.",
        "scope": "Functional tests, regression tests, edge cases, acceptance criteria validation, risk-based testing, and defect reporting.",
    },
    {
        "id": "EP5",
        "role": "DevOps Engineer",
        "senior_framing": "You are a senior DevOps engineer responsible for deployment readiness and operational workflow.",
        "goal": "Plan environment, build, release, monitoring, and rollback work without deploying anything automatically.",
        "scope": "Local development setup, CI checks, configuration, deployment plan, observability, release checklist, and rollback notes.",
    },
    {
        "id": "EP6",
        "role": "Security Reviewer",
        "senior_framing": "You are a senior security engineer responsible for reviewing the plan for security and privacy risks.",
        "goal": "Review implementation plans for security, privacy, access control, data handling, and compliance risks.",
        "scope": "Threat modeling, authentication and authorization concerns, sensitive data handling, dependency risk, and secure defaults.",
    },
]


def generate_engineering_prompts(plan: ProjectPlan) -> List[EngineeringPrompt]:
    phase_ids = [phase.id for phase in plan.phases]
    constraints = _build_constraints(plan)

    return [
        EngineeringPrompt(
            id=config["id"],
            title=f"{config['role']} implementation prompt",
            target_role=config["role"],
            target_tool=TARGET_TOOLS,
            purpose=config["goal"],
            related_phases=phase_ids,
            prompt_text=_render_prompt_text(plan, config, constraints),
            acceptance_criteria=_build_acceptance_criteria(plan, config["role"]),
            constraints=constraints,
        )
        for config in ROLE_CONFIGS
    ]


def _render_prompt_text(plan: ProjectPlan, config: dict, constraints: List[str]) -> str:
    phases = _format_phases(plan)
    tasks = _format_tasks(plan)
    risks = _format_items([risk.description for risk in plan.risks], "No explicit risks were provided.")
    recommendations = _format_items(
        [item.recommendation for item in plan.recommendations],
        "No explicit recommendations were provided.",
    )
    assumptions = _format_items(plan.assumptions, "No explicit assumptions were provided.")
    acceptance_criteria = _format_items(_build_acceptance_criteria(plan, config["role"]), "Use the project plan as the acceptance baseline.")
    constraint_text = _format_items(constraints, "Do not exceed the validated project plan.")

    return "\n".join(
        [
            config["senior_framing"],
            "",
            "## Project Context",
            f"Project name: {plan.project_name}",
            f"Project description: {plan.description}",
            f"Domain: {plan.domain}",
            f"Project type: {plan.project_type}",
            f"Complexity: {plan.complexity}",
            f"Summary: {plan.summary}",
            "",
            "## Your Role",
            config["role"],
            "",
            "## Goal",
            config["goal"],
            "",
            "## Technical Scope",
            config["scope"],
            "",
            "Relevant tasks:",
            tasks,
            "",
            "Risks to account for:",
            risks,
            "",
            "Recommendations to preserve:",
            recommendations,
            "",
            "Assumptions to keep visible:",
            assumptions,
            "",
            "## Related Phases",
            phases,
            "",
            "## Constraints",
            constraint_text,
            "",
            "## Expected Output",
            f"Produce implementation guidance or artifacts for {TARGET_TOOLS}. The output should be ready for an engineer to review and apply externally.",
            "The planner itself must not build, deploy, or modify software.",
            "",
            "## Acceptance Criteria",
            acceptance_criteria,
            "",
            "## Do Not Do",
            "- Do not build or deploy the application automatically.",
            "- Do not invent requirements, credentials, budgets, deadlines, integrations, or production infrastructure.",
            "- Do not treat this draft as production-ready when requirements are incomplete.",
            "- Do not remove assumptions, warnings, risks, or acceptance criteria from the engineering handoff.",
            "- Do not treat this prompt as a substitute for engineer review.",
        ]
    )


def _format_phases(plan: ProjectPlan) -> str:
    if not plan.phases:
        return "- No execution phases were generated; use clarification questions before implementation."
    return "\n".join(
        f"- {phase.id}: {phase.name} ({phase.estimated_duration}) - {phase.objective}"
        for phase in plan.phases
    )


def _format_tasks(plan: ProjectPlan) -> str:
    tasks = [
        f"- {task.id}: {task.title} - {task.description}"
        for phase in plan.phases
        for task in phase.tasks
    ]
    return "\n".join(tasks) if tasks else "- No implementation tasks were generated."


def _build_acceptance_criteria(plan: ProjectPlan, role: str) -> List[str]:
    criteria = [
        f"The {role} output is aligned with the validated project plan.",
        "Relevant phases, tasks, assumptions, risks, and recommendations are addressed.",
        "The output is structured for engineer review before use in an external AI coding tool.",
    ]

    task_criteria = [
        criterion
        for phase in plan.phases
        for task in phase.tasks
        for criterion in task.acceptance_criteria
    ]
    criteria.extend(task_criteria[:3])
    return criteria


def _build_constraints(plan: ProjectPlan) -> List[str]:
    constraints = [
        "Use the generated project plan as the source of truth.",
        "Do not build, deploy, or modify software from inside the planner.",
        f"Keep implementation guidance appropriate for {TARGET_TOOLS}.",
    ]
    constraints.extend(plan.assumptions)
    constraints.extend(plan.warnings)
    return constraints


def _format_items(items: List[str], empty_text: str) -> str:
    values = [item for item in items if item]
    if not values:
        return f"- {empty_text}"
    return "\n".join(f"- {item}" for item in values)
