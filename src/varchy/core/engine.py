"""Unified Varchy Core Engine coordinator."""

from pathlib import Path
from typing import Optional

from varchy.core.compiler.compiler import DocCompiler
from varchy.core.models.blueprint import Blueprint
from varchy.core.models.common import GenerationMode, ProjectCategory
from varchy.core.models.project import ProjectMetadata
from varchy.core.models.validation import ReadinessReport
from varchy.core.storage.workspace import WorkspaceManager
from varchy.core.validator.engine import ValidationEngine
from varchy.providers.manager import ProviderManager
from varchy.providers.mock import MockAIProvider


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

    async def generate_blueprint(
        self,
        idea: str,
        category: ProjectCategory = ProjectCategory.DEV_TOOL,
        provider_name: Optional[str] = None,
    ) -> Blueprint:
        """
        Execute generation pipeline and persist blueprint.
        Produces full structured blueprint and compiles docs.
        """
        # Ensure project workspace is initialized
        if not self.workspace.is_initialized():
            self.initialize_project(
                name="ArchitectedProject",
                description=idea,
                category=category,
            )

        provider = self.provider_mgr.get_provider(provider_name)
        # Using mock or live provider to get structured model
        if isinstance(provider, MockAIProvider):
            blueprint = provider.generate_mock_blueprint(
                name=self.workspace.load_metadata().name,
                idea=idea,
            )
        else:
            blueprint = await provider.complete_structured(
                prompt=f"Generate complete software blueprint for idea: {idea}",
                response_model=Blueprint,
            )

        # Save structured source of truth
        self.workspace.save_blueprint(blueprint)

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

