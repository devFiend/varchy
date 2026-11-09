"""UI/UX stage: generates DesignSpec, ScreenSpec (SCREEN-###), and design system."""

from varchy.core.models.common import StageID
from varchy.core.models.design import DesignSpec, DesignSystem, InteractionState, ScreenSpec
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class UXStage(BaseStage[DesignSpec]):
    stage_id = StageID.UX
    depends_on = [StageID.PRODUCT]

    async def execute(self, ctx: StageContext) -> DesignSpec:
        ctx.log_progress(self.stage_id, "Designing Information Architecture and screen specifications...")
        product = ctx.get_data("product")
        req_ids = [r.id for r in product.requirements] if product else ["REQ-001"]

        try:
            prompt = (
                f"Generate complete DesignSpec for '{ctx.metadata.name}'. "
                f"Cover Information Architecture, Design System conventions, and key screens "
                f"with unique IDs (SCREEN-001, etc.) mapping to requirement IDs {req_ids}."
            )
            spec = await ctx.provider.complete_structured(
                prompt=prompt,
                response_model=DesignSpec,
                system_prompt="You are a Principal Product Designer & UI Architect. Create detailed screen specs with interaction states (Loading, Empty, Error, Success).",
            )
        except Exception:
            # Fallback deterministic design spec
            spec = DesignSpec(
                information_architecture="Two-tier navigation: Global sidebar for primary workflows and contextual canvas/detail view.",
                design_system=DesignSystem(
                    color_palette={
                        "primary": "#2563EB",
                        "secondary": "#475569",
                        "background": "#0F172A",
                        "surface": "#1E293B",
                        "error": "#EF4444",
                    },
                    typography={
                        "font_family": "Inter, system-ui, sans-serif",
                        "code_font": "JetBrains Mono, monospace",
                    },
                    spacing_scale=["4px", "8px", "16px", "24px", "32px", "48px"],
                    component_conventions=[
                        "Accessible focus rings",
                        "High contrast text",
                        "Responsive layout grids",
                    ],
                ),
                screens=[
                    ScreenSpec(
                        id="SCREEN-001",
                        title="Primary Dashboard / Workspace",
                        purpose="Main interface for monitoring and executing core workflows",
                        route_or_view="/dashboard",
                        required_components=["SidebarNav", "MetricsSummary", "ActivityFeed", "ActionBar"],
                        actions=["Trigger Action", "Filter View", "Export Report"],
                        interaction_states=[
                            InteractionState(state_name="Loading", behavior="Render skeleton placeholders for widgets"),
                            InteractionState(state_name="Empty", behavior="Display getting-started guide with CTA"),
                            InteractionState(state_name="Error", behavior="Show inline retry banner with error details"),
                        ],
                        requirement_ids=req_ids[:1],
                    )
                ],
            )

        ctx.set_data("design", spec)
        return spec

