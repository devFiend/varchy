"""Data & API stage: generates database entities (ENT-###) and API contracts (API-###)."""

from varchy.core.models.common import StageID
from varchy.core.models.data_api import ApiEndpoint, DataApiSpec, DatabaseAttribute, DatabaseEntity
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class DataApiStage(BaseStage[DataApiSpec]):
    stage_id = StageID.DATA_API
    depends_on = [StageID.ARCHITECTURE]

    async def execute(self, ctx: StageContext) -> DataApiSpec:
        ctx.log_progress(self.stage_id, "Designing database schemas (ENT-###) and API contracts (API-###)...")
        product = ctx.get_data("product")
        req_ids = [r.id for r in product.requirements] if product else ["REQ-001"]

        try:
            prompt = (
                f"Generate complete DataApiSpec for '{ctx.metadata.name}'. "
                f"Create normalized DatabaseEntity objects with primary keys, attributes, and indexes. "
                f"Define REST/RPC ApiEndpoint contracts with HTTP methods, paths, status codes, "
                f"and map endpoints to requirement IDs: {req_ids}."
            )
            spec = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=DataApiSpec,
                system_prompt="You are a Principal Database Administrator & API Architect. Ensure all entities have explicit primary keys and API endpoints specify response schemas.",
            )
        except Exception:
            spec = DataApiSpec(
                entities=[
                    DatabaseEntity(
                        id="ENT-001",
                        name="projects",
                        description="Core project records containing configuration and execution state.",
                        attributes=[
                            DatabaseAttribute(name="id", data_type="UUID", is_primary_key=True),
                            DatabaseAttribute(name="name", data_type="VARCHAR(255)", is_nullable=False),
                            DatabaseAttribute(name="slug", data_type="VARCHAR(255)", is_unique=True, is_nullable=False),
                            DatabaseAttribute(name="status", data_type="VARCHAR(50)", is_nullable=False),
                            DatabaseAttribute(name="created_at", data_type="TIMESTAMP WITH TIME ZONE", is_nullable=False),
                        ],
                        indexes=["idx_projects_slug", "idx_projects_created_at"],
                    ),
                    DatabaseEntity(
                        id="ENT-002",
                        name="execution_runs",
                        description="Transaction log for individual orchestrator pipeline executions.",
                        attributes=[
                            DatabaseAttribute(name="id", data_type="UUID", is_primary_key=True),
                            DatabaseAttribute(name="project_id", data_type="UUID", foreign_key_target="projects.id", is_nullable=False),
                            DatabaseAttribute(name="current_stage", data_type="VARCHAR(50)", is_nullable=False),
                            DatabaseAttribute(name="readiness_score", data_type="NUMERIC(5,2)", is_nullable=False),
                        ],
                        indexes=["idx_execution_project_id"],
                    ),
                ],
                endpoints=[
                    ApiEndpoint(
                        id="API-001",
                        path="/api/v1/projects",
                        method="POST",
                        summary="Initialize or register a new project workspace",
                        auth_required=True,
                        request_body_schema={"type": "object", "properties": {"name": {"type": "string"}, "description": {"type": "string"}}, "required": ["name"]},
                        response_body_schema={"type": "object", "properties": {"id": {"type": "string"}, "status": {"type": "string"}}},
                        status_codes=[201, 400, 401, 500],
                        requirement_ids=req_ids[:1],
                    ),
                    ApiEndpoint(
                        id="API-002",
                        path="/api/v1/projects/{id}/blueprint",
                        method="GET",
                        summary="Retrieve current structured architecture blueprint and readiness report",
                        auth_required=True,
                        response_body_schema={"type": "object", "properties": {"blueprint": {"type": "object"}, "readiness_score": {"type": "number"}}},
                        status_codes=[200, 401, 404, 500],
                        requirement_ids=req_ids[:1],
                    ),
                ],
                mermaid_er_diagram="""erDiagram
    PROJECTS ||--o{ EXECUTION_RUNS : contains
    PROJECTS {
        uuid id PK
        string name
        string slug UK
        string status
        timestamp created_at
    }
    EXECUTION_RUNS {
        uuid id PK
        uuid project_id FK
        string current_stage
        float readiness_score
    }""",
            )

        ctx.set_data("data_api", spec)
        return spec
