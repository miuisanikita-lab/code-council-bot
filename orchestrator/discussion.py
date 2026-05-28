"""Discussion orchestrator — coordinates multi-agent code discussions."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable

from agents.base import AgentProfile, AgentResponse
from agents.profiles import AGENT_PROFILES
from agents.providers.provider_factory import create_provider
from config import Config

logger = logging.getLogger(__name__)


@dataclass
class DiscussionMessage:
    """A single message in the discussion thread."""
    agent_name: str
    emoji: str
    content: str
    round_num: int
    message_type: str = "opinion"  # opinion, critique, suggestion, code


@dataclass
class DiscussionResult:
    """Result of a full multi-agent discussion."""
    prompt: str
    messages: list[DiscussionMessage] = field(default_factory=list)
    agent_responses: list[AgentResponse] = field(default_factory=list)
    final_code: str = ""
    final_explanation: str = ""
    participating_agents: list[str] = field(default_factory=list)


class DiscussionOrchestrator:
    """Orchestrates multi-agent code discussions."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._providers: dict = {}
        self._init_providers()

    def _init_providers(self) -> None:
        for provider_name in self.config.get_enabled_providers():
            self._providers[provider_name] = create_provider(provider_name, self.config)

    def _get_available_agents(self) -> list[AgentProfile]:
        available = []
        for agent in AGENT_PROFILES:
            if agent.provider in self._providers:
                available.append(agent)
        return available

    def _select_agents(self, count: int) -> list[AgentProfile]:
        available = self._get_available_agents()
        if len(available) <= count:
            return available

        seen_providers: set[str] = set()
        selected: list[AgentProfile] = []
        for agent in available:
            if agent.provider not in seen_providers:
                selected.append(agent)
                seen_providers.add(agent.provider)
                if len(selected) >= count:
                    break

        for agent in available:
            if agent not in selected and len(selected) < count:
                selected.append(agent)

        return selected[:count]

    async def _query_agent(
        self,
        agent: AgentProfile,
        messages: list[dict[str, str]],
    ) -> str:
        provider = self._providers.get(agent.provider)
        if not provider:
            return f"[{agent.name}: provider not available]"

        return await provider.generate(
            messages=messages,
            model=agent.model_override,
            temperature=0.7,
            max_tokens=4096,
        )

    async def run_discussion(
        self,
        prompt: str,
        on_message: Callable[[DiscussionMessage], None] | None = None,
    ) -> DiscussionResult:
        """Run a full multi-agent discussion on a coding task."""
        result = DiscussionResult(prompt=prompt)
        agents = self._select_agents(self.config.max_agents_per_task)

        if not agents:
            result.final_code = "No AI providers configured. Please set API keys."
            return result

        result.participating_agents = [a.name for a in agents]
        logger.info(
            "Starting discussion with %d agents: %s",
            len(agents),
            ", ".join(a.name for a in agents),
        )

        # === ROUND 1: Initial code generation ===
        round1_tasks = []
        for agent in agents:
            msgs = [
                {"role": "system", "content": agent.build_system_prompt()},
                {
                    "role": "user",
                    "content": (
                        f"Write code for the following task. "
                        f"Provide your solution with explanation.\n\n"
                        f"TASK:\n{prompt}\n\n"
                        f"Format your response as:\n"
                        f"EXPLANATION: (brief explanation of your approach)\n"
                        f"CONFIDENCE: (0.0 to 1.0)\n"
                        f"```\n(your code here)\n```"
                    ),
                },
            ]
            round1_tasks.append(self._query_agent(agent, msgs))

        round1_responses = await asyncio.gather(*round1_tasks, return_exceptions=True)

        for agent, response in zip(agents, round1_responses):
            if isinstance(response, Exception):
                content = f"[Error: {response}]"
            else:
                content = response

            code = self._extract_code(content)
            explanation = self._extract_explanation(content)
            confidence = self._extract_confidence(content)

            agent_response = AgentResponse(
                agent_name=agent.name,
                code=code,
                explanation=explanation,
                confidence=confidence,
            )
            result.agent_responses.append(agent_response)

            msg = DiscussionMessage(
                agent_name=agent.name,
                emoji=agent.emoji,
                content=content,
                round_num=1,
                message_type="code",
            )
            result.messages.append(msg)
            if on_message:
                on_message(msg)

        # === ROUND 2: Review and critique ===
        if self.config.discussion_rounds >= 2 and len(agents) > 1:
            all_solutions = self._format_all_solutions(result.agent_responses)

            review_tasks = []
            for agent in agents:
                msgs = [
                    {"role": "system", "content": agent.build_system_prompt()},
                    {
                        "role": "user",
                        "content": (
                            f"Here is the original task:\n{prompt}\n\n"
                            f"Here are all the solutions from different AI agents:\n\n"
                            f"{all_solutions}\n\n"
                            f"Review all solutions. Point out:\n"
                            f"1. Bugs or issues in each solution\n"
                            f"2. Which solution is best and why\n"
                            f"3. What improvements you'd suggest\n"
                            f"4. Your improved version combining the best ideas\n\n"
                            f"Format:\n"
                            f"REVIEW: (your analysis)\n"
                            f"BEST_SOLUTION: (agent name)\n"
                            f"```\n(your improved code)\n```"
                        ),
                    },
                ]
                review_tasks.append(self._query_agent(agent, msgs))

            review_responses = await asyncio.gather(*review_tasks, return_exceptions=True)

            for agent, response in zip(agents, review_responses):
                if isinstance(response, Exception):
                    content = f"[Review error: {response}]"
                else:
                    content = response

                code = self._extract_code(content)
                if code:
                    for ar in result.agent_responses:
                        if ar.agent_name == agent.name:
                            ar.code = code
                            ar.critique = content

                msg = DiscussionMessage(
                    agent_name=agent.name,
                    emoji=agent.emoji,
                    content=content,
                    round_num=2,
                    message_type="critique",
                )
                result.messages.append(msg)
                if on_message:
                    on_message(msg)

        return result

    def _format_all_solutions(self, responses: list[AgentResponse]) -> str:
        parts = []
        for r in responses:
            parts.append(
                f"=== {r.agent_name} (confidence: {r.confidence:.1f}) ===\n"
                f"{r.explanation}\n```\n{r.code}\n```\n"
            )
        return "\n".join(parts)

    @staticmethod
    def _extract_code(text: str) -> str:
        if "```" not in text:
            return text.strip()

        blocks: list[str] = []
        in_block = False
        current: list[str] = []

        for line in text.split("\n"):
            if line.strip().startswith("```") and not in_block:
                in_block = True
                continue
            elif line.strip().startswith("```") and in_block:
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
    def _extract_explanation(text: str) -> str:
        for line in text.split("\n"):
            lower = line.lower().strip()
            if lower.startswith("explanation:"):
                return line.split(":", 1)[1].strip()
        return ""

    @staticmethod
    def _extract_confidence(text: str) -> float:
        for line in text.split("\n"):
            lower = line.lower().strip()
            if lower.startswith("confidence:"):
                try:
                    val = float(line.split(":", 1)[1].strip())
                    return max(0.0, min(1.0, val))
                except ValueError:
                    pass
        return 0.7
