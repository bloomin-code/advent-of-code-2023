#!/usr/bin/env python

from itertools import combinations
import fileinput

def make_row_offsets(obs, size=1):
    count = 0
    for row in obs:
        if all(ob == '.' for ob in row):
            count += size
        yield count

def make_col_offsets(obs, size=1):
    count = 0
    for col in range(len(obs[0])):
        if all(row[col] == '.' for row in obs):
            count += size
        yield count

def indexed_iter(iter):
    for i, row in enumerate(iter):
        for j, item in enumerate(row):
            yield (i, j, item)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def part1(observations):
    row_offsets = list(make_row_offsets(observations))
    col_offsets = list(make_col_offsets(observations))

    galaxies = []
    for row, col, obs in indexed_iter(observations):
        if obs == '#':
            galaxies.append((
                row_offsets[row] + row,
                col_offsets[col] + col
            ))
    total = sum([manhattan(a, b) for a, b in combinations(galaxies, 2)])
    print(f'Part 1: {total}')

def part2(observations):
    row_offsets = list(make_row_offsets(observations, 999_999))
    col_offsets = list(make_col_offsets(observations, 999_999))

    galaxies = []
    for row, col, obs in indexed_iter(observations):
        if obs == '#':
            galaxies.append((
                row_offsets[row] + row,
                col_offsets[col] + col
            ))
    total = sum([manhattan(a, b) for a, b in combinations(galaxies, 2)])
    print(f'Part 2: {total}')


if __name__ == '__main__':
    with fileinput.input() as lines:
        observations = list(line.strip() for line in lines)
    part1(observations)
    part2(observations)
