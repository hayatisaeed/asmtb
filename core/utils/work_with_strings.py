
async def beautify_numbers(number):
    number = str(number)
    i = len(number) - 3
    while i > 0:
        number = number[:i] + ',' + number[i:]
        i -= 3

    return number
