from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


Domain = Literal["software", "analytics", "business", "academic", "healthcare", "unknown"]
Complexity = Literal["low", "medium", "high"]
PlanStatus = Literal["plan_generated", "clarification_required"]


class Task(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    owner_role: str = Field(..., min_length=1)
    estimated_effort: str = Field(..., min_length=1)
    acceptance_criteria: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)


class Phase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    objective: str = Field(..., min_length=1)
    estimated_duration: str = Field(..., min_length=1)
    tasks: List[Task] = Field(default_factory=list)
    deliverables: List[str] = Field(default_factory=list)


class Milestone(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    target_phase_id: str = Field(..., min_length=1)


class Risk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    impact: Literal["low", "medium", "high"]
    likelihood: Literal["low", "medium", "high"]
    mitigation: str = Field(..., min_length=1)


class Dependency(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    source_task_id: str = Field(..., min_length=1)
    target_task_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class Recommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    recommendation: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)


class ProjectPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    domain: Domain
    project_type: str = Field(..., min_length=1)
    complexity: Complexity
    status: PlanStatus
    summary: str = Field(..., min_length=1)
    phases: List[Phase] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    clarification_questions: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "1.0"
