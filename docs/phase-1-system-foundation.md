# Phase 1: System Foundation

## Phase Goal

Build the backend-only foundation for the planner without AI integration. The goal is to prove the application workflow, data contracts, exports, validation, CLI behavior, logging, configuration, and tests using a deterministic mock planning engine.

Phase 1 should make Phase 2 safer. AI integration should plug into existing interfaces instead of forcing a redesign.

## Repository Structure

Recommended structure:

```text
ai-assisted-project-planner/
  docs/
  src/
    planner/
      __init__.py
      cli/
      app/
      domain/
      planning/
      validation/
      export/
      config/
      logging/
  tests/
    unit/
    integration/
    fixtures/
  outputs/
  prompts/
```

Exact language and framework choices can be finalized during implementation, but the module boundaries should remain stable.

## Code Module Design

### CLI Module

Responsibilities:

- Parse command arguments.
- Accept direct text input.
- Accept future file-based input.
- Call the application service.
- Print summary, validation errors, clarification questions, and output locations.
- Return meaningful exit codes.

### Application Module

Responsibilities:

- Coordinate the planning workflow.
- Convert CLI input into internal request objects.
- Call validators, understanding service, planning engine, and exporters.
- Return structured success or failure results.

### Domain Module

Responsibilities:

- Define project planning domain models.
- Keep business concepts independent of CLI, AI provider, and export formatting.

### Planning Module

Responsibilities:

- Define planning engine interface.
- Implement mock planning engine.
- Select domain-specific plan templates for Phase 1.

### Validation Module

Responsibilities:

- Validate input contracts.
- Validate project understanding objects.
- Validate execution plans.
- Validate export payloads.

### Export Module

Responsibilities:

- Generate JSON.
- Generate Markdown.
- Manage output filenames.
- Report export failures.

### Configuration Module

Responsibilities:

- Load environment variables and local configuration files.
- Resolve output paths.
- Validate required settings.
- Provide typed configuration objects.

## Domain Models

Phase 1 should define stable models even before AI is connected.

### PlanningRequest

Represents user input and execution options:

- description
- optional project name
- optional output directory
- requested output formats
- optional metadata

### ProjectUnderstanding

Represents what the system believes about the project:

- domain
- project type
- intent
- target users
- deliverables
- constraints
- missing information
- assumptions
- risks
- confidence
- requires clarification

### ClarificationQuestion

Represents one question the user should answer:

- question text
- reason
- category
- priority

### ExecutionPlan

Represents the final structured plan:

- project summary
- phases
- milestones
- timeline estimate
- dependencies
- risks
- recommendations
- assumptions
- metadata

### Phase

Represents a major stage of work:

- id
- name
- objective
- tasks
- deliverables
- estimated duration

### Task

Represents executable work:

- id
- title
- description
- owner role
- dependencies
- estimated effort
- acceptance criteria

### Risk

Represents uncertainty or project threat:

- description
- impact
- likelihood
- mitigation

## Input Contracts

Minimum input contract:

- Description must not be empty.
- Description must contain enough semantic content to classify intent.
- Input length should be bounded to prevent accidental large payloads.
- CLI flags must be valid.
- Output directory must be writable.

Vague input should not be treated as an error if it is valid text. It should route to clarification.

## Output Contracts

Successful planning returns:

- Structured plan object.
- JSON export path.
- Markdown export path.
- validation summary.
- warnings, if any.

Clarification-required result returns:

- project understanding summary.
- clarification questions.
- reason planning was paused.
- no final plan export unless explicitly requested in a future mode.

Failure result returns:

- error category.
- user-facing message.
- optional diagnostic details in logs.

## JSON Export Design

JSON should be the canonical export for automated tests and future integrations. It should include:

- schema version.
- generated timestamp.
- source description.
- project understanding.
- plan phases.
- tasks.
- milestones.
- dependencies.
- risks.
- recommendations.
- assumptions.
- validation metadata.

The JSON format should be stable, versioned, and validated before writing.

## Markdown Export Design

Markdown should be optimized for human review:

- Project Overview
- Understanding Summary
- Assumptions
- Execution Roadmap
- Phase Details
- Milestones
- Timeline Estimate
- Dependencies
- Risks and Mitigations
- Recommendations
- Validation Notes

Markdown should be generated from the same validated plan object as JSON.

## Mock Planning Engine

The mock planning engine should simulate domain-aware behavior without calling AI.

It should:

- Classify obvious project types using deterministic rules.
- Produce domain-specific phase templates.
- Return clarification questions for vague input.
- Produce stable output for repeatable tests.
- Avoid pretending to be intelligent beyond its Phase 1 purpose.

Example deterministic behavior:

- "expense tracker app" maps to software MVP phases.
- "Power BI dashboard" maps to analytics phases.
- "marketing campaign" maps to business campaign phases.
- "research study" maps to academic research phases.
- "something for students" returns clarification questions.

## CLI Interaction Design

Initial command:

```text
planner plan --description "Build a food delivery MVP for a college campus"
```

Expected successful summary:

```text
Project type: Software MVP
Status: Plan generated
JSON: outputs/food-delivery-mvp.plan.json
Markdown: outputs/food-delivery-mvp.plan.md
```

Expected clarification summary:

```text
Project type: Unknown or incomplete
Status: Clarification required
Questions:
1. Who are the target users?
2. What outcome should the project deliver?
3. Is this software, research, business, or analytics work?
```

## Logging

Logs should capture:

- Request start and completion.
- Validation failures.
- Project classification result.
- Clarification decision.
- Export paths.
- Unexpected exceptions.

Logs should not expose API keys or sensitive user content beyond what is necessary for debugging.

## Configuration Handling

Phase 1 configuration should include:

- output directory.
- log level.
- schema version.
- default export formats.
- feature flags for future AI integration.

Phase 2 configuration will add provider names, model names, API keys, timeouts, retry limits, and prompt template paths.

## Unit Testing Strategy

Unit tests should cover:

- Input validation.
- Domain model serialization.
- Mock project classification.
- Clarification decision behavior.
- Plan validation.
- JSON export formatting.
- Markdown export formatting.
- CLI success and failure paths.
- Configuration loading.
- Error mapping.

Integration tests should run CLI workflows using fixtures from `docs/test-scenarios.md`.

## Success Criteria Before AI Integration

Phase 1 is complete when:

- CLI can accept descriptions and return structured results.
- Empty and vague inputs are handled correctly.
- Mock engine generates domain-specific plans.
- JSON and Markdown exports are deterministic.
- Validation prevents malformed plans from being exported.
- Unit tests cover core workflow behavior.
- Integration tests prove the CLI works end to end.
- AI engine can be introduced behind an existing planning interface without changing CLI contracts.
