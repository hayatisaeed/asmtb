
async def create_new_payment(price, user_id):
    payment_id = 12345
    return payment_id


async def get_payment_link(payment_id):
    return 'https://www.google.com'


async def payment_done(payment_id):
    if payment_id == 12345:
        return True
    else:
        return False
