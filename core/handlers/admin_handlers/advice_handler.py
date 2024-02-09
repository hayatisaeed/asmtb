from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.user_handlers.basic_settings_handler


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="Sorry you are not authorized to use this part.")
        await core.handlers.user_handlers.basic_settings_handler.return_home(update, context)
        return ConversationHandler.END
    else:
        pass


async def show_categories(update: Update, context: CallbackContext):
    pass


async def show_advice(update: Update, context: CallbackContext):
    pass
