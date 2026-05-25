import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api import app
from planner import generate_mock_project_plan


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

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
