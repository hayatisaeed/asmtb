import re


async def mobile_number_is_valid(phone_number):
    mobile_pattern = "^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$"
    if re.search(mobile_pattern, phone_number):
        return True
    return False
