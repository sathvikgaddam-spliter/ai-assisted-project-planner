# AI-Assisted Project Planner

AI-Assisted Project Planner is a full-stack AI planning product that turns a natural-language project description into a structured execution plan and engineering handoff package. It combines a React product UI, a FastAPI backend, Gemini-powered planning, deterministic fallback generation, Pydantic validation, role-based engineering prompts, prompt quality evaluation, one-line project understanding, implementation-ready build-pack generation, and an evaluation framework for benchmarking planning quality.

The system is designed for portfolio, classroom, and research demonstration use: users can describe a project, generate a plan, inspect phases/tasks/milestones/risks/dependencies, export results, download Prompt Pack and Build Pack ZIP files, and evaluate planner behavior across realistic benchmark scenarios.

## Key Features

- Apple-inspired React UI with polished product-page styling
- FastAPI backend with health and plan generation endpoints
- Gemini AI integration with configurable model selection
- Deterministic fallback planner when AI generation is unavailable
- Pydantic models for structured validation of generated plans
- Project analyzer for domain, type, complexity, and ambiguity detection
- Deterministic project understanding for one-line project ideas
- Project-type detection for SaaS, AI, dashboard, ecommerce, marketplace, mobile, backend, and generic web apps
- Role-based engineering prompts for frontend, backend, database, QA, DevOps, and security work
- Deterministic prompt quality evaluation with scores, issues, strengths, and suggestions
- Implementation-ready coding-agent job package generation
- Export actions for JSON, Markdown, Prompt Pack ZIP, Coding Agent ZIP, and summary copy
- Sample prompt cards for fast demos
- Warning/debug notes for local testing without exposing API keys
- Benchmark evaluation framework with scenarios, scoring, and reports
- CLI support retained alongside the API and frontend

## Architecture

```text
React Frontend
    |
    | POST /generate-plan
    | POST /generate-plan-zip
    | POST /generate-build-pack-zip
    v
FastAPI Backend
    |
    v
Planner Engine
    |
    +--> Gemini AI Provider
    |
    +--> Deterministic Fallback Planner
    |
    v
Pydantic ProjectPlan Validation
    |
    +--> Engineering Prompt Generator
    |
    +--> Prompt Quality Evaluator
    |
    +--> Build Pack Specification Generator
    |
    v
JSON Response / UI Dashboard / Markdown Export / Prompt Pack ZIP / Coding Agent ZIP / Benchmark Reports
```

The backend keeps the planner logic modular so the same planning engine can be used by the CLI, API, benchmark runner, and future integrations.

## Tech Stack

- **Frontend:** React, Vite, Framer Motion, CSS
- **Backend:** Python, FastAPI, Uvicorn
- **AI:** Google Gemini via `google-generativeai`
- **Validation:** Pydantic
- **Testing:** Pytest, FastAPI TestClient
- **Evaluation:** Custom benchmark runner, rubric-based scoring, Markdown/JSON reports

## Folder Structure

```text
.
├── docs/
│   └── README_PROJECT.md
├── evaluation/
│   ├── benchmark_runner.py
│   ├── scenarios.json
│   ├── scoring_rubric.md
│   └── sample_outputs/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.js
├── prompts/
├── reports/
│   ├── experiment_results.md
│   └── final_report.md
├── src/
│   ├── ai_provider.py
│   ├── api.py
│   ├── evaluator.py
│   ├── main.py
│   ├── models.py
│   ├── planner.py
│   ├── prompt_evaluator.py
│   ├── prompt_generator.py
│   ├── project_analyzer.py
│   ├── spec_generators.py
│   ├── utils.py
│   └── scorer.py
├── tests/
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone and enter the project

```bash
git clone <repo-url>
cd ai-assisted-project-planner
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

## Environment Variables

Create a `.env` file in the project root for local AI configuration:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

Do not commit `.env`. The project is configured to keep local environment files ignored. If `GEMINI_API_KEY` is missing or Gemini fails, the planner keeps working through the deterministic fallback planner.

Optional frontend API override:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The frontend defaults to `http://127.0.0.1:8000`.

## Run the Backend

```bash
uvicorn src.api:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/health
```

Generate a plan:

```bash
curl -X POST http://127.0.0.1:8000/generate-plan \
  -H "Content-Type: application/json" \
  -d "{\"project_description\":\"Build a hospital appointment scheduling system with doctor availability and patient reminders\"}"
```

Frontend API plan generation:

```bash
curl -X POST http://127.0.0.1:8000/api/generate-plan \
  -H "Content-Type: application/json" \
  -d "{\"description\":\"Build a racing game\"}"
```

The `/api/generate-plan` response wraps the full plan:

```json
{
  "message": "Plan generated successfully",
  "is_draft": true,
  "requires_clarification": true,
  "plan": {}
}
```

Download a Prompt Pack ZIP:

```bash
curl -X POST http://127.0.0.1:8000/generate-plan-zip \
  -H "Content-Type: application/json" \
  -o project-prompt-pack.zip \
  -d "{\"project_description\":\"Build a hospital appointment scheduling system with doctor availability and patient reminders\"}"
```

Download a Coding Agent ZIP:

```bash
curl -X POST http://127.0.0.1:8000/generate-build-pack-zip \
  -H "Content-Type: application/json" \
  -o project-coding-agent-job.zip \
  -d "{\"project_description\":\"Build a SaaS expense tracker\"}"
```

## Run the Frontend

```bash
cd frontend
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

The frontend calls:

```text
http://127.0.0.1:8000/api/generate-plan
http://127.0.0.1:8000/generate-plan-zip
http://127.0.0.1:8000/generate-build-pack-zip
```

Make sure the backend is running before generating a plan or downloading ZIP exports from the UI.

Frontend users can:

- generate a project plan.
- inspect phases, risks, dependencies, milestones, and recommendations.
- download JSON.
- download Markdown.
- download Prompt Pack ZIP.
- download Coding Agent ZIP.
- copy a summary.

Example frontend fetch:

```js
const response = await fetch("http://localhost:8000/api/generate-plan", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ description: "Build a racing game" }),
});

const payload = await response.json();
```

## Run the CLI

```bash
python src/main.py
```

The CLI uses the same planner engine as the API and keeps fallback behavior enabled.

The CLI saves:

- `outputs/<project>.plan.json`
- `outputs/<project>.plan.md`
- `outputs/<project>-project-plan.zip`
- `outputs/<project>-coding-agent-job.zip`

## Phase 5 — Engineering Prompt Pack

Phase 5 adds role-based engineering prompt generation and prompt quality evaluation.

The system does not build software automatically. It prepares implementation prompts that engineers can review, copy, and use externally in tools such as Codex, Cursor, Claude Code, GitHub Copilot, Lovable, or Bolt.

Generated prompts are role-based and use senior engineer framing, such as:

- "You are a senior frontend engineer..."
- "You are a senior backend engineer..."
- "You are a senior database engineer..."
- "You are a senior QA engineer..."
- "You are a senior DevOps engineer..."
- "You are a senior security engineer..."

Each generated prompt includes project context, role, goal, technical scope, related phases, constraints, expected output, acceptance criteria, and "Do Not Do" instructions. Prompt quality is evaluated with a deterministic score out of 100 across clarity, specificity, technical completeness, expected output quality, and acceptance criteria quality.

## Prompt Pack ZIP

The Prompt Pack ZIP contains the project plan, role-based implementation prompts, and prompt quality report.

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

Clarification-required plans still produce a ZIP with `project-plan/project_plan.md` and `project-plan/project_plan.json`, but they do not include engineering prompt files because there is not enough implementation detail yet.

Meaningful but incomplete draft plans may include provisional engineering prompts, prompt evaluations, and draft notes. Meaningless or unusable inputs remain clarification-only and do not receive prompt artifacts.

## Phase 6 — AI Coding-Agent Build Pack

Phase 6 adds deterministic project understanding and implementation-ready build-pack generation.

The system does not automatically build software. It prepares structured implementation documents that engineers can review and then provide to Codex, Claude Code, Cursor, GitHub Copilot, Lovable, Bolt, Gemini, or similar coding agents.

Users can enter a one-line project idea, such as "Build a SaaS expense tracker" or "Build a marketplace for used textbooks." The planner infers project type, domain, target users, likely user roles, workflows, core features, data entities, frontend needs, backend/API needs, testing needs, and deployment assumptions.

Supported deterministic project-type detection includes:

- backend platform
- AI application
- dashboard
- SaaS application
- mobile application
- ecommerce application
- marketplace
- generic web application

Unknown or unclear meaningful projects fall back to `generic web application`.

## Coding Agent ZIP

The Coding Agent ZIP is the main handoff artifact for Codex, Claude Code, Cursor, GitHub Copilot, Lovable, Bolt, Gemini, or similar coding agents. It is designed to tell the coding agent exactly what to build and to prevent documentation-only responses.

```text
START_HERE.md
COPY_THIS_PROMPT.md

generated_project/
  START_HERE.md
  COPY_THIS_PROMPT.md
  project_brief.md
  requirements.md
  mvp_scope.md
  architecture.md
  database_schema.md
  api_spec.md
  frontend_spec.md
  implementation_steps.md
  testing_plan.md
  deployment_plan.md
  assumptions.md
  coding_agent_prompt.md
  project_plan.md
  project_plan.json
```

Users should open `COPY_THIS_PROMPT.md`, paste it into Codex/Claude/Cursor, and attach or reference the rest of the ZIP contents. The prompt explicitly instructs the coding agent to build the requested app, generate actual source code, create build/runtime configuration, write tests, and add local run commands.

The generated documents are deterministic, project-adaptive, and designed to give coding agents enough structure to implement a complete MVP rather than a minimal prototype. `START_HERE.md` tells coding agents to generate actual source code, build/runtime configuration, run scripts, tests, and a README with local commands. The `coding_agent_prompt.md` file instructs coding agents to follow the architecture, database schema, API spec, frontend spec, testing plan, and assumptions.

## Project Boundary

This project helps users plan and prepare implementation. It does not automatically build, deploy, or guarantee production-ready software.

Generated plans, prompts, and build packs should be reviewed by engineers before use. Prompt packs and build packs are intended to improve handoff quality for external AI coding tools, not to replace architecture review, security review, QA, deployment judgment, or human ownership of the implementation.

Coding agents should follow the generated specifications, but human review is still required before treating any generated software as production-ready.

The platform should not be treated as an autonomous website builder, application generator, production deployment tool, or compliance guarantee.

## Run Tests

From the project root:

```bash
python -m pytest -q
```

Build the frontend:

```bash
cd frontend
npm run build
```

## Run Benchmark Evaluation

Run all benchmark scenarios:

```bash
python evaluation/benchmark_runner.py
```

The evaluation framework uses:

- `evaluation/scenarios.json` for benchmark prompts
- `evaluation/scoring_rubric.md` for quality criteria
- `src/evaluator.py` and `src/scorer.py` for rubric-based scoring
- `evaluation/sample_outputs/` for generated sample plans
- `evaluation/benchmark_results.json` for structured results
- `reports/experiment_results.md` for a Markdown summary

## Sample Prompts

Try these prompts in the UI or API:

- Build a hospital appointment scheduling system
- Build an AI study planner for students
- Build a food delivery analytics dashboard
- Build a healthcare chatbot MVP
- Build a personal expense tracker web app
- Create a RAG assistant for university course materials
- Design a BI dashboard for sales forecasting and inventory planning
- Plan a semester-long academic research project

## AI Fallback Behavior

The planner first attempts AI generation when Gemini is configured. If Gemini is unavailable, misconfigured, rate-limited, or returns invalid output, the system falls back to a deterministic planner.

Fallback behavior is intentional:

- The product continues to return a valid `ProjectPlan`.
- Local warnings include a sanitized failure reason.
- API keys are never printed or returned.
- The frontend shows an AI/Fallback mode badge based on response warnings.

This makes the app reliable for demos, testing, and offline development.

## Screenshots

Add screenshots or demo GIFs here:

```text
docs/screenshots/hero-preview.png
docs/screenshots/generated-plan-dashboard.png
docs/screenshots/export-actions.png
docs/screenshots/benchmark-report.png
```

Suggested screenshots:

- Apple-inspired landing page and product mockup
- Planner input with sample prompts
- Generated plan dashboard
- Timeline, risks, dependencies, and recommendations
- Export actions
- Benchmark evaluation report

## Future Improvements

- Add persistent project history and saved plans
- Add user authentication and workspace support
- Add streaming AI generation updates
- Add richer dependency graph visualization
- Add editable plans and manual task refinement
- Add PDF export
- Add model comparison experiments across multiple AI providers
- Add human evaluation workflows for academic studies
- Add deployment configuration for hosted frontend/backend environments
