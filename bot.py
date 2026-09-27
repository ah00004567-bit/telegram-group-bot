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

        # لا تطبق العقوبة على البوتات
        if user and user.is_bot:
            return

        try:
            # حذف الرسالة
            await message.delete()

            # حظر العضو
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

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
