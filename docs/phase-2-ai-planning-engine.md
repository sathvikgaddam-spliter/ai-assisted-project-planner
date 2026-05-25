# Phase 2: AI Planning Engine

## Phase Goal

Add AI-assisted reasoning while preserving the backend workflow created in Phase 1. The planner must first understand the project before generating output. If the input is vague, contradictory, or missing critical planning information, the system must ask clarification questions instead of generating a speculative plan.

## Prompt Orchestration Design

Planning should be decomposed into separate AI tasks:

1. Project understanding.
2. Clarification decision.
3. Plan generation.
4. Optional repair of malformed structured output.
5. Optional quality evaluation.

Each task should have a dedicated prompt template, response schema, validation rules, and retry policy.

The orchestrator should control sequencing. The AI provider should only execute model calls.

## Prompt Template Management

Prompt templates should live outside application logic, ideally under a versioned `prompts/` directory:

```text
prompts/
  project-understanding.v1.md
  clarification-questions.v1.md
  plan-generation.v1.md
  response-repair.v1.md
  quality-evaluation.v1.md
```

Templates should define:

- system role.
- task objective.
- required reasoning boundaries.
- allowed assumptions.
- response schema.
- examples for domain-specific planning.
- rules for when not to generate a plan.

Prompt versions should be recorded in output metadata so plan quality can be traced to a prompt variant.

## Project Understanding Workflow

The first AI call should produce a `ProjectUnderstanding` object. It should identify:

- domain.
- project type.
- user intent.
- target users.
- expected deliverables.
- technical constraints.
- non-technical constraints.
- missing information.
- assumptions.
- risks.
- confidence.
- recommended next action.

The recommended next action should be one of:

- ask clarification questions.
- generate plan.
- reject invalid input.

Example:

Input:

```text
I want to build something for students.
```

Expected understanding:

- Domain is unclear.
- Project type is unclear.
- Target users are broadly "students" but not specific enough.
- Deliverables are unknown.
- Constraints are unknown.
- Clarification is required.

The system should not generate phases for a software app, campaign, research project, or dashboard because the user did not specify which kind of project they need.

## Clarification Question Workflow

Clarification questions should be targeted and limited. The system should ask only questions needed to choose a responsible planning path.

Questions should cover:

- project domain.
- intended outcome.
- target users.
- deliverables.
- timeline.
- constraints.
- available resources.

The system should avoid long questionnaires. For a vague request, three to seven high-value questions are enough.

Clarification output should include:

- question text.
- reason the question matters.
- category.
- priority.

## AI Provider Abstraction Layer

The AI integration should use a provider-neutral interface. The application should not depend directly on Gemini, OpenAI, or any specific SDK.

Provider abstraction should support:

- model invocation.
- structured response mode where available.
- timeout settings.
- retry behavior.
- provider error normalization.
- token or usage metadata.
- safety and content filtering metadata when available.

The interface should return a normalized provider response containing:

- raw text or structured payload.
- parsed content when possible.
- provider name.
- model name.
- prompt version.
- request duration.
- token usage, if available.
- error details, if any.

## Gemini and OpenAI Integration Strategy

Gemini and OpenAI should be implemented as separate provider adapters behind the same interface.

Gemini strategy:

- Use Gemini for structured planning calls where configured.
- Keep model name configurable.
- Normalize safety, timeout, and malformed response errors.

OpenAI strategy:

- Use OpenAI structured output capabilities where configured.
- Keep model name configurable.
- Normalize refusal, tool, timeout, and schema errors.

The application should be able to switch providers through configuration without changing planning code.

## Structured Response Generation

AI responses should be requested in structured format matching the internal domain contracts. The planner should never rely on free-form text as the source of truth.

Structured outputs should be used for:

- project understanding.
- clarification questions.
- execution plan.
- plan quality evaluation.

Free-form text may appear inside fields such as task descriptions, risk descriptions, or recommendations, but the containing object must be schema-valid.

## Schema Validation

Every AI response must be validated before use.

Validation should check:

- required fields.
- enum values.
- non-empty phase and task names.
- valid dependency references.
- timeline consistency.
- risk mitigation presence.
- no final plan when clarification is required.
- confidence threshold behavior.

Malformed AI output should route to repair or retry, not export.

## Fallback Handling

Fallback behavior should be explicit:

- If the provider is unavailable, return a provider failure.
- If response parsing fails, attempt one repair call.
- If repair fails, return malformed AI response.
- If understanding confidence is low, ask clarifying questions.
- If the timeline is unrealistic, flag a warning or ask clarification.
- If configuration is missing, fail before making provider calls.

The mock planning engine from Phase 1 can remain available as a development fallback, but production AI failures should not silently degrade into mock plans unless a user explicitly selects mock mode.

## Retry Strategies

Retries should be limited and typed:

- Retry transient provider failures.
- Retry timeouts only within configured limits.
- Retry malformed output once with a repair prompt.
- Do not retry validation failures caused by insufficient user input.
- Do not retry missing API keys or invalid configuration.

Retries should use backoff and should log each attempt.

## Integration Testing

Integration tests should verify:

- provider adapter success path.
- provider timeout behavior.
- malformed AI response handling.
- schema validation failures.
- clarification workflow for vague input.
- domain-specific plan generation.
- no plan is exported when clarification is required.
- JSON and Markdown exports from AI-generated plans.
- provider configuration errors.

AI integration tests should use recorded fixtures or controlled test doubles where possible. Live provider tests should be clearly marked and excluded from default local test runs unless credentials are configured.

## Success Criteria Before UI

Phase 2 is complete when:

- The planner performs project understanding before planning.
- Vague input returns clarification questions.
- Domain-specific plans are generated for realistic project scenarios.
- AI responses are schema validated.
- Malformed outputs do not reach final exports.
- Provider selection is configuration-driven.
- Gemini and OpenAI can be supported behind the same abstraction.
- Retry and fallback behavior is tested.
- JSON and Markdown outputs remain stable.
- Test scenarios show acceptable reasoning quality across software, AI, analytics, business, academic, healthcare, and edge cases.
