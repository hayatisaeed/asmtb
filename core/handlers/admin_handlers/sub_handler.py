from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import core.data_handler
import core.utils.work_with_strings
import core.utils.date_and_time

main_admin_sub_keyboard = [
    ["لیست مشترکان"],
    ["رایگان کردن کاربر"],
    ["مشاهده کاربران رایگان"],
    ['🔙 | بازگشت به منوی اصلی']
]
main_admin_sub_markup = ReplyKeyboardMarkup(main_admin_sub_keyboard, one_time_keyboard=True)
cancel_keyboard = [['🔙 | بازگشت به منوی اصلی']]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="قسمت مدیریت اشتراک ها",
                                       reply_markup=main_admin_sub_markup)
        return 'CHOOSING'


async def show_sub_list(update: Update, context: CallbackContext):
    sub_list = await core.data_handler.get_sub_list()

    table_data = [
        ['user_id', 'name', 'phone', 'buy_date', '*']
    ]

    for sub in sub_list:
        user_data = await core.data_handler.get_user_data(sub)
        name = user_data['name']
        phone = user_data['phone_number']
        buy_date = sub_list[sub]['buy_date']
        status = '✅' if await core.utils.date_and_time.calculate_age_in_days(buy_date) <= 30 else '❌'
        table_data.append([sub, name, phone, buy_date, status])

    table = await core.utils.work_with_strings.generate_formatted_table(table_data)

    text = f"""
لیست کاربرانی که اشتراک خریداری کرده اند:

<pre>{table}</pre>

    """

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=main_admin_sub_markup)
    return 'CHOOSING'


async def make_user_free(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا آیدی عددی کاربر مورد نظر را ارسال کنید",
                                   reply_markup=cancel_markup)
    return 'FREE_GET_ID'


async def make_user_free_show_status(update: Update, context: CallbackContext):
    user_id = update.message.text
    if not await core.data_handler.user_is_saved(user_id):
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="این کاربر وجود ندارید")
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="لطفا آیدی عددی کاربر مورد نظر را ارسال کنید",
                                       reply_markup=cancel_markup)
        return 'FREE_GET_ID'
    else:
        is_free = await core.data_handler.user_is_free_sub(user_id)

        keyboard = []
        if is_free:
            keyboard.append(
                [InlineKeyboardButton("تغییر به عادی", callback_data=f"change-free-status {user_id}")]
            )
        else:
            keyboard.append(
                [InlineKeyboardButton("رایگان کردن کاربر", callback_data=f"change-free-status {user_id}")]
            )
        markup = InlineKeyboardMarkup(keyboard)

        text = f"""
این کاربر در حال حاضر 
{'✅ رایگان' if is_free else '💰 کاربر عادی'}
میباشد.
برای تغییر وضعیت این کاربر از دکمه زیر استفاده کنید.

        """

        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=markup)
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END


async def change_user_free_status(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.data.split()[1]

    user_is_free = await core.data_handler.user_is_free_sub(user_id)
    if user_is_free:
        new_text = f"""
این کاربر در حال حاضر 
{'✅ رایگان' if user_is_free else '💰 کاربر عادی'}
میباشد.
برای تغییر وضعیت این کاربر از دکمه زیر استفاده کنید.

        """

        new_keyboard = [
            [InlineKeyboardButton("رایگان کردن کاربر", callback_data=f"change-free-status {user_id}")]
        ]
        new_markup = InlineKeyboardMarkup(new_keyboard)

        await query.message.edit_text(text=new_text, reply_markup=new_markup)
        await query.answer("💰 کاربر عادی شد")

    else:
        user_text = """
✅ تبریک!

بات از اکنون برای شما رایگان است. میتوانید از بخش های مختلف استفاده کنید.
برای استفاده یکبار بات را /start کنید.
        """

        new_keyboard = [
            [InlineKeyboardButton("تغییر به عادی", callback_data=f"change-free-status {user_id}")]
        ]
        new_markup = InlineKeyboardMarkup(new_keyboard)
        new_text = f"""
این کاربر در حال حاضر 
{'✅ رایگان' if not user_is_free else '💰 کاربر عادی'}
میباشد.
برای تغییر وضعیت این کاربر از دکمه زیر استفاده کنید.

        """

        await context.bot.send_message(chat_id=user_id, text=user_text)
        await query.edit_message_text(text=new_text, reply_markup=new_markup)
        await query.answer("✅ کاربر رایگان شد")
