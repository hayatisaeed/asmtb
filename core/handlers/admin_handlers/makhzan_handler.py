from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import core.data_handler

main_keyboard = [
    ['اضافه کردن دسته بندی'],
    ['🔙 | بازگشت به منوی اصلی']
]
markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)

cancel_keyboard = [
    ['🔙 | بازگشت به منوی اصلی']
]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != Config.ADMIN_ID:
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END

    makhzan_data = core.data_handler.get_makhzan_data()

    inline_keyboard = []

    for category_id in makhzan_data:
        category_name = makhzan_data[category_id]['name']
        inline_keyboard.append([
            InlineKeyboardButton(f"{category_name}", callback_data=f"show-foc {category_id}"),
            InlineKeyboardButton("❌", callback_data=f"admin-rem-mcat {category_id}")
        ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="مخازن", reply_markup=inline_markup)
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="از منوی زیر انتخاب کنید", reply_markup=markup)
    return 'CHOOSING'


async def new_category(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="نام دسته بندی جدید را وارد کنید:",
                                   reply_markup=cancel_markup)
    return 'SEND_CAT_NAME'


async def save_new_category(update: Update, context: CallbackContext):
    new_category_name = update.message.text
    makhzan_data = core.data_handler.get_makhzan_data()
    new_key = max(makhzan_data) + 1
    makhzan_data[new_key] = {'name': new_category_name, "files": {}}
    core.data_handler.edit_makhzan_data(makhzan_data)

    text = f"""
    دسته بندی جدیدی با نام زیر در مخزن اضافه شد:
    {new_category_name}
    """
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=markup)
    return 'CHOOSING'


async def remove_category(update: Update, context: CallbackContext):
    query = update.callback_query
    category_id = query.data.split()[1]

    makhzan_data = core.data_handler.get_makhzan_data()

    try:
        makhzan_data.pop(int(category_id))
        core.data_handler.edit_makhzan_data(makhzan_data)
    except Exception as e:
        print("error in remove_category admin_handler/makhzan_handler.py: ", e)

    inline_keyboard = []

    for category_id in makhzan_data:
        category_name = makhzan_data[category_id]['name']
        inline_keyboard.append([
            InlineKeyboardButton(f"{category_name}", callback_data=f"show-foc {category_id}"),
            InlineKeyboardButton("❌", callback_data=f"admin-rem-mcat {category_id}")  # mcat = makhzan category
        ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    await query.edit_message_reply_markup(reply_markup=inline_markup)
    await query.answer("حذف شد")
