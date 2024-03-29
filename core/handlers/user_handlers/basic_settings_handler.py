from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import core.data_handler
import core.handlers.start_handler
import core.utils.validator


user_basic_settings_keyboard = [
    ['تنظیم نام و نام خانوادگی', 'تنظیم رشته'],
    ['تنظیم وضعیت تحصیل', 'تنظیم جنسیت'],
    ['تنظیم پایه', 'شماره تلفن'],
    ['🔙 | بازگشت به منوی اصلی']
]
user_basic_settings_markup = ReplyKeyboardMarkup(user_basic_settings_keyboard, one_time_keyboard=True)

cancel_keyboard = [['🔙 | بازگشت به منوی اصلی']]
cancel_markup = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data = await core.data_handler.get_user_data(user_id)
    message = f"""

📄 اطلاعات شما به شرح زیر میباشد:

نام: {user_data['name']}

جنسیت: {user_data['gender']}

رشته تحصیلی: {user_data['reshte']}

پایه: {user_data['grade']}

وضعیت تحصیل: {user_data['status']}

شماره تلفن: {user_data['phone_number']}

برای ویرایش اطلاعات از منوی زیر استفاده کنید:


    """
    await context.bot.send_message(chat_id=user_id, text=message, reply_markup=user_basic_settings_markup)
    return 'CHOOSING'


# Gender
gender_keyboard = [['پسر'], ['دختر'], ['🔙 | بازگشت به منوی اصلی']]
gender_markup = ReplyKeyboardMarkup(gender_keyboard, one_time_keyboard=True)


async def change_gender(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="جنسیت خود را انتخاب کنید:", reply_markup=gender_markup)
    return 'CHOOSING_GENDER'


async def save_gender(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    gender = update.message.text
    if gender in ['پسر', 'دختر']:
        user_data = await core.data_handler.get_user_data(user_id)
        user_data['gender'] = gender
        if await core.data_handler.save_user_data(user_id, user_data):
            await context.bot.send_message(chat_id=user_id, text="جنسیت با موفقیت تنظیم شد.")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ خطا در عملیات، لطفا بعدا تلاش کنید")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'

    else:
        await context.bot.send_message(chat_id=user_id, text="لطفا جنسیت خود را از منوی زیر انتخاب کنید:",
                                       reply_markup=gender_markup)
        return 'CHOOSING_GENDER'


async def wrong_gender(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="لطفا جنسیت خود را از منوی زیر انتخاب کنید:",
                                   reply_markup=gender_markup)
    return 'CHOOSING_GENDER'


# Status
status_keyboard = [['دانش آموز'], ['فارغ التحصیل'], ['🔙 | بازگشت به منوی اصلی']]
status_markup = ReplyKeyboardMarkup(status_keyboard, one_time_keyboard=True)


async def change_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="لطفا وضعیت تحصیلی خود را از این منو انتخاب کنید",
                                   reply_markup=status_markup)
    return 'CHOOSING_STATUS'


async def save_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    status = update.message.text
    if status in ['دانش آموز', 'فارغ التحصیل']:
        user_data = await core.data_handler.get_user_data(user_id)
        user_data['status'] = status
        if await core.data_handler.save_user_data(user_id, user_data):
            await context.bot.send_message(chat_id=user_id, text="وضعیت تحصیلی با موفقیت تنظیم شد.")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ خطا در عملیات، لطفا بعدا تلاش کنید")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
    else:
        await context.bot.send_message(chat_id=user_id, text="دستور اشتباه. لطفا از منوی زیر انتخاب کنید:",
                                       reply_markup=status_markup)
        return 'CHOOSING_STATUS'


async def wrong_status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="دستور اشتباه. لطفا از منوی زیر انتخاب کنید:",
                                   reply_markup=status_markup)
    return 'CHOOSING_STATUS'


# Reshte
reshte_keyboard = [['ریاضی'], ['تجربی'], ['انسانی'], ['سایر'], ['🔙 | بازگشت به منوی اصلی']]
reshte_markup = ReplyKeyboardMarkup(reshte_keyboard, one_time_keyboard=True)


async def change_reshte(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="لطفا رشته‌ی خود را انتخاب کنید:", reply_markup=reshte_markup)
    return 'CHOOSING_RESHTE'


async def save_reshte(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    reshte = update.message.text

    if reshte in ['ریاضی', 'تجربی', 'انسانی', 'سایر']:
        user_data = await core.data_handler.get_user_data(user_id)
        user_data['reshte'] = reshte
        if await core.data_handler.save_user_data(user_id, user_data):
            await context.bot.send_message(chat_id=user_id, text="رشته تحصیلی با موفقیت تنظیم شد.")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ خطا در عملیات، لطفا بعدا تلاش کنید")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
    else:
        await context.bot.send_message(chat_id=user_id, text="دستور اشتباه. لطفا از منوی زیر انتخاب کنید:",
                                       reply_markup=reshte_markup)
        return 'CHOOSING_RESHTE'


async def wrong_reshte(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="دستور اشتباه. لطفا از منوی زیر انتخاب کنید:",
                                   reply_markup=reshte_markup)
    return 'CHOOSING_RESHTE'


# Name
async def change_name(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="لطفا نام خود را ارسال کنید", reply_markup=cancel_markup)
    return 'CHOOSING_NAME'


async def save_name(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    name = update.message.text
    user_data = await core.data_handler.get_user_data(user_id)
    user_data['name'] = name

    if await core.data_handler.save_user_data(user_id, user_data):
        await context.bot.send_message(chat_id=user_id, text="نام و نام خانوادگی با موفقیت تنظیم شد")
        await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                       reply_markup=user_basic_settings_markup)
        return 'CHOOSING'
    else:
        await context.bot.send_message(chat_id=user_id, text="❌ خطا در عملیات، لطفا بعدا تلاش کنید")
        await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                       reply_markup=user_basic_settings_markup)
        return 'CHOOSING'


async def wrong_name(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="❌ خطا", reply_markup=user_basic_settings_markup)
    return 'CHOOSING'


# Invalid command
async def choose_what_to_edit(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه را انتخاب کنید:",
                                   reply_markup=user_basic_settings_markup)
    return 'CHOOSING'


# phone number
async def change_phone_number(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    keyboard = [
        ['🔙 | بازگشت به منوی اصلی']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=user_id, text="لطفا شماره تلفن خود را ارسال کنید", reply_markup=markup)
    return 'CHOOSING_PHONE'


async def save_phone_number(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    phone_number = update.message.text

    if await core.utils.validator.mobile_number_is_valid(phone_number):
        user_data = await core.data_handler.get_user_data(user_id)
        user_data['phone_number'] = phone_number
        if await core.data_handler.save_user_data(user_id, user_data):
            await context.bot.send_message(chat_id=user_id, text="شماره تلفن با موفقیت تنظیم شد")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ خطا در عملیات، لطفا بعدا تلاش کنید")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
    else:
        keyboard = [
            ['🔙 | بازگشت به منوی اصلی']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        text = """
        شماره تلفن نا معتبر است. لطفا در فرمت زیر ارسال کنید:
        09xxxxxxxxx
        """
        await context.bot.send_message(chat_id=user_id, text=text, reply_markup=markup)
        return 'CHOOSING_PHONE'


async def wrong_phone_number(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="❌ خطا", reply_markup=user_basic_settings_markup)
    return 'CHOOSING'


# Grade
async def change_grade(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    keyboard = [
        ['10', '11', '12'],
        ['🔙 | بازگشت به منوی اصلی']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=user_id, text="پایه تحصیلی خود را انتخاب کنید:", reply_markup=markup)
    return 'CHOOSING_GRADE'


async def save_grade(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    grade = update.message.text

    if grade not in ['10', '11', '12']:
        keyboard = [
            ['10', '11', '12'],
            ['🔙 | بازگشت به منوی اصلی']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await context.bot.send_message(chat_id=user_id, text="پایه تحصیلی اشتباه است. لطفا از منوی زیر انتخاب کنید:",
                                       reply_markup=markup)
        return 'CHOOSING_GRADE'
    else:
        user_data = await core.data_handler.get_user_data(user_id)
        user_data['grade'] = grade
        if await core.data_handler.save_user_data(user_id, user_data):
            await context.bot.send_message(chat_id=user_id, text="پایه تحصیلی با موفقیت تنظیم شد")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'
        else:
            await context.bot.send_message(chat_id=user_id, text="❌ خطا در عملیات، لطفا بعدا تلاش کنید")
            await context.bot.send_message(chat_id=user_id, text="لطفا از منوی زیر یک گزینه انتخاب کنید",
                                           reply_markup=user_basic_settings_markup)
            return 'CHOOSING'


async def wrong_grade(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="❌ خطا", reply_markup=user_basic_settings_markup)
    return 'CHOOSING'


# Cancel
async def return_home(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="بازگشت به منوی اصلی ...")
    await core.handlers.start_handler.handle(update, context)
    return ConversationHandler.END
