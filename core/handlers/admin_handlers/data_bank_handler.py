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
        for message_id in file_bank["ids"][0:min(10, len(file_bank["ids"]))]:
            inline_keyboard.append(
                [InlineKeyboardButton(f"{file_bank['titles'][message_id]}", callback_data=f"show-file {message_id}")]
            )
        inline_keyboard.append(
            [
                InlineKeyboardButton("قبلی >>", callback_data="previous-page 1"),
                InlineKeyboardButton(f"Page 1", callback_data="none 1"),
                InlineKeyboardButton("<< بعدی", callback_data="next-page 1")
            ]
        )
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        text = """
🏦 بانک فایل

صفحه اول
        """
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=inline_markup)
        await core.handlers.start_handler.handle(update, context)


async def pre_page(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = int(query.data.split()[1])

    if query_data == 1:
        await query.answer("صفحه اول")
    else:
        file_bank = await core.data_handler.get_all_file_bank()
        inline_keyboard = []

        total_length = len(file_bank["ids"])

        for message_id in file_bank["ids"][(query_data - 2) * 10: min(total_length, query_data * 10 - 10)]:
            inline_keyboard.append(
                [InlineKeyboardButton(f"{file_bank['titles'][message_id]}", callback_data=f"show-file {message_id}")]
            )

        inline_keyboard.append(
            [
                InlineKeyboardButton("قبلی >>", callback_data=f"previous-page {query_data - 1}"),
                InlineKeyboardButton(f"Page {query_data - 1}", callback_data=f"none {query_data - 1}"),
                InlineKeyboardButton("<< بعدی", callback_data=f"next-page {query_data - 1}")
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

        for message_id in file_bank["ids"][query_data * 10: min(total_length, query_data * 10 + 10)]:
            inline_keyboard.append(
                [InlineKeyboardButton(f"{file_bank['titles'][message_id]}", callback_data=f"show-file {message_id}")]
            )

        inline_keyboard.append(
            [
                InlineKeyboardButton("قبلی >>", callback_data=f"previous-page {query_data + 1}"),
                InlineKeyboardButton(f"Page {query_data + 1}", callback_data=f"none {query_data + 1}"),
                InlineKeyboardButton("<< بعدی", callback_data=f"next-page {query_data + 1}")
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
    message_id = query.data.split()[1]
    if await core.data_handler.file_in_motivation(message_id):
        motivation_button_text = "حذف از محتوای انگیزشی"
    else:
        motivation_button_text = "⭐️ اضافه کردن به محتوای انگیزشی"

    delete_keyboard = [
        [InlineKeyboardButton("🔗 لینک این فایل 🔗", callback_data=f"show-link {message_id}")],
        [InlineKeyboardButton(motivation_button_text, callback_data=f"change-motivation-status {message_id}")],
        [InlineKeyboardButton("نکات مشاوره‌ای", callback_data=f"data-bank-advice {message_id}")],
        [InlineKeyboardButton("❌ حذف این فایل ❌", callback_data=f"delete-file {message_id}")]
    ]
    delete_markup = InlineKeyboardMarkup(delete_keyboard)
    await query.delete_message()
    try:
        await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=Config.ADMIN_ID,
                                       message_id=int(message_id), reply_markup=delete_markup)
        await query.answer("✅")
    except:
        await query.answer("❌ خطا")

    await core.handlers.start_handler.handle(update, context)


async def show_link(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]
    data = await core.data_handler.get_file_in_file_bank(message_id)
    text = f"""
link for file {data["title"]}:

{data["link"]}
    """
    inline_keyboard = [
        [InlineKeyboardButton("بازگشت", callback_data=f"show-file {message_id}")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    await query.delete_message()
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=inline_markup)
    await query.answer("🔗 لینک")


async def show_none(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split()[1]
    await query.answer(f"page {query_data}")


async def delete_file(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]

    if await core.data_handler.delete_file_in_bank(message_id):
        await query.delete_message()
        await query.answer("✅ فایل حذف شد")
        await core.handlers.start_handler.handle(update, context)
    else:
        await query.answer("❌ خطا")


async def change_motivation_status(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]

    if await core.data_handler.file_in_motivation(message_id):
        await core.data_handler.delete_from_motivation(message_id)

        motivation_button_text = "⭐️ اضافه کردن به محتوای انگیزشی"

        delete_keyboard = [
            [InlineKeyboardButton("🔗 لینک این فایل 🔗", callback_data=f"show-link {message_id}")],
            [InlineKeyboardButton(motivation_button_text, callback_data=f"change-motivation-status {message_id}")],
            [InlineKeyboardButton("نکات مشاوره‌ای", callback_data=f"data-bank-advice {message_id}")],
            [InlineKeyboardButton("❌ حذف این فایل ❌", callback_data=f"delete-file {message_id}")]
        ]
        delete_markup = InlineKeyboardMarkup(delete_keyboard)
        await query.edit_message_reply_markup(reply_markup=delete_markup)
        await query.answer("حذف شد از لیست انگیزشی")
    else:
        await core.data_handler.add_motivation_message(message_id)
        motivation_button_text = "حذف از محتوای انگیزشی"

        delete_keyboard = [
            [InlineKeyboardButton("🔗 لینک این فایل 🔗", callback_data=f"show-link {message_id}")],
            [InlineKeyboardButton(motivation_button_text, callback_data=f"change-motivation-status {message_id}")],
            [InlineKeyboardButton("❌ حذف این فایل ❌", callback_data=f"delete-file {message_id}")]
        ]
        delete_markup = InlineKeyboardMarkup(delete_keyboard)
        await query.edit_message_reply_markup(reply_markup=delete_markup)
        await query.answer("اضافه شد به محتوای انگیزشی")


# advice file bank
async def show_advice_categories(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]
    advices = await core.data_handler.get_all_advice()
    keyboard = []

    for category_hash in advices:
        text = ""
        if str(message_id) in advices[category_hash]:
            text += "✅"
        else:
            text += "➕"
        text += advices[category_hash][category_hash]
        keyboard.append(
            [InlineKeyboardButton(text, callback_data=f"admin-db-add-advice-to-category {message_id} {category_hash}")]
        )

    keyboard.append([InlineKeyboardButton("بازگشت", callback_data=f"show-file {message_id}")])
    markup = InlineKeyboardMarkup(keyboard)
    await query.delete_message()
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="دسته بندی‌ها", reply_markup=markup)
    await query.answer("✅")


async def add_file_to_advice_category(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]
    category_hash = query.data.split()[2]

    advices = await core.data_handler.get_all_advice()

    if message_id in advices[category_hash]:  # delete advice from category
        await core.data_handler.delete_advice(category_hash, message_id)

    else:  # add advice to category
        title = await core.data_handler.get_file_in_file_bank(message_id)
        title = title["title"]
        await core.data_handler.new_advice(category_hash, title, message_id)

    await show_advice_categories(update, context)
