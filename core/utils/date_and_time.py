import datetime


async def get_date(day="today"):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if day == 'today':
        return f"{today.year}-{today.month}-{today.day}"
    else:
        return f"{tomorrow.year}-{tomorrow.month}-{tomorrow.day}"
