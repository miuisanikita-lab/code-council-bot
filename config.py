"""Configuration for Code Council Bot."""

import os
from dataclasses import dataclass, field


@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    enabled: bool = False


@dataclass
class Config:
    """Main bot configuration."""

    telegram_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    openai: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url="https://api.openai.com/v1",
        model="gpt-4o",
        enabled=bool(os.getenv("OPENAI_API_KEY")),
    ))

    anthropic: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        base_url="https://api.anthropic.com",
        model="claude-sonnet-4-20250514",
        enabled=bool(os.getenv("ANTHROPIC_API_KEY")),
    ))

    google: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("GOOGLE_API_KEY", ""),
        base_url="https://generativelanguage.googleapis.com",
        model="gemini-2.5-pro",
        enabled=bool(os.getenv("GOOGLE_API_KEY")),
    ))

    deepseek: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url="https://api.deepseek.com/v1",
        model="deepseek-coder",
        enabled=bool(os.getenv("DEEPSEEK_API_KEY")),
    ))

    mistral: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
        base_url="https://api.mistral.ai/v1",
        model="codestral-latest",
        enabled=bool(os.getenv("MISTRAL_API_KEY")),
    ))

    together: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("TOGETHER_API_KEY", ""),
        base_url="https://api.together.xyz/v1",
        model="meta-llama/CodeLlama-70b-Instruct-hf",
        enabled=bool(os.getenv("TOGETHER_API_KEY")),
    ))

    groq: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("GROQ_API_KEY", ""),
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        enabled=bool(os.getenv("GROQ_API_KEY")),
    ))

    openrouter: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        api_key=os.getenv("OPENROUTER_API_KEY", ""),
        base_url="https://openrouter.ai/api/v1",
        model="qwen/qwen-2.5-coder-32b-instruct",
        enabled=bool(os.getenv("OPENROUTER_API_KEY")),
    ))

    discussion_rounds: int = 2
    max_agents_per_task: int = 5
    director_provider: str = "anthropic"

    @classmethod
    def load(cls) -> "Config":
        return cls()

    def get_provider(self, name: str) -> ProviderConfig:
        return getattr(self, name, ProviderConfig())

    def get_enabled_providers(self) -> list[str]:
        providers = [
            "openai", "anthropic", "google", "deepseek",
            "mistral", "together", "groq", "openrouter",
        ]
        return [p for p in providers if getattr(self, p).enabled]
