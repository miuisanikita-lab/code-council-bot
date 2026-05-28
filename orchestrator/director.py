"""Director agent — makes final decisions and produces the best code."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from agents.providers.provider_factory import create_provider
from config import Config
from orchestrator.discussion import DiscussionResult

logger = logging.getLogger(__name__)

DIRECTOR_SYSTEM_PROMPT = """\
You are the DIRECTOR of Code Council — a team of 20 world-class AI coding assistants.

Your role:
1. Review ALL solutions and critiques from the team
2. Identify the BEST code from all proposals
3. Combine the best ideas into ONE perfect solution
4. Fix any bugs, add error handling, optimize performance
5. Produce FINAL production-ready code

RULES:
- Output ONLY the final, perfect code
- Include ALL necessary imports
- Add proper error handling and type hints
- Follow best practices and design patterns
- The code must be complete and immediately runnable
- No placeholder comments like "TODO" or "implement here"

Format your response EXACTLY as:
DIRECTOR_DECISION: (brief explanation of which solutions you combined and why)
FINAL_CODE:
```
(the perfect, final code)
```
"""


@dataclass
class DirectorDecision:
    """Final decision from the Director."""
    code: str
    explanation: str
    agents_credited: list[str]


class Director:
    """The Director agent that produces final code."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._provider = self._select_provider()

    def _select_provider(self):
        preferred = self.config.director_provider
        enabled = self.config.get_enabled_providers()

        if preferred in enabled:
            return create_provider(preferred, self.config)

        if enabled:
            return create_provider(enabled[0], self.config)

        return None

    async def make_decision(self, discussion: DiscussionResult) -> DirectorDecision:
        """Analyze all agent responses and produce final code."""
        if not self._provider:
            best = max(discussion.agent_responses, key=lambda r: r.confidence)
            return DirectorDecision(
                code=best.code,
                explanation=f"Used {best.agent_name}'s solution (no director provider available)",
                agents_credited=[best.agent_name],
            )

        solutions_text = self._format_discussion(discussion)

        messages = [
            {"role": "system", "content": DIRECTOR_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"ORIGINAL TASK:\n{discussion.prompt}\n\n"
                    f"TEAM DISCUSSION:\n{solutions_text}\n\n"
                    f"Now produce the FINAL, PERFECT code. "
                    f"Combine the best ideas from all agents."
                ),
            },
        ]

        response = await self._provider.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=8192,
        )

        code = self._extract_final_code(response)
        explanation = self._extract_decision(response)

        return DirectorDecision(
            code=code,
            explanation=explanation,
            agents_credited=[r.agent_name for r in discussion.agent_responses],
        )

    def _format_discussion(self, discussion: DiscussionResult) -> str:
        parts = []

        parts.append("=== ROUND 1: INITIAL SOLUTIONS ===\n")
        for msg in discussion.messages:
            if msg.round_num == 1:
                parts.append(f"{msg.emoji} {msg.agent_name}:\n{msg.content}\n")
                parts.append("-" * 40 + "\n")

        round2_msgs = [m for m in discussion.messages if m.round_num == 2]
        if round2_msgs:
            parts.append("\n=== ROUND 2: REVIEWS & CRITIQUES ===\n")
            for msg in round2_msgs:
                parts.append(f"{msg.emoji} {msg.agent_name}:\n{msg.content}\n")
                parts.append("-" * 40 + "\n")

        return "\n".join(parts)

    @staticmethod
    def _extract_final_code(text: str) -> str:
        if "```" not in text:
            return text.strip()

        blocks: list[str] = []
        in_block = False
        current: list[str] = []

        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("```") and not in_block:
                in_block = True
                continue
            elif stripped.startswith("```") and in_block:
                in_block = False
                blocks.append("\n".join(current))
                current = []
                continue
            if in_block:
                current.append(line)

        if current:
            blocks.append("\n".join(current))

        return max(blocks, key=len) if blocks else text.strip()

    @staticmethod
    def _extract_decision(text: str) -> str:
        for line in text.split("\n"):
            lower = line.lower().strip()
            if lower.startswith("director_decision:"):
                return line.split(":", 1)[1].strip()
        return "Combined best solutions from all agents"
