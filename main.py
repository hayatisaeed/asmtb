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
import core.handlers.admin_handlers.broadcast_handler
import core.handlers.admin_handlers.start_handler
import core.handlers.user_handlers.basic_settings_handler
import core.handlers.admin_handlers.uploader_handler



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
        entry_points=[MessageHandler(filters.Regex('^⚙️ | تنظیمات کلی بات&'),
                                     core.handlers.admin_handlers.general_settings_handler.handle)],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔴 خاموش | روشن 🟢&'),
                               core.handlers.admin_handlers.general_settings_handler.change_power_status),
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.admin_handlers.general_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.general_settings_handler.unknown_command)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.admin_handlers.general_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.general_settings_handler.return_home)
        ]
    )

    admin_broadcast_message_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^📣 | ارسال اطلاعیه$'),
                           core.handlers.admin_handlers.broadcast_handler.handle)
        ],
        states={
            'SEND_MESSAGE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.admin_handlers.broadcast_handler.return_home),
                MessageHandler(filters.ALL, core.handlers.admin_handlers.broadcast_handler.do_the_broadcast)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.admin_handlers.broadcast_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.broadcast_handler.return_home)
        ]
    )

    user_basic_settings_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^تنظیمات کاربری 🔧$'),
                           core.handlers.user_handlers.basic_settings_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^تنظیم نام و نام خانوادگی$'),
                               core.handlers.user_handlers.basic_settings_handler.change_name),
                MessageHandler(filters.Regex('^تنظیم وضعیت تحصیل$'),
                               core.handlers.user_handlers.basic_settings_handler.change_status),
                MessageHandler(filters.Regex('^تنظیم جنسیت$'),
                               core.handlers.user_handlers.basic_settings_handler.change_gender),
                MessageHandler(filters.Regex('^تنظیم رشته$'),
                               core.handlers.user_handlers.basic_settings_handler.change_reshte),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.choose_what_to_edit)
            ],
            'CHOOSING_GENDER': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_gender),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_gender)
            ],
            'CHOOSING_RESHTE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_reshte),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_reshte)
            ],
            'CHOOSING_STATUS': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_status),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_status)
            ],
            'CHOOSING_NAME': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_name),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_name)
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    admin_uploader_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^📤 آپلودر$'),
                                     core.handlers.admin_handlers.uploader_handler.handle)],
        states={
            'NEW_UPLOAD': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.ALL, core.handlers.admin_handlers.uploader_handler.new_file)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.uploader_handler.return_home)
        ]
    )

    # Add Handlers To Application
    application.add_handler(start_handler)
    application.add_handler(joined_channel_handler)
    application.add_handler(admin_bot_general_settings)
    application.add_handler(admin_broadcast_message_handler)
    application.add_handler(user_basic_settings_handler)
    application.add_handler(admin_uploader_handler)

    # Run Application Forever
    application.run_polling()


if __name__ == '__main__':
    print('-- Bot started and running ... --')
    main()
