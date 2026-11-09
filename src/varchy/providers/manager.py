"""Provider manager and factory."""

from typing import Optional
from varchy.core.storage.keystore import KeyStore
from varchy.providers.base import BaseAIProvider
from varchy.providers.gemini import GeminiProvider
from varchy.providers.mock import MockAIProvider
from varchy.providers.ollama import OllamaProvider
from varchy.providers.openai import OpenAIProvider


class ProviderManager:
    """Manages AI provider selection, fallback policies, and credential discovery."""

    def __init__(self, default_provider: str = "openai"):
        self.default_provider = default_provider

    def get_provider(self, name: Optional[str] = None) -> BaseAIProvider:
        provider_name = (name or self.default_provider).lower().strip()

        if provider_name == "mock":
            return MockAIProvider()

        if provider_name in ("openai", "gpt"):
            api_key = KeyStore.get_api_key("openai")
            if api_key:
                return OpenAIProvider(api_key=api_key)
            # If no live key is set, fallback to Mock for offline execution
            return MockAIProvider()

        if provider_name in ("gemini", "google"):
            api_key = KeyStore.get_api_key("gemini")
            if api_key:
                return GeminiProvider(api_key=api_key)
            return MockAIProvider()

        if provider_name == "ollama":
            return OllamaProvider()

        # Fallback to mock provider
        return MockAIProvider()
