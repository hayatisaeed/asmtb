from telegram import Update
from telegram.ext import CallbackContext
from core.config import Config
import core.handlers.admin_handlers.start_handler as admin_start_handler
import core.utils.chat_member


async def handle(context: CallbackContext, update: Update) -> None:
    user_id = update.effective_user.id
    if user_id == Config.ADMIN_ID:  # load admin panel
        await admin_start_handler.handle(context, update)

    else:  # load user panel
        if not await core.utils.chat_member.user_joined_channel(context, user_id, Config.CHANNEL_ID):
            pass # user not joined the channel
        else:
            pass # user joined the channel



