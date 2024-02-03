# in the name of Allah

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler
)
from core.config import Config
import core.handlers.start_handler
import core.utils.chat_member


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)


TOKEN = Config.BOT_TOKEN
ADMIN_ID = Config.ADMIN_ID


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Define Handlers
    start_handler = CommandHandler('start', core.handlers.start_handler.handle)
    joined_channel_handler = CallbackQueryHandler(core.utils.chat_member.channel_lock_button_pressed,
                                                  pattern='^joined channel$')

    # Add Handlers To Application
    application.add_handler(start_handler)
    application.add_handler(joined_channel_handler)

    # Run Application Forever
    application.run_polling()


if __name__ == '__main__':
    main()
