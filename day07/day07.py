import sys
from collections import Counter
from functools import cmp_to_key

def cmp(a, b):
    return (a > b) - (a < b)

def get_type(hand):
    card_count = Counter(hand)
    return [count for _, count in card_count.most_common()]

def get_joker_type(hand):
    card_count = Counter(hand)
    joker_count = card_count['J']
    del card_count['J']
    counts = [count for _, count in card_count.most_common()]
    if not counts:
        counts = [0]
    counts[0] += joker_count 
    return counts

def card_to_rank(card):
    return '23456789TJQKA'.index(card)

def card_to_joker_rank(card):
    return 'J23456789TQKA'.index(card)

def compare_hands(hand1, hand2, type_cmp, rank_cmp):
    type1 = type_cmp(hand1)
    type2 = type_cmp(hand2)

    if cmp(type1, type2):
        return cmp(type1, type2)

    # fallthrough
    ranks1 = [rank_cmp(card) for card in hand1]
    ranks2 = [rank_cmp(card) for card in hand2]
    return cmp(ranks1, ranks2)

def get_winnings(hands):
    return sum(rank * hand[1] for rank, hand in enumerate(hands, 1)) 

def main():
    with open(sys.argv[1]) as f:
        hands = [(hand, int(bid)) for hand, bid in [line.strip().split() for line in f.readlines()]]

    # part 1
    sorted_hands = sorted(hands, key=cmp_to_key(lambda h1, h2: \
                                                 compare_hands(h1[0],
                                                               h2[0],
                                                               get_type,
                                                               card_to_rank)))
    print(get_winnings(sorted_hands))

    # part 2
    sorted_hands = sorted(hands, key=cmp_to_key(lambda h1, h2: \
                                                 compare_hands(h1[0],
                                                               h2[0],
                                                               get_joker_type,
                                                               card_to_joker_rank)))
    print(get_winnings(sorted_hands))

if __name__ == '__main__':
    main()
