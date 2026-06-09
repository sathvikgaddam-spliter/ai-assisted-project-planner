import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_provider import AIProvider, AIProviderError
from planner import generate_project_plan


class NotConfiguredProvider(AIProvider):
    provider_name = "fake"
    model_name = "fake-model"

    def is_configured(self):
        return False

    def generate_text(self, prompt, timeout_seconds=60):
        raise AssertionError("generate_text should not be called when provider is not configured")


class InvalidJsonProvider(AIProvider):
    provider_name = "fake"
    model_name = "fake-model"

    def is_configured(self):
        return True

    def generate_text(self, prompt, timeout_seconds=60):
        return "not json"


class LeakyErrorProvider(AIProvider):
    provider_name = "fake"
    model_name = "fake-model"

    def is_configured(self):
        return True

    def generate_text(self, prompt, timeout_seconds=60):
        raise AIProviderError("Gemini request failed: api_key=AIzaSecretValue123456789 denied")


class ValidJsonProvider(AIProvider):
    provider_name = "fake"
    model_name = "fake-model"

    def is_configured(self):
        return True

    def generate_text(self, prompt, timeout_seconds=60):
        return """
        {
          "project_name": "AI Generated Expense Tracker",
          "description": "Build an expense tracker app for college students.",
          "domain": "software",
          "project_type": "software MVP",
          "complexity": "medium",
          "status": "plan_generated",
          "summary": "AI-generated structured software plan.",
          "phases": [
            {
              "id": "P1",
              "name": "Discovery",
              "objective": "Define requirements.",
              "estimated_duration": "1 week",
              "tasks": [
                {
                  "id": "T1",
                  "title": "Define MVP",
                  "description": "Confirm core budgeting and expense features.",
                  "owner_role": "Product Lead",
                  "estimated_effort": "2 days",
                  "acceptance_criteria": ["MVP scope is approved."],
                  "dependencies": []
                }
              ],
              "deliverables": ["MVP scope"]
            }
          ],
          "milestones": [
            {
              "id": "M1",
              "name": "Discovery Complete",
              "description": "Requirements are approved.",
              "target_phase_id": "P1"
            }
          ],
          "dependencies": [],
          "risks": [
            {
              "id": "R1",
              "description": "Scope may expand.",
              "impact": "medium",
              "likelihood": "medium",
              "mitigation": "Use MVP boundaries."
            }
          ],
          "recommendations": [
            {
              "id": "REC1",
              "category": "Planning",
              "recommendation": "Validate assumptions.",
              "rationale": "Input may omit constraints."
            }
          ],
          "assumptions": ["No timeline was provided."],
          "warnings": [],
          "clarification_questions": []
        }
        """


def test_missing_ai_configuration_falls_back_to_mock_plan():
    plan = generate_project_plan(
        "Build an expense tracker app for college students.",
        provider=NotConfiguredProvider(),
    )

    assert plan.status == "plan_generated"
    assert plan.domain == "software"
    assert any("AI planning failed" in warning for warning in plan.warnings)
    assert any("Reason: AI provider is not configured." in warning for warning in plan.warnings)
    assert len(plan.engineering_prompts) == 6
    assert len(plan.prompt_evaluations) == 6


def test_invalid_ai_json_falls_back_to_mock_plan():
    plan = generate_project_plan(
        "Create a Power BI dashboard for sales managers showing revenue.",
        provider=InvalidJsonProvider(),
    )

    assert plan.status == "plan_generated"
    assert plan.domain == "analytics"
    assert any("AI planning failed" in warning for warning in plan.warnings)
    assert any("AI response was not valid JSON" in warning for warning in plan.warnings)


def test_ai_failure_warning_includes_sanitized_reason():
    plan = generate_project_plan(
        "Build an expense tracker app for college students.",
        provider=LeakyErrorProvider(),
    )

    warning_text = " ".join(plan.warnings)
    assert "Gemini request failed" in warning_text
    assert "api_key=[redacted]" in warning_text
    assert "AIzaSecretValue" not in warning_text


def test_valid_ai_json_is_used_when_provider_succeeds():
    plan = generate_project_plan(
        "Build an expense tracker app for college students.",
        provider=ValidJsonProvider(),
    )

    assert plan.project_name == "AI Generated Expense Tracker"
    assert plan.status == "plan_generated"
    assert len(plan.phases) == 1
    assert len(plan.engineering_prompts) == 6
    assert len(plan.prompt_evaluations) == 6


def test_vague_input_does_not_call_ai_provider():
    plan = generate_project_plan("I want to build something for students.", provider=InvalidJsonProvider())

    assert plan.status == "clarification_required"
    assert plan.phases == []
    assert plan.clarification_questions
