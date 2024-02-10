from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import core.handlers.start_handler
import datetime
import core.data_handler

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
        day_keyboard.append([InlineKeyboardButton('امروز', callback_data='user-call-new-reservation today')])
        available_to_reserve = True

    if weekly_plan[tomorrow_name]:
        day_keyboard.append([InlineKeyboardButton('فردا', callback_data='user-call-new-reservation tomorrow')])
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

    date = await get_day_name('date')

    keyboard = [
        [InlineKeyboardButton('✅ تایید و پرداخت', callback_data=f'user-call-confirm-reservation {date}')]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    user_data = await core.data_handler.get_user_data(user_id)
    phone_number = user_data['phone_number']

    text = f"""
رزرو جلسه تلفنی برای {'امروز' if day == 'today' else 'فردا'} با شماره تلفن {phone_number} مورد تایید است؟
    """
    await query.edit_message_text(text=text, reply_markup=markup)
    await query.answer()


async def confirm_reservation(update: Update, context: CallbackContext):
    query = update.callback_query

    await query.answer("✅")


async def show_payment(update: Update, context: CallbackContext):
    pass


async def save_reservation(update: Update, context: CallbackContext):
    pass
