import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import generate_project_plan
from utils import save_json_output, save_markdown_output, save_prompt_pack_zip


def test_save_json_output(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    path = save_json_output(plan, tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert path.exists()
    assert payload["domain"] == "software"
    assert payload["status"] == "plan_generated"
    assert payload["phases"]


def test_save_markdown_output(tmp_path):
    plan = generate_project_plan("Create a Power BI dashboard for sales managers.", use_ai=False)

    path = save_markdown_output(plan, tmp_path)
    content = path.read_text(encoding="utf-8")

    assert path.exists()
    assert "# " in content
    assert "## Phases" in content
    assert "analytics" in content


def test_markdown_output_includes_engineering_prompt_pack(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    path = save_markdown_output(plan, tmp_path)
    content = path.read_text(encoding="utf-8")

    assert "## Engineering Prompt Pack" in content
    assert "### Backend Engineer implementation prompt" in content
    assert "**Target Role:** Backend Engineer" in content
    assert "**Target Tool:** Codex, Cursor, Claude Code, Claude, GitHub Copilot, Lovable, or Bolt" in content
    assert "**Related Phases:**" in content
    assert "**Constraints:**" in content
    assert "**Acceptance Criteria:**" in content
    assert "**Prompt:**" in content
    assert "```text" in content
    assert "You are a senior backend engineer" in content


def test_markdown_output_includes_prompt_quality_evaluations(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    path = save_markdown_output(plan, tmp_path)
    content = path.read_text(encoding="utf-8")

    assert "## Prompt Quality Evaluations" in content
    assert "### Evaluation for EP1" in content
    assert "- Score:" in content
    assert "- Ready to use: True" in content
    assert "**Strengths:**" in content
    assert "**Issues:**" in content
    assert "**Improvement Suggestions:**" in content


def test_clarification_output_can_be_saved(tmp_path):
    plan = generate_project_plan("Dashboard.", use_ai=False)

    json_path = save_json_output(plan, tmp_path)
    markdown_path = save_markdown_output(plan, tmp_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert payload["status"] == "clarification_required"
    assert payload["clarification_questions"]
    content = markdown_path.read_text(encoding="utf-8")
    assert "Clarification Questions" in content
    assert "Engineering Prompt Pack" not in content
    assert "Prompt Quality Evaluations" not in content


def test_save_prompt_pack_zip_creates_expected_files_for_generated_plan(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

        assert "project-plan/project_plan.md" in names
        assert "project-plan/project_plan.json" in names
        assert "prompt-evaluations/prompt_quality_report.md" in names
        assert "engineering-prompts/frontend_engineer_prompt.md" in names
        assert "engineering-prompts/backend_engineer_prompt.md" in names
        assert "engineering-prompts/database_engineer_prompt.md" in names
        assert "engineering-prompts/qa_testing_engineer_prompt.md" in names
        assert "engineering-prompts/devops_engineer_prompt.md" in names
        assert "engineering-prompts/security_reviewer_prompt.md" in names


def test_prompt_pack_zip_prompt_file_contains_full_prompt(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        content = archive.read("engineering-prompts/backend_engineer_prompt.md").decode("utf-8")

    assert "# Backend Engineer implementation prompt" in content
    assert "**Target Role:** Backend Engineer" in content
    assert "## Related Phases" in content
    assert "## Constraints" in content
    assert "## Acceptance Criteria" in content
    assert "## Prompt" in content
    assert "You are a senior" in content


def test_prompt_pack_zip_quality_report_contains_evaluation_details(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        content = archive.read("prompt-evaluations/prompt_quality_report.md").decode("utf-8")

    assert "# Prompt Quality Report" in content
    assert "## EP1" in content
    assert "- Score:" in content
    assert "- Ready to use: True" in content
    assert "### Strengths" in content
    assert "### Issues" in content
    assert "### Improvement Suggestions" in content


def test_prompt_pack_zip_omits_prompt_files_for_clarification_plan(tmp_path):
    plan = generate_project_plan("Dashboard.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

    assert "project-plan/project_plan.md" in names
    assert "project-plan/project_plan.json" in names
    assert not any(name.startswith("engineering-prompts/") for name in names)
    assert "prompt-evaluations/prompt_quality_report.md" not in names


def test_prompt_pack_zip_includes_prompts_for_meaningful_incomplete_request(tmp_path):
    plan = generate_project_plan("Build a racing game", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

    assert plan.status == "clarification_required"
    assert "engineering-prompts/backend_engineer_prompt.md" in names
    assert "prompt-evaluations/prompt_quality_report.md" in names
