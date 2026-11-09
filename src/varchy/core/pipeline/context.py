"""Pipeline execution context and transaction state."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from varchy.core.models.common import GenerationMode, StageID
from varchy.core.models.project import ProjectMetadata
from varchy.core.storage.workspace import WorkspaceManager
from varchy.providers.base import BaseAIProvider


@dataclass
class StageContext:
    """Carries execution state across pipeline stages."""

    workspace: WorkspaceManager
    provider: BaseAIProvider
    metadata: ProjectMetadata
    mode: GenerationMode = GenerationMode.AUTONOMOUS
    stage_data: dict[str, Any] = field(default_factory=dict)
    prompt_callback: Optional[Callable[[str, list[str]], str]] = None
    progress_callback: Optional[Callable[[StageID, str], None]] = None

    def get_data(self, key: str, default: Any = None) -> Any:
        return self.stage_data.get(key, default)

    def set_data(self, key: str, value: Any) -> None:
        self.stage_data[key] = value

    def log_progress(self, stage_id: StageID, message: str) -> None:
        if self.progress_callback:
            self.progress_callback(stage_id, message)
