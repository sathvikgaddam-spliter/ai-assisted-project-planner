import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import generate_project_plan
from utils import save_json_output, save_markdown_output


def test_save_json_output(tmp_path):
    plan = generate_project_plan("Build an expense tracker app for college students.")

    path = save_json_output(plan, tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert path.exists()
    assert payload["domain"] == "software"
    assert payload["status"] == "plan_generated"
    assert payload["phases"]


def test_save_markdown_output(tmp_path):
    plan = generate_project_plan("Create a Power BI dashboard for sales managers.")

    path = save_markdown_output(plan, tmp_path)
    content = path.read_text(encoding="utf-8")

    assert path.exists()
    assert "# " in content
    assert "## Phases" in content
    assert "analytics" in content


def test_clarification_output_can_be_saved(tmp_path):
    plan = generate_project_plan("Dashboard.")

    json_path = save_json_output(plan, tmp_path)
    markdown_path = save_markdown_output(plan, tmp_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert payload["status"] == "clarification_required"
    assert payload["clarification_questions"]
    assert "Clarification Questions" in markdown_path.read_text(encoding="utf-8")
