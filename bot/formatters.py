"""Message formatters for Telegram output."""

from __future__ import annotations

from orchestrator.discussion import DiscussionMessage, DiscussionResult
from orchestrator.director import DirectorDecision


MAX_TG_MESSAGE_LEN = 4096


def format_agent_thinking(msg: DiscussionMessage) -> str:
    """Format a single agent's discussion message for Telegram."""
    if msg.round_num == 1:
        phase = "Kod yozmoqda"
    else:
        phase = "Tahlil qilmoqda"

    return f"{msg.emoji} <b>{msg.agent_name}</b> — {phase}..."


def format_discussion_summary(result: DiscussionResult) -> str:
    """Format a summary of the discussion."""
    agents_list = ", ".join(result.participating_agents)
    return (
        f"\U0001f4ac <b>Muhokama yakunlandi</b>\n"
        f"\U0001f465 Ishtirokchilar: {agents_list}\n"
        f"\U0001f504 Raundlar: {_count_rounds(result)}\n"
    )


def format_final_result(
    decision: DirectorDecision,
    result: DiscussionResult,
) -> list[str]:
    """Format the final result for Telegram. Returns list of messages (for splitting)."""
    header = (
        f"\U0001f3c6 <b>DIRECTOR QARORI</b>\n\n"
        f"\U0001f4a1 {decision.explanation}\n\n"
        f"\U0001f465 Kreditlar: {', '.join(decision.agents_credited)}\n\n"
    )

    code_block = f"<pre><code>{_escape_html(decision.code)}</code></pre>"
    full_message = header + code_block

    if len(full_message) <= MAX_TG_MESSAGE_LEN:
        return [full_message]

    messages = [header]
    code_chunks = _split_code(decision.code, MAX_TG_MESSAGE_LEN - 100)
    for i, chunk in enumerate(code_chunks, 1):
        label = f"\U0001f4c4 Kod ({i}/{len(code_chunks)}):\n" if len(code_chunks) > 1 else ""
        messages.append(f"{label}<pre><code>{_escape_html(chunk)}</code></pre>")

    return messages


def format_agent_detail(msg: DiscussionMessage) -> str:
    """Format detailed agent response."""
    content = msg.content
    if len(content) > 3000:
        content = content[:3000] + "\n... (qisqartirildi)"

    return (
        f"{msg.emoji} <b>{msg.agent_name}</b> "
        f"(Raund {msg.round_num}):\n\n"
        f"{_escape_html(content)}"
    )


def format_status(agents_done: int, total: int, current_agent: str) -> str:
    """Format a progress status message."""
    pct = int(agents_done / total * 100) if total > 0 else 0
    bar_filled = pct // 10
    bar_empty = 10 - bar_filled
    bar = "\u2588" * bar_filled + "\u2591" * bar_empty

    return (
        f"\u23f3 <b>Jarayon:</b> {bar} {pct}%\n"
        f"\U0001f916 Hozir: {current_agent}\n"
        f"\u2705 Tayyor: {agents_done}/{total}"
    )


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _count_rounds(result: DiscussionResult) -> int:
    if not result.messages:
        return 0
    return max(m.round_num for m in result.messages)


def _split_code(code: str, max_len: int) -> list[str]:
    if len(code) <= max_len:
        return [code]

    chunks = []
    lines = code.split("\n")
    current: list[str] = []
    current_len = 0

    for line in lines:
        if current_len + len(line) + 1 > max_len:
            chunks.append("\n".join(current))
            current = [line]
            current_len = len(line)
        else:
            current.append(line)
            current_len += len(line) + 1

    if current:
        chunks.append("\n".join(current))

    return chunks
