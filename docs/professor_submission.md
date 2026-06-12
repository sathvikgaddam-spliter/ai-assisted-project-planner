# AI-Assisted Project Planner

## Important Note for Evaluation

This project should be evaluated from the Git branch `phase-5-engineering-prompt-pack`.

The `main` branch is not the final full-stack submission branch. The completed work, including the React frontend, FastAPI backend, Prompt Pack ZIP export, Coding Agent Build Pack ZIP export, prompt evaluation, and tests, is on `phase-5-engineering-prompt-pack`.

The command `python src/main.py` runs only the CLI version of the planner. For the complete project demonstration, run the backend with Uvicorn and the frontend with Vite as described in the README.

## 1. Title Page

**Project Title:** AI-Assisted Project Planner  
**Project Type:** Full-Stack AI-Based Web Application  
**Submitted By:** [Your Name]  
**Submitted To:** [Professor Name]  
**Course:** [Course Name]  
**Institution:** [College/University Name]  
**Date:** [Submission Date]

## 2. Abstract

AI-Assisted Project Planner is a full-stack software project that converts a natural-language project idea into a structured execution plan. The application helps users move from a rough idea to an organized project plan containing phases, tasks, milestones, risks, dependencies, recommendations, and implementation guidance.

The system uses a React frontend, a FastAPI backend, Google Gemini AI integration, Pydantic validation, deterministic fallback planning, prompt generation, and benchmark evaluation. If the AI service is unavailable, the application still produces a valid plan using its fallback planner. The project also supports exporting generated plans as JSON, Markdown, Prompt Pack ZIP files, and Coding Agent Build Pack ZIP files.

This project is designed for academic, portfolio, and demonstration purposes. It shows how AI can support software planning, improve project handoff quality, and assist developers in preparing implementation-ready documentation.

## 3. Introduction

Project planning is an important step in software development. Many students and developers begin with a general idea but struggle to convert it into clear phases, technical tasks, risks, dependencies, and deliverables. Poor planning can lead to missed requirements, unclear scope, and inefficient implementation.

AI-Assisted Project Planner addresses this problem by using AI and deterministic logic to create structured project plans from simple user descriptions. A user can enter an idea such as "Build a hospital appointment scheduling system" or "Build a SaaS expense tracker", and the system generates a detailed planning package.

The project combines modern frontend and backend technologies with AI-based generation. It also includes validation, testing, prompt evaluation, and downloadable artifacts that can be reused by developers or AI coding assistants.

## 4. Problem Statement

Students and developers often have project ideas but may not know how to break those ideas into structured development plans. Manual planning can be time-consuming and inconsistent. Existing AI tools can generate text, but they may not always produce reliable, structured, or implementation-ready outputs.

The problem addressed by this project is:

**How can a system convert a natural-language project idea into a structured, validated, and useful software project plan that can support implementation and academic documentation?**

## 5. Objectives

- To build a full-stack web application for AI-assisted project planning.
- To allow users to enter project descriptions in natural language.
- To generate structured project plans with phases, tasks, milestones, risks, dependencies, and recommendations.
- To integrate Gemini AI for intelligent planning.
- To provide deterministic fallback planning when AI is unavailable.
- To validate generated plans using Pydantic models.
- To generate role-based engineering prompts for implementation support.
- To export project plans in JSON, Markdown, and ZIP formats.
- To provide a React-based user interface for easy interaction.
- To test the system using unit tests, API tests, and benchmark evaluation.

## 6. Scope of the Project

The project focuses on planning and preparation for software implementation. It does not automatically build or deploy a complete software application. Instead, it generates structured plans and handoff materials that can be reviewed by students, developers, or instructors.

The scope includes:

- Project idea analysis.
- Project plan generation.
- Backend API development.
- Frontend user interface development.
- AI integration and fallback handling.
- Prompt pack generation.
- Coding-agent build pack generation.
- Export functionality.
- Testing and evaluation.

The project does not include:

- Production deployment.
- User authentication.
- Persistent project history.
- Real-time collaboration.
- Automatic software implementation.

## 7. Technology Stack

| Layer | Technologies Used |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn |
| AI Integration | Google Gemini API |
| Validation | Pydantic |
| Testing | Pytest, FastAPI TestClient |
| Evaluation | Benchmark runner, rubric-based scoring |
| Export | JSON, Markdown, ZIP files |
| Development Tools | Git, GitHub, VS Code |

## 8. System Architecture

The system follows a client-server architecture.

```text
React Frontend
    |
    | HTTP API Requests
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
Pydantic Validation
    |
    +--> Prompt Generator
    +--> Prompt Evaluator
    +--> Build Pack Generator
    |
    v
JSON Response / Markdown Export / ZIP Download
```

The frontend collects user input and displays generated planning results. The backend receives requests, analyzes the project description, generates a plan, validates the result, and returns structured data to the frontend.

## 9. Module Description

### Frontend Module

The frontend is built with React and Vite. It provides the user interface where users can enter project descriptions, generate plans, view results, and download exports. It includes components for the planner form, result dashboard, phase timeline, risk cards, milestone tracking, and export actions.

### API Module

The API module is built with FastAPI. It exposes endpoints for health checks, plan generation, prompt pack generation, and coding-agent build pack generation.

### Planner Module

The planner module is the core logic of the system. It accepts a project description and produces a structured project plan. It can use Gemini AI when configured or use deterministic fallback logic when AI generation is unavailable.

### AI Provider Module

The AI provider connects the application to the Gemini API. It sends planning prompts to the AI model and receives generated planning content.

### Project Analyzer Module

The project analyzer identifies project type, domain, complexity, ambiguity, and other planning details. This helps the system generate more relevant plans.

### Models Module

The models module defines structured data models using Pydantic. These models ensure generated project plans follow a valid structure.

### Prompt Generator Module

The prompt generator creates role-based engineering prompts for frontend, backend, database, QA, DevOps, and security work.

### Prompt Evaluator Module

The prompt evaluator checks generated prompts for quality, clarity, technical completeness, expected output, and acceptance criteria.

### Spec Generator Module

The spec generator creates implementation-ready build-pack documents such as requirements, architecture, API specifications, frontend specifications, testing plans, deployment plans, and coding-agent prompts.

### Testing Module

The testing module contains unit tests and API tests to verify planner behavior, fallback behavior, model validation, prompt generation, and backend endpoints.

## 10. Features and Functionality

- Natural-language project input.
- AI-assisted project plan generation.
- Deterministic fallback plan generation.
- Project domain and type detection.
- Complexity and ambiguity analysis.
- Structured phase and task generation.
- Milestone, risk, dependency, and recommendation generation.
- JSON export.
- Markdown export.
- Prompt Pack ZIP download.
- Coding Agent Build Pack ZIP download.
- React dashboard for result visualization.
- FastAPI backend endpoints.
- CLI support.
- Benchmark evaluation framework.
- Unit and API test coverage.

## 11. Implementation Details

The application is implemented as a full-stack system. The backend is written in Python using FastAPI. It defines endpoints that receive project descriptions and return structured responses. The planning logic first attempts to use Gemini AI if the API key is available. If Gemini is missing, misconfigured, rate-limited, or returns invalid data, the fallback planner produces a valid deterministic plan.

Pydantic models are used to validate the structure of generated plans. This improves reliability because the frontend receives predictable data. The frontend is built with React and displays plans in a readable dashboard format. Users can inspect timelines, risks, dependencies, milestones, and recommendations.

The system also generates implementation handoff materials. The Prompt Pack ZIP contains role-based engineering prompts and prompt quality reports. The Coding Agent Build Pack ZIP contains documents that can guide AI coding tools or developers during implementation.

## 12. API Description

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Checks backend health status |
| `/api/health` | GET | Checks API health status |
| `/generate-plan` | POST | Generates a structured project plan |
| `/api/generate-plan` | POST | Generates a frontend-compatible project plan response |
| `/generate-plan-zip` | POST | Downloads a Prompt Pack ZIP |
| `/generate-build-pack-zip` | POST | Downloads a Coding Agent Build Pack ZIP |

Example request:

```json
{
  "project_description": "Build a hospital appointment scheduling system"
}
```

Example response structure:

```json
{
  "message": "Plan generated successfully",
  "is_draft": true,
  "requires_clarification": false,
  "plan": {}
}
```

## 13. Testing and Evaluation

Testing is performed using Pytest and FastAPI TestClient. The test suite verifies important parts of the project, including:

- Planner output generation.
- AI fallback behavior.
- API endpoint responses.
- Pydantic model validation.
- Prompt generation.
- Prompt quality evaluation.
- ZIP export generation.
- CLI output behavior.

The project also includes a benchmark evaluation framework. Benchmark scenarios are stored in JSON format and scored using a rubric-based scoring system. This helps evaluate the quality and completeness of generated project plans.

Test command:

```bash
python -m pytest -q
```

Frontend build command:

```bash
cd frontend
npm run build
```

## 14. Screenshots

[Insert Screenshot: GitHub Repository]

[Insert Screenshot: Home Page]

[Insert Screenshot: Project Description Input Form]

[Insert Screenshot: Generated Plan Dashboard]

[Insert Screenshot: Phase Timeline]

[Insert Screenshot: Risks and Dependencies]

[Insert Screenshot: Export Options]

[Insert Screenshot: Prompt Pack ZIP Output]

[Insert Screenshot: API Test Output]

[Insert Screenshot: Pytest Output]

## 15. Advantages

- Saves time in project planning.
- Converts vague ideas into structured plans.
- Works even when AI is unavailable due to fallback planning.
- Produces validated and predictable output.
- Supports both web interface and backend API usage.
- Generates useful handoff documents for developers.
- Includes testing and evaluation support.
- Useful for academic projects, portfolio projects, and demonstrations.

## 16. Limitations

- The system does not automatically build the final software product.
- Generated plans should be reviewed by humans before implementation.
- AI output quality depends on the input description and model behavior.
- Gemini API requires configuration through an API key.
- The current version does not include authentication or saved project history.
- The application is intended for planning and demonstration, not production deployment.

## 17. Future Enhancements

- Add user authentication.
- Add saved project history.
- Add editable generated plans.
- Add PDF export support.
- Add streaming AI generation updates.
- Add project collaboration features.
- Add deployment support for hosted frontend and backend.
- Add model comparison between multiple AI providers.
- Add richer visualizations for dependencies and timelines.
- Add database persistence for generated plans.

## 18. Conclusion

AI-Assisted Project Planner demonstrates how AI can be used to improve the software planning process. The project converts natural-language ideas into structured plans and implementation guidance. It combines React, FastAPI, Gemini AI, Pydantic validation, fallback planning, prompt generation, export functionality, and testing.

The project is useful for students, developers, and teams who need to plan software projects more efficiently. It also shows practical knowledge of full-stack development, AI integration, API design, structured validation, and software testing. Overall, the project provides a strong academic and practical demonstration of AI-assisted software engineering.

## 19. References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- React Documentation: https://react.dev/
- Vite Documentation: https://vitejs.dev/
- Pydantic Documentation: https://docs.pydantic.dev/
- Pytest Documentation: https://docs.pytest.org/
- Google Gemini API Documentation: https://ai.google.dev/
- GitHub Repository: https://github.com/sathvikgaddam-spliter/ai-assisted-project-planner
