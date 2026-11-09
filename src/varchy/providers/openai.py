"""OpenAI provider adapter supporting GPT-4o and o-series models with structured output."""

import json
from typing import TypeVar
import httpx
from pydantic import BaseModel

from varchy.core.storage.keystore import KeyStore
from varchy.providers.base import BaseAIProvider

TModel = TypeVar("TModel", bound=BaseModel)


class OpenAIProvider(BaseAIProvider):
    """Integrates with OpenAI API using native JSON schema structured outputs."""

    DEFAULT_BASE_URL = "https://api.openai.com/v1"
    DEFAULT_MODEL = "gpt-4o"

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL, base_url: str = DEFAULT_BASE_URL):
        self.api_key = api_key or KeyStore.get_api_key("openai")
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
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable or run `varchy config set-key openai`."
            )

        schema = response_model.model_json_schema()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "strict": True,
                    "schema": schema,
                },
            },
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
