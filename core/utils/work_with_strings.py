import prettytable as pt


async def beautify_numbers(number):
    number = str(number)
    i = len(number) - 3
    while i > 0:
        number = number[:i] + ',' + number[i:]
        i -= 3

    return number


async def generate_formatted_table(data):
    table = pt.PrettyTable(data[0])

    for row in data[1:]:
        table.add_row(row)

    return table
