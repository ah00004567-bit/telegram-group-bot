import os
import re

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


BANNED_PHRASES = [
    "سكليف",
    "سكليفات",
    "دخل يومي",
    "عذر طبي",
    "عمل حلو",
]


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.text:
        return

    text = normalize_text(message.text)

    if any(phrase in text for phrase in BANNED_PHRASES):

        user = update.effective_user

        if user and user.is_bot:
            return

        try:
            await message.delete()

            await context.bot.ban_chat_member(
                chat_id=update.effective_chat.id,
                user_id=user.id
            )

            print(f"Banned user: {user.id}")

        except Exception as error:
            print("Error:", error)


def main():
    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            check_message
        )
    )

    port = int(os.environ.get("PORT", "10000"))
    render_url = os.environ["RENDER_EXTERNAL_URL"]

    print("Bot is running...")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=f"{render_url}/telegram"
    )


if __name__ == "__main__":
    main()
