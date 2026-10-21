# 🍲 Chashni

**Chashni** is a bot for the **Bale messaging platform** that helps you decide what to cook based on the ingredients you have at home.

Instead of spending too much time wondering what to make, simply provide your available ingredients, choose a meal and preparation time, and discover suitable food options.

> 🚧 This project is under development, and some features may not be fully implemented yet.

## ✨ Features

- 🥕 **Ingredient-based food suggestions:** Find meals based on the ingredients you have available.
- 🍽️ **Meal selection:** Choose lunch, dinner, or both.
- ⏱️ **Preparation time filtering:** Filter meals by preparation time, from quick to time-consuming.
- 🗂️ **Expandable food database:** Store and manage food information in a separate JSON file.
- 💬 **Interactive buttons:** Navigate the food suggestion process using interactive keyboards.
- ❌ **Cancel the current process:** Stop an ongoing suggestion process using the `/cancel` command.

## 🧰 Technologies

- **Python** — Programming language
- **python-telegram-bot** — Handles messages, commands, and conversations through the Bale API
- **JSON** — Stores food data
- **Bale Bot API** — Connects the bot to the Bale messaging platform
- **Long Polling** — Retrieves updates from the Bale server

## 📁 Project Structure

```text
chashni/
├── main.py           # Main application and bot logic
├── filter.py         # Food filtering functions
├── foods.json        # Food database
├── users.json        # User data and previously selected meals
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## 🚀 Getting Started

### 1. Prerequisites

Before running the project, make sure you have:

- Python 3.10 or later
- A bot token obtained through Bale's bot management system
- The project files, including `main.py`, `filter.py`, `foods.json`, and `users.json`

### 2. Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone <REPOSITORY_URL>
cd chashni
```

Replace `<REPOSITORY_URL>` with your GitHub repository URL.

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Bot Token

Keep your bot token private. Never commit it to your GitHub repository.

On Linux or macOS, set the environment variable before running the bot:

```bash
export BALE_BOT_TOKEN="YOUR_BOT_TOKEN"
```

On Windows PowerShell:

```powershell
$env:BALE_BOT_TOKEN="YOUR_BOT_TOKEN"
```

Replace `YOUR_BOT_TOKEN` with your actual bot token.

The application reads the token from the `BALE_BOT_TOKEN` environment variable. If the variable is not configured, the application will raise an error.

### 6. Run the Bot

```bash
python main.py
```

If the token and dependencies are configured correctly and all required files are present, the bot will start receiving updates through long polling.

## 🤖 Usage

Open the bot in the Bale messaging app and start a conversation.

| Command | Description |
|---|---|
| `/start` | Start interacting with the bot |
| `/help` | Display the available commands |
| `/suggest` | Start the food suggestion process |
| `/random_suggest` | Request random food suggestions |
| `/cancel` | Cancel the current suggestion process |

During the suggestion process, the bot asks about available ingredients and lets users filter food options by meal, preparation time, and category.

Users can also skip certain questions using the provided skip option.

## 🗃️ Food Database

Food information is stored in `foods.json`. Each food entry contains fields such as the following:

```json
{
  "name": "Tomato Omelette",
  "ingredients": [
    "Eggs",
    "Tomatoes",
    "Oil"
  ],
  "meal": "Breakfast",
  "category": "Simple Bread-Based Meals",
  "time": 1,
  "difficulty": 1
}
```

### Field Descriptions

| Field | Description |
|---|---|
| `name` | Name of the dish |
| `ingredients` | List of ingredients required |
| `meal` | Meal associated with the dish |
| `category` | Food category |
| `time` | Numeric value representing preparation time |
| `difficulty` | Numeric value representing preparation difficulty |

The numeric values of `time` and `difficulty` should follow the conventions defined by the application's filtering logic.

To add a new dish, append another object with the same structure to the `foods.json` array.

## 🛠️ Contributing

Contributions and suggestions are welcome!

Here are some ways to improve Chashni:

- Add more dishes and expand the food database.
- Improve the ingredient-matching algorithm.
- Enhance filtering by preparation difficulty and food category.
- Improve the bot's messages and overall user experience.
- Add tests for filtering functions and conversation flows.

For major changes, consider opening an issue first to discuss the proposed improvements.

## 🔐 Security

- Never hardcode your bot token in source code.
- Never commit secrets or credentials to your repository.
- Add `.env` files and local environment directories to `.gitignore`.
- If a valid token has been exposed in a public repository or shared code, revoke or regenerate it.
- Before publishing changes, check that no sensitive information is included.

## 📌 Project Status

Chashni is a Python-based project focused on making everyday meal planning easier through ingredient-based food suggestions.

Future improvements may include more advanced filtering, a larger food database, and more reliable deployment and data storage.

---

Made with 🍲 and Python
