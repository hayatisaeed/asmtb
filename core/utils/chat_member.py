
async def chat_member_status(context, user_id, channel_id):
    membership_status = await context.bot.get_chat_member(channel_id, user_id)
    membership_status = membership_status['status'].lower()
    return membership_status


async def user_joined_channel(context, user_id, channel_id):
    membership_status = await context.bot.get_chat_member(channel_id, user_id)
    membership_status = membership_status['status'].lower()
    if membership_status == 'member' or membership_status == 'administrator' or membership_status == 'creator':
        return True
    else:
        return False
