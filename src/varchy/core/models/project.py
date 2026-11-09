"""Project level schemas: metadata, brief, and assumptions."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

from varchy.core.models.common import GenerationMode, ProjectCategory, RiskLevel


class ProjectMetadata(BaseModel):
    name: str = Field(..., description="Project name")
    slug: str = Field(..., description="Filesystem-safe identifier")
    description: str = Field(..., description="One-sentence project concept")
    category: ProjectCategory = Field(default=ProjectCategory.SAAS)
    generation_mode: GenerationMode = Field(default=GenerationMode.AUTONOMOUS)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    varchy_version: str = Field(default="0.1.2")


class Assumption(BaseModel):
    id: str = Field(..., description="e.g. ASM-001")
    statement: str = Field(..., description="Assumption text")
    category: str = Field(..., description="Area of assumption e.g. Auth, Scale, Hosting")
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM)
    confirmed: bool = Field(default=False)
    resolution_notes: Optional[str] = None


class ProjectBrief(BaseModel):
    raw_idea: str
    target_audience: list[str] = Field(default_factory=list)
    core_problem: str
    proposed_solution: str
    key_features: list[str] = Field(default_factory=list)
    technical_complexity: str = "medium"
    identified_risks: list[str] = Field(default_factory=list)

