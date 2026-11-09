"""Development planning schemas: phases, tasks, and dependencies."""

from pydantic import BaseModel, Field

from varchy.core.models.common import Priority


class Task(BaseModel):
    id: str = Field(..., description="Stable identifier e.g. TASK-001")
    phase_id: str = Field(..., description="e.g. PHASE-1")
    title: str
    description: str
    priority: Priority = Field(default=Priority.MEDIUM)
    dependencies: list[str] = Field(
        default_factory=list,
        description="IDs of prerequisite tasks e.g. ['TASK-001']"
    )
    requirement_ids: list[str] = Field(
        default_factory=list,
        description="IDs of requirements realized by this task"
    )
    completion_criteria: list[str] = Field(
        default_factory=list,
        description="Clear criteria for task completion"
    )


class Phase(BaseModel):
    id: str = Field(..., description="e.g. PHASE-1")
    name: str
    objective: str
    order: int


class PlanningSpec(BaseModel):
    phases: list[Phase] = Field(default_factory=list)
    tasks: list[Task] = Field(default_factory=list)

