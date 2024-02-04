import json


async def user_is_saved(user_id):
    with open('data/user_data.json', 'r') as f:
        data = json.load(f)

    try:
        data = data[str(user_id)]
        return True
    except KeyError:
        return False


TEMPLATE_USER_DATA = {
    'name': 'تعیین نشده',
    'gender': 'تعیین نشده',
    'grade': 'تعیین نشده',
    'reshte': 'تعیین نشده',
    'status': 'تعیین نشده'
}


async def save_user(user_id):
    with open('data/user_data.json', 'r') as f:
        data = json.load(f)
    data[str(user_id)] = TEMPLATE_USER_DATA
    with open('data/user_data.json', 'w') as f:
        json.dump(data, f)


async def get_user_data(user_id):
    with open('data/user_data.json', 'r') as f:
        data = json.load(f)
        return data[str(user_id)]


async def save_user_data(user_id, user_data):
    try:
        with open('data/user_data.json', 'r') as f:
            data = json.load(f)

        data[str(user_id)] = user_data

        with open('data/user_data.json', 'w') as f:
            json.dump(data, f)

        return True

    except:
        return False


async def get_all_user_data():
    with open('data/user_data.json', 'r') as f:
        data = json.load(f)

    result = []
    for i in data:
        result.append(i)

    return result
