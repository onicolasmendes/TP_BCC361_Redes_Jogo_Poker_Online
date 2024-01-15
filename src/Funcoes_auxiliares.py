from itertools import combinations
from collections import Counter

def generate_combinations(cards, number):
        real_sequences = []
        total_sequences = combinations(cards, number)
        for sequence in total_sequences:
            sequence = list(sequence)
            real_sequences.append(sequence)
        return real_sequences
        
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
        elif card.suit_getter() == "♢":
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
    
def iniciate_list_zero(number):
    sequence = []
    for i in range(number):
        sequence.append(0)
    return sequence

def counting_double_triple(sequence):
    doubles = 0
    triples = 0
    
    for i in sequence:
        if (i == 2):
            doubles = doubles + 1
        elif (i == 3):
            triples = triples + 1
    
    return doubles, triples

def verify_full_house(doubles, triples):
    if doubles == 1 and triples == 1:
        return True
    else:
        return False

def verify_straight(frequency):
    count = 0
    for i in frequency:
        if (i != 0):
            count += 1
        else:
            count = 0
    
        if count == 5:
            return True
    return False
    
def verify_triple(triples):
    if triples == 1:
        return True
    else:
        return False

def verify_two_doubles(doubles):
    if doubles == 2:
        return True
    else:
        return False

def verify_double(doubles):
    if doubles == 1:
        return True
    else:
        return False
       
def verify_double_triple(sequence):
    
    
    
    frequency = iniciate_list_zero(13)
    
    for i in sequence:
        if (i == 2):
            frequency[0] += 1
        elif (i == 3):
            frequency[1] += 1
        elif (i == 4):
            frequency[2] += 1
        elif (i == 5):
            frequency[3] += 1
        elif (i == 6):
            frequency[4] += 1
        elif (i == 7):
            frequency[5] += 1
        elif (i == 8):
            frequency[6] += 1
        elif (i == 9):
            frequency[7] += 1
        elif (i == 10):
            frequency[8] += 1
        elif (i == 11):
            frequency[9] += 1
        elif (i == 12):
            frequency[10] += 1
        elif (i == 13):
            frequency[11] += 1
        else:
            frequency[12] += 1
    
    return frequency

def big_triple_or_pair(sequences):
    if len(sequences) == 0:
        return 0
    higher_value = 0
    
    for sequence in sequences:
        contagem = Counter(sequence)
        triple_value = max(contagem, key=contagem.get)
        if(triple_value > higher_value):
            higher_value = triple_value
    
    return higher_value 
 
def big_sequence(sequences):
    
    bigger_value = 0
    
    if(len(sequences) == 0):
        return 0
    elif(len(sequences) == 1):
        return sequences[0][4]
    else:
        for sequence in sequences:
            if sequence[4] > bigger_value:
                bigger_value = sequence[4]
        return bigger_value

def verify_highest_card(game_cards):
    game_cards = sorted(game_cards, key=lambda card : card.value_getter())

    return game_cards[6].value_getter()
         