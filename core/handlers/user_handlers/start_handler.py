from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

user_main_keyboard = [[]]
user_main_reply_markup = ReplyKeyboardMarkup(user_main_keyboard, one_time_keyboard=True)


async def handle(context: CallbackContext, update: Update) -> None:
    pass
