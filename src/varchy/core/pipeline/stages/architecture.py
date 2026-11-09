"""Architecture stage: generates ArchitectureSpec, tech stack trade-offs, and security."""

from varchy.core.models.architecture import ArchitectureSpec, SecuritySpec, ServiceBoundary, TechStackItem
from varchy.core.models.common import StageID
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class ArchitectureStage(BaseStage[ArchitectureSpec]):
    stage_id = StageID.ARCHITECTURE
    depends_on = [StageID.PRODUCT]

    async def execute(self, ctx: StageContext) -> ArchitectureSpec:
        ctx.log_progress(self.stage_id, "Formulating technical architecture and security boundaries...")
        product = ctx.get_data("product")
        brief = ctx.get_data("brief")

        try:
            prompt = (
                f"Design technical architecture for '{ctx.metadata.name}'. "
                f"Requirements: {[r.title for r in product.requirements] if product else []}. "
                f"Define technology stack with explicit trade-off justifications, service boundaries, "
                f"frontend/backend architectures, and comprehensive security controls."
            )
            spec = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=ArchitectureSpec,
                system_prompt="You are an Enterprise Software Architect. Justify every technology decision with trade-offs.",
            )
        except Exception:
            spec = ArchitectureSpec(
                tech_stack=[
                    TechStackItem(
                        category="Language & Runtime",
                        name="Python 3.12+",
                        justification="Modern type annotations, high async I/O throughput, and rich library ecosystem.",
                    ),
                    TechStackItem(
                        category="Persistence",
                        name="PostgreSQL / SQLite",
                        justification="Strong ACID guarantees, relational indexing, and rock-solid reliability.",
                    ),
                    TechStackItem(
                        category="CLI & Orchestration",
                        name="Typer + Rich",
                        justification="Ergonomic developer experience with rich terminal formatting and automatic validation.",
                    ),
                ],
                service_boundaries=[
                    ServiceBoundary(
                        name="Core Orchestration Engine",
                        description="Executes workflow stages, validates state, and compiles artifacts.",
                        responsibilities=["Stage execution", "DAG state persistence", "Schema validation"],
                    ),
                    ServiceBoundary(
                        name="Storage & Vault Adapter",
                        description="Manages local project state, checkpoints, and secure key retrieval.",
                        responsibilities=["Filesystem transactions", "Keyring security", "Atomic writes"],
                    ),
                ],
                frontend_architecture="Modern responsive presentation shell with accessible interaction patterns.",
                backend_architecture="Clean Hexagonal (Ports & Adapters) domain-driven service architecture.",
                security=SecuritySpec(
                    authentication="Industry-standard cryptographic token authentication (JWT / Bearer / Passphrase).",
                    authorization="Granular Role-Based Access Control (RBAC) with least-privilege principles.",
                    secret_management="Zero plaintext disk exposure; hardware-backed OS Keychain storage.",
                    input_validation="Strict Pydantic v2 schema validation on all inbound payloads.",
                    data_protection="TLS 1.3 in transit and AES-256-GCM encryption at rest.",
                    rate_limiting="Sliding window token bucket rate limiter to mitigate abuse.",
                ),
                deployment_topology="Containerized OCI image deployable across Linux, macOS, and cloud hosts.",
                scalability_notes="Horizontally scalable stateless services with pooled persistent database connections.",
            )

        ctx.set_data("architecture", spec)
        return spec

