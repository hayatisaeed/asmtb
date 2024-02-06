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
    'grade': '12',
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


async def get_all_file_bank():
    with open('data/file_bank.json', 'r') as f:
        data = json.load(f)
        return data


async def get_file_in_file_bank(message_id):
    with open('data/file_bank.json', 'r') as f:
        data = json.load(f)
    try:
        new_data = {"title": data["titles"][str(message_id)], "link": data["links"][str(message_id)]}
        return new_data

    except:
        False


async def new_file_in_bank(message_id, title, link):
    try:
        with open('data/file_bank.json', 'r') as f:
            data = json.load(f)

        data["titles"][str(message_id)] = title
        data["ids"].append(str(message_id))
        data["links"][str(message_id)] = link

        with open('data/file_bank.json', 'w') as f:
            json.dump(data, f)

        return True
    except:
        return False


async def delete_file_in_bank(message_id):
    try:
        with open('data/file_bank.json', 'r') as f:
            data = json.load(f)
        del data["titles"][str(message_id)]
        while message_id in data["ids"]:
            for i in range(0, len(data["ids"])):
                if data["ids"][i] == message_id:
                    del data["titles"][i]
                    break
        return True
    except:
        return False
