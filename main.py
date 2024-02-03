# in the name of Allah

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler
)
from core.config import Config
import core.handlers.start_handler
import core.handlers.admin_handlers.general_settings_handler
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

    admin_bot_general_settings = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^⚙️ | تنظیمات کلی بات$'),
                                     core.handlers.admin_handlers.general_settings_handler.handle)],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔴 خاموش | روشن 🟢&'),
                               core.handlers.admin_handlers.general_settings_handler.change_power_status),
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.admin_handlers.general_settings_handler.return_home),
                MessageHandler(filters.ALL,
                               core.handlers.admin_handlers.general_settings_handler.unknown_command)
            ]
        },
        fallbacks=[]
    )

    # Add Handlers To Application
    application.add_handler(start_handler)
    application.add_handler(joined_channel_handler)
    application.add_handler(admin_bot_general_settings)

    # Run Application Forever
    application.run_polling()


if __name__ == '__main__':
    main()
