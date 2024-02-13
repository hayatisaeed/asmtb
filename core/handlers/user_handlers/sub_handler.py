from telegram import Update
from telegram.ext import CallbackContext


async def handle(update: Update, context: CallbackContext):
    pass


async def show_my_sub_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id


async def buy_sub(update: Update, context: CallbackContext):
    pass
