import datetime
import core.data_handler
import core.utils.date_and_time
import core.utils.hash_funcs


async def create_new_payment(amount, user_id):
    amount = amount // 10
    now = await core.utils.date_and_time.get_exact_date_and_time()
    payment_id = await core.utils.hash_funcs.truncated_md5(now + str(user_id) + str(amount))
    await core.data_handler.new_payment(payment_id, user_id, amount, now)
    return payment_id


async def get_payment_link(payment_id, amount):
    amount = amount // 10
    return 'http://103.75.197.206:5000/new_payment?paymentId={}&amount={}'.format(payment_id, amount)


async def payment_done(payment_id):
    transaction_data = await core.data_handler.get_transaction_data(payment_id)
    if transaction_data["transaction_done"]:
        return True
    else:
        return False
