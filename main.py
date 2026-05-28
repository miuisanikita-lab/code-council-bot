"""Code Council Bot — 20 AI coding agents in one Telegram bot."""

import logging
import sys

from dotenv import load_dotenv

load_dotenv()

from bot.handlers import create_application
from config import Config
from utils.logger import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the Code Council Bot."""
    setup_logging()

    config = Config.load()

    if not config.telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set! Please set it in .env file.")
        sys.exit(1)

    enabled_providers = config.get_enabled_providers()
    if not enabled_providers:
        logger.warning(
            "No AI providers configured! The bot will start but cannot process requests. "
            "Set at least one API key in .env file."
        )
    else:
        logger.info("Enabled providers: %s", ", ".join(enabled_providers))

    app = create_application(config)

    logger.info("Code Council Bot is starting...")
    logger.info(
        "Active: %d providers, up to %d agents per task",
        len(enabled_providers),
        config.max_agents_per_task,
    )

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
