from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
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
    ["تغییر قیمت اشتراک"],
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

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=main_admin_sub_markup,
                                   parse_mode=ParseMode.HTML)
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
{user_id}
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
{user_id}
این کاربر در حال حاضر 
💰 کاربر عادی
میباشد.
برای تغییر وضعیت این کاربر از دکمه زیر استفاده کنید.

        """

        new_keyboard = [
            [InlineKeyboardButton("رایگان کردن کاربر", callback_data=f"change-free-status {user_id}")]
        ]
        new_markup = InlineKeyboardMarkup(new_keyboard)

        await query.message.edit_text(text=new_text, reply_markup=new_markup)
        await core.data_handler.change_user_free_status(user_id)
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
{user_id}
این کاربر در حال حاضر 
✅ رایگان
میباشد.
برای تغییر وضعیت این کاربر از دکمه زیر استفاده کنید.

        """

        await context.bot.send_message(chat_id=user_id, text=user_text)
        await query.edit_message_text(text=new_text, reply_markup=new_markup)
        await core.data_handler.change_user_free_status(user_id)
        await query.answer("✅ کاربر رایگان شد")


async def show_free_users(update: Update, context: CallbackContext):
    free_users_data = await core.data_handler.get_free_users()
    free_users = free_users_data['free_users']
    table = "*********\n"

    for user in free_users:
        user_data = await core.data_handler.get_user_data(user)
        user_name = user_data['name']
        table += f"{user_name} --> <code>{user}</code>\n*********\n"

    text = f"""
لیست کاربران رایگان:


{table}

    """

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=main_admin_sub_markup,
                                   parse_mode=ParseMode.HTML)
    return 'CHOOSING'


async def make_bot_free_for_all(update: Update, context: CallbackContext):
    bot_is_free_data = await core.data_handler.get_bot_is_free()
    bot_is_free = bot_is_free_data['bot_is_free']
    text = f"""
بات در حال حاضر

{'🟢 رایگان' if bot_is_free else '💰 پولی'}

است. برای تغییر وضعیت از دکمه زیر استفاده کنید

    """

    keyboard = [
        [InlineKeyboardButton(f"{'💰 تبدیل به پولی' if bot_is_free else '🟢 تبدیل به رایگان'}",
                              callback_data="change-bot-is-free-status")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=markup)
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END


async def change_bot_is_free(update: Update, context: CallbackContext):
    query = update.callback_query
    bot_is_free_status = await core.data_handler.get_bot_is_free()
    bot_is_free = bot_is_free_status['bot_is_free']

    text = f"""
بات در حال حاضر

{'🟢 رایگان' if not bot_is_free else '💰 پولی'}

است. برای تغییر وضعیت از دکمه زیر استفاده کنید

    """
    keyboard = [
        [InlineKeyboardButton(f"{'💰 تبدیل به پولی' if not bot_is_free else '🟢 تبدیل به رایگان'}",
                              callback_data="change-bot-is-free-status")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await core.data_handler.change_bot_is_free_status()
    await query.edit_message_text(text=text, reply_markup=markup)
    await query.answer("✅")


async def change_sub_price(update: Update, context: CallbackContext):
    sub_price = await core.utils.work_with_strings.beautify_numbers(await core.data_handler.get_sub_price())

    text = """
قیمت اشتراک ماهانه در حال حاضر 
{}
میباشد. (ریال)

قیمت جدید را وارد کنید (به صورت لاتین و به ریال) 
    """
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=cancel_markup)
    return 'NEW_PRICE'


async def save_new_sub_price(update: Update, context: CallbackContext):
    new_price = update.message.text

    try:
        new_price = int(new_price)
        past_price = await core.utils.work_with_strings.beautify_numbers(await core.data_handler.get_sub_price())
        bea_price = await core.utils.work_with_strings.beautify_numbers(new_price)

        text = f"""
انجام شد ✅

قیمت قبلی:
{past_price}

قیمت جدید:
{bea_price}
        """
        await core.data_handler.change_sub_price(new_price)
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=cancel_markup)
        return 'CHOOSING'
    except ValueError:
        text = "عدد نا معتبر. لطفا به صورت اعداد لاتین و به ریال وارد کنید."
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=cancel_markup)
        return 'NEW_PRICE'
