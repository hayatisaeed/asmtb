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
    'status': 'تعیین نشده',
    'auto_motivation': 0
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
        return False


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
        del data["links"][str(message_id)]
        while message_id in data["ids"]:
            for i in range(0, len(data["ids"])):
                if data["ids"][i] == message_id:
                    del data["ids"][i]
                    break
        with open('data/file_bank.json', 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False


async def get_motivation_messages():
    try:
        with open('data/motivation.json', 'r') as f:
            data = json.load(f)
            if len(data["ids"]):
                return data["ids"]
            else:
                return False
    except:
        return False


async def file_in_motivation(message_id):
    with open('data/motivation.json', 'r') as f:
        data = json.load(f)
    if message_id in data["ids"]:
        return True
    else:
        return False


async def add_motivation_message(message_id):
    with open('data/motivation.json', 'r') as f:
        data = json.load(f)

    data["ids"].append(message_id)
    with open('data/motivation.json', 'w') as f:
        json.dump(data, f)


async def delete_from_motivation(message_id):
    with open('data/motivation.json', 'r') as f:
        data = json.load(f)

    while message_id in data["ids"]:
        for i in range(0, len(data["ids"])):
            if data["ids"][i] == message_id:
                del data["ids"][i]

    with open('data/motivation.json', 'w') as f:
        json.dump(data, f)


async def get_all_advice():
    with open('data/advice.json', 'r') as f:
        data = json.load(f)
        return data


async def new_advice_category(title, category_hash):
    with open('data/advice.json', 'r') as f:
        data = json.load(f)

    data[str(category_hash)] = {f"{category_hash}": f"{title}"}

    with open('data/advice.json', 'w') as f:
        json.dump(data, f)


async def new_advice(key, title, message_id):
    with open('data/advice.json', 'r') as f:
        data = json.load(f)

    data[str(key)][str(message_id)] = str(title)

    with open('data/advice.json', 'w') as f:
        json.dump(data, f)


async def delete_advice_category(category_hash):
    with open('data/advice.json', 'r') as f:
        data = json.load(f)

    if category_hash in data:
        del data[category_hash]
        with open('data/advice.json', 'w') as f:
            json.dump(data, f)


async def delete_advice(category_hash, advice):
    with open('data/advice.json', 'r') as f:
        data = json.load(f)

    del data[category_hash][advice]

    with open('data/advice.json', 'w') as f:
        json.dump(data, f)
