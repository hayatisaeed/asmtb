import random

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.data_handler
import core.handlers.start_handler


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    motivation_messages = await core.data_handler.get_motivation_messages()
    if motivation_messages:
        random_motivation_message = random.choice(motivation_messages)
    else:
        await context.bot.send_message(chat_id=user_id,
                                       text="فایل انگیزشی در حال حاضر موجود نیست. لطفا بعدا درخواست بدید.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END

    try:
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=user_id,
                                       message_id=random_motivation_message)
        await core.handlers.start_handler.handle(update, context)
    except Exception as e:
        print(f'Exception happened in core/handlers/user_handlers/motivation_handler.py (handle):\n---> {e}')
        await context.bot.send_message(chat_id=user_id, text="خطا")
        await core.handlers.start_handler.handle(update, context)

    return ConversationHandler.END
