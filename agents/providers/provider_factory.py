"""Factory for creating AI providers."""

from __future__ import annotations

from agents.providers.anthropic_provider import AnthropicProvider
from agents.providers.base_provider import BaseProvider
from agents.providers.google_provider import GoogleProvider
from agents.providers.openai_provider import OpenAICompatibleProvider
from config import Config


def create_provider(provider_name: str, config: Config) -> BaseProvider:
    """Create a provider instance by name."""
    provider_config = config.get_provider(provider_name)

    if provider_name == "anthropic":
        return AnthropicProvider(provider_config)
    elif provider_name == "google":
        return GoogleProvider(provider_config)
    else:
        return OpenAICompatibleProvider(provider_config, provider_name=provider_name)
