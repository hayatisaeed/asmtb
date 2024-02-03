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
    'first_name': '',
    'last_name': '',
    'gender': 'پسر',
    'grade': '12',
    'reshte': 'ریاضی',
    'status': 'محصل'
}


async def save_user(user_id):
    with open('data/user_data.json', 'r') as f:
        data = json.load(f)
    data[str(user_id)] = TEMPLATE_USER_DATA
    with open('data/user_data.json', 'w') as f:
        json.dump(data, f)


async def get_all_user_data():
    with open('data/user_data.json', 'r') as f:
        data = json.load(f)

    result = []
    for i in data:
        result.append(i)

    return result
