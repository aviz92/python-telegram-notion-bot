import datetime
import logging
import os
import asyncio
import nest_asyncio
import pytz
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


def build_properties(name: str, description: str) -> dict:
    jerusalem = pytz.timezone("Asia/Jerusalem")
    due_date = jerusalem.localize(
        datetime.datetime.now() + datetime.timedelta(days=1)
    ).replace(hour=10, minute=0, second=0, microsecond=0)
    properties = {
        "Done": {"checkbox": False},
        "Name": {"title": [{"text": {"content": name}}]},
        "Description": {"rich_text": [{"text": {"content": description}}]},
        "Status": {"status": {"name": "Not started"}},
        "Type": {"multi_select": []},
        "Date": {"date": {"start": datetime.datetime.now(pytz.timezone("Asia/Jerusalem")).isoformat()}},
        # "Due Date": {"date": {"start": due_date.isoformat()}},
    }
    return properties


def data_preparation(text: str) -> tuple[str, str]:
    for prefix in TASK_PREFIXES + IDEA_PREFIXES:
        if prefix.lower() not in text.lower():
            continue

        text = text[len(prefix):]
    text_split = text.split("\n\n", 1)
    name, description = text_split if len(text_split) > 1 else (text_split[0], "")
    return name, description


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

    name, description = data_preparation(text)
    properties = build_properties(name=name.strip(), description=description.strip())
    notion_client.add_row_to_db(
        notion_database_id=notion_db_id,
        properties=properties
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
