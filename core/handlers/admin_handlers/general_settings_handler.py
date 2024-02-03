from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler


settings_options_keyboard = [['🔴 خاموش | روشن 🟢'], ['🔙 | بازگشت به منوی اصلی']]
settings_options_markup = ReplyKeyboardMarkup(settings_options_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        # user is not admin
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END

    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="از منوی زیر انتخاب کنید:",
                                       reply_markup=settings_options_markup)
        return 'CHOOSING'


async def change_power_status(update: Update, context: CallbackContext):
    power_status = '🟢 ON' if Config.BOT_POWER_ON else '🔴 OFF'
    new_status = '🟢 ON' if not Config.BOT_POWER_ON else '🔴 OFF'
    message = f"""
انجام شد! ✅
----
Before: {power_status}
----
Now: {new_status}
    """
    Config.BOT_POWER_ON = not Config.BOT_POWER_ON
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=message, reply_markup=settings_options_markup)
    return 'CHOOSING'


async def unknown_command(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="متوجه نشدم. از منوی زیر انتخاب کنید:",
                                   reply_markup=settings_options_markup)
    return 'CHOOSING'


async def return_home(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="بازگشت به منوی اصلی ...")
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END
