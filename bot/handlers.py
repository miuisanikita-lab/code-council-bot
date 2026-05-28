"""Telegram bot handlers."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.formatters import (
    format_discussion_summary,
    format_final_result,
    format_status,
)
from config import Config
from orchestrator.director import Director
from orchestrator.discussion import DiscussionMessage, DiscussionOrchestrator

logger = logging.getLogger(__name__)


class CodeCouncilBot:
    """Telegram bot for Code Council."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.orchestrator = DiscussionOrchestrator(config)
        self.director = Director(config)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        enabled = self.config.get_enabled_providers()
        available = self.orchestrator._get_available_agents()

        text = (
            "\U0001f3db\ufe0f <b>Code Council Bot</b>\n\n"
            "\U0001f4a1 20 ta eng kuchli AI koderlari bitta botda!\n\n"
            "\U0001f3af <b>Qanday ishlaydi:</b>\n"
            "1\ufe0f\u20e3 Siz kod vazifasini yuboring\n"
            "2\ufe0f\u20e3 Barcha AI agentlar kod yozadi\n"
            "3\ufe0f\u20e3 Agentlar bir-birining kodini tahlil qiladi\n"
            "4\ufe0f\u20e3 Director eng yaxshi kodni tanlaydi\n"
            "5\ufe0f\u20e3 Siz mukammal kodni olasiz!\n\n"
            f"\u2705 Faol provayderlar: {len(enabled)}\n"
            f"\U0001f916 Tayyor agentlar: {len(available)}/20\n\n"
            "\U0001f4dd Kod vazifangizni yuboring yoki /help buyrug'ini bosing."
        )

        await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        text = (
            "\U0001f4d6 <b>Yordam</b>\n\n"
            "<b>Buyruqlar:</b>\n"
            "/start — Botni boshlash\n"
            "/help — Yordam\n"
            "/agents — Barcha agentlar ro'yxati\n"
            "/status — Bot holati\n"
            "/settings — Sozlamalar\n\n"
            "<b>Foydalanish:</b>\n"
            "Oddiy matn yuboring — bot uni kod vazifasi deb qabul qiladi.\n\n"
            "<b>Misollar:</b>\n"
            "<code>Python'da FastAPI bilan REST API yoz</code>\n"
            "<code>React TypeScript bilan todo app yaz</code>\n"
            "<code>PostgreSQL uchun migration script yoz</code>\n"
        )

        await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    async def agents_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /agents command — list all agents."""
        available = self.orchestrator._get_available_agents()
        all_agents_from_profiles = __import__("agents.profiles", fromlist=["AGENT_PROFILES"]).AGENT_PROFILES

        lines = ["\U0001f916 <b>Code Council Agentlari (20 ta):</b>\n"]
        for agent in all_agents_from_profiles:
            status = "\u2705" if agent in available else "\u274c"
            lines.append(
                f"{status} {agent.emoji} <b>{agent.name}</b> — {agent.specialization}"
            )

        text = "\n".join(lines)
        if len(text) > 4096:
            text = text[:4090] + "..."

        await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command."""
        enabled = self.config.get_enabled_providers()
        available = self.orchestrator._get_available_agents()

        text = (
            "\U0001f4ca <b>Bot Holati</b>\n\n"
            f"Faol provayderlar: {', '.join(enabled) if enabled else 'Yoq'}\n"
            f"Tayyor agentlar: {len(available)}/20\n"
            f"Muhokama raundlari: {self.config.discussion_rounds}\n"
            f"Director: {self.config.director_provider}\n"
        )

        await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /settings command."""
        text = (
            "\u2699\ufe0f <b>Sozlamalar</b>\n\n"
            "Sozlamalarni .env fayl orqali o'zgartiring:\n\n"
            "<code>TELEGRAM_BOT_TOKEN</code> — Bot tokeni\n"
            "<code>OPENAI_API_KEY</code> — OpenAI kaliti\n"
            "<code>ANTHROPIC_API_KEY</code> — Anthropic kaliti\n"
            "<code>GOOGLE_API_KEY</code> — Google AI kaliti\n"
            "<code>DEEPSEEK_API_KEY</code> — DeepSeek kaliti\n"
            "<code>MISTRAL_API_KEY</code> — Mistral kaliti\n"
            "<code>TOGETHER_API_KEY</code> — Together AI kaliti\n"
            "<code>GROQ_API_KEY</code> — Groq kaliti\n"
            "<code>OPENROUTER_API_KEY</code> — OpenRouter kaliti\n"
        )

        await update.message.reply_text(text, parse_mode=ParseMode.HTML)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming text messages — run code council discussion."""
        prompt = update.message.text
        if not prompt or len(prompt.strip()) < 3:
            await update.message.reply_text(
                "\u26a0\ufe0f Iltimos, aniqroq kod vazifasi yuboring."
            )
            return

        available = self.orchestrator._get_available_agents()
        if not available:
            await update.message.reply_text(
                "\u274c Hech qanday AI provider sozlanmagan.\n"
                "/settings buyrug'i bilan API kalitlarini sozlang."
            )
            return

        status_msg = await update.message.reply_text(
            f"\U0001f3db\ufe0f <b>Code Council yig'ilishi boshlandi!</b>\n\n"
            f"\U0001f4cb Vazifa: <code>{self._escape_html(prompt[:200])}</code>\n"
            f"\U0001f916 {len(available)} ta agent ishga tushmoqda...\n\n"
            f"\u23f3 Iltimos kuting...",
            parse_mode=ParseMode.HTML,
        )

        agents_done = 0
        total_agents = min(len(available), self.config.max_agents_per_task)

        async def on_message(msg: DiscussionMessage) -> None:
            nonlocal agents_done
            agents_done += 1
            try:
                status_text = format_status(agents_done, total_agents * 2, msg.agent_name)
                await status_msg.edit_text(status_text, parse_mode=ParseMode.HTML)
            except Exception:
                pass

        try:
            discussion = await self.orchestrator.run_discussion(
                prompt=prompt,
                on_message=on_message,
            )

            await status_msg.edit_text(
                "\U0001f3c6 <b>Director yakuniy qaror qabul qilmoqda...</b>",
                parse_mode=ParseMode.HTML,
            )

            decision = await self.director.make_decision(discussion)

            summary = format_discussion_summary(discussion)
            await status_msg.edit_text(summary, parse_mode=ParseMode.HTML)

            result_messages = format_final_result(decision, discussion)
            for msg_text in result_messages:
                await update.message.reply_text(msg_text, parse_mode=ParseMode.HTML)

        except Exception:
            logger.exception("Discussion failed")
            await status_msg.edit_text(
                "\u274c Xatolik yuz berdi. Iltimos qayta urinib ko'ring.",
                parse_mode=ParseMode.HTML,
            )

    @staticmethod
    def _escape_html(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def create_application(config: Config) -> Application:
    """Create and configure the Telegram bot application."""
    bot = CodeCouncilBot(config)
    app = Application.builder().token(config.telegram_token).build()

    app.add_handler(CommandHandler("start", bot.start_command))
    app.add_handler(CommandHandler("help", bot.help_command))
    app.add_handler(CommandHandler("agents", bot.agents_command))
    app.add_handler(CommandHandler("status", bot.status_command))
    app.add_handler(CommandHandler("settings", bot.settings_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

    return app
