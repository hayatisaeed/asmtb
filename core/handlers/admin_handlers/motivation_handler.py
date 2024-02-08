from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from core.config import Config
import core.handlers.start_handler

main_motivation_keyboard = [
    ['فایل‌های انگیزشی'],
    ['زمان ارسال خودکار'],
    ['🔙 | بازگشت به منوی اصلی']
]
main_motivation_markup = ReplyKeyboardMarkup(main_motivation_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا از منوی زیر گزینه مد نظر خود را انتخاب کنید",
                                       reply_markup=main_motivation_markup)
        return 'CHOOSING'


async def handle_files(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID,
                                   text="برای اضافه یا حذف فایل های انگیزشی از قسمت بانک فایل استفاده کنید.")
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="از منوی زیر انتخاب کنید",
                                   reply_markup=main_motivation_markup)
    return 'CHOOSING'


async def handle_time(update: Update, context: CallbackContext):
    text = f"""
    تایم ارسال پیام انگیزشی به همه:
    {Config.MOTIVATION_HOUR}:{Config.MOTIVATION_MINUTE}
    """
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=main_motivation_markup)
    return 'CHOOSING'


async def return_home(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="بازگشت به منوی اصلی ...")
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END
