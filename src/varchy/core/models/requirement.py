"""Product Requirements Document (PRD) schemas."""

from typing import Optional
from pydantic import BaseModel, Field

from varchy.core.models.common import Priority, RequirementType


class Requirement(BaseModel):
    id: str = Field(..., description="Stable identifier e.g. REQ-001")
    title: str = Field(...)
    description: str = Field(...)
    type: RequirementType = Field(default=RequirementType.FUNCTIONAL)
    priority: Priority = Field(default=Priority.HIGH)
    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="List of verifiable acceptance criteria"
    )
    user_story: Optional[str] = Field(
        None,
        description="As a <role>, I want <goal>, so that <benefit>"
    )


class Feature(BaseModel):
    id: str = Field(..., description="e.g. FEAT-001")
    title: str
    description: str
    requirement_ids: list[str] = Field(default_factory=list)


class Persona(BaseModel):
    id: str = Field(..., description="e.g. PERS-001")
    name: str
    role: str
    goals: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)


class ProductSpec(BaseModel):
    overview: str
    problem_statement: str
    vision: str
    personas: list[Persona] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)
    features: list[Feature] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)

