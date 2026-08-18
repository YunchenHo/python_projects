def royal_flush(hand):
    # To be implemented
    return True

def straight_flush(hand):
    # To be implemented
    return True

def four_kind(hand):
    # To be implemented
    return True

def full_house(hand):
    # To be implemented
    return True

def flush(hand):
    # To be implemented
    return True

def straight(hand):
    # To be implemented
    return True

def three_kind(hand):
    # To be implemented
    return True

def two_pairs(hand):
    # To be implemented
    return True

def one_pair(hand):
    # To be implemented
    return True

def high_card(hand):
    # To be implemented
    return True

def card_power(hand):
    card_types = [royal_flush, straight_flush, four_kind, full_house, flush,
                  straight, three_kind, two_pairs, one_pair, high_card]
    for i in range(10):
        if card_types[i](hand):
            return i
    return 10

def card_type(hand):
    # To be implemented
    return "None"

def main():
    pass

if __name__ == "__main__":
    main()