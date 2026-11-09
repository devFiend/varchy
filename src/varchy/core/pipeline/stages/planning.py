"""Planning stage: generates phases and implementation tasks (TASK-###) with acyclic dependencies."""

from varchy.core.models.common import Priority, StageID
from varchy.core.models.planning import Phase, PlanningSpec, Task
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class PlanningStage(BaseStage[PlanningSpec]):
    stage_id = StageID.PLANNING
    depends_on = [StageID.DATA_API]

    async def execute(self, ctx: StageContext) -> PlanningSpec:
        ctx.log_progress(self.stage_id, "Decomposing blueprint into phased implementation tasks (TASK-###)...")
        product = ctx.get_data("product")
        req_ids = [r.id for r in product.requirements] if product else ["REQ-001", "REQ-002"]

        try:
            prompt = (
                f"Generate complete PlanningSpec for '{ctx.metadata.name}'. "
                f"Define ordered Phases (PHASE-1, PHASE-2, etc.) and atomic Tasks (TASK-001, etc.). "
                f"Every task must map to requirement IDs ({req_ids}), specify explicit completion criteria, "
                f"and declare dependencies without circular deadlocks."
            )
            spec = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=PlanningSpec,
                system_prompt="You are an Engineering Program Manager. Break requirements into strictly ordered, non-circular development tasks with measurable completion criteria.",
            )
        except Exception:
            spec = PlanningSpec(
                phases=[
                    Phase(
                        id="PHASE-1",
                        name="Foundation & Architecture Setup",
                        objective="Scaffold project repository, environment configuration, and database migrations.",
                        order=1,
                    ),
                    Phase(
                        id="PHASE-2",
                        name="Core Engine & Domain Services",
                        objective="Implement business logic, data models, and API endpoints.",
                        order=2,
                    ),
                    Phase(
                        id="PHASE-3",
                        name="UI/UX & Integration Testing",
                        objective="Build presentation layer and complete end-to-end integration verification.",
                        order=3,
                    ),
                ],
                tasks=[
                    Task(
                        id="TASK-001",
                        phase_id="PHASE-1",
                        title="Repository Scaffolding & Configuration",
                        description="Initialize package build configuration, virtual environment, and dependency manifests.",
                        priority=Priority.CRITICAL,
                        dependencies=[],
                        requirement_ids=[req_ids[0]],
                        completion_criteria=[
                            "Project installs cleanly in virtual environment.",
                            "Linting and formatting tools pass with zero warnings.",
                        ],
                    ),
                    Task(
                        id="TASK-002",
                        phase_id="PHASE-1",
                        title="Database Migration & Schema Definition",
                        description="Configure relational persistence models, connection pooling, and baseline migrations.",
                        priority=Priority.HIGH,
                        dependencies=["TASK-001"],
                        requirement_ids=[req_ids[1] if len(req_ids) > 1 else req_ids[0]],
                        completion_criteria=[
                            "Database connects with credentials from secure vault.",
                            "Automated migration creates all entity tables cleanly.",
                        ],
                    ),
                    Task(
                        id="TASK-003",
                        phase_id="PHASE-2",
                        title="Implement Core Workflow Engine",
                        description="Implement service boundaries, domain operations, and state machine transitions.",
                        priority=Priority.CRITICAL,
                        dependencies=["TASK-002"],
                        requirement_ids=[req_ids[0]],
                        completion_criteria=[
                            "Unit test coverage on core service exceeds 90%.",
                            "Execution latency remains below 200ms per transaction.",
                        ],
                    ),
                    Task(
                        id="TASK-004",
                        phase_id="PHASE-2",
                        title="Expose REST & Contract APIs",
                        description="Implement API controllers, request validation filters, and error handlers.",
                        priority=Priority.HIGH,
                        dependencies=["TASK-003"],
                        requirement_ids=[req_ids[0]],
                        completion_criteria=[
                            "Endpoints conform strictly to documented OpenAPI / JSON schemas.",
                            "Authentication middleware blocks unauthorized requests.",
                        ],
                    ),
                    Task(
                        id="TASK-005",
                        phase_id="PHASE-3",
                        title="Implement Presentation Views & Screens",
                        description="Build UI views according to screen specifications and interaction states.",
                        priority=Priority.MEDIUM,
                        dependencies=["TASK-004"],
                        requirement_ids=[req_ids[0]],
                        completion_criteria=[
                            "All documented interaction states (Loading, Error, Empty) are rendered.",
                            "Keyboard navigation and accessibility standards are satisfied.",
                        ],
                    ),
                ],
            )

        ctx.set_data("planning", spec)
        return spec

