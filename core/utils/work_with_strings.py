from tabulate import tabulate


async def beautify_numbers(number):
    number = str(number)
    i = len(number) - 3
    while i > 0:
        number = number[:i] + ',' + number[i:]
        i -= 3

    return number


async def generate_formatted_table(data):
    # Create a table with customized formatting
    table = tabulate(data, headers="firstrow", tablefmt="grid")

    # Replace the separator line after the first row with a thicker line
    table_lines = table.split("\n")
    table_lines.insert(2, "+" + "-"*8 + "+" + "-"*6 + "+" + "-"*8 + "+")

    # Find the index of the row containing "Bob"
    bob_index = next((i for i, row in enumerate(data) if "Bob" in row), None)

    if bob_index is not None:
        # Insert horizontal line after the row containing "Bob"
        table_lines.insert(bob_index + 2, "+" + "-"*8 + "+" + "-"*6 + "+" + "-"*8 + "+")

    return "\n".join(table_lines)
