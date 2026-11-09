"""Google Gemini provider adapter supporting Gemini 2.5/3 Pro and Flash models."""

import json
from typing import TypeVar
import httpx
from pydantic import BaseModel

from varchy.core.storage.keystore import KeyStore
from varchy.providers.base import BaseAIProvider

TModel = TypeVar("TModel", bound=BaseModel)


class GeminiProvider(BaseAIProvider):
    """Integrates with Google Gemini API using native JSON schema structured outputs."""

    DEFAULT_MODEL = "gemini-2.5-pro"

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or KeyStore.get_api_key("gemini")
        self.model = model

    async def complete_structured(
        self,
        prompt: str,
        response_model: type[TModel],
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> TModel:
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable or run `varchy config set-key gemini`."
            )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        schema = response_model.model_json_schema()

        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instructions: {system_prompt}"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json",
                "responseSchema": schema,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(raw_text)
            return response_model.model_validate(parsed_json)
