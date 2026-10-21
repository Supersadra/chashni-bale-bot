import logging
import json
import filter
import random
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler, filters, ContextTypes, Application
from telegram.ext.filters import MessageFilter

# Variables
INGREDIENTS, MEAL, TIME, CATEGORY, SAVE = range(5) # States for conversation handler
bot_token = os.getenv("BALE_BOT_TOKEN")
if not bot_token:
    raise RuntimeError("BALE_BOT_TOKEN تنظیم نشده است.")

def skip_keyboard():
    skip_keyboard = ReplyKeyboardMarkup(
    [["رد کردن سوال"]],
    resize_keyboard=True,
    is_persistent=True
    )
    return skip_keyboard
async def load_data(application: Application) -> None:
    path = Path(__file__).resolve().parent / "foods.json"
    with open(path, "r", encoding="utf-8") as file:
        application.bot_data["foods"] = json.load(file)
    


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
        سلام! با این ربات دیگه دغدغه پیدا کردن غذا
        برای برنامه های مختلف رو نداشته باش.
         از مهمونی و دورهمی تا برنامه غذایی هفتگی!

    """)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("در حال حاضر دستورات زیر در ربات فعال هستن:\n\n/suggest\nبا استفاده از این دستور می‌تونی پیشنهاد غذا بگیری.")

######################### Suggest command conversation #########################
async def suggest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("filtered_foods", None)

    await update.message.reply_text("چه مواد غذایی تو خونه داری؟\nموارد رو با ویرگول جدا کن.", 
    reply_markup=skip_keyboard())

    return INGREDIENTS


async def ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    foods = context.bot_data["foods"] #Foods JSON file
    context.user_data["filtered_foods"] = foods
    
    keyboard = [[
        InlineKeyboardButton("ناهار", callback_data="lunch"),
        InlineKeyboardButton("شام", callback_data="dinner")],
        [InlineKeyboardButton("شام و ناهار", callback_data="lunch&dinner")
    ]]

    if update.message.text != "رد کردن سوال":
        ingredients = update.message.text.split('،') #User inputs

        filtered = filter.filter_ingredients(foods, ingredients)
        
        if not filtered:
            await update.message.reply_text("غذایی با این مشخصات یافت نشد.")
            return ConversationHandler.END
        else:
            context.user_data["filtered_foods"] = filtered
            await update.message.reply_text(
            "وعده غذایی مورد نظرت رو انتخاب کن.",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await update.message.reply_text("می‌تونی با استفاده از منوی زیر سوال رو رد کنی.",
            reply_markup=skip_keyboard())
            return MEAL
    else:
        await update.message.reply_text(
        "وعده غذایی مورد نظرت رو انتخاب کن.",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await update.message.reply_text("می‌تونی با استفاده از منوی زیر سوال رو رد کنی.",
        reply_markup=skip_keyboard())
   
        return MEAL


async def meal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[
        InlineKeyboardButton("سریع", callback_data="fast"),
        InlineKeyboardButton("متوسط", callback_data="normal"),
        InlineKeyboardButton("زمانبر", callback_data="time_consuming")
    ]]

    try:
        query = update.callback_query
        await query.answer()
        meal = query.data
        filtered_foods = context.user_data["filtered_foods"]

        filtered = filter.filter_meal(filtered_foods, meal)
        
        if not filtered:
            await query.edit_message_text("غذایی با این مشخصات یافت نشد.")
            return ConversationHandler.END
        else:
            context.user_data["filtered_foods"] = filtered
            await query.edit_message_text("پاسخ شما ثبت شد.")
            
            await query.message.reply_text(
            "میزان زمانبری غذا رو انتخاب کن.",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await query.message.reply_text("می‌تونی با استفاده از منوی زیر سوال رو رد کنی.",
            reply_markup=skip_keyboard())

            return TIME
    
    except AttributeError:

        await update.message.reply_text(
        "میزان زمانبری غذا رو انتخاب کن.",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await update.message.reply_text("می‌تونی با استفاده از منوی زیر سوال رو رد کنی.",
        reply_markup=skip_keyboard())        
        
        return TIME


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[
        InlineKeyboardButton("فست‌فود", callback_data="fastfood"),
        InlineKeyboardButton("ماکارونی و پاستا", callback_data="pasta")],
        
        [InlineKeyboardButton("برنجی", callback_data="rice"),
        InlineKeyboardButton("خورشت و خوراک", callback_data="stew")],
        
        [InlineKeyboardButton("آش و سوپ", callback_data="soup"),
        InlineKeyboardButton("نانی ساده", callback_data="bread")],

        [InlineKeyboardButton("غذا های سرد", callback_data="cold"),
        InlineKeyboardButton("غذا های تیلیتی", callback_data="tilit")
    ]]

    try:
        query = update.callback_query
        await query.answer()
        time = query.data
        
        filtered_foods = context.user_data["filtered_foods"]
        filtered = filter.filter_time(filtered_foods, time)
        
        if not filtered:
            await query.edit_message_text("غذایی با این مشخصات یافت نشد.")
            return ConversationHandler.END
        else:
            context.user_data["filtered_foods"] = filtered
            await query.edit_message_text("پاسخ شما ثبت شد.")
            
            await query.message.reply_text(
            "دسته‌بندی غذا رو انتخاب کن.",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await query.message.reply_text("می‌تونی با استفاده از منوی زیر سوال رو رد کنی.",
            reply_markup=skip_keyboard())

            return CATEGORY
    
    except AttributeError:
        
        await update.message.reply_text(
        "دسته‌بندی غذا رو انتخاب کن.",
        reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await update.message.reply_text("می‌تونی با استفاده از منوی زیر سوال رو رد کنی.",
        reply_markup=skip_keyboard())        

        return CATEGORY


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    try:
        query = update.callback_query
        await query.answer()
        category = query.data
        
        filtered_foods = context.user_data["filtered_foods"]
        filtered = filter.filter_category(filtered_foods, category)
        
        if not filtered:
            await query.edit_message_text("غذایی با این مشخصات یافت نشد.")
            return ConversationHandler.END
        else:
            context.user_data["filtered_foods"] = filtered
            await query.edit_message_text("پاسخ شما ثبت شد.")
            
            user_id = query.from_user.id
            path = Path(__file__).resolve().parent / "users.json"
            with open(path, "r", encoding="utf-8") as file:
                users = json.load(file)
            
            # Deleting repetitive foods
            for user in users:
                if user["user_id"] == user_id:
                    final_list = set([food["name"] for food in filtered]) - set(user["foods"])
                    break
            
            # Generating Keyboard for food selection
            keyboard = []
            for food_name in final_list:
                button = InlineKeyboardButton(f"{food_name}", callback_data=f"{food_name}")
                keyboard.append([button])
            
            # Show final filtered_foods
            await query.edit_message_text("فهرست غذا ها\n- غذای موردنظر خود را از فهرست زیر انتخاب کنید",
            reply_markup=InlineKeyboardMarkup(keyboard))


            return SAVE
    
    except AttributeError:

        user_id = update.message.from_user.id
        path = Path(__file__).resolve().parent / "users.json"
        with open(path, "r", encoding="utf-8") as file:
            users = json.load(file)
            
        # Deleting repetitive foods
        if users:
            for user in users:
                if user["user_id"] == user_id:
                    final_list = set([food["name"] for food in context.user_data["filtered_foods"]]) - set(user["foods"])
                    break
        else:
            final_list = set([food["name"] for food in context.user_data["filtered_foods"]])

        keyboard = []
        for food_name in final_list:
            button = InlineKeyboardButton(f"{food_name}", callback_data=f"{food_name}")
            keyboard.append([button])
        
        # Show final filtered_foods
        await update.message.reply_text("فهرست غذا ها\n- غذای موردنظر خود را از فهرست زیر انتخاب کنید",
        reply_markup=InlineKeyboardMarkup(keyboard))
        
        
        return SAVE


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_food = query.data
    user_id = query.from_user.id
    print(user_id)
    
    path = Path(__file__).resolve().parent / "users.json"
    with open(path, "r", encoding="utf-8") as file:
        users = json.load(file)
    
    if users:
        for user in users:
            if user["user_id"] == user_id:
                if len(user["foods"]) >= 10:
                    del user["foods"][0]
                user["foods"].append(selected_food)
                break
            
            elif user == users[-1]:
                new_save = {"user_id": user_id, "foods": [selected_food]}
                users.append(new_save)
                break
    else:
        new_save = {"user_id": user_id, "foods": [selected_food]}
        users.append(new_save)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)
    
    await query.edit_message_text("غذای انتخابی شما ثبت شد. نوش جان!")
    context.user_data.pop("filtered_foods", None)
    
    return ConversationHandler.END
####################################################################
async def random_suggest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    food_names = [food["name"] for food in context.bot_data["foods"]]
    random_foods = random.sample(food_names, 3)
    
    keyboard = []
    for food_name in random_foods:
        button = InlineKeyboardButton(f"{food_name}", callback_data=f"{food_name}")
        keyboard.append([button])
    
    await update.message.reply_text(f"*غذاهای تصادفی*",
    reply_markup=InlineKeyboardMarkup(keyboard))
    
    return SAVE 


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("filtered_foods", None)

    await update.message.reply_text(
        "فرآیند لغو شد."
    )

    return ConversationHandler.END


class HealthHandler(BaseHTTPRequestHandler):
    """Minimal HTTP endpoint so Render Web Service can detect an open port."""

    def do_GET(self):
        if self.path in ("/", "/health"):
            body = b"Chashni bot is running"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Keep routine health checks out of the logs.
        return


def start_health_server() -> None:
    # Render provides PORT. 10000 is a local-development fallback.
    port = int(os.getenv("PORT", "10000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info("Health server listening on port %s", port)


def main() -> None:
    start_health_server()
    application = Application.builder().token(bot_token).post_init(load_data).base_url("https://tapi.bale.ai/bot").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("suggest", suggest_command),
        CommandHandler("random_suggest", random_suggest_command)],
        states={
            INGREDIENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ingredients)],
            
            MEAL: [CallbackQueryHandler(meal),
            MessageHandler(filters.TEXT & ~filters.COMMAND, meal)],
            
            TIME: [CallbackQueryHandler(time),
            MessageHandler(filters.TEXT & ~filters.COMMAND, time)],
            
            CATEGORY: [CallbackQueryHandler(category),
            MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            
            SAVE: [CallbackQueryHandler(save)]
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    ))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()