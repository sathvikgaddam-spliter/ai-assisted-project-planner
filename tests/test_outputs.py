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
    assert payload["is_draft"] is False
    assert payload["requires_clarification"] is False
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
    assert payload["is_draft"] is False
    assert payload["requires_clarification"] is True
    assert payload["clarification_questions"]
    content = markdown_path.read_text(encoding="utf-8")
    assert "Clarification Questions" in content
    assert "Engineering Prompt Pack" not in content
    assert "Prompt Quality Evaluations" not in content


def test_json_output_marks_meaningful_incomplete_plan_as_draft(tmp_path):
    plan = generate_project_plan("Build a racing game", use_ai=False)

    path = save_json_output(plan, tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["status"] == "clarification_required"
    assert payload["is_draft"] is True
    assert payload["requires_clarification"] is True
    assert payload["phases"]
    assert payload["engineering_prompts"]


def test_markdown_output_includes_draft_warning_for_meaningful_incomplete_plan(tmp_path):
    plan = generate_project_plan("Build a portfolio website", use_ai=False)

    path = save_markdown_output(plan, tmp_path)
    content = path.read_text(encoding="utf-8")

    assert "## Draft Plan Warning" in content
    assert "This is a draft execution plan generated from incomplete requirements." in content
    assert "Clarification is required before implementation." in content
    assert "Engineering prompts are provisional." in content


def test_complete_markdown_output_does_not_include_draft_warning(tmp_path):
    plan = generate_project_plan(
        "Build an expense tracker app for college students to track spending and budgets over a semester.",
        use_ai=False,
    )

    path = save_markdown_output(plan, tmp_path)
    content = path.read_text(encoding="utf-8")

    assert plan.status == "plan_generated"
    assert "## Draft Plan Warning" not in content


def test_save_prompt_pack_zip_creates_expected_files_for_generated_plan(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

        assert "project-summary.md" in names
        assert "manifest.json" in names
        assert "project-plan/project_plan.md" in names
        assert "project-plan/project_plan.json" in names
        assert "prompt-evaluations/prompt_quality_report.md" in names
        assert "engineering-prompts/frontend_engineer_prompt.md" in names
        assert "engineering-prompts/backend_engineer_prompt.md" in names
        assert "engineering-prompts/database_engineer_prompt.md" in names
        assert "engineering-prompts/qa_testing_engineer_prompt.md" in names
        assert "engineering-prompts/devops_engineer_prompt.md" in names
        assert "engineering-prompts/security_reviewer_prompt.md" in names


def test_prompt_pack_zip_manifest_lists_generated_artifacts(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))

    assert set(manifest["generated_artifacts"]) == names
    assert manifest["planner_version"] == "0.1.0"
    assert manifest["project"]["title"] == plan.project_name
    assert manifest["project"]["status"] == "plan_generated"
    assert manifest["project"]["is_draft"] is False
    assert manifest["project"]["requires_clarification"] is False
    assert manifest["metrics"]["phase_count"] == len(plan.phases)
    assert manifest["metrics"]["engineering_prompt_count"] == len(plan.engineering_prompts)


def test_project_summary_contains_status_and_metrics(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        summary = archive.read("project-summary.md").decode("utf-8")

    assert f"# {plan.project_name} Export Summary" in summary
    assert f"- Planner status: {plan.status}" in summary
    assert "- Draft status: False" in summary
    assert f"- Number of phases: {len(plan.phases)}" in summary
    assert f"- Number of engineering prompts: {len(plan.engineering_prompts)}" in summary
    assert "This plan is implementation-ready based on the available requirements." in summary
    assert "DRAFT PLAN" not in summary


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


def test_prompt_pack_zip_includes_draft_notes_for_meaningful_incomplete_request(tmp_path):
    plan = generate_project_plan("Build a racing game", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        summary = archive.read("project-summary.md").decode("utf-8")
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        draft_warning = archive.read("draft-notes/draft-warning.md").decode("utf-8")

    assert "DRAFT PLAN — REQUIREMENTS INCOMPLETE" in summary
    assert "- Draft status: True" in summary
    assert "- Clarification required: True" in summary
    assert "Clarification is required before implementation." in summary
    assert manifest["project"]["is_draft"] is True
    assert manifest["project"]["requires_clarification"] is True
    assert manifest["metrics"]["phase_count"] == len(plan.phases)
    assert manifest["metrics"]["engineering_prompt_count"] == len(plan.engineering_prompts)
    assert "draft-notes/assumptions.md" in names
    assert "draft-notes/clarification-questions.md" in names
    assert "draft-notes/draft-warning.md" in names
    assert "not production-ready" in draft_warning
    assert "engineering-prompts/backend_engineer_prompt.md" in names
    assert "prompt-evaluations/prompt_quality_report.md" in names


def test_prompt_pack_zip_omits_draft_notes_for_complete_plan(tmp_path):
    plan = generate_project_plan(
        "Build an expense tracker app for college students to track spending and budgets over a semester.",
        use_ai=False,
    )

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        summary = archive.read("project-summary.md").decode("utf-8")

    assert plan.status == "plan_generated"
    assert not any(name.startswith("draft-notes/") for name in names)
    assert "DRAFT PLAN" not in summary
    assert "- Draft status: False" in summary


def test_prompt_pack_zip_omits_draft_notes_for_meaningless_input(tmp_path):
    plan = generate_project_plan("build something", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        summary = archive.read("project-summary.md").decode("utf-8")
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))

    assert plan.status == "clarification_required"
    assert plan.phases == []
    assert plan.engineering_prompts == []
    assert plan.prompt_evaluations == []
    assert "- Number of phases: 0" in summary
    assert "- Number of engineering prompts: 0" in summary
    assert "DRAFT PLAN" not in summary
    assert manifest["project"]["is_draft"] is False
    assert manifest["metrics"]["phase_count"] == 0
    assert manifest["metrics"]["engineering_prompt_count"] == 0
    assert not any(name.startswith("draft-notes/") for name in names)
    assert not any(name.startswith("engineering-prompts/") for name in names)
