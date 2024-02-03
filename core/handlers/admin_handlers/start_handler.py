from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from core.config import Config

admin_main_keyboard = [['⚙️ | تنظیمات کلی بات']]
admin_main_reply_markup = ReplyKeyboardMarkup(admin_main_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext) -> None:
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="🏠 | پنل ادمین", reply_markup=admin_main_reply_markup)

