"""Clarification stage: generates documented assumptions or conducts interactive discovery interview."""

from varchy.core.models.common import GenerationMode, RiskLevel, StageID
from varchy.core.models.project import Assumption
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage


class ClarificationStage(BaseStage[list[Assumption]]):
    stage_id = StageID.CLARIFICATION
    depends_on = [StageID.DISCOVERY]

    # Pre-defined discovery interview questions for interactive discovery
    DISCOVERY_QUESTIONS = [
        {
            "id": "target_platform",
            "prompt": "Which platforms should this software support? (e.g. Web, CLI, Mobile, Desktop, Headless API)",
            "default": "Web and Headless API",
            "category": "Platform",
        },
        {
            "id": "auth_strategy",
            "prompt": "What authentication and identity model is required? (e.g. JWT/OAuth2, API Keys, Local Passphrase, None)",
            "default": "JWT / OAuth2 Bearer token authentication",
            "category": "Security",
        },
        {
            "id": "persistence_tier",
            "prompt": "What data persistence model should be used? (e.g. PostgreSQL, Local SQLite, Key-Value)",
            "default": "PostgreSQL relational persistence",
            "category": "Storage",
        },
        {
            "id": "billing_integrations",
            "prompt": "Are third-party payment or billing integrations required? (e.g. Stripe, None)",
            "default": "None (core functionality first)",
            "category": "Integrations",
        },
    ]

    async def execute(self, ctx: StageContext) -> list[Assumption]:
        ctx.log_progress(self.stage_id, "Formulating architectural assumptions and scope boundaries...")
        assumptions: list[Assumption] = []

        if ctx.mode == GenerationMode.INTERACTIVE and ctx.prompt_callback:
            # Interactive Interview Loop
            ctx.log_progress(self.stage_id, "Starting interactive architecture discovery interview...")
            for idx, q in enumerate(self.DISCOVERY_QUESTIONS, 1):
                user_answer = ctx.prompt_callback(q["prompt"], [q["default"]])
                answer_text = user_answer.strip() if user_answer else q["default"]
                assumptions.append(
                    Assumption(
                        id=f"ASM-{idx:03d}",
                        statement=f"Decision for {q['category']}: {answer_text}",
                        category=q["category"],
                        risk_level=RiskLevel.LOW,
                        confirmed=True,
                        resolution_notes="Confirmed via interactive developer interview.",
                    )
                )
        else:
            # Autonomous Assumption Generation
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
