from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from core.config import Config
import core.handlers.start_handler
import core.data_handler
import core.utils.work_with_strings

call_handler_main_keybaord = [
    ['رزرو های امروز و فردا'],
    ['تنظیم برنامه هفتگی'],
    ['تنظیم هزینه', 'سابقه تماس‌ها'],
    ['🔙 | بازگشت به منوی اصلی']
]
call_handler_main_markup = ReplyKeyboardMarkup(call_handler_main_keybaord, one_time_keyboard=True)


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
    currunt_price = await core.data_handler.get_price()
    currunt_price = await core.utils.work_with_strings.beautify_numbers(currunt_price)
    keybaord = [
        ['🔙 | بازگشت به منوی اصلی']
    ]
    markup = ReplyKeyboardMarkup(keybaord, one_time_keyboard=True)
    text = f"""
قیمت فعلی:  {currunt_price} ریال.

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
