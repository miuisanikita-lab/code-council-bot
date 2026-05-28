"""Anthropic (Claude) provider."""

from __future__ import annotations

import logging

import aiohttp

from agents.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseProvider):
    """Provider for Anthropic Claude API."""

    async def generate(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        model = self._get_model(model)
        url = f"{self.config.base_url}/v1/messages"
        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        system_msg = ""
        api_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                api_messages.append(msg)

        payload: dict = {
            "model": model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system_msg:
            payload["system"] = system_msg

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)
                ) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error("[anthropic] API error %d: %s", resp.status, error_text)
                        return f"[anthropic error: {resp.status}]"
                    data = await resp.json()
                    return data["content"][0]["text"]
        except Exception:
            logger.exception("[anthropic] Request failed")
            return "[anthropic request failed]"
