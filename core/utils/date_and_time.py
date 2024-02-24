import datetime


async def get_date(day):  # day must be today or tomorrow
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if day == 'today':
        date = f"{today.year}-{today.month}-{today.day}"
        month_str = date.split('-')[1]
        if len(month_str) == 1:
            month_str = '0' + month_str
        day_str = date.split('-')[2]
        if len(day_str) == 1:
            day_str = '0' + day_str
        date = f"{date.split('-')[0]}-{month_str}-{day_str}"
    else:
        date = f"{tomorrow.year}-{tomorrow.month}-{tomorrow.day}"
        month_str = date.split('-')[1]
        if len(month_str) == 1:
            month_str = '0' + month_str
        day_str = date.split('-')[2]
        if len(day_str) == 1:
            day_str = '0' + day_str
        date = f"{date.split('-')[0]}-{month_str}-{day_str}"

    return date


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


async def x_days_after_date(x: int, date_string: str):
    day = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    x_days_after = day + datetime.timedelta(days=x)
    return f"{x_days_after.year}-{x_days_after.month}-{x_days_after.day}"


async def get_exact_date_and_time():
    now = datetime.datetime.now()
    return f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
