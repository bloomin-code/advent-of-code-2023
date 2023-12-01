
def main():
    total = 0
    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            numbers = [c for c in line if c.isdigit()]
            d1 = numbers[0]
            d2 = numbers[-1]
            total += int(f'{d1}{d2}')

    print(f'part 1: {total}')


if __name__ == '__main__':
    main()