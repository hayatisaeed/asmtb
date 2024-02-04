from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import base64


cancel_keyboard = [['🔙 | بازگشت به منوی اصلی']]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا فایل خود را آپلود کرده یا فوروارد نمایید.",
                                       reply_markup=cancel_markup)
        return 'NEW_UPLOAD'


async def new_file(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    encoded_bytes = base64.b64encode(str(message_id).encode())
    encoded_string = encoded_bytes.decode()

    message = f"""

فایل آپلود شد.
لطفا این پیام را حذف نکنید.

🔗 لینک فایل:

https://t.me/{Config.BOT_USERNAME}?start={encoded_string}

    """
    await update.message.reply_text(message)
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا فایل خود را آپلود کرده یا فوروارد نمایید.",
                                   reply_markup=cancel_markup)
    return 'NEW_UPLOAD'


async def return_home(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="بازگشت به منوی اصلی ...")
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END
