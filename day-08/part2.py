#!/usr/bin/env python

from collections import namedtuple
from itertools import cycle
from math import lcm
import fileinput

Node = namedtuple('Node', ['left', 'right'])

def find_cycle(label, nodes, directions):
    looping_directions = cycle(directions)
    current_node = label
    total = 0
    while not current_node.endswith('Z'):
        total += 1
        if next(looping_directions) == 'L':
            current_node = nodes[current_node].left
        else:
            current_node = nodes[current_node].right
    return total

def main():
    with fileinput.input() as lines:
        directions = next(lines).strip()
        next(lines)
        nodes = {}
        for line in lines:
            label, node_parts = line.strip().split(' = ')
            left, right = node_parts[1:-1].split(', ')
            nodes[label] = Node(left, right)
    cycle_counts = [
        find_cycle(label, nodes, directions)
        for label in nodes.keys()
        if label.endswith('A')
    ]
    total_cycles = lcm(*cycle_counts)
    print(f'Part 2: {total_cycles}')


if __name__ == '__main__':
    main()