from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from planner import generate_project_plan
from project_analyzer import analyze_project
from utils import is_draft_plan, save_build_pack_zip, save_prompt_pack_zip


class GeneratePlanRequest(BaseModel):
    project_description: str = Field(..., min_length=3)


class ApiGeneratePlanRequest(BaseModel):
    description: str = Field(..., min_length=3)


app = FastAPI(title="AI-Assisted Project Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/health")
def api_health() -> dict:
    return {"status": "ok"}


@app.post("/generate-plan")
def generate_plan(request: GeneratePlanRequest):
    try:
        return generate_project_plan(request.project_description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/generate-plan")
def api_generate_plan(request: ApiGeneratePlanRequest):
    try:
        plan = generate_project_plan(request.description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return _build_api_plan_response(plan)


@app.post("/generate-plan-zip")
def generate_plan_zip(request: GeneratePlanRequest):
    try:
        plan = generate_project_plan(request.project_description)
        zip_path = Path(save_prompt_pack_zip(plan))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=zip_path.name,
    )


@app.post("/generate-build-pack-zip")
def generate_build_pack_zip(request: GeneratePlanRequest):
    return _generate_coding_agent_zip_response(request)


@app.post("/generate-coding-agent-zip")
def generate_coding_agent_zip(request: GeneratePlanRequest):
    return _generate_coding_agent_zip_response(request)


def _generate_coding_agent_zip_response(request: GeneratePlanRequest):
    try:
        project_analysis = analyze_project(request.project_description)
        plan = generate_project_plan(request.project_description)
        zip_path = Path(save_build_pack_zip(project_analysis, plan))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=zip_path.name,
    )


def _build_api_plan_response(plan) -> dict:
    return {
        "message": "Plan generated successfully",
        "is_draft": is_draft_plan(plan),
        "requires_clarification": plan.status == "clarification_required",
        "plan": plan,
    }
