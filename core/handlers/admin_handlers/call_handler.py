from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import core.data_handler
import core.utils.work_with_strings
import core.utils.date_and_time

call_handler_main_keybaord = [
    ['رزرو های امروز و فردا'],
    ['تنظیم برنامه هفتگی', 'تنظیم هزینه'],
    ['🔙 | بازگشت به منوی اصلی']
]
call_handler_main_markup = ReplyKeyboardMarkup(call_handler_main_keybaord, one_time_keyboard=True)

translate = {"Sat": "شنبه", "Sun": "یکشنبه", "Mon": "دوشنبه", "Tue": "سه شنبه", "Wed": "چهارشنبه", "Thu": "پنجشنبه",
             "Fri": "جمعه"}


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != Config.ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="❌ | این عملکرد فقط برای ادمین قابل استفاده است.")
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="تنظیمات رزرو جلسه تلفنی",
                                       reply_markup=call_handler_main_markup)
        return 'CHOOSING'


async def set_price(update: Update, context: CallbackContext):
    current_price = await core.data_handler.get_price()
    current_price = await core.utils.work_with_strings.beautify_numbers(current_price)
    keyboard = [
        ['🔙 | بازگشت به منوی اصلی']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    text = f"""
قیمت فعلی:  {current_price} ریال.

قیمت جدید را ارسال کنید (اعداد لاتین و به ریال)    
    """
    await context.bot.send_message(chat_id=Config.ADMIN_ID, text=text, reply_markup=markup)
    return 'SEND_PRICE'


async def save_price(update: Update, context: CallbackContext):
    price = update.message.text

    try:
        price = int(price)
        await core.data_handler.save_new_price(price)
        price = await core.utils.work_with_strings.beautify_numbers(price)
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text=f"قیمت جدید: {price} ریال",
                                       reply_markup=call_handler_main_markup)
        return 'CHOOSING'

    except ValueError:
        keybaord = [
            ['🔙 | بازگشت به منوی اصلی']
        ]
        markup = ReplyKeyboardMarkup(keybaord, one_time_keyboard=True)
        await context.bot.send_message(chat_id=Config.ADMIN_ID, text="عدد وارد شده نامعتبر است. دوباره وارد کنید",
                                       reply_markup=markup)
        return 'SEND_PRICE'


async def show_weekly_plan(update: Update, context: CallbackContext):
    weekly_plan = await core.data_handler.get_weekly_plan()

    keyboard = []

    for day in weekly_plan:
        keyboard.append([
            InlineKeyboardButton("➕", callback_data=f"call-handler-weekly-plan-plus-one {day}"),
            InlineKeyboardButton(f"{translate[day]} ({weekly_plan[day]})", callback_data="none none"),
            InlineKeyboardButton("➖", callback_data=f"call-handler-weekly-plan-minus-one {day}")
        ])

    inline_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="تنظیم تعداد تماس روزانه", reply_markup=inline_markup)
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END


async def change_weekly_plan(update: Update, context: CallbackContext):
    query = update.callback_query
    command = query.data.split()[0]
    day = query.data.split()[1]
    weekly_plan = await core.data_handler.get_weekly_plan()

    if command == "call-handler-weekly-plan-plus-one":
        value = weekly_plan[day] + 1
        await core.data_handler.edit_weekly_plan(day, value)
    else:
        if weekly_plan[day] > 0:
            value = weekly_plan[day] - 1
            await core.data_handler.edit_weekly_plan(day, value)

    weekly_plan = await core.data_handler.get_weekly_plan()
    keyboard = []

    for day in weekly_plan:
        keyboard.append([
            InlineKeyboardButton("➕", callback_data=f"call-handler-weekly-plan-plus-one {day}"),
            InlineKeyboardButton(f"{translate[day]} ({weekly_plan[day]})", callback_data="none none"),
            InlineKeyboardButton("➖", callback_data=f"call-handler-weekly-plan-minus-one {day}")
        ])

    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_reply_markup(reply_markup=inline_markup)
    await query.answer("✅")


async def show_reservations(update: Update, context: CallbackContext):
    today_date = await core.utils.date_and_time.get_date('today')
    tomorrow_date = await core.utils.date_and_time.get_date('tomorrow')

    keyboard = [
        [InlineKeyboardButton("امروز", callback_data=f"admin-show-res {today_date}")],
        [InlineKeyboardButton("فردا", callback_data=f"admin-show-res {tomorrow_date}")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=Config.ADMIN_ID, text="کدام رو نمایش بدم؟", reply_markup=markup)
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END


async def display_reservations(update: Update, context: CallbackContext):
    query = update.callback_query
    date = query.data.split()[1]

    keyboard = []
    reservations = await core.data_handler.get_reservations(date)
    if not reservations:
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌", callback_data="none ❌")]])
        await query.edit_message_text("هیچ رزروی برای این روز موجود نیست", reply_markup=markup)
    else:
        for user_id in reservations['reservations']:
            user_data = await core.data_handler.get_user_data(user_id)
            keyboard.append(
                [InlineKeyboardButton(f"{user_data['name']} ({user_data['phone_number']})",
                                      callback_data=f"admin-show-det {user_id} {date}")]
            )
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"برنامه رزرو های \n{date}", reply_markup=markup)
    await query.answer()


async def display_reservation_details(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.data.split()[1]
    date = query.data.split()[2]

    user_data = await core.data_handler.get_user_data(user_id)
    user_reservations = await core.data_handler.get_user_reserve_history(user_id)
    user_related_reservation_count = user_reservations[date]

    key_translate = {
        "name": "نام و نام خانوادگی",
        "gender": "جنسیت",
        "grade": "پایه تحصیلی",
        "reshte": "رشته تحصیلی",
        "status": "وضعیت تحصیل",
        "phone_number": "شماره تلفن",
    }

    user_details = ""

    for key in user_data:
        if key != "auto_motivation":
            user_details += f"{key_translate[key]}: {user_data[key]}\n"

    text = f"""
کاربر با مشخصات زیر:

{user_details}

به تعداد زیر جلسه رزرو کرده است:
{user_related_reservation_count}

<pre>{user_data['phone_number']}</pre>

    """

    keyboard = [
        [InlineKeyboardButton("بازگشت", callback_data=f"admin-show-res {date}")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
    await query.answer()
