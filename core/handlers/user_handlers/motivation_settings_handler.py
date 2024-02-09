from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
import core.data_handler
import core.handlers.user_handlers.motivation_handler
import random
from core.config import Config
import core.handlers.start_handler

motivation_settings_keyboard = [
    ['ارسال خودکار پیام انگیزشی'],
    ['🔙 | بازگشت به منوی اصلی']
]
motivation_settings_markup = ReplyKeyboardMarkup(motivation_settings_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="تنظیمات پیام انگیزشی. لطفا از منوی زیر انتخاب کنید:",
                                   reply_markup=motivation_settings_markup)
    return 'CHOOSING'


async def auto_motivation(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data = await core.data_handler.get_user_data(user_id)

    if user_data['auto_motivation']:
        keyboard = [
            ['غیر فعال کردن ارسال خودکار'],
            ['🔙 | بازگشت به منوی اصلی']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await context.bot.send_message(chat_id=user_id,
                                       text="آیا میخواهید دریافت خودکار پیام انگیزشی را 🔴 غیر فعال کنید؟",
                                       reply_markup=markup)
        return 'AUTO_MOTIVATION'
    else:
        keyboard = [
            ['فعال کردن ارسال خودکار'],
            ['🔙 | بازگشت به منوی اصلی']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await context.bot.send_message(chat_id=user_id,
                                       text="آیا میخواهید دریافت خودکار پیام انگیزشی را 🟢 فعال کنید؟",
                                       reply_markup=markup)
        return 'AUTO_MOTIVATION'


async def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()


async def set_motivation_job_queue(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await remove_job_if_exists(str(user_id), context)

    context.job_queue.run_once(core.handlers.user_handlers.motivation_settings_handler.new_motivation_job_queue,
                               1, chat_id=user_id, name=str(user_id))

    await context.bot.send_message(chat_id=user_id, text="ارسال خودکار پیام انگیزشی 🟢 فعال شد")
    await context.bot.send_message(chat_id=user_id, text="تنظیمات پیام انگیزشی. لطفا از منوی زیر انتخاب کنید:",
                                   reply_markup=motivation_settings_markup)
    return 'CHOOSING'


async def new_motivation_job_queue(context: CallbackContext):
    job = context.job
    user_id = job.chat_id
    motivation_messages = await core.data_handler.get_motivation_messages()
    if motivation_messages:
        random_motivation_message = random.choice(motivation_messages)
    else:
        return

    try:
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=user_id,
                                       message_id=random_motivation_message)
    finally:
        pass


async def remove_motivation_job_queue(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    await remove_job_if_exists(str(user_id), context)

    await context.bot.send_message(chat_id=user_id, text="ارسال خودکار پیام انگیزشی 🔴 غیر فعال شد")
    await context.bot.send_message(chat_id=user_id, text="تنظیمات پیام انگیزشی. لطفا از منوی زیر انتخاب کنید:",
                                   reply_markup=motivation_settings_markup)
    return 'CHOOSING'
