from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from core.config import Config
import core.handlers.start_handler


async def chat_member_status(context, user_id, channel_id):
    membership_status = await context.bot.get_chat_member(channel_id, user_id)
    membership_status = membership_status['status'].lower()
    return membership_status


async def user_joined_channel(context, user_id, channel_id):
    membership_status = await context.bot.get_chat_member(channel_id, user_id)
    membership_status = membership_status['status'].lower()
    if membership_status == 'member' or membership_status == 'administrator' or membership_status == 'creator':
        return True
    else:
        return False


async def channel_lock_button_pressed(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = update.callback_query

    if await user_joined_channel(context, user_id, Config.CHANNEL_ID):
        await query.answer("✅ عضویت شما تایید شد ✅")
        await context.bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
        await core.handlers.start_handler.handle(update, context)

    else:
        await query.answer("❌ عضویت شما تایید نشد ❌")


async def channel_lock(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message = f"""
کاربر محترم لطفا ابتدا در کانال زیر عضو شده و سپس روی دکمه عضو شدم کلیک کنید

{Config.CHANNEL_LINK}

    """
    inline_keyboard = [[InlineKeyboardButton("🔗 عضویت در کانال 🔗", url=Config.CHANNEL_LINK)],
                       [InlineKeyboardButton("عضو شدم ✅", callback_data="joined channel")]]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=inline_markup)

