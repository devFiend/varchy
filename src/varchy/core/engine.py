"""Unified Varchy Core Engine coordinator."""

from pathlib import Path
from typing import Callable, Optional

from varchy.core.compiler.compiler import DocCompiler
from varchy.core.models.blueprint import Blueprint
from varchy.core.models.common import GenerationMode, ProjectCategory, StageID
from varchy.core.models.project import ProjectBrief, ProjectMetadata
from varchy.core.models.validation import ReadinessReport
from varchy.core.pipeline.context import StageContext
from varchy.core.pipeline.orchestrator import PipelineOrchestrator
from varchy.core.pipeline.stages.discovery import DiscoveryStage
from varchy.core.storage.workspace import WorkspaceManager
from varchy.core.validator.engine import ValidationEngine
from varchy.providers.manager import ProviderManager


class VarchyEngine:
    """
    Central business logic coordinator.
    Both CLI and MCP server call into this engine.
    """

    def __init__(self, workspace_path: Path | str | None = None):
        target_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.workspace = WorkspaceManager(target_path)
        self.provider_mgr = ProviderManager()
        self.validator = ValidationEngine()
        self.compiler = DocCompiler(self.workspace)

    def initialize_project(
        self,
        name: str,
        description: str,
        category: ProjectCategory = ProjectCategory.SAAS,
        mode: GenerationMode = GenerationMode.AUTONOMOUS,
    ) -> ProjectMetadata:
        """Initialize workspace and metadata."""
        slug = "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")
        metadata = ProjectMetadata(
            name=name,
            slug=slug,
            description=description,
            category=category,
            generation_mode=mode,
        )
        self.workspace.initialize(metadata)
        return metadata

    async def analyze_idea(
        self,
        idea: str,
        category: ProjectCategory = ProjectCategory.DEV_TOOL,
        provider_name: Optional[str] = None,
    ) -> ProjectBrief:
        """Analyze raw idea and return structured ProjectBrief."""
        metadata = ProjectMetadata(
            name="AnalysisProject",
            slug="analysis",
            description=idea,
            category=category,
        )
        provider = self.provider_mgr.get_provider(provider_name)
        ctx = StageContext(workspace=self.workspace, provider=provider, metadata=metadata)
        stage = DiscoveryStage()
        return await stage.execute(ctx)

    async def generate_blueprint(
        self,
        idea: str,
        category: ProjectCategory = ProjectCategory.DEV_TOOL,
        provider_name: Optional[str] = None,
        mode: GenerationMode = GenerationMode.AUTONOMOUS,
        resume: bool = True,
        progress_callback: Optional[Callable[[StageID, str], None]] = None,
    ) -> Blueprint:
        """
        Execute full 10-stage generation pipeline via DAG orchestrator and persist blueprint.
        Produces full structured blueprint and compiles docs.
        """
        # Ensure project workspace is initialized
        if not self.workspace.is_initialized():
            self.initialize_project(
                name="ArchitectedProject",
                description=idea,
                category=category,
                mode=mode,
            )

        metadata = self.workspace.load_metadata()
        provider = self.provider_mgr.get_provider(provider_name)

        orchestrator = PipelineOrchestrator(
            workspace=self.workspace,
            provider=provider,
            metadata=metadata,
            mode=mode,
        )

        blueprint = await orchestrator.run(
            resume=resume,
            progress_callback=progress_callback,
        )

        # Compile documentation and agent instructions
        self.compiler.compile_all(blueprint)

        return blueprint

    def validate_blueprint(self) -> ReadinessReport:
        """Validate loaded blueprint and return deterministic readiness report."""
        blueprint = self.workspace.load_blueprint()
        return self.validator.evaluate(blueprint)

    def export_instructions(self) -> dict[str, Path]:
        """Compile and re-export markdown and agent instruction files."""
        blueprint = self.workspace.load_blueprint()
        return self.compiler.compile_all(blueprint)
