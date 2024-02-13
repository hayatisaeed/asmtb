import core.data_handler
import core.utils.date_and_time


async def user_is_authenticated(user_id):
    bot_is_free = await core.data_handler.get_bot_is_free()

    user_is_free = await core.data_handler.user_is_free_sub(user_id)

    subs = await core.data_handler.get_sub_list()
    user_has_sub = str(user_id) in subs and await core.utils.date_and_time.calculate_age_in_days(
        subs[str(user_id)]["exp_date"]) <= 0

    if bot_is_free or user_is_free:
        return True
    elif user_has_sub:
        return True
    else:
        return False
