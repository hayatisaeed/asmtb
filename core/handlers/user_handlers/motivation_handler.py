import random

from telegram import Update
from telegram.ext import CallbackContext
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
        return

    try:
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=user_id,
                                       message_id=random_motivation_message)
        await core.handlers.start_handler.handle(update, context)
    except:
        await context.bot.send_message(chat_id=user_id, text="خطا")
        await core.handlers.start_handler.handle(update, context)


async def send_motivation_for_all(context: CallbackContext):
    motivation_messages = await core.data_handler.get_motivation_messages()
    if motivation_messages:
        motivation_message = random.choice(motivation_messages)
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID,
                                       text="امروز پیام انگیزشی ارسال نشد. علت: نبود انگیزه!")
        return False

    user_ids = await core.data_handler.get_all_user_data()

    done = 0
    failed = 0

    for user_id in user_ids:
        try:
            await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=user_id, message_id=motivation_message)
            done += 1
        except:
            failed += 1
    text = f"""
پیام های انگیزشی امروز ارسال شدند

تعداد ارسال موفق: {done}
تعداد ارسال ناموفق: {failed}
    """
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text)
    return True
