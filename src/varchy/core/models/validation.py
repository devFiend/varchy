"""Validation reports and readiness scoring schemas."""

from pydantic import BaseModel, Field

from varchy.core.models.common import Severity


class ValidationIssue(BaseModel):
    category: str
    severity: Severity
    entity_id: str | None = None
    message: str
    suggestion: str | None = None


class CategoryScore(BaseModel):
    category: str
    max_points: int
    awarded_points: float
    notes: str = ""


class ReadinessReport(BaseModel):
    total_score: float = Field(..., ge=0.0, le=100.0)
    max_score: float = 100.0
    passed: bool = Field(..., description="True if score >= 80 and zero critical blockers")
    category_scores: list[CategoryScore] = Field(default_factory=list)
    critical_blockers: list[ValidationIssue] = Field(default_factory=list)
    warnings: list[ValidationIssue] = Field(default_factory=list)
    recommendations: list[ValidationIssue] = Field(default_factory=list)

