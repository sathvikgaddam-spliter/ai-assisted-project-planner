import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import generate_project_plan
from project_analyzer import analyze_project
from spec_generators import REQUIRED_BUILD_PACK_FILES
from utils import save_build_pack_zip, save_prompt_pack_zip


def test_save_build_pack_zip_creates_generated_project_bundle(tmp_path):
    description = "Build a SaaS expense tracker"
    analysis = analyze_project(description)
    plan = generate_project_plan(description, use_ai=False)

    zip_path = Path(save_build_pack_zip(analysis, plan, str(tmp_path)))

    assert zip_path.exists()
    assert zip_path.name == "saas-expense-tracker-coding-agent-job.zip"

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        root_prompt = archive.read("COPY_THIS_PROMPT.md").decode("utf-8")
        start_here = archive.read("generated_project/START_HERE.md").decode("utf-8")

    expected_names = {f"generated_project/{filename}" for filename in REQUIRED_BUILD_PACK_FILES}
    expected_names.update(
        {
            "generated_project/project_plan.md",
            "generated_project/project_plan.json",
        }
    )
    assert "START_HERE.md" in names
    assert "COPY_THIS_PROMPT.md" in names
    assert expected_names.issubset(names)
    assert "Your task is to build the application the user requested." in root_prompt
    assert "Create a complete runnable MVP application" in start_here
    assert "generate actual source code" in start_here


def test_save_build_pack_zip_contents_are_non_empty(tmp_path):
    description = "Build a marketplace for used textbooks"
    analysis = analyze_project(description)
    plan = generate_project_plan(description, use_ai=False)

    zip_path = Path(save_build_pack_zip(analysis, plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            assert archive.read(name).decode("utf-8").strip()


def test_build_pack_zip_contains_serialized_project_plan(tmp_path):
    description = "Build an AI study planner"
    analysis = analyze_project(description)
    plan = generate_project_plan(description, use_ai=False)

    zip_path = Path(save_build_pack_zip(analysis, plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        markdown = archive.read("generated_project/project_plan.md").decode("utf-8")
        payload = json.loads(archive.read("generated_project/project_plan.json").decode("utf-8"))

    assert "# " in markdown
    assert "## Phases" in markdown
    assert payload["project_name"] == plan.project_name
    assert payload["phases"]


def test_build_pack_zip_preserves_phase_5_prompt_pack_zip_structure(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.", use_ai=False)

    zip_path = Path(save_prompt_pack_zip(plan, str(tmp_path)))

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

    assert "project-plan/project_plan.md" in names
    assert "project-plan/project_plan.json" in names
    assert "engineering-prompts/backend_engineer_prompt.md" in names
    assert "prompt-evaluations/prompt_quality_report.md" in names
    assert "generated_project/project_brief.md" not in names
