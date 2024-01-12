from itertools import combinations

def generate_combinations(cards, number):
        real_sequences = []
        total_sequences = combinations(cards, number)
        for sequence in total_sequences:
            sequence = list(sequence)
            real_sequences.append(sequence)
        return real_sequences

def player_menu():
    print("Ação:")
    print("1 - Aumentar a aposta")
    print("2 - Call")
    print("3 - Fold")
    print("4 - Check")
    print("5 - AllIn")
    
def menu():
    print("Poker Texas Hold'em")
    print("1 - Iniciar")
    print("2 - Sair")
        
def verify_royal_flush(sequence):
    royal_flush = [10, 11, 12, 13, 14]
    if sequence == royal_flush:
        return True
    return False

def verify_straight_flush(sequence):
    straight_flush = [[2,3,4,5,6], [3,4,5,6,7], [4,5,6,7,8], [5,6,7,8,9], [6,7,8,9,10], [7,8,9,10,11], [8,9,10,11,12], [9,10,11,12,13]]
    for sequence_ in straight_flush:
        if sequence == sequence_:
            return True
    return False   

def generate_all_combinations(hearts, spades, diamonds, clubs, number):
    hearts_cards = generate_combinations(hearts,number)
    spades_cards = generate_combinations(spades,number)
    diamonds_cards = generate_combinations(diamonds,number)
    clubs_cards = generate_combinations(clubs,number)
      
    total_sequences = hearts_cards + spades_cards +  diamonds_cards + clubs_cards
      
      
    return total_sequences

def separate_cards_by_suit(hearts, spades, diamonds, clubs, cards):
  for card in cards:
        if card.suit_getter() == "♡":
            hearts.append(card.value_getter())
        elif card.suit_getter() == "♠":
            spades.append(card.value_getter())
        elif card.suit_getter == "♢":
            diamonds.append(card.value_getter())
        else:
            clubs.append(card.value_getter())

def separate_cards_by_number(two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, cards):
    for card in cards:
        if card.value_getter() == 2:
            two.append(2)
        elif card.value_getter() == 3:
            three.append(3)
        elif card.value_getter() == 4:
            four.append(4)
        elif card.value_getter() == 5:
            five.append(5)
        elif card.value_getter() == 6:
            six.append(6)
        elif card.value_getter() == 7:
            seven.append(7)
        elif card.value_getter() == 8:
            eight.append(8)
        elif card.value_getter() == 9:
            nine.append(9)
        elif card.value_getter() == 10:
            ten.append(10)
        elif card.value_getter() == 11:
            eleven.append(11)
        elif card.value_getter() == 12:
            twelve.append(12)
        elif card.value_getter() == 13:
            thirteen.append(13)
        else:
            fourteen.append(14)  

def verify_four(two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen):
    if len(fourteen) == 4:
        return 14
    elif len(thirteen) == 4:
        return 13
    elif len(twelve) == 4:
        return 12
    elif len(eleven) == 4:
        return 11
    elif len(ten) == 4:
        return 10
    elif len(nine) == 4:
        return 9
    elif len(eight) == 4:
        return 8
    elif len(seven) == 4:
        return 7
    elif len(six) == 4:
        return 6
    elif len(five) == 4:
        return 5
    elif len(four) == 4:
        return 4
    elif len(three) == 4:
        return 3
    elif len(two) == 4:
        return 2
    else:
        return 0      
def big_flush(sequences):
    
    bigger_value = 0
    bigger_sequence = []
    
    if(len(sequences) == 0):
        return 0
    elif(len(sequences) == 1):
        return sequences[0][4]
    else:
        for sequence in sequences:
            if sequence[4] > bigger_value:
                bigger_sequence = sequence
                bigger_value = sequence[4]
        return bigger_value
        
        