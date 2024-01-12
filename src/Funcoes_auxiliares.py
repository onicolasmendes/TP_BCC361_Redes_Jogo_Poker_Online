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

def big_straight_flush(sequences):
    
    bigger_value = 0
    bigger_sequence = []
    
    if(len(sequences) == 0):
        return []
    elif(len(sequences) == 1):
        return sequences[0][4]
    else:
        for sequence in sequences:
            if sequence[4] > bigger_value:
                bigger_sequence = sequence
                bigger_value = sequence[4]
        return bigger_value
        
        