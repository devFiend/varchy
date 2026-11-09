"""Base stage abstraction for Varchy pipeline DAG."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from pydantic import BaseModel

from varchy.core.models.common import StageID
from varchy.core.pipeline.context import StageContext

TOutput = TypeVar("TOutput", bound=BaseModel)


class BaseStage(ABC, Generic[TOutput]):
    """Abstract stage unit in the Varchy architecture generation pipeline."""

    stage_id: StageID
    depends_on: list[StageID] = []

    @abstractmethod
    async def execute(self, ctx: StageContext) -> TOutput:
        """Execute stage logic with context and return typed output."""
        ...

    def validate_output(self, output: TOutput) -> list[str]:
        """Perform stage-specific validation checks. Returns empty list if valid."""
        return []
