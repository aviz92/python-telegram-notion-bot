# python-telegram-notion-bot
This app listens to messages from a Telegram bot and creates tasks in Notion accordingly.

---

## Features
- Connects to a Telegram bot. 
- Parses messages and turns them into structured tasks or ideas.
- Creates tasks in a Notion database.

---

## Requirements
- Python 3.11+
- Notion API token
- Notion database ID
- Telegram bot token
- Install Docker Desktop

---

## Installation
```bash
pip install python-telegram-notion-bot
```

or use Docker Compose to run the app in a containerized environment.
```bash
docker-compose up --build
```
or use Docker Compose in the background:
```bash
docker-compose up --build -d
docker-compose down
```

---

## How to Use

### Configuration
The package uses environment variables for authentication and configuration:
```bash
NOTION_TOKEN="your_notion_api_token"
TELEGRAM_TOKEN="your_telegram_bot_token"
NOTION_TASKER_DB_ID="your_notion_database_id"
NOTION_IDEAS_DB_ID="your_notion_database_id"
```

---

### 🤖 Creating a Telegram Bot
1. Open Telegram and search for @BotFather. 
2. Send the command /newbot. 
3. Follow the prompts to name your bot and choose a username. 
4. In the end, you'll get a Bot Token – save it, you'll need it in the .env file.

---

### 🧠 Setting Up Notion Integration
1. Go to https://www.notion.so/my-integrations. 
2. Click + New integration. 
3. Give it a name and select the workspace.
4. Save the generated Internal Integration Token. 
5. Create a new database in Notion with the following properties:
   - Done (checkbox)
   - Name (title)
   - Description (text)
   - Status (select)
     - Not started (must)
   - Type (text)
   - Date (date)
6. Share the target database page with the integration (via "tree dots → connections → choose your integration").

---

## 🤝 Contributing
If you have a helpful tool, pattern, or improvement to suggest:
Fork the repo <br>
Create a new branch <br>
Submit a pull request <br>
I welcome additions that promote clean, productive, and maintainable development. <br>

---

## 🙏 Thanks
Thanks for exploring this repository! <br>
Happy coding! <br>
