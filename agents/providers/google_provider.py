"""Google Gemini provider."""

from __future__ import annotations

import logging

import aiohttp

from agents.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class GoogleProvider(BaseProvider):
    """Provider for Google Gemini API."""

    async def generate(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        model = self._get_model(model)
        url = (
            f"{self.config.base_url}/v1beta/models/{model}"
            f":generateContent?key={self.config.api_key}"
        )

        system_instruction = ""
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
            elif msg["role"] == "assistant":
                contents.append({"role": "model", "parts": [{"text": msg["content"]}]})

        payload: dict = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error("[google] API error %d: %s", resp.status, error_text)
                        return f"[google error: {resp.status}]"
                    data = await resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            logger.exception("[google] Request failed")
            return "[google request failed]"
