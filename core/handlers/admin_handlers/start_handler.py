from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

admin_main_keyboard = [[]]
admin_main_reply_markup = ReplyKeyboardMarkup(admin_main_keyboard, one_time_keyboard=True)


async def handle(context: CallbackContext, update: Update) -> None:
    pass
