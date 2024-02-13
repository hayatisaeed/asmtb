from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler
import core.data_handler
import core.utils.date_and_time
import core.utils.work_with_strings
import core.handlers.start_handler
import core.handlers.user_handlers.wallet_handler


main_sub_keyboard = [
    ["خرید یا تمدید اشتراک"],
    ["وضعیت اشتراک من"],
    ['🔙 | بازگشت به منوی اصلی']
]
main_sub_markup = ReplyKeyboardMarkup(main_sub_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message("مدیریت اشتراک", reply_markup=main_sub_markup)
    return 'CHOOSING'


async def show_my_sub_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    subs = await core.data_handler.get_sub_list()
    if str(user_id) not in subs:
        await context.bot.send_message(chat_id=user_id, text="شما تا کنون اشتراک تهیه نکرده‌اید.",
                                       reply_markup=main_sub_markup)
        return 'CHOOSING'
    else:
        exp_date = subs[str(user_id)]['exp_date']
        age = await core.utils.date_and_time.calculate_age_in_days(exp_date)
        if age > 0:
            await context.bot.send_message(chat_id=user_id, text="اشتراک شما به اتمام رسیده است.",
                                           reply_markup=main_sub_markup)
            return 'CHOOSING'
        else:
            text = f"""
اشتراک شما تا

{age * -1}

روز دیگر به اتمام میرسد.
            """
            await context.bot.send_message(chat_id=user_id, text=text, reply_markup=main_sub_markup)
            return 'CHOOSING'


async def buy_sub(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    price = await core.utils.work_with_strings.beautify_numbers(await core.data_handler.get_sub_price())
    text = f"""
آيا میخواهید اشتراک ماهانه با قیمت
{price}
خریداری کنید؟

در صورتی که اشتراک داشته باشید و هنوز از اشتراک شما باقی مانده باشد، ۳۰ روز به مدت اشتراک شما افزوده میشود.
    """
    keyboard = [
        [InlineKeyboardButton("تایید و پرداخت از کیف پول", callback_data="user-buy-sub")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=markup)
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END


async def buy_sub_do(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    sub_price = await core.data_handler.get_sub_price()
    subs = await core.data_handler.get_sub_list()

    if str(user_id) in subs:
        exp_date = subs[str(user_id)]['exp_date']
        new_buy_date = await core.utils.date_and_time.get_date('today')
        new_exp_date = await core.utils.date_and_time.x_days_after_date(30, exp_date)

        if await core.handlers.user_handlers.wallet_handler.spend_credit(user_id, sub_price):
            new_data = subs
            new_data[str(user_id)]['exp_date'] = new_exp_date
            new_data[str(user_id)]['buy_date'] = new_buy_date
            await core.data_handler.edit_sub(new_data)
            text = "اشتراک شما با موفقیت تمدید شد"
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("انجام شد", callback_data="none *")]])
            await query.edit_message_text(text=text, reply_markup=markup)
            await query.answer("✅")
        else:
            await query.answer("❌ موجودی کافی نیست")

    else:
        today_date = await core.utils.date_and_time.get_date('today')
        exp_date = await core.utils.date_and_time.x_days_after_date(30, today_date)

        if await core.handlers.user_handlers.wallet_handler.spend_credit(user_id, sub_price):
            new_data = subs
            new_data[str(user_id)] = {
                "exp_date": exp_date,
                "buy_date": today_date
            }
            await core.data_handler.edit_sub(new_data)
            text = "اشتراک با موفقیت خریداری شد"
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("انجام شد", callback_data="none *")]])
            await query.edit_message_text(text=text, reply_markup=markup)
            await query.answer("✅")
        else:
            await query.answer("❌ موجودی کافی نیست")
