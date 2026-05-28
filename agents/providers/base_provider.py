"""Base provider interface for AI API calls."""

from __future__ import annotations

import abc
import logging
from typing import Any

from config import ProviderConfig

logger = logging.getLogger(__name__)


class BaseProvider(abc.ABC):
    """Abstract base class for AI providers."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @abc.abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Generate a response from the AI model."""
        ...

    def _get_model(self, model_override: str | None) -> str:
        return model_override or self.config.model
