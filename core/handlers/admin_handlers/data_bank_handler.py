from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from core.config import Config
import core.handlers.start_handler
import core.data_handler


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        # user is not admin
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END

    else:
        file_bank = await core.data_handler.get_all_file_bank()
        inline_keyboard = []
        for message_id in file_bank["ids"][0:10+1]:
            inline_keyboard.append(
                [InlineKeyboardButton(f"{file_bank['titles'][message_id]}", callback_data=f"show_file {message_id}")]
            )
        inline_keyboard.append(
            [
                InlineKeyboardButton(">>", callback_data="previous-page 1"),
                InlineKeyboardButton(f"Page 1", callback_data="none 1"),
                InlineKeyboardButton("<<", callback_data="next-page 1")
            ]
        )
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        text = """
🏦 بانک فایل

صفحه اول
        """
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=inline_markup)


async def pre_page(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = int(query.data.split()[1])

    if query_data == 1:
        await query.answer("صفحه اول")
    else:
        file_bank = await core.data_handler.get_all_file_bank()
        inline_keyboard = []

        total_length = len(file_bank["ids"])

        for message_id in file_bank["ids"][(query_data - 1) * 10 + 1: min(total_length, query_data * 10) + 1]:
            inline_keyboard.append(
                [InlineKeyboardButton(f"{file_bank['titles'][message_id]}", callback_data=f"show_file {message_id}")]
            )

        inline_keyboard.append(
            [
                InlineKeyboardButton(">>", callback_data=f"previous-page {query_data - 1}"),
                InlineKeyboardButton(f"Page 1", callback_data=f"none {query_data - 1}"),
                InlineKeyboardButton("<<", callback_data=f"next-page {query_data - 1}")
            ]
        )
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        text = f"""
        🏦 بانک فایل

        صفحه {query_data - 1}
                """

        await query.message.edit_text(text=text)
        await query.edit_message_reply_markup(reply_markup=inline_markup)

        await query.answer("بازگشت به صفحه قبل ...")


async def next_page(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = int(query.data.split()[1])

    file_bank = await core.data_handler.get_all_file_bank()

    if query_data * 10 >= len(file_bank["ids"]):
        await query.answer("صفحه آخر")
    else:
        inline_keyboard = []

        total_length = len(file_bank["ids"])

        for message_id in file_bank["ids"][query_data * 10 + 1: min(total_length, query_data * 10) + 1]:
            inline_keyboard.append(
                [InlineKeyboardButton(f"{file_bank['titles'][message_id]}", callback_data=f"show_file {message_id}")]
            )

        inline_keyboard.append(
            [
                InlineKeyboardButton("<<", callback_data=f"next-page {query_data + 1}"),
                InlineKeyboardButton(f"Page 1", callback_data=f"none {query_data + 1}"),
                InlineKeyboardButton(">>", callback_data=f"previous-page {query_data + 1}")
            ]
        )
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        text = f"""
            🏦 بانک فایل

            صفحه {query_data + 1}
                    """

        await query.message.edit_text(text=text)
        await query.edit_message_reply_markup(reply_markup=inline_markup)

        await query.answer("مشاهده صفحه بعد ...")


async def show_file(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.message.message_id
    delete_keyboard = [
        [InlineKeyboardButton("🔗 لینک این فایل 🔗", callback_data=f"show-link {message_id}")],
        [InlineKeyboardButton("❌ حذف این فایل ❌", callback_data=f"delete-file {message_id}")]
    ]
    delete_markup = InlineKeyboardMarkup(delete_keyboard)
    await query.delete_message()
    try:
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=Config.ADMIN_ID, message_id=message_id,
                                       reply_markup=delete_markup)
        await query.answer("✅")
    except:
        await query.answer("❌ خطا")


async def show_link(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]
    data = await core.data_handler.get_file_in_file_bank(message_id)
    text = f"""
link for file {data["title"]}:

{data["link"]}
    """
    inline_keyboard = [
        [InlineKeyboardButton("بازگشت", callback_data=f"show_file {message_id}")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.edit_message_text(text="text")
    await query.edit_message_reply_markup(reply_markup=inline_markup)
    await query.answer("🔗 لینک")


async def show_none(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split()[1]
    await query.answer(f"page {query_data}")


async def delete_file(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]

    if core.data_handler.delete_file_in_bank(message_id):
        await query.delete_message()
        await query.answer("✅ فایل حذف شد")
        await core.handlers.start_handler.handle(update, context)
    else:
        await query.answer("❌ خطا")
