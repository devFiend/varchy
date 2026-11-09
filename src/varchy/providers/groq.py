"""Groq provider adapter supporting ultra-fast LPU inference (llama-3.3-70b-versatile, llama-3.1-8b-instant)."""

import json
from typing import TypeVar
import httpx
from pydantic import BaseModel

from varchy.core.storage.keystore import KeyStore
from varchy.providers.base import BaseAIProvider

TModel = TypeVar("TModel", bound=BaseModel)


class GroqProvider(BaseAIProvider):
    """Integrates with Groq API for ultra-fast LPU inference using OpenAI-compatible endpoints."""

    DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"
    DEFAULT_MODEL = "openai/gpt-oss-120b"

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL):
        self.api_key = api_key if api_key is not None else KeyStore.get_api_key("groq")
        self.model = model
        self.base_url = base_url.rstrip("/")

    async def complete_structured(
        self,
        prompt: str,
        response_model: type[TModel],
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> TModel:
        if not self.api_key:
            raise ValueError(
                "Groq API key not found. Set GROQ_API_KEY environment variable or run `varchy config set-key groq`."
            )

        schema = response_model.model_json_schema()
        schema_instruction = (
            f"You MUST output valid, parseable JSON conforming strictly to this JSON Schema:\n"
            f"{json.dumps(schema, indent=2)}\n"
            "Return only the raw JSON object. Do not include markdown codeblocks, commentary, or extra text."
        )

        full_system = f"{system_prompt}\n\n{schema_instruction}" if system_prompt else schema_instruction

        messages = [
            {"role": "system", "content": full_system},
            {"role": "user", "content": prompt},
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            raw_content = data["choices"][0]["message"]["content"]
            parsed_json = json.loads(raw_content)
            return response_model.model_validate(parsed_json)
