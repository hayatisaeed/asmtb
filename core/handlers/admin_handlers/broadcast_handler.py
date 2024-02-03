from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import core.data_handler
import core.handlers.admin_handlers.start_handler


broadcast_cancel_keyboard = [['🔙 | بازگشت به منوی اصلی']]
return_home_markup = ReplyKeyboardMarkup(broadcast_cancel_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        # user is not admin
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END

    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID,
                                       text="پیامی که میخواهید به عنوان اطلاعیه ارسال شود را بنویسید یا فوروارد کنید",
                                       reply_markup=return_home_markup)
        return 'SEND_MESSAGE'


async def do_the_broadcast(update: Update, context: CallbackContext):
    users = await core.data_handler.get_all_user_data()
    message_id = update.message.message_id
    done = 0
    failed = 0
    for user_id in users:
        try:
            await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=user_id, message_id=message_id)
            done += 1
        except:
            failed += 1
            print(Exception)
    message = f"""
انجام شد. ✅

🟢 ارسال با موفقیت به {done} کاربر
عدم ارسال موفق به {failed} کاربر 
    """
    await core.handlers.admin_handlers.start_handler.handle(update, context)
    return ConversationHandler.END


async def return_home(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="بازگشت به منوی اصلی ...")
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END
