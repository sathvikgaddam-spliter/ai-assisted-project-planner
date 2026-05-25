# Test Scenarios

These scenarios test both system behavior and AI reasoning quality. A passing system should not only run successfully; it should understand the project, ask clarifying questions when needed, avoid hallucinated assumptions, order dependencies correctly, and produce domain-appropriate plans.

## Software Projects

### Expense Tracker

- Scenario name: College expense tracker app.
- User input: "Build an expense tracker app for college students to track spending, set monthly budgets, and see category summaries."
- System should understand: This is a software MVP for student personal finance with mobile or web app characteristics, user accounts, transaction entry, budget tracking, and reporting.
- Expected planner behavior: Generate software phases covering requirements, UX, architecture, data model, implementation, testing, deployment, and iteration.
- Validation criteria: Includes authentication or user identity as a consideration, transaction and budget data models, reporting views, privacy risks, and dependencies where design and data modeling precede implementation.

### E-Commerce Platform

- Scenario name: Small business e-commerce platform.
- User input: "Create an e-commerce platform for a local clothing boutique with product listings, cart, checkout, inventory tracking, and order management."
- System should understand: This is a commerce software project with customer-facing and admin workflows.
- Expected planner behavior: Plan catalog, inventory, cart, checkout, payment integration, order management, security, testing, and launch.
- Validation criteria: Payment and security risks are identified, inventory and checkout dependencies are ordered correctly, and the plan does not assume a specific payment provider unless marked as an assumption.

### Food Delivery MVP

- Scenario name: Campus food delivery MVP.
- User input: "Plan a food delivery MVP for a college campus where students can order from nearby restaurants and drivers can accept deliveries."
- System should understand: This is a two-sided or three-sided marketplace MVP involving students, restaurants, and drivers.
- Expected planner behavior: Include role workflows, ordering, restaurant menu management, driver assignment, payments, notifications, operations, and pilot launch.
- Validation criteria: Detects marketplace complexity, includes operational risks, sequences MVP discovery before full automation, and flags logistics constraints.

### SaaS Platform

- Scenario name: B2B SaaS task management platform.
- User input: "Build a SaaS platform for small teams to manage projects, assign tasks, track progress, and invite team members."
- System should understand: This is a multi-tenant SaaS software project.
- Expected planner behavior: Include tenant model, user management, roles, task workflows, billing as optional or future depending on scope, deployment, monitoring, and customer onboarding.
- Validation criteria: Identifies multi-tenancy and access control risks, avoids overbuilding enterprise features unless requested, and produces a realistic MVP sequence.

## AI Projects

### RAG Document Assistant

- Scenario name: Internal RAG document assistant.
- User input: "Build an AI assistant that answers employee questions from company policy PDFs and cites the source documents."
- System should understand: This is a retrieval-augmented generation project with document ingestion, chunking, embeddings, retrieval, answer generation, citation, and evaluation.
- Expected planner behavior: Include data ingestion, indexing, retrieval design, prompt design, evaluation set, access control, hallucination mitigation, and deployment.
- Validation criteria: Requires citation grounding, includes document update workflow, evaluates answer quality, and flags privacy or permission risks.

### Chatbot

- Scenario name: Customer support chatbot.
- User input: "Create a chatbot for customer support that can answer FAQs, collect order numbers, and escalate to a human when needed."
- System should understand: This is a conversational AI support workflow with intent handling, knowledge source management, escalation, and integration needs.
- Expected planner behavior: Include conversation design, knowledge base preparation, escalation rules, testing, monitoring, and fallback behavior.
- Validation criteria: Includes human handoff, avoids claiming full automation is safe, and identifies missing details about support channels and integrations.

### AI Planner

- Scenario name: AI-assisted project planner.
- User input: "Build an AI planner that turns project descriptions into phases, tasks, milestones, dependencies, risks, and recommendations."
- System should understand: This project is an AI planning system requiring project understanding before generation, structured output, validation, and evaluation.
- Expected planner behavior: Include domain classification, clarification workflow, prompt orchestration, provider abstraction, schema validation, evaluation scenarios, and export formats.
- Validation criteria: Does not produce a generic CRUD app plan, includes hallucination controls, and recognizes that plan quality must be evaluated.

## Data and Analytics

### Power BI Dashboard

- Scenario name: Sales performance Power BI dashboard.
- User input: "Create a Power BI dashboard for sales managers showing revenue, quota attainment, pipeline, regional performance, and monthly trends."
- System should understand: This is a BI dashboard project with data sources, metric definitions, data modeling, report design, validation, and stakeholder review.
- Expected planner behavior: Include requirements workshops, KPI definitions, data access, ETL or semantic model design, dashboard mockups, DAX measures, validation, publishing, and training.
- Validation criteria: Metric definition comes before visualization, data quality risks are included, and the plan does not treat this as a software application build.

### ETL Reporting Workflow

- Scenario name: Automated ETL reporting workflow.
- User input: "Build an ETL workflow that pulls weekly sales data from CSV files, cleans it, loads it into a database, and generates a summary report."
- System should understand: This is a data pipeline and reporting automation project.
- Expected planner behavior: Include source profiling, schema design, cleaning rules, transformation pipeline, load process, reporting, scheduling, monitoring, and error handling.
- Validation criteria: Includes data validation checks, failure handling, repeatable scheduling, and clear dependency order from profiling to reporting.

## Business Projects

### Digital Marketing Campaign

- Scenario name: Digital marketing campaign for a new tutoring service.
- User input: "Plan a digital marketing campaign to launch an online tutoring service for high school students."
- System should understand: This is a business and marketing project, not a software build.
- Expected planner behavior: Include audience research, positioning, channel strategy, content calendar, landing page or signup funnel, budget planning, launch execution, and performance measurement.
- Validation criteria: Uses marketing phases, includes metrics such as leads and conversion rate, and asks for budget if missing or marks it as an assumption.

### Product Launch Plan

- Scenario name: Product launch plan for a fitness app.
- User input: "Create a product launch plan for a fitness app targeting working professionals."
- System should understand: This is a go-to-market launch project.
- Expected planner behavior: Include market positioning, launch messaging, beta feedback, pricing or packaging considerations, channel planning, launch timeline, and post-launch metrics.
- Validation criteria: Distinguishes launch planning from app development, identifies missing launch date and budget, and includes stakeholder coordination.

## Academic Projects

### Research Workflow Planning

- Scenario name: Academic research project on remote work productivity.
- User input: "Plan a research project studying how remote work affects productivity for software engineers."
- System should understand: This is an academic or applied research workflow.
- Expected planner behavior: Include research question refinement, literature review, methodology, participant or data selection, ethics review if applicable, data collection, analysis, writing, and presentation.
- Validation criteria: Includes methodology before data collection, flags ethics and privacy considerations, and avoids inventing findings.

### Independent Study Planning

- Scenario name: Independent study on machine learning for finance.
- User input: "I want to do an independent study on machine learning applications in finance over one semester."
- System should understand: This is an academic learning and research planning project.
- Expected planner behavior: Include learning objectives, reading plan, project scope, advisor checkpoints, implementation or case study work, deliverables, and final presentation.
- Validation criteria: Produces semester-appropriate phases, asks or assumes weekly time commitment, and does not over-scope into a full production system.

## Healthcare

### Patient Scheduling Workflow

- Scenario name: Patient scheduling workflow improvement.
- User input: "Improve the patient scheduling workflow for a small clinic so staff can reduce phone backlogs and patients can get appointment reminders."
- System should understand: This is a healthcare operations workflow with possible software, process, compliance, and communication components.
- Expected planner behavior: Include current workflow discovery, stakeholder interviews, requirements, compliance and privacy review, reminder process, scheduling policy, pilot rollout, staff training, and measurement.
- Validation criteria: Flags HIPAA or privacy considerations, does not assume direct EHR integration without confirmation, and includes change management.

## Edge Cases

### Vague Input

- Scenario name: Vague student project.
- User input: "I want to build something for students."
- System should understand: Domain, deliverable, user segment, and outcome are unclear.
- Expected planner behavior: Ask clarification questions instead of generating a plan.
- Validation criteria: No final plan is exported by default, questions ask about project type, target users, goal, deliverable, constraints, and timeline.

### Empty Input

- Scenario name: Empty description.
- User input: ""
- System should understand: No project information was provided.
- Expected planner behavior: Return input validation error.
- Validation criteria: No AI call is made, no plan is generated, and CLI returns a validation failure.

### Short Input

- Scenario name: Minimal project description.
- User input: "Dashboard."
- System should understand: The input hints at analytics but lacks domain, audience, metrics, data sources, and deliverables.
- Expected planner behavior: Ask clarification questions.
- Validation criteria: Does not generate a Power BI plan unless the user provides enough context, and asks about metrics, users, data sources, and reporting goals.

### Unrealistic Timeline

- Scenario name: Enterprise platform in one week.
- User input: "Build a full e-commerce marketplace with payments, inventory, seller dashboards, mobile apps, and analytics in one week."
- System should understand: Scope and timeline are unrealistic.
- Expected planner behavior: Flag timeline risk, recommend MVP scope reduction, and possibly ask clarification about priorities.
- Validation criteria: Does not accept the timeline as realistic, identifies major scope risks, and proposes phased delivery.

### Conflicting Requirements

- Scenario name: No-login personalized app.
- User input: "Create a personalized budgeting app that syncs user data across devices, but it must not have user accounts or store any user data."
- System should understand: Requirements conflict.
- Expected planner behavior: Ask clarification or present tradeoffs before planning.
- Validation criteria: Detects conflict between personalization, sync, no accounts, and no storage.

### Impossible Resource Constraints

- Scenario name: Solo developer building regulated healthcare platform.
- User input: "One student developer must build a HIPAA-compliant telemedicine platform with video calls, prescriptions, billing, and EHR integration in two weeks."
- System should understand: Resource, compliance, scope, and timeline constraints are not feasible.
- Expected planner behavior: Reject or heavily qualify the plan, ask for scope reduction, and identify compliance risk.
- Validation criteria: Does not produce a normal implementation plan as if feasible, and clearly flags regulatory and delivery risks.

### Malformed AI Outputs

- Scenario name: Provider returns invalid plan schema.
- User input: Simulated provider response missing required phase IDs and containing dependencies to nonexistent tasks.
- System should understand: AI response is malformed.
- Expected planner behavior: Attempt repair or retry according to policy; fail safely if still invalid.
- Validation criteria: Invalid plan is not exported, validation errors are logged, and user receives a clear failure message.

### API Failure

- Scenario name: AI provider timeout.
- User input: "Build a chatbot for internal HR policies."
- System should understand: The request may be valid, but provider call failed.
- Expected planner behavior: Retry if configured, then return provider failure if unavailable.
- Validation criteria: Does not fabricate a plan, preserves error category, and suggests checking provider configuration or retrying.

### Missing Configuration

- Scenario name: Missing API key.
- User input: "Plan a Power BI dashboard for finance reporting."
- System should understand: Runtime configuration is incomplete.
- Expected planner behavior: Fail before making provider calls.
- Validation criteria: Error clearly identifies missing configuration, no AI call is attempted, and no output files are created.
