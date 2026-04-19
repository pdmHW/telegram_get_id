from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📢 Channel ID", callback_data="get_channel"),
            InlineKeyboardButton("👥 Group ID", callback_data="get_group"),
        ],
        [InlineKeyboardButton("🙋‍♂️ My ID", callback_data="get_user")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select:", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "get_user":
        user_id = query.from_user.id
        await query.edit_message_text(f"🙋‍♂️ Your Telegram ID: `{user_id}`", parse_mode="Markdown")

    elif data == "get_channel":
        await query.edit_message_text("📢 Please, send channel `@username` or `https://t.me/channel` URL.")

    elif data == "get_group":
        await query.edit_message_text("👥 Please, send group `@username` or `https://t.me/group` URL. ")


async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("@"):
        username = text
    elif "t.me/" in text:
        username = "@" + text.split("t.me/")[1].strip().replace("/", "")
    else:
        await update.message.reply_text("❌ Error ", parse_mode="Markdown")
        return

    try:
        chat = await context.bot.get_chat(username)
        await update.message.reply_text(f"🆔 ID: `{chat.id}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error.\nError: {e}")


def main():
    app = ApplicationBuilder().token("BOT_TOKEN").build() #Change BOT_TOKEN to your actually Bot Token, you will get it from Telegram @BotFather

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))

    print("✅ Bot Started working")
    app.run_polling()


if __name__ == "__main__":
    main()
