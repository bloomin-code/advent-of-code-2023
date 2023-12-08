#!/usr/bin/env python

from collections import namedtuple
from itertools import cycle
import fileinput

Node = namedtuple('Node', ['left', 'right'])

def main():
    with fileinput.input() as lines:
        directions = next(lines).strip()
        next(lines)
        mapper = {}
        for line in lines:
            label, node_parts = line.strip().split(' = ')
            left, right = node_parts[1:-1].split(', ')
            mapper[label] = Node(left, right)
    current_node = 'AAA'
    looping_directions = cycle(directions)
    total = 0
    while current_node != 'ZZZ':
        total += 1
        if next(looping_directions) == 'L':
            current_node = mapper[current_node].left
        else:
            current_node = mapper[current_node].right
    print(f'Part 1: {total}')

    
if __name__ == '__main__':
    main()