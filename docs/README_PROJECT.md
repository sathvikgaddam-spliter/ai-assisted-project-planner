# AI-Assisted Project Planner

## Executive Overview

AI-Assisted Project Planner is a backend-first planning system that transforms a user's project description into a structured execution plan. The product is designed to reason before it plans: it must understand the project domain, project type, target users, deliverables, constraints, risks, and missing information before generating phases, tasks, milestones, dependencies, timeline estimates, and recommendations.

The first release will not include a user interface. Phase 0 establishes the architecture and implementation roadmap. Phase 1 will build a deterministic CLI/backend foundation with mock planning behavior. Phase 2 will integrate AI planning with structured prompts, provider abstraction, schema validation, and clarification workflows. Phase 3 will evaluate planning quality using realistic scenarios before any UI investment.

## Problem Statement

Most AI planning tools produce generic task lists from shallow prompts. This creates plans that look useful but often miss the actual domain, ignore constraints, invent assumptions, sequence work incorrectly, or fail to ask clarifying questions when the request is vague.

The core product problem is not simply "generate a plan." The problem is to create a reliable planning workflow that:

- Identifies what kind of project is being planned.
- Separates known facts from assumptions.
- Detects missing information and asks clarifying questions when needed.
- Adapts the plan structure to the domain.
- Produces structured, validated outputs that can be tested and exported.
- Avoids hallucinated details and unsupported recommendations.

## Project Objective

Build a reliable backend planning engine that accepts a project description and produces a validated project plan only after completing a project understanding step.

The system should support:

- CLI-based project planning workflow.
- Domain-aware project classification.
- Clarification question generation for vague or incomplete inputs.
- Structured plan generation.
- JSON and Markdown exports.
- Validation of AI responses against strict schemas.
- Test scenarios that evaluate both software behavior and reasoning quality.

## Target Users

- Students planning academic, capstone, research, or independent study projects.
- Software teams planning MVPs, platforms, or internal tools.
- Data analysts planning dashboards, ETL workflows, and reporting systems.
- Business users planning campaigns, launches, and operational initiatives.
- Technical leads evaluating planning quality before committing to implementation.
- Future UI users who need guided project planning without starting from a blank page.

## Key Product Capabilities

- Project intake from plain-language descriptions.
- Project understanding before plan generation.
- Domain and project-type classification.
- Extraction of goals, deliverables, users, constraints, risks, dependencies, and missing information.
- Clarification workflow when the project is too vague or contradictory.
- Domain-specific planning strategies.
- Structured execution plans with phases, tasks, milestones, dependencies, risks, and recommendations.
- JSON output for machine-readable integration.
- Markdown output for human review and reporting.
- Validation layer to reject malformed or low-confidence outputs.
- Provider abstraction for Gemini, OpenAI, or future model providers.
- Evaluation suite focused on planning quality, not only command success.

## Development Roadmap

### Phase 0: Architecture and Planning

Define the product architecture, module boundaries, phased roadmap, test scenarios, and engineering decisions. No implementation code is created in this phase.

### Phase 1: System Foundation

Build a backend-only CLI application with deterministic mock planning behavior. Establish data models, contracts, validation, logging, configuration, exports, and unit tests. The goal is to prove the workflow and output contracts before connecting an AI model.

### Phase 2: AI Planning Engine

Add the AI orchestration layer. Implement project understanding, clarification question generation, provider abstraction, prompt template management, structured response parsing, schema validation, retries, and fallback behavior.

### Phase 3: Evaluation and Delivery

Run prompt experiments, evaluate output quality across realistic scenarios, document limitations, prepare final reports and demos, and define the future UI roadmap.

## Final Deliverables

- Architecture documentation.
- Backend CLI workflow.
- Domain models and structured output contracts.
- JSON and Markdown export formats.
- Mock planning engine for deterministic testing.
- AI planning engine with provider abstraction.
- Prompt templates and orchestration strategy.
- Validation and error handling layer.
- Realistic reasoning-focused test suite.
- Evaluation report with quality metrics and prompt comparison results.
- Demo-ready CLI examples.
- Future UI roadmap.
