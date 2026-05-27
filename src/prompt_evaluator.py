from typing import List, Tuple

from models import EngineeringPrompt, PromptEvaluation


READY_TO_USE_THRESHOLD = 75
REQUIRED_SECTIONS = [
    "Project Context",
    "Your Role",
    "Goal",
    "Technical Scope",
    "Related Phases",
    "Constraints",
    "Expected Output",
    "Acceptance Criteria",
    "Do Not Do",
]

QUALITY_CHECKS = [
    "Objective",
    "Context",
    "Scope or Requirements",
    "Constraints",
    "Acceptance Criteria",
    "Assumptions or Dependencies",
    "Review/Validation Notes",
    "Expected Deliverables or Output Expectations",
]


def evaluate_engineering_prompt(prompt: EngineeringPrompt) -> PromptEvaluation:
    strengths: List[str] = []
    issues: List[str] = []
    suggestions: List[str] = []
    quality = validate_prompt_quality(prompt)

    category_results = [
        _score_clarity(prompt),
        _score_specificity(prompt),
        _score_technical_completeness(prompt),
        _score_expected_output_quality(prompt),
        _score_acceptance_criteria_quality(prompt),
    ]

    score = sum(result[0] for result in category_results)
    for _, category_strengths, category_issues, category_suggestions in category_results:
        strengths.extend(category_strengths)
        issues.extend(category_issues)
        suggestions.extend(category_suggestions)

    issues.extend([f"Missing quality section: {section}." for section in quality["missing_sections"]])
    suggestions.extend(quality["review_notes"])
    score = max(0, min(100, min(score, quality["quality_score"])))
    return PromptEvaluation(
        prompt_id=prompt.id,
        score=score,
        quality_score=quality["quality_score"],
        ready_to_use=score >= READY_TO_USE_THRESHOLD,
        passed_checks=quality["passed_checks"],
        missing_sections=quality["missing_sections"],
        warnings=quality["warnings"],
        review_notes=quality["review_notes"],
        strengths=_unique(strengths),
        issues=_unique(issues),
        improvement_suggestions=_unique(suggestions),
    )


def evaluate_engineering_prompts(prompts: List[EngineeringPrompt]) -> List[PromptEvaluation]:
    return [evaluate_engineering_prompt(prompt) for prompt in prompts]


def validate_prompt_quality(prompt: EngineeringPrompt) -> dict:
    checks = {
        "Objective": _has_objective(prompt),
        "Context": _has_context(prompt),
        "Scope or Requirements": _has_scope_or_requirements(prompt),
        "Constraints": _has_constraints(prompt),
        "Acceptance Criteria": _has_acceptance_criteria(prompt),
        "Assumptions or Dependencies": _has_assumptions_or_dependencies(prompt),
        "Review/Validation Notes": _has_review_or_validation_notes(prompt),
        "Expected Deliverables or Output Expectations": _has_expected_output(prompt),
    }
    passed_checks = [name for name in QUALITY_CHECKS if checks[name]]
    missing_sections = [name for name in QUALITY_CHECKS if not checks[name]]
    quality_score = round((len(passed_checks) / len(QUALITY_CHECKS)) * 100)
    warnings = []
    review_notes = ["Engineer review recommended before production implementation."]

    for section in missing_sections:
        warnings.append(f"Prompt quality gate warning: missing {section}.")
        review_notes.append(f"Add {section.lower()} before using this prompt for implementation.")

    prompt_text = prompt.prompt_text.lower()
    if "requirements are incomplete" in prompt_text or "draft" in prompt_text:
        warnings.append("Draft prompt warning: requirements are incomplete and assumptions must be validated.")
        review_notes.append("Validate assumptions and answer clarification questions before production implementation.")

    return {
        "quality_score": quality_score,
        "passed_checks": passed_checks,
        "missing_sections": missing_sections,
        "warnings": _unique(warnings),
        "review_notes": _unique(review_notes),
    }


def _score_clarity(prompt: EngineeringPrompt) -> Tuple[int, List[str], List[str], List[str]]:
    score = 0
    strengths = []
    issues = []
    suggestions = []
    text = prompt.prompt_text

    if text.startswith("You are a senior"):
        score += 8
        strengths.append("Prompt starts with senior role framing.")
    else:
        issues.append("Prompt is missing senior role framing.")
        suggestions.append("Start the prompt with senior role framing.")

    present_sections = [section for section in REQUIRED_SECTIONS if _has_section(text, section)]
    score += min(8, round((len(present_sections) / len(REQUIRED_SECTIONS)) * 8))
    if len(present_sections) == len(REQUIRED_SECTIONS):
        strengths.append("Prompt includes all required structure sections.")
    else:
        missing = [section for section in REQUIRED_SECTIONS if section not in present_sections]
        issues.append(f"Prompt is missing required sections: {', '.join(missing)}.")
        suggestions.append("Add the missing required prompt sections.")

    if len(text.split()) >= 120:
        score += 4
        strengths.append("Prompt has enough detail for engineering use.")
    else:
        issues.append("Prompt is too short for reliable engineering handoff.")
        suggestions.append("Add project context, role scope, constraints, expected output, and acceptance criteria.")

    return score, strengths, issues, suggestions


def _score_specificity(prompt: EngineeringPrompt) -> Tuple[int, List[str], List[str], List[str]]:
    score = 0
    strengths = []
    issues = []
    suggestions = []

    if prompt.target_role and prompt.target_role.lower() in prompt.prompt_text.lower():
        score += 5
        strengths.append("Prompt names the target role.")
    else:
        issues.append("Prompt does not clearly name the target role.")
        suggestions.append("Include the exact target role in the prompt text.")

    if prompt.target_tool:
        score += 4
        strengths.append("Prompt identifies target AI coding tools.")
    else:
        issues.append("Prompt does not identify target AI coding tools.")
        suggestions.append("Specify which AI coding tools the prompt is intended for.")

    if prompt.related_phases and "Related Phases" in prompt.prompt_text:
        score += 5
        strengths.append("Prompt is tied to related plan phases.")
    else:
        issues.append("Prompt is not tied to related plan phases.")
        suggestions.append("Reference relevant phase IDs or explain why phases are unavailable.")

    if prompt.purpose and prompt.purpose.lower() in prompt.prompt_text.lower():
        score += 3
        strengths.append("Prompt purpose is reflected in the prompt text.")
    else:
        issues.append("Prompt purpose is not reflected in the prompt text.")
        suggestions.append("Add a goal section that matches the prompt purpose.")

    if any(token in prompt.prompt_text.lower() for token in ["project name:", "domain:", "complexity:"]):
        score += 3
        strengths.append("Prompt includes project-specific metadata.")
    else:
        issues.append("Prompt lacks project-specific metadata.")
        suggestions.append("Include project name, domain, complexity, and summary.")

    return score, strengths, issues, suggestions


def _score_technical_completeness(prompt: EngineeringPrompt) -> Tuple[int, List[str], List[str], List[str]]:
    score = 0
    strengths = []
    issues = []
    suggestions = []
    text = prompt.prompt_text.lower()

    if _has_section(prompt.prompt_text, "Technical Scope"):
        score += 5
        strengths.append("Prompt includes technical scope.")
    else:
        issues.append("Prompt is missing technical scope.")
        suggestions.append("Add a Technical Scope section.")

    if _has_section(prompt.prompt_text, "Constraints") and _has_meaningful_items(prompt.constraints):
        score += 5
        strengths.append("Prompt includes meaningful constraints.")
    else:
        issues.append("Prompt constraints are missing or too sparse.")
        suggestions.append("Add concrete constraints from assumptions, warnings, and product boundaries.")

    if "risks" in text or "risk" in text:
        score += 3
        strengths.append("Prompt references risk handling.")
    else:
        issues.append("Prompt does not reference risks.")
        suggestions.append("Include relevant risks from the project plan.")

    if "task" in text or "tasks" in text:
        score += 3
        strengths.append("Prompt references implementation tasks.")
    else:
        issues.append("Prompt does not reference implementation tasks.")
        suggestions.append("Include related tasks from the plan.")

    if "do not build" in text or "must not build" in text or "do not deploy" in text:
        score += 4
        strengths.append("Prompt preserves the product boundary.")
    else:
        issues.append("Prompt does not clearly preserve the product boundary.")
        suggestions.append("State that the planner does not build or deploy software.")

    return score, strengths, issues, suggestions


def _score_expected_output_quality(prompt: EngineeringPrompt) -> Tuple[int, List[str], List[str], List[str]]:
    score = 0
    strengths = []
    issues = []
    suggestions = []
    text = prompt.prompt_text.lower()

    if _has_section(prompt.prompt_text, "Expected Output"):
        score += 8
        strengths.append("Prompt includes an Expected Output section.")
    else:
        issues.append("Prompt is missing an Expected Output section.")
        suggestions.append("Add an Expected Output section.")

    if any(tool.lower() in text for tool in ["codex", "cursor", "claude", "github copilot", "lovable", "bolt"]):
        score += 5
        strengths.append("Prompt is positioned for external AI coding tools.")
    else:
        issues.append("Prompt does not mention external AI coding tools.")
        suggestions.append("Name supported external AI coding tools or the expected tool context.")

    if "engineer" in text and "review" in text:
        score += 4
        strengths.append("Prompt keeps engineer review in the workflow.")
    else:
        issues.append("Prompt does not clearly require engineer review.")
        suggestions.append("State that outputs should be reviewed by an engineer before use.")

    if "artifact" in text or "guidance" in text or "output" in text:
        score += 3
        strengths.append("Prompt describes the expected deliverable type.")
    else:
        issues.append("Prompt does not describe the deliverable type.")
        suggestions.append("Describe the implementation guidance or artifact expected from the coding tool.")

    return score, strengths, issues, suggestions


def _score_acceptance_criteria_quality(prompt: EngineeringPrompt) -> Tuple[int, List[str], List[str], List[str]]:
    score = 0
    strengths = []
    issues = []
    suggestions = []

    if _has_section(prompt.prompt_text, "Acceptance Criteria"):
        score += 5
        strengths.append("Prompt includes an Acceptance Criteria section.")
    else:
        issues.append("Prompt is missing an Acceptance Criteria section.")
        suggestions.append("Add an Acceptance Criteria section.")

    if _has_meaningful_items(prompt.acceptance_criteria):
        score += 7
        strengths.append("Prompt includes meaningful acceptance criteria.")
    else:
        issues.append("Prompt acceptance criteria are missing or too sparse.")
        suggestions.append("Add measurable acceptance criteria.")

    if len(prompt.acceptance_criteria) >= 3:
        score += 4
        strengths.append("Prompt includes multiple acceptance criteria.")
    else:
        issues.append("Prompt has too few acceptance criteria.")
        suggestions.append("Include at least three acceptance criteria.")

    acceptance_text = " ".join(prompt.acceptance_criteria).lower()
    if any(term in acceptance_text for term in ["validated", "tested", "review", "aligned", "coverage"]):
        score += 4
        strengths.append("Acceptance criteria include validation or review expectations.")
    else:
        issues.append("Acceptance criteria do not clearly require validation or review.")
        suggestions.append("Add validation, testing, or engineer review expectations to acceptance criteria.")

    return score, strengths, issues, suggestions


def _has_section(text: str, section: str) -> bool:
    return f"## {section}" in text or f"{section}:" in text


def _has_objective(prompt: EngineeringPrompt) -> bool:
    text = prompt.prompt_text
    return bool(prompt.purpose) and (_has_section(text, "Goal") or _has_section(text, "Objective"))


def _has_context(prompt: EngineeringPrompt) -> bool:
    text = prompt.prompt_text.lower()
    return _has_section(prompt.prompt_text, "Project Context") and all(
        token in text for token in ["project name:", "domain:", "complexity:"]
    )


def _has_scope_or_requirements(prompt: EngineeringPrompt) -> bool:
    text = prompt.prompt_text.lower()
    return _has_section(prompt.prompt_text, "Technical Scope") or "requirements" in text


def _has_constraints(prompt: EngineeringPrompt) -> bool:
    return _has_section(prompt.prompt_text, "Constraints") and _has_meaningful_items(prompt.constraints)


def _has_acceptance_criteria(prompt: EngineeringPrompt) -> bool:
    return _has_section(prompt.prompt_text, "Acceptance Criteria") and _has_meaningful_items(prompt.acceptance_criteria)


def _has_assumptions_or_dependencies(prompt: EngineeringPrompt) -> bool:
    text = prompt.prompt_text.lower()
    return "assumptions" in text or "dependencies" in text or bool(prompt.related_phases)


def _has_review_or_validation_notes(prompt: EngineeringPrompt) -> bool:
    text = prompt.prompt_text.lower()
    return "review" in text or "validation" in text or "validated" in text or "tested" in text


def _has_expected_output(prompt: EngineeringPrompt) -> bool:
    text = prompt.prompt_text.lower()
    return _has_section(prompt.prompt_text, "Expected Output") and any(
        term in text for term in ["artifact", "guidance", "output", "deliverable"]
    )


def _has_meaningful_items(items: List[str]) -> bool:
    return any(len(item.strip().split()) >= 4 for item in items)


def _unique(items: List[str]) -> List[str]:
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return unique_items
