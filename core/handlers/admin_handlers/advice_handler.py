from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.user_handlers.basic_settings_handler
import core.data_handler
import core.handlers.start_handler


advice_settings_keyboard = [
    ['مشاهده دسته بندی‌ها'],
    ['دسته بندی جدید'],
    ['🔙 | بازگشت به منوی اصلی']
]
advice_settings_markup = ReplyKeyboardMarkup(advice_settings_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="Sorry you are not authorized to use this part.")
        await core.handlers.user_handlers.basic_settings_handler.return_home(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID,
                                       text="تنظیمات نکات مشاوره‌ای. لطفا از منوی زیر انتخاب کنید:",
                                       reply_markup=advice_settings_markup)
        return 'CHOOSING'


async def show_categories(update: Update, context: CallbackContext):
    buttons = []
    advices = await core.data_handler.get_all_advice()

    for category in advices:
        buttons.append([
            InlineKeyboardButton(str(category), callback_data=f"admin-show-advice-category {category}"),
            InlineKeyboardButton("❌", callback_data=f"admin-delete-advice-category {category}")
        ])

    inline_markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="دسته بندی‌ها", reply_markup=inline_markup)
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END


async def new_category(update: Update, context: CallbackContext):
    keyboard = [
        ['🔙 | بازگشت به منوی اصلی']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="حله! عنوان دسته بندی جدید رو بفرست",
                                   reply_markup=reply_markup)

    return 'GET_CATEGORY_TITLE'


async def save_new_category(update: Update, context: CallbackContext):
    title = update.message.text
    await core.data_handler.new_advice_category(title)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="انجام شد!", reply_markup=advice_settings_markup)
    return 'CHOOSING'


async def delete_category(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split()[1]

    keyboard = [
        [InlineKeyboardButton(text="بله حذف شود", callback_data=f"yes-delete {category}")],
        [InlineKeyboardButton(text="خیر! بازگشت", callback_data="admin-return-advice-categories")]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    text = """
آیا تمایل دارید دسته بندی زیر و همه‌ی فایل‌های مربوطه حذف شود؟

{category}
    """
    await query.edit_message_text(text=text, reply_markup=inline_markup)
    await query.answer()


async def yes_delete_category(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split()[1]
    await core.data_handler.delete_advice_category(category)
    await query.answer("✅")
    keyboard = [[InlineKeyboardButton(text="بازگشت", callback_data="admin-return-advice-categories")]]
    inline_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"دسته بندی {category} و همه فایل‌های آن حذف شدند.", reply_markup=inline_markup)


async def admin_return_advice_categories(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.delete_message()
    await query.answer()

    keyboard = []
    advice_categories = await core.data_handler.get_all_advice()

    for category in advice_categories:
        keyboard.append([
            InlineKeyboardButton(str(category), callback_data=f"admin-show-advice-category {category}"),
            InlineKeyboardButton("❌", callback_data=f"admin-delete-advice-category {category}")
        ])

    inline_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="دسته بندی‌ها", reply_markup=inline_markup)
    await core.handlers.start_handler.handle(update, context)


async def admin_show_advice_category(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split()[1]
    advices = await core.data_handler.get_all_advice()
    advices = advices[str(category)]

    buttons = []

    for advice in advices:
        buttons.append([
            InlineKeyboardButton(advices[advice], callback_data=f"admin-show-advice-message {advice}"),
            InlineKeyboardButton("❌", callback_data="admin-delete-advice {category} {advice}")
        ])
    buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="admin-return-advice-categories")])
    await query.delete_message()
    await query.answer()

    markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=f"{category}", reply_markup=markup)


async def admin_delete_advice(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split()[1]
    advice = query.data.split()[2]

    await core.data_handler.delete_advice(category, advice)
    await query.answer("با موفقیت حذف شد ✅")

    advices = await core.data_handler.get_all_advice()
    advices = advices[category]
    buttons = []

    for _ in advices:
        buttons.append([
            InlineKeyboardButton(advices[_], callback_data=f"admin-show-advice-message {_}"),
            InlineKeyboardButton("❌", callback_data="admin-delete-advice {category} {advice}")
        ])
    buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="admin-return-advice-categories")])
    await query.delete_message()
    await query.answer()

    markup = InlineKeyboardMarkup(buttons)

    await query.edit_message_reply_markup(reply_markup=markup)


async def admin_show_advice_message(update: Update, context: CallbackContext):
    query = update.callback_query
    message_id = query.data.split()[1]

    keyboard = [[InlineKeyboardButton(text="بازگشت", callback_data="admin-return-advice-categories")]]
    markup = InlineKeyboardMarkup(keyboard)

    await query.delete_message()

    await context.bot.copy_message(from_chat_id=Config.ADMIN_ID, chat_id=Config.ADMIN_ID, message_id=int(message_id),
                                   reply_markup=markup)
    await query.answer("✅")


async def new_message_in_category(update: Update, context: CallbackContext):
    query = update.callback_query
    advice_key = query.data.split()[1]

    context.user_data['advice_key'] = advice_key

    await query.delete_message()
    await query.answer("✅")

    text = f"""
پیام جدید در قسمت:
{advice_key}

عنوان فایل را وارد کنید:
    """
    keyboard = [
        ['🔙 | بازگشت به منوی اصلی']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=reply_markup)
    return 'SEND_TITLE'


async def new_message_get_file(update: Update, context: CallbackContext):
    title = update.message.text
    context.user_data['title'] = title

    keyboard = [
        ['🔙 | بازگشت به منوی اصلی']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)

    text = """
در حال آپلود فایل برای 
{advice_key}

با عنوان
{title}

لطفا پیام خود را نوشته یا فوروارد کنید.
    """

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=reply_markup)
    return 'SEND_FILE'


async def save_advice(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    title = context.user_data['title']
    advice_key = context.user_data['advice_key']

    await core.data_handler.new_advice(advice_key, title, message_id)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="انجام شد!", reply_markup=advice_settings_markup)
    return 'CHOOSING'
