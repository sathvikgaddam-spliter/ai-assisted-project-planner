from typing import Dict, List, Mapping, Optional


REQUIRED_BUILD_PACK_FILES = [
    "START_HERE.md",
    "COPY_THIS_PROMPT.md",
    "project_brief.md",
    "requirements.md",
    "mvp_scope.md",
    "architecture.md",
    "database_schema.md",
    "api_spec.md",
    "frontend_spec.md",
    "implementation_steps.md",
    "testing_plan.md",
    "deployment_plan.md",
    "assumptions.md",
    "coding_agent_prompt.md",
]


def generate_build_pack(project_analysis, project_plan=None):
    return {
        "START_HERE.md": generate_start_here(project_analysis),
        "COPY_THIS_PROMPT.md": generate_copy_this_prompt(project_analysis),
        "project_brief.md": generate_project_brief(project_analysis),
        "requirements.md": generate_requirements(project_analysis),
        "mvp_scope.md": generate_mvp_scope(project_analysis),
        "architecture.md": generate_architecture(project_analysis),
        "database_schema.md": generate_database_schema(project_analysis),
        "api_spec.md": generate_api_spec(project_analysis),
        "frontend_spec.md": generate_frontend_spec(project_analysis),
        "implementation_steps.md": generate_implementation_steps(project_analysis, project_plan),
        "testing_plan.md": generate_testing_plan(project_analysis),
        "deployment_plan.md": generate_deployment_plan(project_analysis),
        "assumptions.md": generate_assumptions(project_analysis),
        "coding_agent_prompt.md": generate_coding_agent_prompt(project_analysis),
    }


def generate_start_here(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Start Here",
            "",
            "## Purpose",
            f"This folder is a coding-agent execution pack for building a runnable {context['detected_project_type']}.",
            "",
            "## Instruction for Codex, Claude Code, Cursor, Copilot, Lovable, Bolt, Gemini, or Similar Agents",
            "Create a complete runnable MVP application from these specifications.",
            "",
            "You must generate actual source code, build/runtime configuration, run scripts, and tests.",
            "Do not only summarize, critique, or restate the markdown documents.",
            "",
            "## Source of Truth",
            _numbered(
                [
                    "Read coding_agent_prompt.md first.",
                    "Follow requirements.md for functional scope and acceptance criteria.",
                    "Follow architecture.md for component boundaries and data flow.",
                    "Follow database_schema.md for data models, fields, relationships, and constraints.",
                    "Follow api_spec.md for backend routes, request/response expectations, and authorization behavior.",
                    "Follow frontend_spec.md for pages, components, user flows, and UI states.",
                    "Follow testing_plan.md for required validation coverage.",
                    "Use assumptions.md when the original user request is incomplete.",
                ]
            ),
            "",
            "## Required Output",
            _bullets(
                [
                    "A runnable application source tree.",
                    "Build and runtime configuration such as package.json, pyproject.toml, requirements.txt, pom.xml, build.gradle, Makefile, or equivalent for the selected stack.",
                    "Frontend and backend source files when the architecture requires both.",
                    "Database models, migrations, seed data, or in-memory persistence suitable for the MVP.",
                    "Automated tests for core behavior.",
                    "A README with exact install, run, test, and build commands.",
                ]
            ),
            "",
            "## Completion Rule",
            "The implementation is not complete until a developer can run the generated project locally using the commands documented in the generated README.",
        ]
    )


def generate_copy_this_prompt(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Copy This Prompt",
            "",
            "Paste this prompt into Codex, Claude Code, Cursor, GitHub Copilot, Lovable, Bolt, Gemini, or a similar coding agent.",
            "",
            "```text",
            f"You are a senior full-stack coding agent responsible for building a complete runnable MVP for a {context['detected_project_type']}.",
            "",
            "Use the attached/generated project files as the source of truth. Start with START_HERE.md, then follow requirements.md, architecture.md, database_schema.md, api_spec.md, frontend_spec.md, testing_plan.md, implementation_steps.md, assumptions.md, project_plan.md, and project_plan.json.",
            "",
            "Your task is to build the application the user requested. Generate actual source code, project structure, build/runtime configuration, run scripts, tests, and a README with exact install, run, test, and build commands.",
            "",
            "Do not only summarize the documents. Do not stop at planning. Do not say the workspace only contains documentation. Create or modify files until the project is runnable locally.",
            "",
            "If requirements are incomplete, use assumptions.md and clearly mark assumptions in the implementation README. Prefer a complete MVP over a minimal placeholder.",
            "```",
        ]
    )


def generate_project_brief(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Project Brief",
            "",
            "## Overview",
            f"Build an implementation-ready {context['detected_project_type']} in the {context['domain']} domain.",
            f"Planner project type: {context['project_type']}.",
            "",
            "## Target Users",
            _bullets(context["target_users"]),
            "",
            "## Goals",
            _bullets([f"Support {workflow}." for workflow in context["workflows"]]),
            "",
            "## Success Criteria",
            _bullets([f"{feature.capitalize()} is implemented, tested, and reviewable." for feature in context["features"]]),
        ]
    )


def generate_requirements(project_analysis):
    context = _context(project_analysis)
    stories = [f"As a {role}, I can use {workflow} so the project supports the intended workflow." for role in context["roles"] for workflow in context["workflows"][:2]]
    acceptance = [f"{feature.capitalize()} has validation, error handling, and documented acceptance criteria." for feature in context["features"]]
    return _join(
        [
            "# Requirements",
            "",
            "## Functional Requirements",
            _numbered([f"Implement {feature}." for feature in context["features"]]),
            "",
            "## Target Users and Roles",
            _bullets([*context["target_users"], *context["roles"]]),
            "",
            "## Non-Functional Requirements",
            _bullets([
                "Use clear validation and error states.",
                "Protect role-specific actions with authorization checks.",
                "Keep implementation modular enough for coding-agent handoff.",
                *context["infrastructure"],
            ]),
            "",
            "## User Stories",
            _bullets(stories),
            "",
            "## Acceptance Criteria",
            _bullets(acceptance),
        ]
    )


def generate_mvp_scope(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# MVP Scope",
            "",
            "## In Scope",
            _bullets(context["features"]),
            "",
            "## Out of Scope",
            _bullets([
                "Advanced enterprise administration unless explicitly requested.",
                "Production payment processing without a reviewed integration plan.",
                "Native mobile applications unless the detected type requires mobile delivery.",
                "Automated deployment without engineer review.",
            ]),
            "",
            "## MVP Success Criteria",
            _bullets([f"Users can complete {workflow} in a tested flow." for workflow in context["workflows"]]),
        ]
    )


def generate_architecture(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Architecture",
            "",
            "## Recommended Architecture",
            f"Use a modular full-stack architecture for a {context['detected_project_type']}.",
            "",
            "## Major Components",
            _bullets([
                "Frontend application for user workflows and stateful interactions.",
                "Backend API service for business logic, validation, and authorization.",
                "Database layer for persistent entities and relationships.",
                "Testing layer for unit, API, integration, and end-to-end validation.",
            ]),
            "",
            "## Frontend Layer",
            _bullets(context["frontend"]),
            "",
            "## Backend/API Layer",
            _bullets(context["backend"]),
            "",
            "## Data Layer",
            _bullets([f"Persist {entity} records with ownership, timestamps, and validation metadata." for entity in context["entities"]]),
            "",
            "## Data Flow",
            _numbered([
                "User completes a frontend workflow.",
                "Frontend validates required fields and calls backend APIs.",
                "Backend authorizes the request and applies business rules.",
                "Database stores or retrieves the relevant entities.",
                "Frontend renders success, error, empty, and loading states.",
            ]),
            "",
            "## Module Breakdown",
            _bullets([f"{entity} module: model, API routes, service logic, validation, and tests." for entity in context["entities"]]),
        ]
    )


def generate_database_schema(project_analysis):
    context = _context(project_analysis)
    sections = ["# Database Schema", ""]
    for entity in context["entities"]:
        sections.extend(
            [
                f"## {entity}",
                "",
                "Suggested fields:",
                _bullets(_entity_fields(entity)),
                "",
                "Relationships and constraints:",
                _bullets([
                    "Include a stable primary key.",
                    "Track created_at and updated_at timestamps.",
                    "Add indexes for owner, status, and lookup fields where applicable.",
                ]),
                "",
            ]
        )
    return _join(sections)


def generate_api_spec(project_analysis):
    context = _context(project_analysis)
    lines = [
        "# API Specification",
        "",
        "## Authentication",
        "Use authenticated routes for user-owned data and admin-only routes for administrative actions.",
        "",
        "## Required API Capabilities",
        _bullets(context["backend"]),
        "",
    ]
    for entity in context["entities"]:
        resource = _resource_name(entity)
        lines.extend(
            [
                f"## {entity} Endpoints",
                "",
                f"- `GET /api/{resource}`: list {resource}; supports pagination and filtering.",
                f"- `POST /api/{resource}`: create a {entity}; validates request body and ownership.",
                f"- `GET /api/{resource}/{{id}}`: fetch one {entity}; returns 404 when unavailable.",
                f"- `PATCH /api/{resource}/{{id}}`: update a {entity}; enforces authorization.",
                f"- `DELETE /api/{resource}/{{id}}`: archive or delete a {entity}; requires authorization.",
                "",
            ]
        )
    lines.extend(["## Request/Response Expectations", _bullets(["Use JSON request bodies.", "Return validation errors with field-level messages.", "Return consistent success envelopes for created and updated records."])])
    return _join(lines)


def generate_frontend_spec(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Frontend Specification",
            "",
            "## Pages and Screens",
            _bullets(["Landing or dashboard screen", "Authentication or onboarding screen", *context["frontend"], "Settings or profile screen"]),
            "",
            "## Components",
            _bullets([f"{feature.capitalize()} component" for feature in context["features"]] + ["Shared form controls", "Loading, empty, and error states"]),
            "",
            "## User Flows",
            _numbered(context["workflows"]),
            "",
            "## States",
            _bullets(["loading", "empty", "validation error", "success", "permission denied"]),
        ]
    )


def generate_implementation_steps(project_analysis, project_plan=None):
    context = _context(project_analysis)
    plan_steps = _phase_steps(project_plan)
    steps = plan_steps or [
        "Set up project structure, linting, environment configuration, and test runner.",
        "Implement data models and migrations for core entities.",
        "Implement backend services and API routes.",
        "Build frontend screens and connect them to APIs.",
        "Add unit, integration, API, and end-to-end tests.",
        "Prepare deployment configuration and operational documentation.",
    ]
    return _join(
        [
            "# Implementation Steps",
            "",
            "## Build Order",
            _numbered(steps),
            "",
            "## Module-Level Tasks",
            _bullets([f"Build {entity} model, API, UI, and tests." for entity in context["entities"]]),
            "",
            "## Dependencies",
            _bullets(["Data model before API routes.", "API routes before frontend integration.", "Core workflows before polish and deployment."]),
            "",
            "## Milestones",
            _bullets([f"{workflow.capitalize()} workflow is implemented and tested." for workflow in context["workflows"]]),
            "",
            "## Testing Checkpoints",
            _bullets(["Run unit tests after each module.", "Run API integration tests before frontend wiring.", "Run end-to-end tests before release handoff."]),
        ]
    )


def generate_testing_plan(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Testing Plan",
            "",
            "## Unit Tests",
            _bullets([f"Validate {entity} model rules and service behavior." for entity in context["entities"]]),
            "",
            "## Integration and API Tests",
            _bullets([f"Test {need} with success, validation, and authorization cases." for need in context["backend"]]),
            "",
            "## Frontend Tests",
            _bullets([f"Test {need} screen states and user interactions." for need in context["frontend"]]),
            "",
            "## End-to-End Tests",
            _bullets([f"Verify complete {workflow} flow." for workflow in context["workflows"]]),
            "",
            "## Edge Cases",
            _bullets(["unauthenticated access", "invalid input", "empty data", "permission denied", "network failure"]),
        ]
    )


def generate_deployment_plan(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Deployment Plan",
            "",
            "## Local Setup",
            _numbered(["Install dependencies.", "Create environment file.", "Run database migrations.", "Start backend and frontend development servers."]),
            "",
            "## Environment Variables",
            _bullets(["DATABASE_URL", "AUTH_SECRET", "API_BASE_URL", "LOG_LEVEL"]),
            "",
            "## Build and Run Commands",
            _bullets(["backend: run tests and start API server", "frontend: run build and serve static assets", "database: apply migrations before release"]),
            "",
            "## Deployment Approach",
            f"Deploy the {context['detected_project_type']} as a reviewed MVP with separate build, test, and release steps.",
            "",
            "## Logging and Monitoring",
            _bullets(["request logging", "error tracking", "health checks", *context["infrastructure"]]),
        ]
    )


def generate_assumptions(project_analysis):
    context = _context(project_analysis)
    assumptions = [
        "The user may have provided only a one-line project idea.",
        "Target users, timeline, budget, and compliance requirements may need confirmation.",
        "Generated specifications are implementation guidance and require engineer review.",
        f"The project is treated as a {context['detected_project_type']} unless later clarified.",
    ]
    return _join(["# Assumptions", "", _bullets(assumptions)])


def generate_coding_agent_prompt(project_analysis):
    context = _context(project_analysis)
    return _join(
        [
            "# Coding Agent Prompt",
            "",
            f"You are a Codex/Claude/Cursor-style coding agent acting as a senior full-stack engineer building a complete MVP for a {context['detected_project_type']}.",
            "",
            "Your task is implementation, not analysis. Generate a runnable application source tree from these documents.",
            "",
            "Use these build-pack documents as source of truth:",
            _bullets(["START_HERE.md", "requirements.md", "architecture.md", "database_schema.md", "api_spec.md", "frontend_spec.md", "testing_plan.md", "assumptions.md"]),
            "",
            "Implementation instructions:",
            _numbered([
                "Create actual source code, not only planning notes or summaries.",
                "Create build and runtime configuration for the selected stack.",
                "Follow architecture.md for component boundaries and data flow.",
                "Implement the database schema from database_schema.md.",
                "Implement API endpoints from api_spec.md with validation and authorization.",
                "Implement frontend screens and states from frontend_spec.md.",
                "Build the complete MVP, not only a minimal prototype.",
                "Write unit, integration, API, frontend, and end-to-end tests.",
                "Add a README with exact install, run, test, and build commands.",
                "Use assumptions.md when details are incomplete and mark assumptions in code comments or documentation.",
            ]),
            "",
            "Do not stop after reading files. Do not return only a status report. Do not skip tests, do not invent production credentials, and do not remove validation or engineer-review steps.",
        ]
    )


def _context(project_analysis: Mapping[str, object]) -> Dict[str, object]:
    understanding = project_analysis.get("build_pack_understanding", {}) or {}
    return {
        "domain": project_analysis.get("domain", "unknown"),
        "project_type": project_analysis.get("project_type", "unknown project type"),
        "detected_project_type": project_analysis.get("detected_project_type") or understanding.get("detected_project_type", "generic web application"),
        "target_users": _list_value(understanding, "target_users"),
        "roles": _list_value(understanding, "likely_user_roles"),
        "workflows": _list_value(understanding, "likely_workflows"),
        "features": _list_value(understanding, "core_features"),
        "entities": _list_value(understanding, "likely_data_entities"),
        "frontend": _list_value(understanding, "frontend_needs"),
        "backend": _list_value(understanding, "backend_api_needs"),
        "infrastructure": _list_value(understanding, "infrastructure_testing_assumptions"),
    }


def _list_value(source: Mapping[str, object], key: str) -> List[str]:
    value = source.get(key, [])
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)] if value else []


def _entity_fields(entity: str) -> List[str]:
    base = ["id", "created_at", "updated_at", "status"]
    entity_lower = entity.lower()
    if "user" in entity_lower:
        return [*base, "email", "display_name", "role"]
    if "order" in entity_lower or "transaction" in entity_lower or "payment" in entity_lower:
        return [*base, "user_id", "amount", "currency", "payment_status"]
    if "listing" in entity_lower or "product" in entity_lower or "item" in entity_lower:
        return [*base, "owner_id", "title", "description", "price"]
    if "prompt" in entity_lower or "response" in entity_lower:
        return [*base, "user_id", "content", "model_metadata"]
    return [*base, "name", "description", "owner_id"]


def _resource_name(entity: str) -> str:
    resource = "".join([f"-{char.lower()}" if char.isupper() else char for char in entity]).strip("-")
    return resource.replace("_", "-") + "s"


def _phase_steps(project_plan) -> List[str]:
    phases = getattr(project_plan, "phases", None)
    if not phases:
        return []
    return [f"Complete {phase.name}: {phase.objective}" for phase in phases]


def _bullets(items: List[str]) -> str:
    values = [item for item in items if item]
    return "\n".join(f"- {item}" for item in values) if values else "- Not specified"


def _numbered(items: List[str]) -> str:
    values = [item for item in items if item]
    return "\n".join(f"{index}. {item}" for index, item in enumerate(values, start=1)) if values else "1. Not specified"


def _join(lines: List[str]) -> str:
    return "\n".join(lines).strip() + "\n"
