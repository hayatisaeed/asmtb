import datetime


async def get_date(day):  # day must be today or tomorrow
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if day == 'today':
        return f"{today.year}-{today.month}-{today.day}"
    else:
        return f"{tomorrow.year}-{tomorrow.month}-{tomorrow.day}"


async def get_day_name(day):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    today_name = today.strftime("%A")[:3]
    tomorrow_name = tomorrow.strftime('%A')[:3]

    if day == 'today':
        return f"{today_name}"
    elif day == 'tomorrow':
        return f"{tomorrow_name}"


async def calculate_age_in_days(date_string):
    birth_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    today_date = datetime.datetime.now()
    age_delta = today_date - birth_date
    return age_delta.days