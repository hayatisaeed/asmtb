from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import core.data_handler
import core.handlers.start_handler
from core.config import Config


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    makhzan_data = core.data_handler.get_makhzan_data()

    inline_keyboard = []

    for category_id in makhzan_data:
        category_name = makhzan_data[category_id]['name']
        inline_keyboard.append([
            InlineKeyboardButton(f"{category_name}", callback_data=f"show-foc {category_id}"),
        ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    text = """
    مخزن فایل
    """
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=inline_markup)
    await core.handlers.start_handler.handle(update, context)


async def show_foc(update: Update, context: CallbackContext):
    query = update.callback_query
    category_id = query.data.split()[1]

    makhzan_data = core.data_handler.get_makhzan_data()[category_id]

    name = makhzan_data['name']

    inline_keyboard = []

    for file_id in makhzan_data['files']:
        inline_keyboard.append([
            InlineKeyboardButton(f"{makhzan_data['files'][file_id]}", callback_data=f" {file_id}")
        ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    text = f"""
    نمایش فایل ها در دسته بندی {name}
    """

    await query.edit_message_text(text=text, reply_markup=inline_markup)
    await query.answer()


async def show_the_file(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]

    await query.delete_message()

    try:
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=query.message.chat_id,
                                       message_id=int(message_id))
    except Exception as e:
        print("error in show_the_file user_handlers/makhzan_handler.py: ", e)

    await query.answer()
