#!/usr/bin/env python

from collections import deque
from itertools import islice
import fileinput

def sliding_window(iterable, n):
    """ sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG """
    it = iter(iterable)
    # fill window with the first n - 1 elements
    window = deque(islice(it, n - 1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)

def extrapolate_forward(data):
    if all(i == 0 for i in data):
        return 0
    new_data = [b - a for a, b in sliding_window(data, 2)]
    return data[-1] + extrapolate_forward(new_data)

def extrapolate_backward(data):
    if all(i == 0 for i in data):
        return 0
    new_data = [b - a for a, b in sliding_window(data, 2)]
    return data[0] - extrapolate_backward(new_data)

def main():
    with fileinput.input() as lines:
        data = [ [ int(i) for i in line.strip().split(' ') ] for line in lines ]
    part1 = sum(extrapolate_forward(i) for i in data)
    print(f'Part 1: {part1}')
    part2 = sum(extrapolate_backward(i) for i in data)
    print(f'Part 2: {part2}')

if __name__ == '__main__':
    main()
