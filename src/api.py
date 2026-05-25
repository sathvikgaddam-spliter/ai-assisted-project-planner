from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from planner import generate_project_plan


class GeneratePlanRequest(BaseModel):
    project_description: str = Field(..., min_length=3)


app = FastAPI(title="AI-Assisted Project Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/generate-plan")
def generate_plan(request: GeneratePlanRequest):
    try:
        return generate_project_plan(request.project_description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
