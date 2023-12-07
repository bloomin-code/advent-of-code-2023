from collections import defaultdict
from functools import total_ordering
from enum import Enum
import fileinput

CARD_ORDERING = {k: v for v, k in enumerate('23456789TJQKA')}

class CardType(Enum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1

@total_ordering
class Hand:
    def __init__(self, hand):
        self.hand = hand

    def __str__(self):
        return f'Hand({self.hand})'

    def card_type(self):
        card_counts = defaultdict(int)
        for card in self.hand:
            card_counts[card] += 1
        max_count = max(card_counts.values())
        total_card_kinds = len(card_counts)
        match (max_count, total_card_kinds):
            case (5, 1):
                return CardType.FiveOfAKind
            case (4, 2):
                return CardType.FourOfAKind
            case (3, 2):
                return CardType.FullHouse
            case (3, 3):
                return CardType.ThreeOfAKind
            case (2, 3):
                return CardType.TwoPair
            case (2, 4):
                return CardType.OnePair
            case (1, 5):
                return CardType.HighCard
            case _:
                raise Exception("Impossible hand")

    def __lt__(self, other):
        self_type = self.card_type().value
        other_type = other.card_type().value
        if self_type == other_type:
            for s, o in zip(self.hand, other.hand):
                s_ord, o_ord = CARD_ORDERING[s], CARD_ORDERING[o]
                if s_ord != o_ord:
                    return s_ord < o_ord
            return False
        else:
            return self_type < other_type
    
    def __eq__(self, other):
        return self.hand == other.hand

@total_ordering
class Round:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid

    def __str__(self):
        return f'Round({self.hand}, {self.bid})'

    def __lt__(self, other):
        return self.hand < other.hand

    def __eq__(self, other):
        return self.hand == other.hand

def parseRound(line):
    hand, bid = line.strip().split(' ')
    return Round(Hand(hand), int(bid))

def main():
    rounds = [parseRound(line) for line in fileinput.input()]
    rounds.sort()
    total = 0
    for i, r in enumerate(rounds):
        total += (i + 1) * r.bid
    print(f'Part 1: {total}')


if __name__ == '__main__':
    main()