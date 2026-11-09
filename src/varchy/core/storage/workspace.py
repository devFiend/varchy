"""Workspace management for Varchy project structures."""

import json
from pathlib import Path
from typing import Any

from varchy.core.models.blueprint import Blueprint
from varchy.core.models.project import ProjectMetadata


class WorkspaceManager:
    """Manages the .varchy/ hidden project directory and generated files."""

    VARCHY_DIR = ".varchy"
    BLUEPRINTS_DIR = "blueprints"
    CHECKPOINTS_DIR = "checkpoints"
    DOCS_DIR = "docs"

    def __init__(self, root_path: Path | str):
        self.root = Path(root_path).resolve()
        self.varchy_dir = self.root / self.VARCHY_DIR
        self.blueprints_dir = self.varchy_dir / self.BLUEPRINTS_DIR
        self.checkpoints_dir = self.varchy_dir / self.CHECKPOINTS_DIR
        self.docs_dir = self.root / self.DOCS_DIR

    def is_initialized(self) -> bool:
        """Check if project workspace is initialized."""
        return (self.varchy_dir / "project.json").exists()

    def initialize(self, metadata: ProjectMetadata) -> None:
        """Create the .varchy directory structure and save initial project metadata."""
        self.varchy_dir.mkdir(parents=True, exist_ok=True)
        self.blueprints_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

        # Write project.json
        project_json_path = self.varchy_dir / "project.json"
        self._atomic_write(project_json_path, metadata.model_dump_json(indent=2))

        # Write state.json
        state_json_path = self.varchy_dir / "state.json"
        if not state_json_path.exists():
            initial_state = {
                "current_stage": None,
                "completed_stages": [],
                "readiness_score": 0.0,
            }
            self._atomic_write(state_json_path, json.dumps(initial_state, indent=2))

    def load_metadata(self) -> ProjectMetadata:
        """Load project metadata from .varchy/project.json."""
        project_file = self.varchy_dir / "project.json"
        if not project_file.exists():
            raise FileNotFoundError(f"Project not initialized at {self.root}")
        data = json.loads(project_file.read_text(encoding="utf-8"))
        return ProjectMetadata.model_validate(data)

    def save_blueprint(self, blueprint: Blueprint) -> None:
        """Atomically persist the master Blueprint domain model."""
        target_file = self.blueprints_dir / "current.json"
        self._atomic_write(target_file, blueprint.model_dump_json(indent=2))

    def load_blueprint(self) -> Blueprint:
        """Load current blueprint domain model."""
        target_file = self.blueprints_dir / "current.json"
        if not target_file.exists():
            raise FileNotFoundError(f"No blueprint generated yet at {target_file}")
        data = json.loads(target_file.read_text(encoding="utf-8"))
        return Blueprint.model_validate(data)

    def save_checkpoint(self, stage_id: str, data: dict[str, Any]) -> None:
        """Save a discrete stage transaction checkpoint."""
        checkpoint_path = self.checkpoints_dir / f"{stage_id}.json"
        self._atomic_write(checkpoint_path, json.dumps(data, indent=2))

    def load_checkpoint(self, stage_id: str) -> dict[str, Any] | None:
        """Load a stage checkpoint if it exists."""
        checkpoint_path = self.checkpoints_dir / f"{stage_id}.json"
        if not checkpoint_path.exists():
            return None
        return json.loads(checkpoint_path.read_text(encoding="utf-8"))

    def _atomic_write(self, target_path: Path, content: str) -> None:
        """Write to a temporary file first and rename to ensure atomicity."""
        temp_path = target_path.with_suffix(f"{target_path.suffix}.tmp")
        temp_path.write_text(content, encoding="utf-8")
        temp_path.replace(target_path)

