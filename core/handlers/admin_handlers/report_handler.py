from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from core.config import Config
import core.handlers.start_handler


async def manage_subjects(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await core.handlers.start_handler.handle(update, context)
        return
    else:
        keyboard = [
            [InlineKeyboardButton("باز کردن منوی دروس", url="http://103.75.197.206:5000/admin/manageSubjects")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        text = """
        انجام این قابلیت از طریق پنل تحت وب امکان پذیر است.
        """
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=markup)
        await core.handlers.start_handler.handle(update, context)

