"""Pipeline DAG Orchestrator with checkpointing, resumability, and progress feedback."""

from typing import Callable, Optional
from varchy.core.models.blueprint import Blueprint
from varchy.core.models.common import GenerationMode, StageID
from varchy.core.models.project import ProjectMetadata
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.stage import BaseStage
from varchy.core.pipeline.stages.architecture import ArchitectureStage
from varchy.core.pipeline.stages.clarification import ClarificationStage
from varchy.core.pipeline.stages.data_api import DataApiStage
from varchy.core.pipeline.stages.discovery import DiscoveryStage
from varchy.core.pipeline.stages.planning import PlanningStage
from varchy.core.pipeline.stages.product import ProductStage
from varchy.core.pipeline.stages.qa import QAStage
from varchy.core.pipeline.stages.ux import UXStage
from varchy.core.storage.workspace import WorkspaceManager
from varchy.providers.base import BaseAIProvider


class PipelineOrchestrator:
    """
    Executes the multi-stage architecture generation DAG.
    Saves atomic checkpoints after every stage, enabling resumable workflows.
    """

    def __init__(
        self,
        workspace: WorkspaceManager,
        provider: BaseAIProvider,
        metadata: ProjectMetadata,
        mode: GenerationMode = GenerationMode.AUTONOMOUS,
    ):
        self.workspace = workspace
        self.provider = provider
        self.metadata = metadata
        self.mode = mode
        self.context = StageContext(
            workspace=workspace,
            provider=provider,
            metadata=metadata,
            mode=mode,
        )

        # Register stages in topological DAG order
        self.stages: list[BaseStage] = [
            DiscoveryStage(),
            ClarificationStage(),
            ProductStage(),
            UXStage(),
            ArchitectureStage(),
            DataApiStage(),
            PlanningStage(),
            QAStage(),
        ]

    async def run(
        self,
        resume: bool = True,
        progress_callback: Optional[Callable[[StageID, str], None]] = None,
    ) -> Blueprint:
        """Run all pipeline stages and return the compiled Blueprint."""
        if progress_callback:
            self.context.progress_callback = progress_callback

        for stage in self.stages:
            stage_key = stage.stage_id.value

            # Check if checkpoint already exists for this stage
            if resume:
                cached = self.workspace.load_checkpoint(stage_key)
                if cached:
                    self.context.log_progress(stage.stage_id, f"Restoring cached checkpoint for {stage_key}...")
                    # Rehydrate into context
                    self._rehydrate_stage_data(stage.stage_id, cached)
                    continue

            # Execute stage
            result = await stage.execute(self.context)

            # Persist atomic checkpoint
            checkpoint_data = self._serialize_stage_output(result)
            self.workspace.save_checkpoint(stage_key, checkpoint_data)

        # Assemble Master Blueprint
        blueprint = Blueprint(
            metadata=self.metadata,
            brief=self.context.get_data("brief"),
            assumptions=self.context.get_data("assumptions", []),
            product=self.context.get_data("product"),
            design=self.context.get_data("design"),
            architecture=self.context.get_data("architecture"),
            data_api=self.context.get_data("data_api"),
            planning=self.context.get_data("planning"),
            testing=self.context.get_data("testing"),
        )

        # Atomically save master blueprint to workspace
        self.workspace.save_blueprint(blueprint)
        return blueprint

    def _serialize_stage_output(self, output: any) -> dict:
        if hasattr(output, "model_dump"):
            return output.model_dump()
        if isinstance(output, list) and output and hasattr(output[0], "model_dump"):
            return [item.model_dump() for item in output]
        return output

    def _rehydrate_stage_data(self, stage_id: StageID, data: any) -> None:
        from varchy.core.models.architecture import ArchitectureSpec
        from varchy.core.models.data_api import DataApiSpec
        from varchy.core.models.design import DesignSpec
        from varchy.core.models.planning import PlanningSpec
        from varchy.core.models.project import Assumption, ProjectBrief
        from varchy.core.models.requirement import ProductSpec
        from varchy.core.models.testing import TestingSpec

        if stage_id == StageID.DISCOVERY:
            self.context.set_data("brief", ProjectBrief.model_validate(data))
        elif stage_id == StageID.CLARIFICATION:
            self.context.set_data("assumptions", [Assumption.model_validate(item) for item in data])
        elif stage_id == StageID.PRODUCT:
            self.context.set_data("product", ProductSpec.model_validate(data))
        elif stage_id == StageID.UX:
            self.context.set_data("design", DesignSpec.model_validate(data))
        elif stage_id == StageID.ARCHITECTURE:
            self.context.set_data("architecture", ArchitectureSpec.model_validate(data))
        elif stage_id == StageID.DATA_API:
            self.context.set_data("data_api", DataApiSpec.model_validate(data))
        elif stage_id == StageID.PLANNING:
            self.context.set_data("planning", PlanningSpec.model_validate(data))
        elif stage_id == StageID.QA:
            self.context.set_data("testing", TestingSpec.model_validate(data))

