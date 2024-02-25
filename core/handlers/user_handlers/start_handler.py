from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

user_main_keyboard = [
    ['⭐️ انگیزه بگیر!', '⭐ تنظیمات انگیزشی'],
    ['نکات مشاوره‌ای', 'مخزن فایل'],  # '📞 جلسه تلفنی'
    ['📔 گزارش جدید', 'تنظیمات گزارش'],
    # ['💲 کیف پول'],
    ['تنظیمات کاربری 🔧']  # '💳 اشتراک ماهانه'
]
user_main_reply_markup = ReplyKeyboardMarkup(user_main_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="🏠 | منوی اصلی کاربر", reply_markup=user_main_reply_markup)
