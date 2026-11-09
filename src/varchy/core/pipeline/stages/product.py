"""Product stage: generates PRD, requirements REQ-###, features, personas."""

from varchy.core.models.common import Priority, RequirementType, StageID
from varchy.core.models.requirement import Feature, Persona, ProductSpec, Requirement
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class ProductStage(BaseStage[ProductSpec]):
    stage_id = StageID.PRODUCT
    depends_on = [StageID.CLARIFICATION]

    async def execute(self, ctx: StageContext) -> ProductSpec:
        ctx.log_progress(self.stage_id, "Synthesizing Product Requirements Document (PRD)...")
        brief = ctx.get_data("brief")
        idea = ctx.metadata.description

        try:
            prompt = (
                f"Generate complete ProductSpec for project '{ctx.metadata.name}'. "
                f"Idea: '{idea}'. Target audience: {brief.target_audience if brief else 'General Developers'}."
            )
            spec = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=ProductSpec,
                system_prompt="You are a Lead Product Manager. Create rigorous functional requirements with acceptance criteria and user stories.",
            )
        except Exception:
            # Fallback deterministic product spec
            spec = ProductSpec(
                overview=f"Production-grade realization of: {idea}",
                problem_statement="Users face friction and lack unified tools to execute their workflows efficiently.",
                vision=f"To become the gold standard open solution for {ctx.metadata.name}.",
                personas=[
                    Persona(
                        id="PERS-001",
                        name="Alex Rivera",
                        role="Lead Developer / Architect",
                        goals=["Build scalable systems quickly", "Avoid documentation drift"],
                        pain_points=["Incomplete specifications", "Context switching"],
                    )
                ],
                requirements=[
                    Requirement(
                        id="REQ-001",
                        title="Core Domain Workflow Engine",
                        description=f"System provides primary engine executing: {idea}",
                        type=RequirementType.FUNCTIONAL,
                        priority=Priority.CRITICAL,
                        acceptance_criteria=[
                            "Engine initializes successfully from configuration.",
                            "Processes input within sub-second execution thresholds.",
                            "Emits structured validation events on state change.",
                        ],
                        user_story="As a developer, I want the core workflow engine to execute predictably.",
                    ),
                    Requirement(
                        id="REQ-002",
                        title="Persistence & State Management",
                        description="System atomically stores and retrieves state.",
                        type=RequirementType.FUNCTIONAL,
                        priority=Priority.HIGH,
                        acceptance_criteria=[
                            "State survives application restarts.",
                            "Data is validated against schema before commit.",
                        ],
                    ),
                ],
                features=[
                    Feature(
                        id="FEAT-001",
                        title="Engine Execution Pipeline",
                        description="Orchestrates workflow phases and persistence.",
                        requirement_ids=["REQ-001", "REQ-002"],
                    )
                ],
            )

        ctx.set_data("product", spec)
        return spec
