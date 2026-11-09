"""Provider manager and factory."""

from typing import Optional
from varchy.core.storage.keystore import KeyStore
from varchy.providers.base import BaseAIProvider
from varchy.providers.gemini import GeminiProvider
from varchy.providers.grok import GrokProvider
from varchy.providers.groq import GroqProvider
from varchy.providers.mock import MockAIProvider
from varchy.providers.ollama import OllamaProvider
from varchy.providers.openai import OpenAIProvider


class ProviderManager:
    """Manages AI provider selection, fallback policies, and credential discovery."""

    SUPPORTED_PROVIDERS = {
        "openai": {
            "name": "OpenAI",
            "models": ["gpt-4o", "gpt-4o-mini", "o3-mini"],
            "requires_key": True,
            "env_var": "OPENAI_API_KEY",
        },
        "gemini": {
            "name": "Google Gemini",
            "models": ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-1.5-pro"],
            "requires_key": True,
            "env_var": "GEMINI_API_KEY",
        },
        "grok": {
            "name": "xAI Grok",
            "models": ["grok-2-latest", "grok-beta"],
            "requires_key": True,
            "env_var": "XAI_API_KEY",
        },
        "groq": {
            "name": "Groq (LPU Ultra-Fast)",
            "models": ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "llama-3.3-70b-versatile"],
            "requires_key": True,
            "env_var": "GROQ_API_KEY",
        },
        "ollama": {
            "name": "Ollama (Local Offline)",
            "models": ["llama3.1:8b", "qwen2.5:7b", "mistral:7b"],
            "requires_key": False,
            "env_var": "None (Local HTTP at localhost:11434)",
        },
        "mock": {
            "name": "Mock Provider (Test Engine)",
            "models": ["mock-v1"],
            "requires_key": False,
            "env_var": "None",
        },
    }

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
            return MockAIProvider()

        if provider_name in ("gemini", "google"):
            api_key = KeyStore.get_api_key("gemini")
            if api_key:
                return GeminiProvider(api_key=api_key)
            return MockAIProvider()

        if provider_name in ("grok", "xai"):
            api_key = KeyStore.get_api_key("grok")
            if api_key:
                return GrokProvider(api_key=api_key)
            return MockAIProvider()

        if provider_name == "groq":
            api_key = KeyStore.get_api_key("groq")
            if api_key:
                return GroqProvider(api_key=api_key)
            return MockAIProvider()

        if provider_name == "ollama":
            return OllamaProvider()

        # Fallback to mock provider
        return MockAIProvider()
