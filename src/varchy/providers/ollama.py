"""Ollama local inference provider adapter for 100% offline blueprint generation."""

import json
from typing import TypeVar
import httpx
from pydantic import BaseModel

from varchy.providers.base import BaseAIProvider

TModel = TypeVar("TModel", bound=BaseModel)


class OllamaProvider(BaseAIProvider):
    """Integrates with locally running Ollama instance via HTTP API."""

    DEFAULT_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "llama3.1:8b"

    def __init__(self, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL):
        self.model = model
        self.base_url = base_url.rstrip("/")

    async def complete_structured(
        self,
        prompt: str,
        response_model: type[TModel],
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> TModel:
        schema = response_model.model_json_schema()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": schema,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                raw_content = data["message"]["content"]
                parsed_json = json.loads(raw_content)
                return response_model.model_validate(parsed_json)
        except httpx.ConnectError:
            raise ConnectionError(
                f"Could not connect to Ollama at {self.base_url}. Ensure Ollama is running (`ollama serve`)."
            )

