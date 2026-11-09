"""Discovery stage: turns raw project idea into structured ProjectBrief."""

from varchy.core.models.common import StageID
from varchy.core.models.project import ProjectBrief
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class DiscoveryStage(BaseStage[ProjectBrief]):
    stage_id = StageID.DISCOVERY
    depends_on = []

    async def execute(self, ctx: StageContext) -> ProjectBrief:
        ctx.log_progress(self.stage_id, "Analyzing project idea and scope...")
        raw_idea = ctx.metadata.description

        # Generate structured ProjectBrief via provider
        system_prompt = (
            "You are a Principal Software Architect. Analyze the raw software idea and produce "
            "a structured project brief identifying the target audience, core problem, proposed solution, "
            "key features, technical complexity, and high-level risks."
        )
        prompt = f"Analyze idea: '{raw_idea}' for a project in category '{ctx.metadata.category.value}'."

        try:
            brief = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=ProjectBrief,
                system_prompt=system_prompt,
            )
        except Exception:
            # Resilient fallback if provider is mock or lacks direct ProjectBrief schema support
            brief = ProjectBrief(
                raw_idea=raw_idea,
                target_audience=["Developers", "Power Users"],
                core_problem=f"Solves workflow inefficiencies described in: {raw_idea}",
                proposed_solution=f"An engineered software solution realizing: {raw_idea}",
                key_features=["Core Domain Workflow", "Data Persistence", "User Interface / API"],
                technical_complexity="medium",
                identified_risks=["Integration complexity", "Scope creep"],
            )

        ctx.set_data("brief", brief)
        return brief

