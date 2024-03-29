from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import core.data_handler
import core.utils.work_with_strings
import core.utils.payment
import core.handlers.start_handler

main_wallet_keyboard = [
    ['➕ افزایش موجودی'],
    ['🔙 | بازگشت به منوی اصلی']
]
main_wallet_markup = ReplyKeyboardMarkup(main_wallet_keyboard, one_time_keyboard=True)

cancel_markup = ReplyKeyboardMarkup([['🔙 | بازگشت به منوی اصلی']], one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    wallet = await core.data_handler.get_wallet_data(user_id)

    if not wallet:
        wallet = await core.data_handler.new_wallet(user_id)
    credit = await core.utils.work_with_strings.beautify_numbers(wallet['credit'])

    text = f"""
💰 اعتبار کیف پول شما: {credit} ریال. 
    """

    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=main_wallet_markup)
    return 'CHOOSING'


async def add_credit(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = """
لطفا مبلغ مدنظر خود را وارد کنید

واحد: ریال

(لطفا اعداد لاتین وارد کنید)

    """
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=cancel_markup)
    return 'SEND_PRICE'


async def add_credit_get_price(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    price = update.message.text

    try:
        price = int(price)
        if price < 100000:
            text = """
            حداقل مقدار قابل شارژ 10 هزار تومان (معادل 100,000 ریال) میباشد.
            """
            await context.bot.send_message(chat_id=user_id, text=text, reply_markup=cancel_markup)
            return 'SEND_PRICE'
        else:
            button = [[InlineKeyboardButton('✅ تایید', callback_data=f'user-new-payment {price}')]]
            inline_keyboard = InlineKeyboardMarkup(button)
            price = await core.utils.work_with_strings.beautify_numbers(price)
            await context.bot.send_message(chat_id=user_id,
                                           text=f"آیا افزایش موجودی با مبلغ زیر مورد تایید است؟\n{price} ریال",
                                           reply_markup=inline_keyboard)
            await core.handlers.start_handler.handle(update, context)
            return ConversationHandler.END

    except ValueError:
        await context.bot.send_message(chat_id=user_id, text="عدد نامعتبر. به صورت لاتین وارد کنید",
                                       reply_markup=cancel_markup)
        return 'SEND_PRICE'


async def new_payment(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    amount = int(query.data.split()[1])
    payment_id = await core.utils.payment.create_new_payment(amount, user_id)
    payment_link = await core.utils.payment.get_payment_link(payment_id, amount)

    buttons = [
        [InlineKeyboardButton('🔗 پرداخت', url=payment_link)],
        [InlineKeyboardButton('✅ پرداخت کردم', callback_data=f'user-confirm-payment {payment_id} {amount}')]
    ]
    markup = InlineKeyboardMarkup(buttons)

    price = await core.utils.work_with_strings.beautify_numbers(amount)
    text = f"""
لطفا ابتدا VPN خود را خاموش کنید، سپس روی پرداخت بزنید.
پس از انجام پرداخت به بات برگشته و دکمه پرداخت کردم را بزنید.


price: {price} Rials
payment_id: {payment_id}
    """

    await query.edit_message_text(text=text, reply_markup=markup)
    await query.answer()


async def payment_confirmation(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    payment_id = query.data.split()[1]
    price = int(query.data.split()[2])

    payment_data = await core.data_handler.get_transaction_data(payment_id)
    payment_cleared = payment_data['cleared']
    if await core.utils.payment.payment_done(payment_id) and not payment_cleared:
        await core.data_handler.change_transaction_cleared_done(payment_id)
        current_credit = await core.data_handler.get_wallet_data(user_id)
        current_credit = current_credit['credit']

        new_credit = price + current_credit

        price_bea = await core.utils.work_with_strings.beautify_numbers(new_credit)
        button = InlineKeyboardMarkup([[InlineKeyboardButton(price_bea, callback_data=f'none {price_bea}')]])
        await query.edit_message_text(text=f"تراکنش تایید شد! موجودی جدید: {price_bea}", reply_markup=button)

        await core.data_handler.edit_wallet_credit(user_id, new_credit)
        await query.answer()
    else:
        await query.answer("❌ تراکنش تایید نشد")


async def spend_credit(user_id, price):
    credit = await core.data_handler.get_wallet_data(user_id)
    if not credit:
        return False
    credit = credit['credit']

    if price > credit:
        return False
    else:
        new_credit = credit - price
        await core.data_handler.edit_wallet_credit(user_id, new_credit)
        return True
