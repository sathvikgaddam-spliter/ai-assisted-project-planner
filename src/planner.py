import json
from typing import Dict, List, Optional

from ai_provider import AIProvider, AIProviderError, GeminiProvider, sanitize_ai_error
from models import Dependency, Milestone, Phase, ProjectPlan, Recommendation, Risk, Task
from project_analyzer import analyze_project
from prompt_evaluator import evaluate_engineering_prompts
from prompt_generator import generate_engineering_prompts
from prompt_manager import PromptManager


MIN_DESCRIPTION_LENGTH = 3
DRAFT_PLAN_WARNING = (
    "This is a draft execution plan generated from incomplete requirements. "
    "Answer clarification questions before implementation."
)


def generate_project_plan(
    project_description: str,
    use_ai: bool = True,
    provider: Optional[AIProvider] = None,
    prompt_manager: Optional[PromptManager] = None,
) -> ProjectPlan:
    description = _validate_description(project_description)
    analysis = analyze_project(description)

    if analysis["requires_clarification"] and not analysis.get("meaningful_project_intent"):
        return _build_clarification_plan(description, analysis)
    if analysis["requires_clarification"]:
        return generate_mock_project_plan(description)

    if use_ai:
        try:
            return _attach_prompt_pack(_generate_ai_project_plan(description, analysis, provider, prompt_manager))
        except (AIProviderError, FileNotFoundError, ValueError) as exc:
            fallback_plan = generate_mock_project_plan(description)
            reason = sanitize_ai_error(exc)
            fallback_plan.warnings.append(
                f"AI planning failed or was unavailable; generated deterministic mock plan instead. Reason: {reason}"
            )
            return _attach_prompt_pack(fallback_plan)

    return generate_mock_project_plan(description)


def generate_mock_project_plan(project_description: str) -> ProjectPlan:
    description = _validate_description(project_description)
    analysis = analyze_project(description)

    if analysis["requires_clarification"] and not analysis.get("meaningful_project_intent"):
        return _build_clarification_plan(description, analysis)

    phases = _build_domain_phases(analysis["domain"])
    dependencies = _build_dependencies(phases)
    risks = _build_risks(analysis)
    recommendations = _build_recommendations(analysis)
    milestones = _build_milestones(phases)

    status = "clarification_required" if analysis["requires_clarification"] else "plan_generated"
    warnings = list(analysis["warnings"])
    clarification_questions = _build_clarification_questions(analysis) if status == "clarification_required" else []
    if status == "clarification_required" and DRAFT_PLAN_WARNING not in warnings:
        warnings.insert(0, DRAFT_PLAN_WARNING)

    return _attach_prompt_pack(ProjectPlan(
        project_name=_derive_project_name(description, str(analysis["project_type"])),
        description=description,
        domain=analysis["domain"],
        project_type=analysis["project_type"],
        complexity=analysis["complexity"],
        status=status,
        summary=_build_summary(analysis, status),
        phases=phases,
        milestones=milestones,
        dependencies=dependencies,
        risks=risks,
        recommendations=recommendations,
        assumptions=_build_assumptions(analysis),
        warnings=warnings,
        clarification_questions=clarification_questions,
    ))


def _generate_ai_project_plan(
    description: str,
    analysis: Dict[str, object],
    provider: Optional[AIProvider],
    prompt_manager: Optional[PromptManager],
) -> ProjectPlan:
    active_provider = provider or GeminiProvider()
    if not active_provider.is_configured():
        raise AIProviderError("AI provider is not configured.")

    prompts = prompt_manager or PromptManager()
    planning_prompt = prompts.render_prompt(
        "planning_prompt.txt",
        {
            "project_description": description,
            "project_understanding": json.dumps(analysis, indent=2),
        },
    )
    response = active_provider.generate_json(planning_prompt)
    return _validate_ai_plan(response.parsed_json, description)


def _validate_ai_plan(payload: Dict[str, object], original_description: str) -> ProjectPlan:
    payload.setdefault("description", original_description)

    if hasattr(ProjectPlan, "model_validate"):
        return ProjectPlan.model_validate(payload)
    return ProjectPlan.parse_obj(payload)


def _attach_prompt_pack(plan: ProjectPlan) -> ProjectPlan:
    if not plan.phases:
        return plan

    engineering_prompts = generate_engineering_prompts(plan)
    plan.engineering_prompts = engineering_prompts
    plan.prompt_evaluations = evaluate_engineering_prompts(engineering_prompts)
    return plan


def _validate_description(project_description: str) -> str:
    if project_description is None:
        raise ValueError("Project description is required.")

    description = project_description.strip()
    if len(description) < MIN_DESCRIPTION_LENGTH:
        raise ValueError("Project description must contain enough detail to analyze.")

    return description


def _build_clarification_plan(description: str, analysis: Dict[str, object]) -> ProjectPlan:
    return ProjectPlan(
        project_name="Clarification Required",
        description=description,
        domain=analysis["domain"],
        project_type=analysis["project_type"],
        complexity=analysis["complexity"],
        status="clarification_required",
        summary="The project description is too vague to generate a responsible execution plan.",
        clarification_questions=_build_clarification_questions(analysis),
        assumptions=[],
        warnings=analysis["warnings"],
    )


def _build_clarification_questions(analysis: Dict[str, object]) -> List[str]:
    missing = analysis.get("missing_information", [])
    questions = [
        "What type of project is this: software, analytics, business, academic, healthcare, or something else?",
        "Who are the target users or stakeholders?",
        "What concrete deliverable should the project produce?",
        "What timeline, resources, or constraints should the plan respect?",
    ]

    if "success criteria" in missing:
        questions.append("How will you know the project succeeded?")

    return questions


def _build_summary(analysis: Dict[str, object], status: str) -> str:
    base = f"A {analysis['complexity']} complexity {analysis['project_type']} in the {analysis['domain']} domain."
    if status == "clarification_required":
        return f"Draft incomplete plan: {base} Requirements are incomplete and should be clarified before implementation."
    return base


def _build_domain_phases(domain: str) -> List[Phase]:
    builders = {
        "software": _software_phases,
        "analytics": _analytics_phases,
        "business": _business_phases,
        "academic": _academic_phases,
        "healthcare": _healthcare_phases,
    }
    return builders.get(domain, _software_phases)()


def _software_phases() -> List[Phase]:
    return [
        Phase(
            id="P1",
            name="Discovery and Requirements",
            objective="Define users, scope, core workflows, and MVP boundaries.",
            estimated_duration="1-2 weeks",
            tasks=[
                _task("T1", "Identify users and goals", "Document user segments, goals, and success criteria.", "Product Lead", "2-3 days"),
                _task("T2", "Define MVP scope", "Prioritize core features and defer nonessential capabilities.", "Product Lead", "2-3 days", ["T1"]),
            ],
            deliverables=["requirements brief", "MVP scope"],
        ),
        Phase(
            id="P2",
            name="Architecture and Design",
            objective="Design the technical foundation and user experience.",
            estimated_duration="1-2 weeks",
            tasks=[
                _task("T3", "Design data model", "Define entities, relationships, and persistence needs.", "Backend Engineer", "2-4 days", ["T2"]),
                _task("T4", "Design user workflows", "Map primary screens or API flows for the MVP.", "UX or Product Lead", "2-4 days", ["T2"]),
            ],
            deliverables=["architecture outline", "workflow design"],
        ),
        Phase(
            id="P3",
            name="Implementation",
            objective="Build the MVP features in dependency order.",
            estimated_duration="3-6 weeks",
            tasks=[
                _task("T5", "Build backend foundation", "Implement core services, validation, and data access.", "Backend Engineer", "1-2 weeks", ["T3"]),
                _task("T6", "Build user-facing workflow", "Implement the primary user workflow and connect it to backend services.", "Full-stack Engineer", "2-3 weeks", ["T4", "T5"]),
            ],
            deliverables=["working MVP"],
        ),
        Phase(
            id="P4",
            name="Testing and Launch",
            objective="Validate the MVP and prepare a controlled release.",
            estimated_duration="1-2 weeks",
            tasks=[
                _task("T7", "Run functional testing", "Test critical workflows, validation rules, and failure paths.", "QA or Engineer", "3-5 days", ["T6"]),
                _task("T8", "Prepare launch checklist", "Confirm deployment, monitoring, documentation, and rollback steps.", "Technical Lead", "2-3 days", ["T7"]),
            ],
            deliverables=["test report", "launch checklist"],
        ),
    ]


def _analytics_phases() -> List[Phase]:
    return [
        Phase(
            id="P1",
            name="Requirements and KPI Definition",
            objective="Define decision goals, users, metrics, and reporting cadence.",
            estimated_duration="1 week",
            tasks=[
                _task("T1", "Interview stakeholders", "Capture audience, business questions, and reporting needs.", "BI Analyst", "2-3 days"),
                _task("T2", "Define metrics", "Document KPI formulas, grain, filters, and ownership.", "BI Analyst", "2-3 days", ["T1"]),
            ],
            deliverables=["KPI definition document"],
        ),
        Phase(
            id="P2",
            name="Data Discovery and Modeling",
            objective="Profile source data and create a reliable reporting model.",
            estimated_duration="1-2 weeks",
            tasks=[
                _task("T3", "Profile data sources", "Assess schemas, quality gaps, refresh needs, and access constraints.", "Data Analyst", "2-4 days", ["T2"]),
                _task("T4", "Build semantic model", "Create tables, relationships, measures, and validation checks.", "BI Developer", "4-7 days", ["T3"]),
            ],
            deliverables=["data quality notes", "semantic model"],
        ),
        Phase(
            id="P3",
            name="Report Build and Validation",
            objective="Create dashboards and validate results with stakeholders.",
            estimated_duration="1-2 weeks",
            tasks=[
                _task("T5", "Build report pages", "Create visuals, filters, drill paths, and summary views.", "BI Developer", "4-7 days", ["T4"]),
                _task("T6", "Validate numbers", "Reconcile dashboard outputs against source reports or approved samples.", "BI Analyst", "2-4 days", ["T5"]),
            ],
            deliverables=["validated dashboard"],
        ),
        Phase(
            id="P4",
            name="Publish and Enable",
            objective="Publish the report and support adoption.",
            estimated_duration="1 week",
            tasks=[
                _task("T7", "Publish workspace artifact", "Configure permissions, refresh schedule, and deployment location.", "BI Developer", "1-2 days", ["T6"]),
                _task("T8", "Train users", "Document dashboard usage and review core metrics with stakeholders.", "BI Analyst", "1-2 days", ["T7"]),
            ],
            deliverables=["published report", "user guide"],
        ),
    ]


def _business_phases() -> List[Phase]:
    return [
        Phase(id="P1", name="Market and Audience Research", objective="Clarify audience, positioning, and success metrics.", estimated_duration="1 week", tasks=[_task("T1", "Define audience", "Document target segments, pain points, and buying triggers.", "Marketing Lead", "2-3 days"), _task("T2", "Set campaign goals", "Define measurable goals such as leads, signups, conversion, or awareness.", "Marketing Lead", "1-2 days", ["T1"])], deliverables=["campaign brief"]),
        Phase(id="P2", name="Strategy and Content Planning", objective="Select channels, messages, budget assumptions, and content plan.", estimated_duration="1-2 weeks", tasks=[_task("T3", "Choose channels", "Select channels based on audience and budget.", "Marketing Lead", "2-3 days", ["T2"]), _task("T4", "Create content calendar", "Plan launch assets, publishing cadence, and owners.", "Content Lead", "3-5 days", ["T3"])], deliverables=["channel plan", "content calendar"]),
        Phase(id="P3", name="Launch Execution", objective="Run campaign activities and monitor performance.", estimated_duration="2-4 weeks", tasks=[_task("T5", "Launch campaign", "Publish assets and activate selected channels.", "Marketing Lead", "1-2 days", ["T4"]), _task("T6", "Track performance", "Monitor results and adjust targeting or messaging.", "Marketing Analyst", "ongoing", ["T5"])], deliverables=["live campaign", "performance dashboard"]),
    ]


def _academic_phases() -> List[Phase]:
    return [
        Phase(id="P1", name="Research Framing", objective="Define the research question, scope, and expected deliverables.", estimated_duration="1 week", tasks=[_task("T1", "Refine research question", "Turn the topic into a focused research question.", "Researcher", "2-3 days"), _task("T2", "Define methodology", "Choose research method, data needs, and evaluation approach.", "Researcher", "2-4 days", ["T1"])], deliverables=["research proposal"]),
        Phase(id="P2", name="Literature and Data Planning", objective="Review prior work and prepare the evidence collection plan.", estimated_duration="2-4 weeks", tasks=[_task("T3", "Conduct literature review", "Summarize relevant sources and identify gaps.", "Researcher", "1-3 weeks", ["T1"]), _task("T4", "Plan data collection", "Define participants, datasets, instruments, and ethics needs.", "Researcher", "1 week", ["T2"])], deliverables=["literature review notes", "data collection plan"]),
        Phase(id="P3", name="Analysis and Delivery", objective="Analyze findings and produce final academic outputs.", estimated_duration="3-6 weeks", tasks=[_task("T5", "Analyze evidence", "Apply the selected method and document results.", "Researcher", "2-4 weeks", ["T3", "T4"]), _task("T6", "Write final deliverable", "Prepare paper, report, or presentation.", "Researcher", "1-2 weeks", ["T5"])], deliverables=["final report", "presentation"]),
    ]


def _healthcare_phases() -> List[Phase]:
    return [
        Phase(id="P1", name="Workflow Discovery", objective="Understand current clinical or administrative workflow.", estimated_duration="1-2 weeks", tasks=[_task("T1", "Map current workflow", "Document steps, roles, handoffs, and pain points.", "Operations Lead", "3-5 days"), _task("T2", "Identify compliance constraints", "Capture privacy, security, and policy requirements.", "Compliance Lead", "2-4 days", ["T1"])], deliverables=["workflow map", "compliance notes"]),
        Phase(id="P2", name="Solution Design", objective="Design process and technology changes without assuming unsafe integrations.", estimated_duration="1-2 weeks", tasks=[_task("T3", "Define future-state workflow", "Design improved scheduling, reminders, and staff responsibilities.", "Operations Lead", "3-5 days", ["T2"]), _task("T4", "Plan pilot", "Define pilot scope, success metrics, training, and rollback plan.", "Project Lead", "2-3 days", ["T3"])], deliverables=["future workflow", "pilot plan"]),
        Phase(id="P3", name="Pilot and Measurement", objective="Launch a controlled pilot and measure operational impact.", estimated_duration="2-4 weeks", tasks=[_task("T5", "Train staff", "Prepare staff to execute the updated workflow.", "Operations Lead", "1-2 days", ["T4"]), _task("T6", "Measure outcomes", "Track backlog, reminder success, patient experience, and staff workload.", "Project Lead", "2-4 weeks", ["T5"])], deliverables=["pilot results", "rollout recommendation"]),
    ]


def _task(task_id: str, title: str, description: str, owner_role: str, effort: str, dependencies: List[str] = None) -> Task:
    return Task(
        id=task_id,
        title=title,
        description=description,
        owner_role=owner_role,
        estimated_effort=effort,
        dependencies=dependencies or [],
        acceptance_criteria=[f"{title} is reviewed and accepted by the project lead."],
    )


def _build_dependencies(phases: List[Phase]) -> List[Dependency]:
    task_ids = [task.id for phase in phases for task in phase.tasks]
    dependencies = []
    for phase in phases:
        for task in phase.tasks:
            for dependency_id in task.dependencies:
                if dependency_id in task_ids:
                    dependencies.append(
                        Dependency(
                            id=f"D{len(dependencies) + 1}",
                            source_task_id=dependency_id,
                            target_task_id=task.id,
                            description=f"{task.id} depends on completion of {dependency_id}.",
                        )
                    )
    return dependencies


def _build_milestones(phases: List[Phase]) -> List[Milestone]:
    return [
        Milestone(
            id=f"M{index}",
            name=f"{phase.name} Complete",
            description=f"All deliverables for {phase.name} are complete and reviewed.",
            target_phase_id=phase.id,
        )
        for index, phase in enumerate(phases, start=1)
    ]


def _build_risks(analysis: Dict[str, object]) -> List[Risk]:
    risks = [
        Risk(id="R1", description="Project scope may expand beyond the initial plan.", impact="medium", likelihood="medium", mitigation="Maintain an explicit MVP scope and review changes before adding work."),
        Risk(id="R2", description="Missing stakeholder input may lead to rework.", impact="medium", likelihood="medium", mitigation="Confirm requirements and acceptance criteria before implementation."),
    ]

    if analysis["domain"] == "analytics":
        risks.append(Risk(id="R3", description="Data quality issues may undermine trust in outputs.", impact="high", likelihood="medium", mitigation="Profile source data early and validate metrics with stakeholders."))
    if analysis["domain"] == "healthcare":
        risks.append(Risk(id="R3", description="Privacy or compliance requirements may constrain the solution.", impact="high", likelihood="medium", mitigation="Run compliance review before pilot or integration work."))
    if analysis["warnings"]:
        risks.append(Risk(id=f"R{len(risks) + 1}", description=str(analysis["warnings"][0]), impact="high", likelihood="high", mitigation="Reduce scope, extend timeline, or define a smaller pilot."))

    return risks


def _build_recommendations(analysis: Dict[str, object]) -> List[Recommendation]:
    recommendations = [
        Recommendation(id="REC1", category="Planning", recommendation="Validate assumptions before execution starts.", rationale="The Phase 1 engine uses limited input and deterministic rules."),
        Recommendation(id="REC2", category="Delivery", recommendation="Use milestones as decision gates before expanding scope.", rationale="Decision gates reduce rework and keep dependencies visible."),
    ]

    if analysis["warnings"]:
        recommendations.append(Recommendation(id="REC3", category="Scope", recommendation="Create a reduced MVP plan before committing to the full scope.", rationale="The current request includes timeline or scope risk."))

    return recommendations


def _build_assumptions(analysis: Dict[str, object]) -> List[str]:
    assumptions = ["No AI provider was used; this is a deterministic Phase 1 mock plan."]
    if analysis.get("requires_clarification"):
        assumptions.append("Requirements are incomplete; this draft plan must be validated with stakeholders before implementation.")
    missing = analysis.get("missing_information", [])
    for item in missing:
        assumptions.append(f"{item.capitalize()} was not specified and should be confirmed.")
    return assumptions


def _derive_project_name(description: str, project_type: str) -> str:
    words = [word.strip(".,:;!?") for word in description.split()[:6]]
    candidate = " ".join(words).strip()
    return candidate if candidate else project_type.title()
