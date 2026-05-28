"""OpenAI-compatible provider (works with OpenAI, Together, Groq, OpenRouter, DeepSeek)."""

from __future__ import annotations

import logging

import aiohttp

from agents.providers.base_provider import BaseProvider
from config import ProviderConfig

logger = logging.getLogger(__name__)


class OpenAICompatibleProvider(BaseProvider):
    """Provider for any OpenAI-compatible API."""

    def __init__(self, config: ProviderConfig, provider_name: str = "openai") -> None:
        super().__init__(config)
        self.provider_name = provider_name

    async def generate(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        model = self._get_model(model)
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        if self.provider_name == "openrouter":
            headers["HTTP-Referer"] = "https://github.com/code-council-bot"
            headers["X-Title"] = "Code Council Bot"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)
                ) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error(
                            "[%s] API error %d: %s", self.provider_name, resp.status, error_text
                        )
                        return f"[{self.provider_name} error: {resp.status}]"
                    data = await resp.json()
                    return data["choices"][0]["message"]["content"]
        except Exception:
            logger.exception("[%s] Request failed", self.provider_name)
            return f"[{self.provider_name} request failed]"
