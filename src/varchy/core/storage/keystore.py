"""Secure BYOK credential storage using OS Keyring with environment fallbacks."""

import os
from typing import Optional

try:
    import keyring
except ImportError:
    keyring = None  # type: ignore


class KeyStore:
    """Manages API keys securely, never exposing keys to disk or logs."""

    SERVICE_NAME = "varchy"

    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """
        Retrieve API key following the security cascade:
        1. OS Keyring
        2. VARCHY_{PROVIDER}_API_KEY env variable
        3. Standard {PROVIDER}_API_KEY env variable (e.g. OPENAI_API_KEY)
        """
        provider_clean = provider.strip().lower()

        # 1. OS Keyring
        if keyring is not None:
            try:
                secret = keyring.get_password(cls.SERVICE_NAME, provider_clean)
                if secret:
                    return secret
            except Exception:
                # Keyring backend may not be available in headless environments
                pass

        # 2. VARCHY_{PROVIDER}_API_KEY
        varchy_env = f"VARCHY_{provider_clean.upper()}_API_KEY"
        if varchy_env in os.environ:
            return os.environ[varchy_env]

        # 3. Standard Provider Env
        std_env_map = {
            "openai": "OPENAI_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "grok": "XAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
        }
        std_env = std_env_map.get(provider_clean)
        if std_env and std_env in os.environ:
            return os.environ[std_env]

        return None

    @classmethod
    def set_api_key(cls, provider: str, secret: str) -> bool:
        """Store API key into OS Keyring."""
        provider_clean = provider.strip().lower()
        if keyring is not None:
            try:
                keyring.set_password(cls.SERVICE_NAME, provider_clean, secret.strip())
                return True
            except Exception:
                return False
        return False

