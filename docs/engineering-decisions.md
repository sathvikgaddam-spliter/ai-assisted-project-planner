# Engineering Decisions

## Architecture-First

The project is architecture-first because the core challenge is not creating screens or calling an AI API. The hard part is designing a reliable planning workflow where project understanding, clarification, planning, validation, and export are separate responsibilities.

Starting with architecture reduces the risk of building a visually convincing product that produces weak or untrustworthy plans.

## Backend-First

The backend contains the product intelligence:

- project understanding.
- AI orchestration.
- validation.
- planning workflow.
- exports.
- evaluation.

If these are unreliable, a UI will only make unreliable output easier to generate. Backend-first development allows the team to test planning quality directly before adding interface complexity.

## CLI Before UI

A CLI is the fastest way to validate the planning workflow. It supports repeatable test execution, fixture-based scenarios, CI integration, and straightforward debugging.

The CLI also forces clean input and output contracts. Those contracts can later be reused by a web API or UI.

## Phased Implementation

The project is split into phases to reduce risk:

- Phase 0 defines architecture and planning.
- Phase 1 builds deterministic backend foundations.
- Phase 2 adds AI orchestration.
- Phase 3 evaluates quality and prepares delivery.

This sequencing prevents AI behavior from obscuring basic engineering issues such as weak domain models, unclear output contracts, and missing validation.

## Structured Outputs

Plans must be structured because they need to be validated, exported, compared, tested, and eventually edited. Free-form AI prose is not enough.

Structured outputs allow:

- schema validation.
- dependency checking.
- JSON export.
- Markdown generation.
- automated evaluation.
- future UI rendering.

## Validation Layers

Validation is required because AI output is probabilistic. The system must verify that outputs are complete, consistent, and safe to use.

Validation should happen at multiple layers:

- input validation.
- project understanding validation.
- clarification validation.
- plan validation.
- export validation.

This makes failures explicit and prevents malformed AI responses from becoming final deliverables.

## Prompt Templates

Prompt templates should be versioned artifacts, not hidden strings inside application code.

This supports:

- prompt comparison experiments.
- regression testing.
- provider-specific variants.
- traceability from output to prompt version.
- review by technical and non-technical stakeholders.

## Provider Abstraction

The system should support Gemini, OpenAI, and future providers behind a common interface. Provider APIs, model behavior, structured output support, rate limits, and safety controls change over time.

A provider abstraction prevents the application workflow from becoming tightly coupled to one vendor.

## Design Tradeoffs

### More Workflow Complexity, Better Reliability

Separating understanding, clarification, planning, and validation adds complexity. The tradeoff is worthwhile because it prevents generic plans and makes failures easier to diagnose.

### Strict Validation, More Rejections

Strict validation may reject some usable AI responses. This is acceptable for early development because reliable output matters more than maximizing successful completions.

### CLI First, Less Immediate Visual Appeal

Skipping UI reduces demo polish in the short term. The benefit is that the system can be tested deeply before presentation layers are added.

### Mock Engine First, Slower AI Feature Arrival

Building a mock engine before AI integration may feel indirect, but it proves contracts and workflow behavior. AI can then be introduced without changing the whole application.

## Scalability Considerations

The initial system is CLI/backend oriented, but the architecture should support growth.

Future scalability concerns:

- larger prompt and scenario libraries.
- multiple AI providers.
- concurrent planning requests.
- persistent planning sessions.
- user accounts and team collaboration.
- plan versioning.
- integration with project management tools.
- web API and UI clients.
- evaluation dashboards.

Scalability should be addressed through clear module boundaries, provider abstraction, structured outputs, and stateless planning services where possible.

## Product Quality Principle

The planner should prefer asking a useful clarification question over generating a confident but unsupported plan. A paused planning workflow is better than a polished plan built on incorrect assumptions.
