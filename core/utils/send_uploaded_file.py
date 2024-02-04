import base64
from core.config import Config
import core.handlers.start_handler


async def send(update, context, user_id, code):
    decoded_bytes = base64.b64decode(code.encode())
    message_id = int(decoded_bytes.decode())
    try:
        await context.bot.copy_message(chat_id=user_id, from_chat_id=Config.ADMIN_ID, message_id=message_id)
    except:
        await context.bot.send_message(chat_id=user_id, text="فایل یافت نشد؛ احتمالا حذف شده یا تغییر پیدا کرده.")

    await core.handlers.start_handler.handle(update, context)

