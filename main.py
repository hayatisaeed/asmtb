# in the name of Allah

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from core.config import Config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)


TOKEN = Config.BOT_TOKEN
ADMIN_ID = Config.ADMIN_ID


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.run_polling()


if __name__ == '__main__':
    main()
