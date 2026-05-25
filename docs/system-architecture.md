# System Architecture

## High-Level Architecture

The system is organized as a backend planning pipeline with strict separation between intake, understanding, planning, validation, export, and delivery.

At a high level:

1. A user provides a project description through the CLI.
2. The input layer normalizes and validates the request.
3. The project understanding layer classifies the project and extracts known facts, assumptions, constraints, risks, and missing information.
4. The orchestration layer decides whether the system has enough information to generate a plan.
5. If information is missing, the system returns clarification questions instead of generating a speculative plan.
6. If sufficient information is available, the planning engine creates a structured execution plan.
7. The validation layer checks the plan against schemas and quality rules.
8. The output layer exports JSON and Markdown artifacts.

This architecture intentionally treats planning as a multi-step workflow rather than a single AI completion.

## Module Boundaries

### CLI Interface

Responsible for command parsing, collecting user input, selecting output paths, and displaying workflow status. The CLI does not contain planning logic.

### Application Service Layer

Coordinates the end-to-end use case. It calls intake validation, project understanding, clarification handling, planning, validation, and export services.

### Domain Layer

Defines core domain concepts such as project brief, project understanding, clarification question, execution plan, phase, task, milestone, dependency, risk, recommendation, and export result.

### Planning Engine

Generates a plan from a validated project understanding. In Phase 1 this is a mock deterministic engine. In Phase 2 this becomes an AI-assisted engine behind the same interface.

### AI Orchestration Layer

Manages prompt selection, provider calls, retries, response parsing, and model-specific concerns. This layer is isolated from the domain and CLI so providers can be replaced without changing application workflow.

### Validation Layer

Validates input, intermediate understanding objects, AI responses, final plans, and export payloads. It combines schema validation with business rules.

### Output Generation Layer

Converts validated plans into JSON and Markdown. This layer should be deterministic and should not call AI services.

### Configuration Layer

Loads provider settings, model names, API keys, retry limits, output paths, logging levels, and feature flags.

## Core Components

### Project Intake

Receives raw user text and optional metadata. It checks for empty input, minimum usable length, malformed content, and unsupported command options.

### Project Understanding Service

Produces a structured understanding object containing:

- Project domain.
- Project type.
- User intent.
- Target users.
- Expected deliverables.
- Known constraints.
- Technical and non-technical requirements.
- Missing information.
- Risks and assumptions.
- Confidence score.

### Clarification Service

Determines whether clarification is required. It generates targeted questions when the input is vague, contradictory, unrealistic, or missing critical constraints.

### Planning Service

Generates the actual execution plan only after the understanding stage has passed validation. It uses domain-specific planning strategies so a software project, BI dashboard, business campaign, and research project do not receive the same generic phase structure.

### Plan Validator

Checks for structural correctness and planning quality. It verifies that phases contain tasks, tasks have meaningful descriptions, dependencies refer to existing tasks, milestones map to completed outcomes, and risks include mitigation strategies.

### Export Service

Produces:

- Machine-readable JSON for testing and future integrations.
- Human-readable Markdown for reports and review.

## Execution Workflow

1. User runs the CLI with a project description.
2. CLI builds a planning request.
3. Input validator rejects empty or unusable input.
4. Project understanding service analyzes the request.
5. Understanding validator checks classification, confidence, and completeness.
6. Clarification service decides whether to ask questions.
7. If clarification is required, the system returns questions and exits without generating a plan.
8. If planning can continue, planning service generates a structured plan.
9. Plan validator checks schema and quality rules.
10. Export service writes JSON and Markdown outputs.
11. CLI prints a concise summary and output locations.

## Data Flow

Raw input moves through the system as progressively more structured data:

```text
User Text
  -> PlanningRequest
  -> ProjectBrief
  -> ProjectUnderstanding
  -> ClarificationDecision or PlanningContext
  -> ExecutionPlan
  -> ValidatedPlan
  -> JSON Export and Markdown Export
```

Each transition has an explicit contract. The system should not pass raw AI text directly into exports without parsing and validation.

## CLI and Backend Interaction Flow

The CLI should support a simple initial command shape:

```text
planner plan --description "Build an expense tracker for college students" --out ./outputs
```

Expected behavior:

- Display validation errors for empty or invalid input.
- Display clarification questions when planning cannot responsibly continue.
- Generate output files when planning succeeds.
- Return non-zero exit codes for validation, configuration, provider, or export failures.
- Avoid interactive UI assumptions in early phases.

Future CLI extensions may support:

- Reading descriptions from files.
- Supplying constraints as flags.
- Choosing output format.
- Selecting AI provider.
- Running test scenarios.
- Comparing prompt templates.

## AI Orchestration Layer

The AI orchestration layer is responsible for all model interaction. It should expose provider-neutral operations:

- Understand project.
- Generate clarification questions.
- Generate plan.
- Repair malformed structured output.
- Evaluate plan quality.

The orchestrator should use prompt templates with explicit response schemas. It must request structured output and parse responses into typed objects. Provider-specific details such as model names, authentication, timeout behavior, safety settings, and response formats belong in provider adapters.

## Validation Layer

Validation happens at multiple points:

- Input validation rejects empty or unusable descriptions.
- Understanding validation verifies domain, project type, confidence, and missing information.
- Clarification validation ensures questions are specific, useful, and not excessive.
- Plan validation verifies schema integrity and planning consistency.
- Export validation ensures written artifacts match the final plan.

Validation must be strict enough to prevent malformed AI output from becoming a final deliverable.

## Output Generation Layer

JSON exports should preserve the full structured plan and metadata for testing. Markdown exports should provide a readable project planning document with sections for overview, assumptions, phases, tasks, milestones, dependencies, risks, recommendations, and timeline.

The output layer should be deterministic. Given the same validated plan, it should always produce equivalent JSON and Markdown content.

## Error Handling Flow

Errors should be represented by typed failure categories:

- Input validation error.
- Configuration error.
- AI provider unavailable.
- AI provider timeout.
- Malformed AI response.
- Schema validation failure.
- Insufficient project information.
- Export write failure.
- Unexpected application error.

The CLI should translate these failures into concise user-facing messages and actionable next steps. Internal logs should preserve technical details for debugging.

## Extensibility Roadmap

The architecture should allow:

- Additional project domains and planning strategies.
- Additional AI providers.
- Prompt template versioning and experimentation.
- Interactive clarification sessions.
- Persistent planning sessions.
- Web API layer.
- UI frontend.
- Collaboration and review workflows.
- Integration with project management tools.
- Plan evaluation and scoring.

## Architecture Decision Rationale

The system separates understanding from planning because project type determines what a good plan looks like. A BI dashboard requires data source discovery, metric definition, modeling, visualization, and validation. A software MVP requires requirements, architecture, implementation, testing, deployment, and iteration. A research project requires literature review, methodology, data collection, analysis, and write-up.

The architecture also separates AI orchestration from application services because model providers will change. The product should not encode business workflow around a single provider API.

Validation is treated as a first-class layer because AI output is probabilistic. The system should only deliver plans that satisfy explicit contracts.
