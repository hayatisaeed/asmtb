from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import core.handlers.start_handler
import core.data_handler
from core.config import Config


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    advices = await core.data_handler.get_all_advice()

    buttons = []
    for advice_hash in advices:
        buttons.append([
            InlineKeyboardButton(advices[advice_hash][advice_hash], callback_data=f"show-advice-list {advice_hash}")
        ])
    reply_markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(chat_id=user_id, text="توصیه‌ها و نکات مشاوره‌ای", reply_markup=reply_markup)

    await core.handlers.start_handler.handle(update, context)


async def show_advice_list(update: Update, context: CallbackContext):
    query = update.callback_query
    advice_hash = query.data.split()[1]

    advices = await core.data_handler.get_all_advice()
    advices = advices[advice_hash]
    advice_category_title = advices[advice_hash]
    del advices[advice_hash]

    keyboard = []
    for advice in advices:
        title = await core.data_handler.get_file_in_file_bank(str(advice))
        title = title["title"]
        keyboard.append([
            InlineKeyboardButton(title, callback_data=f"show-advice-message {advice}")
        ])
    keyboard.append([
        InlineKeyboardButton("بازگشت", callback_data="return-to-advice-key")
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(f"{advice_category_title}")
    await query.message.edit_reply_markup(reply_markup=reply_markup)
    await query.answer("✅")


async def show_advice_message(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    message_id = query.data.split()[1]

    await query.delete_message()
    try:
        keyboard = [[InlineKeyboardButton("بازگشت", callback_data="return-to-advice-key")]]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=user_id, message_id=int(message_id),
                                       reply_markup=markup)
        await query.answer("✅")
    except Exception as e:
        print(f"Error happened in core/handlers/user_handlers/advice_handler.py (show_advice_message): \n----> {e}")
        await query.answer("خطا، فایل وجود ندارد.")


async def return_to_advice_key(update: Update, context: CallbackContext):
    query = update.callback_query

    await query.delete_message()
    await handle(update, context)
    await query.answer("✅")
