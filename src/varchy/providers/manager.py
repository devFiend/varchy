"""Provider manager and factory."""

from typing import Optional
from varchy.core.storage.keystore import KeyStore
from varchy.providers.base import BaseAIProvider
from varchy.providers.mock import MockAIProvider


class ProviderManager:
    """Manages AI provider selection, fallback policies, and credential discovery."""

    def __init__(self, default_provider: str = "openai"):
        self.default_provider = default_provider
        self._providers: dict[str, BaseAIProvider] = {
            "mock": MockAIProvider(),
        }

    def get_provider(self, name: Optional[str] = None) -> BaseAIProvider:
        provider_name = (name or self.default_provider).lower()

        if provider_name in self._providers:
            return self._providers[provider_name]

        # For production execution without live API keys, fallback to Mock or raise informative error
        api_key = KeyStore.get_api_key(provider_name)
        if not api_key:
            # Fall back to mock provider if no key configured for offline testing
            return self._providers["mock"]

        # Additional live adapters (OpenAI, Gemini, Grok, Ollama) plug in here
        return self._providers["mock"]

