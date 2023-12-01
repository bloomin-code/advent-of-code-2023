TEXT_NUMBERS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def process_line(line):
    # Look fowards to find number
    for i in range(len(line)):
        if line[i].isdigit():
            first = line[i]
            break
        for texual_name, numeric_value in TEXT_NUMBERS.items():
            if line[i:].startswith(texual_name):
                first = numeric_value
                break
        else: # nobreak
            continue
        break
    # Look backwards to find number
    for i in range(len(line), 0, -1):
        if line[i - 1].isdigit():
            last = line[i - 1]
            break
        for texual_name, numeric_value in TEXT_NUMBERS.items():
            if line[:i].endswith(texual_name):
                last = numeric_value
                break
        else:
            continue
        break
    return int(f'{first}{last}')

def main():
    total = 0
    with open('input.txt') as file:
        for line in file:
            total += process_line(line)

    print(f'part 2: {total}')


if __name__ == '__main__':
    main()