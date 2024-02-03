from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from core.config import Config
import core.handlers.admin_handlers.start_handler as admin_start_handler
import core.utils.chat_member
import core.handlers.user_handlers.start_handler


async def handle(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id == Config.ADMIN_ID:  # load admin panel
        await admin_start_handler.handle(update, context)

    else:  # load user panel
        if not await core.utils.chat_member.user_joined_channel(context, user_id, Config.CHANNEL_ID):
            # user not joined the channel
            await core.utils.chat_member.channel_lock(update, context)
        else:
            # user already joined channel
            await core.handlers.user_handlers.start_handler.handle(update, context)



