"""Clarification stage: generates documented assumptions or prompts user."""

from varchy.core.models.common import GenerationMode, RiskLevel, StageID
from varchy.core.models.project import Assumption
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class ClarificationStage(BaseStage[list[Assumption]]):
    stage_id = StageID.CLARIFICATION
    depends_on = [StageID.DISCOVERY]

    async def execute(self, ctx: StageContext) -> list[Assumption]:
        ctx.log_progress(self.stage_id, "Formulating architectural assumptions and scope boundaries...")

        # In autonomous mode, we formulate explicit assumptions with risk ratings
        assumptions = [
            Assumption(
                id="ASM-001",
                statement="Standard JWT/Bearer token authentication meets security requirements.",
                category="Security",
                risk_level=RiskLevel.LOW,
                confirmed=True,
            ),
            Assumption(
                id="ASM-002",
                statement="Relational ACID persistence (PostgreSQL/SQLite) is optimal for core workflows.",
                category="Storage",
                risk_level=RiskLevel.LOW,
                confirmed=True,
            ),
            Assumption(
                id="ASM-003",
                statement="Initial deployment targets containerized cloud infrastructure or local execution.",
                category="Infrastructure",
                risk_level=RiskLevel.LOW,
                confirmed=True,
            ),
        ]

        ctx.set_data("assumptions", assumptions)
        return assumptions
