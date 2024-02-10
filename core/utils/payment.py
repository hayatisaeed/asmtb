
async def create_new_payment(price, user_id):
    payment_id = 12345
    return payment_id


async def payment_done(payment_id):
    if payment_id == 12345:
        return True
    else:
        return False
