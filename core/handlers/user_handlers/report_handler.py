from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import core.data_handler
import core.utils.date_and_time
import core.handlers.start_handler


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("مشاهده گزارش‌های من",
                              url=f"http://103.75.197.206:5000/showMyReports?user_id={user_id}")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    text = """
    تنظیمات گزارش‌های پیشین شما
    """
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=markup)
    await core.handlers.start_handler.handle(update, context)


async def new_report(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data = await core.data_handler.get_user_data(user_id)
    user_name = user_data["name"]

    date = await core.utils.date_and_time.get_date('today')

    user_reports = core.data_handler.get_all_reports(user_id)
    user_has_entered_report = date in user_reports

    if user_has_entered_report:
        message = """
        گزارش شما قبلا ثبت شده است، آیا میخواهید گزارش شما جایگزین قبلی شود؟ توجه کنید که گزارش قبلی حذف میشود.
        """
        keyboard = [
            [InlineKeyboardButton("حذف قبلی و جایگزینی جدید",
                                  url=f"http://103.75.197.206:5000/showReportForm?user_id={user_id}&\
                                  user_name={user_name}&date={date}")]
        ]
    else:
        message = """
        آیا میخواهید گزارش جدیدی برای امروز ثبت کنید؟
        توجه کنید در صورتی که قبلا گزارشی برای امروز ثبت کرده باشید با این گزارش جدید جایگزین خواهد شد.
        """
        keyboard = [
            [InlineKeyboardButton("ثبت گزارش جدید برای امروز",
                                  url=f"http://103.75.197.206:5000/showReportForm?user_id={user_id}&\
                                          user_name={user_name}&date={date}")]
        ]

    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=markup)
    await core.handlers.start_handler.handle(update, context)
