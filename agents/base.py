"""Base Agent class for all AI coding agents."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentResponse:
    """Response from an AI agent."""
    agent_name: str
    code: str
    explanation: str
    confidence: float  # 0.0 to 1.0
    suggestions: list[str] = field(default_factory=list)
    critique: str = ""


@dataclass
class AgentProfile:
    """Profile defining an AI agent's personality and specialization."""
    name: str
    emoji: str
    provider: str
    model_override: str | None = None
    specialization: str = ""
    coding_style: str = ""
    strengths: list[str] = field(default_factory=list)
    system_prompt: str = ""

    def build_system_prompt(self) -> str:
        if self.system_prompt:
            return self.system_prompt
        return (
            f"You are {self.name}, an expert AI coding assistant.\n"
            f"Specialization: {self.specialization}\n"
            f"Coding style: {self.coding_style}\n"
            f"Strengths: {', '.join(self.strengths)}\n\n"
            "RULES:\n"
            "- You ONLY write code. No unnecessary explanations.\n"
            "- Write clean, production-ready, well-structured code.\n"
            "- Follow best practices and design patterns.\n"
            "- Include proper error handling and type hints.\n"
            "- Be concise but thorough.\n"
        )
