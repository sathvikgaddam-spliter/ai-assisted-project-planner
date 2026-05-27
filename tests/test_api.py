import sys
import zipfile
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api import app
from planner import generate_mock_project_plan
from utils import save_prompt_pack_zip


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_plan_endpoint_returns_project_plan(monkeypatch):
    monkeypatch.setattr("api.generate_project_plan", generate_mock_project_plan)

    response = client.post(
        "/generate-plan",
        json={"project_description": "Build a personal expense tracker web app"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "plan_generated"
    assert payload["domain"] == "software"
    assert payload["phases"]


def test_generate_plan_endpoint_validates_description():
    response = client.post("/generate-plan", json={"project_description": ""})

    assert response.status_code == 422


def test_api_generate_plan_returns_wrapped_response(monkeypatch):
    monkeypatch.setattr("api.generate_project_plan", generate_mock_project_plan)

    response = client.post(
        "/api/generate-plan",
        json={"description": "Build a personal expense tracker web app for students over a semester"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["message"] == "Plan generated successfully"
    assert payload["is_draft"] is False
    assert payload["requires_clarification"] is False
    assert payload["plan"]["status"] == "plan_generated"
    assert payload["plan"]["phases"]
    assert payload["plan"]["prompt_evaluations"]


def test_api_generate_plan_returns_draft_for_meaningful_incomplete_request(monkeypatch):
    monkeypatch.setattr("api.generate_project_plan", generate_mock_project_plan)

    response = client.post("/api/generate-plan", json={"description": "Build a racing game"})

    payload = response.json()
    assert response.status_code == 200
    assert payload["is_draft"] is True
    assert payload["requires_clarification"] is True
    assert payload["plan"]["status"] == "clarification_required"
    assert payload["plan"]["phases"]
    assert payload["plan"]["engineering_prompts"]
    assert payload["plan"]["prompt_evaluations"]
    assert payload["plan"]["warnings"]


def test_api_generate_plan_keeps_meaningless_input_protected(monkeypatch):
    monkeypatch.setattr("api.generate_project_plan", generate_mock_project_plan)

    response = client.post("/api/generate-plan", json={"description": "build something"})

    payload = response.json()
    assert response.status_code == 200
    assert payload["is_draft"] is False
    assert payload["requires_clarification"] is True
    assert payload["plan"]["status"] == "clarification_required"
    assert payload["plan"]["phases"] == []
    assert payload["plan"]["engineering_prompts"] == []
    assert payload["plan"]["prompt_evaluations"] == []


def test_api_generate_plan_validates_description():
    response = client.post("/api/generate-plan", json={"description": ""})

    assert response.status_code == 422


def test_generate_plan_zip_endpoint_returns_prompt_pack_zip(monkeypatch, tmp_path):
    monkeypatch.setattr("api.generate_project_plan", generate_mock_project_plan)
    monkeypatch.setattr("api.save_prompt_pack_zip", lambda plan: save_prompt_pack_zip(plan, str(tmp_path)))

    response = client.post(
        "/generate-plan-zip",
        json={"project_description": "Build a personal expense tracker web app"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert response.headers["content-disposition"].startswith("attachment;")

    with zipfile.ZipFile(BytesIO(response.content)) as archive:
        names = set(archive.namelist())
        prompt_content = archive.read("engineering-prompts/backend_engineer_prompt.md").decode("utf-8")

    assert "project-plan/project_plan.md" in names
    assert "project-plan/project_plan.json" in names
    assert "prompt-evaluations/prompt_quality_report.md" in names
    assert "engineering-prompts/backend_engineer_prompt.md" in names
    assert "You are a senior" in prompt_content


def test_generate_plan_zip_endpoint_supports_clarification_plan(monkeypatch, tmp_path):
    monkeypatch.setattr("api.generate_project_plan", generate_mock_project_plan)
    monkeypatch.setattr("api.save_prompt_pack_zip", lambda plan: save_prompt_pack_zip(plan, str(tmp_path)))

    response = client.post(
        "/generate-plan-zip",
        json={"project_description": "Dashboard."},
    )

    assert response.status_code == 200

    with zipfile.ZipFile(BytesIO(response.content)) as archive:
        names = set(archive.namelist())

    assert "project-plan/project_plan.md" in names
    assert "project-plan/project_plan.json" in names
    assert not any(name.startswith("engineering-prompts/") for name in names)
    assert "prompt-evaluations/prompt_quality_report.md" not in names


def test_generate_plan_zip_endpoint_validates_description():
    response = client.post("/generate-plan-zip", json={"project_description": ""})

    assert response.status_code == 422
