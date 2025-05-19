import logging
import os
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from python_notion_plus import NotionClient
from custom_python_logger import get_logger

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NOTION_TASKER_DB_ID = os.getenv("NOTION_TASKER_DB_ID")
NOTION_IDEAS_DB_ID = os.getenv("NOTION_IDEAS_DB_ID")

TASK_PREFIXES = ('task', 'משימה')
IDEA_PREFIXES = ('idea', 'רעיון')

logger = logging.getLogger(__name__)
for telegram_noisy_logger in [
    "telegram", "httpx", "httpcore", "apscheduler", "asyncio",
    "telegram.ext._application", "telegram.bot", "telegram.client"
]:
    logging.getLogger(telegram_noisy_logger).setLevel(logging.WARNING)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notion_client = context.application.bot_data["notion_client"]

    text = update.message.text
    text_lower = text.lower()

    if text_lower.startswith(TASK_PREFIXES):
        notion_db_id = NOTION_TASKER_DB_ID
    elif text_lower.startswith(IDEA_PREFIXES):
        notion_db_id = NOTION_IDEAS_DB_ID
    else:
        await update.message.reply_text("Please start your message with 'task' or 'idea'.")
        return

    for prefix in TASK_PREFIXES + IDEA_PREFIXES:
        # text = text.replace(prefix, '', 1).strip()
        if prefix.lower() not in text.lower():
            continue

        text = text[len(prefix):]

    notion_client.add_row_to_db(
        name=text.strip(),
        notion_database_id=notion_db_id
    )

    await update.message.reply_text("Row added to Notion!")
    logger.debug("Row added to Notion: %s", text.strip())


async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.bot_data["notion_client"] = NotionClient(database_id=os.getenv("NOTION_DATABASE_ID"))  # store it
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    _ = get_logger(
        project_name='Logger Project Test',
        log_level=logging.DEBUG,
        # extra={'user': 'test_user'}
    )

    nest_asyncio.apply()  # allows nested event loops
    asyncio.run(main())
