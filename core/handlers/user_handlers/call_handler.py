from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import core.handlers.start_handler
import datetime
import core.data_handler
import core.utils.work_with_strings
import core.handlers.user_handlers.wallet_handler

user_main_call_handler_keyboard = [
    ['رزرو جدید', 'سابقه رزروها'],
    ['🔙 | بازگشت به منوی اصلی']
]
user_main_call_handler_markup = ReplyKeyboardMarkup(user_main_call_handler_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="قسمت رزرو جلسه تلفنی",
                                   reply_markup=user_main_call_handler_markup)
    return 'CHOOSING'


async def show_reserve_history(update: Update, context: CallbackContext):
    pass


async def get_day_name(day):
    today = datetime.date.today()

    # Get tomorrow's date
    tomorrow = today + datetime.timedelta(days=1)

    # Get the name of tomorrow's day of the week
    today_name = today.strftime("%A")[:3]
    tomorrow_name = tomorrow.strftime('%A')[:3]

    current_datetime = datetime.datetime.now()

    # Extract date from datetime object
    current_date = current_datetime.date()

    if day == 'today':
        return today_name
    elif day == 'tomorrow':
        return tomorrow_name
    elif day == 'date':
        return current_date


async def new_reserve(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    weekly_plan = await core.data_handler.get_weekly_plan()

    today_name = await get_day_name('today')
    tomorrow_name = await get_day_name('tomorrow')

    day_keyboard = []

    available_to_reserve = False

    if weekly_plan[today_name]:
        day_keyboard.append([InlineKeyboardButton('امروز', callback_data='user-call-nr today')])
        available_to_reserve = True

    if weekly_plan[tomorrow_name]:
        day_keyboard.append([InlineKeyboardButton('فردا', callback_data='user-call-nr tomorrow')])
        available_to_reserve = True

    if available_to_reserve:
        markup = InlineKeyboardMarkup(day_keyboard)

        await context.bot.send_message(chat_id=user_id, text="میخوای برای امروز رزور کنی یا فردا؟", reply_markup=markup)
        await core.handlers.start_handler.handle(update, context)
        return ConversationHandler.END

    else:
        await context.bot.send_message(chat_id=user_id, text="متاسفانه همه‌ی وقت‌ها پر شدن!",
                                       reply_markup=user_main_call_handler_markup)
        return 'CHOOSING'


async def new_reserve_choose_day(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    day = query.data.split()[1]

    price = await core.data_handler.get_price()

    date = await get_day_name('date')
    day = await get_day_name(day)

    user_data = await core.data_handler.get_user_data(user_id)
    phone_number = user_data['phone_number']

    if phone_number == 'تعیین نشده':
        text = """
        مشخصات کاربری شما کامل نیست!
        لطفا ابتدا از بخش تنظیمات کاربری مشخصات خود را کامل کنید و سپس روی دکمه زیر بزنید.
        """
        inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton('کلیک برای رزرو', callback_data=query.data)]])
        await query.edit_message_text(
            text=text,
            reply_markup=inline_markup)
    else:
        keyboard = [
            [InlineKeyboardButton('✅ تایید و پرداخت', callback_data=f'user-call-cr {date} {price}\
             {day}')]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        price_bea = await core.utils.work_with_strings.beautify_numbers(price)
        text = f"""
    رزرو جلسه تلفنی برای {'امروز' if day == 'today' else 'فردا'} با شماره تلفن {phone_number} مورد تایید است؟
        
        هزینه این جلسه  {price_bea} است.
        """
        await query.edit_message_text(text=text, reply_markup=markup)

    await query.answer()


async def confirm_reservation(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    date = query.data.split()[1]
    price = int(query.data.split()[2])
    day = query.data.split()[3]

    if await core.data_handler.day_has_capacity(day, date):
        if await core.handlers.user_handlers.wallet_handler.spend_credit(user_id, price):
            await core.data_handler.new_reservation(date)
            await core.data_handler.new_reservations_save_data(user_id, date, day)
            await query.answer("✅")
        else:
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌", callback_data="none ❌")]])
            await query.edit_message_text(text="موجودی کافی نیست. لطفا ابتدا کیف پول خود را شارژ کنید.",
                                          reply_markup=markup)
            await query.answer("موجودی کافی نیست ❌")
    else:
        await query.answer("❌ ظرفیت تکمیل شده است")
