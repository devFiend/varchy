"""Base AI Provider interface and abstractions."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar
from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class BaseAIProvider(ABC):
    """Abstract interface for LLM provider adapters."""

    @abstractmethod
    async def complete_structured(
        self,
        prompt: str,
        response_model: type[TModel],
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> TModel:
        """Execute model request and return validated Pydantic model."""
        ...

