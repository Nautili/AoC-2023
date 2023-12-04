import sys

def get_matches(card):
    card_numbers, winning_numbers = card.split('|')
    card_numbers = set(card_numbers.split()[2:])
    winning_numbers = winning_numbers.split()

    return len(set(winning_numbers).intersection(card_numbers))
    
def get_points(card):
    matches = get_matches(card)
    if matches:
        return 2 ** (matches - 1)
    return 0

def get_total_points(cards):
    return sum(get_points(card) for card in cards)

def get_card_count(cards):
    matches = [get_matches(card) for card in cards]
    card_count = [1] * len(cards)

    for i in range(len(cards)):
        for j in range(1, matches[i] + 1):
            card_count[i + j] += card_count[i]

    return sum(card_count)

def main():
    with open(sys.argv[1]) as f:
        lines = [line.strip() for line in f.readlines()]
    
    print(get_total_points(lines))
    print(get_card_count(lines))

if __name__ == '__main__':
    main()
