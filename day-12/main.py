#!/usr/bin/env python
from functools import cache
from collections import namedtuple
import fileinput

Record = namedtuple('Record', ['conditions', 'damaged'])

def intersperse(sep, items):
    it = iter(items)
    yield next(it)
    for ele in it:
        yield sep
        yield ele

def check_damaged(record, cond_idx=0, damaged_idx=0, damaged_size=0):
    damaged = [int(i) for i in record.damaged.split(',')]
    if damaged_idx < len(damaged) and damaged_size < damaged[damaged_idx]:
        return check_variants(record, cond_idx + 1, damaged_idx, damaged_size + 1)
    else:
        return 0
    
def check_operational(record, cond_idx=0, damaged_idx=0, damaged_size=0):
    damaged = [int(i) for i in record.damaged.split(',')]
    if damaged_idx >= len(damaged) or damaged_size == damaged[damaged_idx]:
        return check_variants(record, cond_idx + 1, damaged_idx + 1, 0)
    elif damaged_size == 0:
        return check_variants(record, cond_idx + 1, damaged_idx, 0)
    else:
        return 0

@cache
def check_variants(record, cond_idx=0, damaged_idx=0, damaged_size=0):
    damaged = [int(i) for i in record.damaged.split(',')]
    if cond_idx == len(record.conditions):
        if (damaged_idx >= len(damaged) and damaged_size == 0) or (damaged_idx == len(damaged) - 1 and damaged_size == damaged[damaged_idx]):
            return 1
        else:
            return 0
    match record.conditions[cond_idx]:
        case '#':
            return check_damaged(record, cond_idx, damaged_idx, damaged_size)
        case '.':
            return check_operational(record, cond_idx, damaged_idx, damaged_size)
        case '?':
            first = check_damaged(record, cond_idx, damaged_idx, damaged_size)
            second = check_operational(record, cond_idx, damaged_idx, damaged_size)
            return first + second

def part1(records):
    total = sum(check_variants(record) for record in records)
    print(f'Part 1: {total}')

def part2(records):
    new_records = []
    for record in records:
        conditions = ''.join(intersperse('?', [record.conditions] * 5))
        damaged = ','.join([record.damaged] * 5)
        new_records.append(Record(conditions, damaged))
    total = sum(check_variants(record) for record in new_records)
    print(f'Part 2: {total}')


if __name__ == '__main__':
    records = []
    with fileinput.input() as lines:
        for line in lines:
            conditions, damaged = line.strip().split(' ')
            records.append(Record(conditions, damaged))
    part1(records)
    part2(records)