# in the name of Allah

import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler
)
from core.config import Config
import core.handlers.start_handler
import core.handlers.admin_handlers.general_settings_handler
import core.utils.chat_member
import core.handlers.admin_handlers.broadcast_handler
import core.handlers.admin_handlers.start_handler
import core.handlers.user_handlers.basic_settings_handler
import core.handlers.admin_handlers.uploader_handler
import core.handlers.admin_handlers.data_bank_handler
import core.handlers.user_handlers.motivation_handler
import core.handlers.admin_handlers.motivation_handler
import core.handlers.user_handlers.motivation_settings_handler
import core.handlers.user_handlers.advice_handler
import core.handlers.admin_handlers.advice_handler
import core.handlers.admin_handlers.call_handler
import core.handlers.user_handlers.call_handler
import core.handlers.user_handlers.wallet_handler
import core.handlers.admin_handlers.wallet_handler
import core.handlers.admin_handlers.sub_handler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)


TOKEN = Config.BOT_TOKEN
ADMIN_ID = Config.ADMIN_ID


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Define Handlers
    start_handler = CommandHandler('start', core.handlers.start_handler.handle)
    joined_channel_handler = CallbackQueryHandler(core.utils.chat_member.channel_lock_button_pressed,
                                                  pattern='^joined channel$')

    admin_bot_general_settings = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^⚙️ | تنظیمات کلی بات&'),
                                     core.handlers.admin_handlers.general_settings_handler.handle)],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔴 خاموش | روشن 🟢&'),
                               core.handlers.admin_handlers.general_settings_handler.change_power_status),
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.admin_handlers.general_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.general_settings_handler.unknown_command)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.admin_handlers.general_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.general_settings_handler.return_home)
        ]
    )

    admin_broadcast_message_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^📣 | ارسال اطلاعیه$'),
                           core.handlers.admin_handlers.broadcast_handler.handle)
        ],
        states={
            'SEND_MESSAGE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.admin_handlers.broadcast_handler.return_home),
                MessageHandler(filters.ALL, core.handlers.admin_handlers.broadcast_handler.do_the_broadcast)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.admin_handlers.broadcast_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.broadcast_handler.return_home)
        ]
    )

    user_basic_settings_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^تنظیمات کاربری 🔧$'),
                           core.handlers.user_handlers.basic_settings_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^تنظیم نام و نام خانوادگی$'),
                               core.handlers.user_handlers.basic_settings_handler.change_name),
                MessageHandler(filters.Regex('^تنظیم وضعیت تحصیل$'),
                               core.handlers.user_handlers.basic_settings_handler.change_status),
                MessageHandler(filters.Regex('^تنظیم جنسیت$'),
                               core.handlers.user_handlers.basic_settings_handler.change_gender),
                MessageHandler(filters.Regex('^تنظیم رشته$'),
                               core.handlers.user_handlers.basic_settings_handler.change_reshte),
                MessageHandler(filters.Regex('^تنظیم پایه$'),
                               core.handlers.user_handlers.basic_settings_handler.change_grade),
                MessageHandler(filters.Regex('^شماره تلفن$'),
                               core.handlers.user_handlers.basic_settings_handler.change_phone_number),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.choose_what_to_edit)
            ],
            'CHOOSING_GENDER': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_gender),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_gender)
            ],
            'CHOOSING_RESHTE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_reshte),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_reshte)
            ],
            'CHOOSING_STATUS': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_status),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_status)
            ],
            'CHOOSING_NAME': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_name),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_name)
            ],
            'CHOOSING_GRADE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_grade),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_grade)
            ],
            'CHOOSING_PHONE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.user_handlers.basic_settings_handler.save_phone_number),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.wrong_phone_number)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    admin_uploader_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^📤 آپلودر$'),
                                     core.handlers.admin_handlers.uploader_handler.handle)],
        states={
            'NEW_UPLOAD': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.ALL, core.handlers.admin_handlers.uploader_handler.new_file)
            ],
            'SET_TITLE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.admin_handlers.uploader_handler.set_title),
                MessageHandler(filters.ALL, core.handlers.user_handlers.basic_settings_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.uploader_handler.return_home)
        ]
    )

    data_bank_handler = MessageHandler(filters.Regex('^🏦 بانک فایل$'),
                                       core.handlers.admin_handlers.data_bank_handler.handle)

    #    # CallbackQueryHandlers (file bank)
    previous_page_handler = CallbackQueryHandler(core.handlers.admin_handlers.data_bank_handler.pre_page,
                                                 pattern="^previous-page")
    next_page_handler = CallbackQueryHandler(core.handlers.admin_handlers.data_bank_handler.next_page,
                                             pattern="^next-page")
    show_file_handler = CallbackQueryHandler(core.handlers.admin_handlers.data_bank_handler.show_file,
                                             pattern="^show-file")
    none_handler = CallbackQueryHandler(core.handlers.admin_handlers.data_bank_handler.show_none, pattern="^none")
    show_link_handler = CallbackQueryHandler(core.handlers.admin_handlers.data_bank_handler.show_link,
                                             pattern="^show-link")
    delete_file_handler = CallbackQueryHandler(core.handlers.admin_handlers.data_bank_handler.delete_file,
                                               pattern="^delete-file")
    change_motivation_status = CallbackQueryHandler(
        core.handlers.admin_handlers.data_bank_handler.change_motivation_status,
        pattern="^change-motivation-status"
    )

    admin_motivation_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^⭐ بخش انگیزشی$'),
                                     core.handlers.admin_handlers.motivation_handler.handle)],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.admin_handlers.motivation_handler.return_home),
                MessageHandler(filters.Regex('^زمان ارسال خودکار$'),
                               core.handlers.admin_handlers.motivation_handler.handle_time),
                MessageHandler(filters.Regex('^فایل‌های انگیزشی$'),
                               core.handlers.admin_handlers.motivation_handler.handle_files),
                MessageHandler(filters.ALL, core.handlers.admin_handlers.motivation_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.uploader_handler.return_home)
        ]
    )

    user_motivation_settings_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^⭐ تنظیمات انگیزشی$'),
                           core.handlers.user_handlers.motivation_settings_handler.handle),
            MessageHandler(filters.Regex('^⭐️ انگیزه بگیر!$'),
                           core.handlers.user_handlers.motivation_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^ارسال خودکار پیام انگیزشی$'),
                               core.handlers.user_handlers.motivation_settings_handler.auto_motivation)
            ],
            'AUTO_MOTIVATION': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^غیر فعال کردن ارسال خودکار$'),
                               core.handlers.user_handlers.motivation_settings_handler.remove_motivation_job_queue),
                MessageHandler(filters.Regex('^فعال کردن ارسال خودکار$'),
                               core.handlers.user_handlers.motivation_settings_handler.set_motivation_job_queue)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    user_advice_handler = MessageHandler(filters.Regex('^نکات مشاوره‌ای$'),
                                         core.handlers.user_handlers.advice_handler.handle)

    return_to_advice_key_handler = CallbackQueryHandler(
        core.handlers.user_handlers.advice_handler.return_to_advice_key,
        pattern="^return-to-advice-key$"
    )

    admin_advice_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^تنظیمات نکات مشاوره‌ای$'),
                           core.handlers.admin_handlers.advice_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^مشاهده دسته بندی‌ها$'),
                               core.handlers.admin_handlers.advice_handler.show_categories),
                MessageHandler(filters.Regex('^دسته بندی جدید$'),
                               core.handlers.admin_handlers.advice_handler.new_category),
            ],
            'GET_CATEGORY_TITLE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.advice_handler.save_new_category),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ],
            'SEND_TITLE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.advice_handler.new_message_get_file),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ],
            'SEND_FILE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.ALL,
                               core.handlers.admin_handlers.advice_handler.save_advice),
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.uploader_handler.return_home)
        ]
    )

    admin_show_advice_message_handler = CallbackQueryHandler(
        core.handlers.admin_handlers.advice_handler.admin_show_advice_message,
        pattern="^admin-show-advice-message"
    )

    user_show_advice_message_handler = CallbackQueryHandler(
        core.handlers.user_handlers.advice_handler.show_advice_message,
        pattern="^show-advice-message"
    )

    admin_show_advice_category_handler = CallbackQueryHandler(
        core.handlers.admin_handlers.advice_handler.admin_show_advice_category,
        pattern="^admin-show-advice-category"
    )

    admin_delete_advice_category_handler = CallbackQueryHandler(
        core.handlers.admin_handlers.advice_handler.delete_category,
        pattern="^admin-delete-advice-category"
    )

    admin_yes_delete_advice_category = CallbackQueryHandler(
        core.handlers.admin_handlers.advice_handler.yes_delete_category,
        pattern="^yes-delete"
    )

    admin_return_advice_categories = CallbackQueryHandler(
        core.handlers.admin_handlers.advice_handler.admin_return_advice_categories,
        pattern="^admin-return-advice-categories"
    )

    admin_delete_advice = CallbackQueryHandler(
        core.handlers.admin_handlers.advice_handler.admin_delete_advice,
        pattern="^admin-delete-advice"
    )

    data_bank_advice_handler = CallbackQueryHandler(
        core.handlers.admin_handlers.data_bank_handler.show_advice_categories,
        pattern="^data-bank-advice"
    )

    data_bank_add_advice_to_category_handler = CallbackQueryHandler(
        core.handlers.admin_handlers.data_bank_handler.add_file_to_advice_category,
        pattern="^admin-db-add-advice-to-category"
    )

    user_show_advice_list_handler = CallbackQueryHandler(
        core.handlers.user_handlers.advice_handler.show_advice_list,
        pattern="^show-advice-list"
    )

    admin_call_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^تنظیمات جلسه تلفنی$'),
                           core.handlers.admin_handlers.call_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^تنظیم هزینه$'),
                               core.handlers.admin_handlers.call_handler.set_price),
                MessageHandler(filters.Regex('^تنظیم برنامه هفتگی$'),
                               core.handlers.admin_handlers.call_handler.show_weekly_plan),
                MessageHandler(filters.Regex('^رزرو های امروز و فردا$'),
                               core.handlers.admin_handlers.call_handler.show_reservations),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ],
            'SEND_PRICE': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.call_handler.save_price),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.admin_handlers.uploader_handler.return_home)
        ]
    )

    weekly_plan_edit_day = CallbackQueryHandler(
        core.handlers.admin_handlers.call_handler.change_weekly_plan,
        pattern="^call-handler-weekly-plan-plus-one|^call-handler-weekly-plan-minus-one"
    )

    user_call_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^📞 جلسه تلفنی$'),
                           core.handlers.user_handlers.call_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^رزرو جدید$'),
                               core.handlers.user_handlers.call_handler.new_reserve),
                MessageHandler(filters.Regex('^سابقه رزروها$'),
                               core.handlers.user_handlers.call_handler.show_reserve_history),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.ALL,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    user_call_reservation_choose_day = CallbackQueryHandler(
        core.handlers.user_handlers.call_handler.new_reserve_choose_day,
        pattern="^user-call-nr"
    )

    user_call_confirm_reservation_handler = CallbackQueryHandler(
        core.handlers.user_handlers.call_handler.confirm_reservation,
        pattern="^user-call-cr"
    )

    user_wallet_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^💲 کیف پول$'),
                           core.handlers.user_handlers.wallet_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^➕ افزایش موجودی$'),
                               core.handlers.user_handlers.wallet_handler.add_credit),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ],
            'SEND_PRICE': [
                MessageHandler(filters.TEXT,
                               core.handlers.user_handlers.wallet_handler.add_credit_get_price),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    user_new_payment_handler = CallbackQueryHandler(
        core.handlers.user_handlers.wallet_handler.new_payment,
        pattern="^user-new-payment"
    )

    user_confirm_payment = CallbackQueryHandler(
        core.handlers.user_handlers.wallet_handler.payment_confirmation,
        pattern="^user-confirm-payment"
    )

    admin_wallet_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^کیف پول کاربران$'),
                           core.handlers.admin_handlers.wallet_handler.handle)
        ],
        states={
            'SEND_USER_ID': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.wallet_handler.show_wallet),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ],
            'SEND_NEW_CREDIT': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.wallet_handler.change_credit),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.ALL,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    admin_show_reservations = CallbackQueryHandler(
        core.handlers.admin_handlers.call_handler.display_reservations,
        pattern="^admin-show-res"
    )

    admin_show_reservation_details = CallbackQueryHandler(
        core.handlers.admin_handlers.call_handler.display_reservation_details,
        pattern="^admin-show-det"
    )

    admin_manage_sub_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^تنظیمات اشتراک&'),
                           core.handlers.admin_handlers.sub_handler.handle)
        ],
        states={
            'CHOOSING': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.Regex('^نمایش لیست مشترکان&'),
                               core.handlers.admin_handlers.sub_handler.show_sub_list),
                MessageHandler(filters.Regex('^رایگان کردن کاربر&'),
                               core.handlers.admin_handlers.sub_handler.make_user_free),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ],
            'FREE_GET_ID': [
                MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                               core.handlers.user_handlers.basic_settings_handler.return_home),
                MessageHandler(filters.TEXT,
                               core.handlers.admin_handlers.sub_handler.make_user_free_show_status),
                MessageHandler(filters.ALL,
                               core.handlers.user_handlers.basic_settings_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^🔙 | بازگشت به منوی اصلی$'),
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.COMMAND,
                           core.handlers.user_handlers.basic_settings_handler.return_home),
            MessageHandler(filters.ALL,
                           core.handlers.user_handlers.basic_settings_handler.return_home)
        ]
    )

    admin_change_free_status = CallbackQueryHandler(
        core.handlers.admin_handlers.sub_handler.change_user_free_status,
        pattern="^change-free-status"
    )

    handlers = [
        start_handler, joined_channel_handler, admin_bot_general_settings, admin_broadcast_message_handler,
        user_basic_settings_handler, admin_uploader_handler, data_bank_handler, previous_page_handler,
        show_file_handler, none_handler, show_link_handler, delete_file_handler, change_motivation_status,
        admin_motivation_handler, user_motivation_settings_handler, user_advice_handler, return_to_advice_key_handler,
        admin_advice_handler, admin_show_advice_message_handler, admin_show_advice_category_handler, next_page_handler,
        admin_delete_advice_category_handler, admin_yes_delete_advice_category, admin_return_advice_categories,
        admin_delete_advice, data_bank_advice_handler, data_bank_add_advice_to_category_handler, admin_call_handler,
        user_show_advice_list_handler, user_show_advice_message_handler, weekly_plan_edit_day, user_call_handler,
        user_call_reservation_choose_day, user_call_confirm_reservation_handler, user_wallet_handler,
        user_new_payment_handler, user_confirm_payment, admin_wallet_handler, admin_show_reservations,
        admin_show_reservation_details, admin_manage_sub_handler, admin_change_free_status
    ]

    # Add Handlers To Application
    for handler in handlers:
        application.add_handler(handler)

    # Run Application Forever
    application.run_polling()


if __name__ == '__main__':
    print('-- Bot started and running ... --')
    main()
