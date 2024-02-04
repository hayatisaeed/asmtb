from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from core.config import Config
import core.handlers.admin_handlers.start_handler as admin_start_handler
import core.utils.chat_member
import core.handlers.user_handlers.start_handler
import core.data_handler
import core.utils.send_uploaded_file


async def handle(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id == Config.ADMIN_ID:  # load admin panel
        await admin_start_handler.handle(update, context)

    else:  # load user panel
        if not await core.data_handler.user_is_saved(user_id):
            await core.data_handler.save_user(user_id)

        if not Config.BOT_POWER_ON:
            await context.bot.send_message(chat_id=user_id,
                                           text="در حال حاضر ربات غیر فعال است. لطفا پس از فعال سازی /start را بزنید.")
            return

        if not await core.utils.chat_member.user_joined_channel(context, user_id, Config.CHANNEL_ID):
            # user not joined the channel
            await core.utils.chat_member.channel_lock(update, context)
            return

        args = context.args
        if args:
            await core.utils.send_uploaded_file.send(update, context, user_id, args[0])

        await core.handlers.user_handlers.start_handler.handle(update, context)



