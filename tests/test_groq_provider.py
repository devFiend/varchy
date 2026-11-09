"""Unit tests for Groq provider adapter."""

import pytest
from pydantic import BaseModel
from unittest.mock import AsyncMock, MagicMock, patch

from varchy.providers.groq import GroqProvider
from varchy.providers.manager import ProviderManager


class DummyResponse(BaseModel):
    summary: str
    score: int


@pytest.mark.asyncio
async def test_groq_provider_initialization():
    provider = GroqProvider(api_key="gsk_test_12345", model="llama-3.3-70b-versatile")
    assert provider.api_key == "gsk_test_12345"
    assert provider.model == "llama-3.3-70b-versatile"
    assert provider.base_url == "https://api.groq.com/openai/v1"


@pytest.mark.asyncio
async def test_groq_provider_missing_key_raises():
    provider = GroqProvider(api_key="")
    with pytest.raises(ValueError, match="Groq API key not found"):
        await provider.complete_structured("Hello", DummyResponse)


@pytest.mark.asyncio
async def test_groq_provider_complete_structured_mock():
    provider = GroqProvider(api_key="gsk_dummy_key")

    mock_json_response = {
        "choices": [
            {
                "message": {
                    "content": '{"summary": "Test architectural brief", "score": 98}'
                }
            }
        ]
    }

    mock_client = AsyncMock()
    mock_post_res = MagicMock()
    mock_post_res.raise_for_status = MagicMock()
    mock_post_res.json.return_value = mock_json_response
    mock_client.post.return_value = mock_post_res
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client):
        res = await provider.complete_structured(
            prompt="Analyze architectural plan",
            response_model=DummyResponse,
            system_prompt="You are a senior architect.",
        )
        assert res.summary == "Test architectural brief"
        assert res.score == 98


def test_provider_manager_recognizes_groq():
    mgr = ProviderManager()
    assert "groq" in mgr.SUPPORTED_PROVIDERS
    provider = mgr.get_provider("groq")
    assert provider is not None
