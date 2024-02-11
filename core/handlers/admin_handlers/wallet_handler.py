from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import core.data_handler
import core.utils.work_with_strings


cancel_keyboard = [['🔙 | بازگشت به منوی اصلی']]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا آیدی عددی کاربر مدنظر را بفرستید",
                                       reply_markup=cancel_markup)
        return 'SEND_USER_ID'


async def show_wallet(update: Update, context: CallbackContext):
    user_id = update.message.text
    context.user_data['user_id'] = user_id
    if not await core.data_handler.user_is_saved(user_id):
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="این یوزر وجود ندارد. مجددا وارد کنید.",
                                       reply_markup=cancel_markup)
        return 'SEND_USER_ID'
    else:
        user_wallet_data = await core.data_handler.get_wallet_data(user_id)
        user_credit = await core.utils.work_with_strings.beautify_numbers(user_wallet_data['credit'])

        text = f"""
        کاربر با آیدی:
        {user_id}
        
        موجودی فعلی:
        {user_credit}
        
        لطفا موجودی مدنظر خود برای این کاربر را ارسال کنید.
        (به صورت عدد و به ریال)
        """
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=cancel_markup)
        return 'SEND_NEW_CREDIT'


async def change_credit(update: Update, context: CallbackContext):
    user_id = context.user_data['user_id']
    new_credit = update.message.text
    wallet_data = await core.data_handler.get_wallet_data(user_id)
    past_credit = await core.utils.work_with_strings.beautify_numbers(wallet_data['credit'])

    try:
        new_credit = int(new_credit)
        await core.data_handler.edit_wallet_credit(user_id, new_credit)
        new_credit = await core.utils.work_with_strings.beautify_numbers(new_credit)
        text = f"""
        انجام شد.
        
        موجودی قبلی:
        {past_credit}
        
        موجودی جدید:
        {new_credit}
        """
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text)
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا آیدی یوزر جدید را وارد کنید",
                                       reply_markup=cancel_markup)
        return 'SEND_USER_ID'
    except ValueError:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="عدد نامعتبر. لطفا دوباره ارسال کنید",
                                       reply_markup=cancel_markup)
        return 'SEND_NEW_CREDIT'
