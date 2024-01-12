from Deck import Deck
from Card import Card
from Jogador import Jogador
from Funcoes_auxiliares import separate_cards_by_suit, separate_cards_by_number, verify_straight_flush, generate_combinations, generate_all_combinations, verify_royal_flush, big_flush, verify_four
import time

class Jogo:
    def __init__(self):
        self._jogadores = []
        self._deck = Deck()
        self._current_value = 0
        self._total = 0
        self._table_cards = []
        self._check_bets = True
        
    def print_table(self):
        print("Cartas na mesa:\n")
        for card in self._table_cards:
            print(card+"\n")
        
    def distribute_cards(self):
        self._deck.shuffle()
        
        for jogador in self._jogadores:
            for i in range(2):
                jogador.cards_push(self._deck.pop())
                
    def raise_current_value(self, value):
        self._current_value = value
    
    def remove_folds(self):
        for jogador in self._jogadores:
            if jogador.fold_getter() == True:
                self._jogadores.pop()
    
    def initial_players(self, qtd, chips):
        for i in range(qtd):   
            name = input(print("Digite o nome do jogador "+ qtd+":"))
            self._jogadores.append(Jogador(name, chips))
            
    def print_line():
        i = 0
        while(i < 70):
            print("=")
            i += 1
        print("\n")
        
    
    
    
    def poker_sequences(self, player_cards):
        
        cards = self._table_cards + player_cards
        
        hearts, spades, diamonds, clubs = [], [], [], []
        
        separate_cards_by_suit(hearts, spades, diamonds, clubs, cards)
        
        two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen = [], [], [], [], [], [], [], [], [], [], [], [], []
        
        separate_cards_by_number(two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, cards)
                
        sequences_weights = {
            "Royal Flush": 10,
            "Straight Flush": 9,
            "Quadra": 8,
            "Full House": 7,
            "Flush": 6,
            "Straight": 5,
            "Trinca": 4,
            "Dois Pares": 3,
            "Par": 2,
            "Carta mais alta": 1
        }
        
        if len(hearts) >= 5 or len(spades) >= 5 or len(diamonds) >= 5 or len(clubs) >= 5:
            
            total_sequences = generate_all_combinations(hearts, spades, diamonds, clubs, 5)
            
            #Royal Flush
            for sequence in total_sequences:
                sequence.sort()
                if verify_royal_flush(sequence):
                    return sequences_weights["Royal Flush"]
                
            #Straight Flush
            potentials_straight_flush = []
            
            for sequence in total_sequences:
                if verify_straight_flush(sequence):
                    potentials_straight_flush.append(sequence)
            
            sequence_value = 0  
            sequence_value = big_flush(potentials_straight_flush)          
            if(sequence_value != 0):
                return sequences_weights["Straight Flush"] * sequence_value
                
            #Flush
            sequence_value = big_flush(total_sequences)
            return sequences_weights["Flush"] * sequence_value 
        elif len(two) == 4 or len(three) == 4 or len(four) == 4 or len(five) == 4 or len(six) == 4 or len(seven) == 4 or len(eight) == 4 or len(nine) == 4 or len(ten) == 4 or len(eleven) == 4 or len(twelve) == 4 or len(thirteen) == 4 or len(fourteen) == 4:
            #Four
            sequence_value = 0
            
            sequence_value = verify_four(two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen)
            
            if sequence_value != 0:
                return sequences_weights["Quadra"] * sequence_value
            
    def run(self):
        
        self.menu()
        menu_choice = int(input("Opção: "))

        if menu_choice == 1:
            self.print_line()
            initial_chips = int(input(print("Digite a quantidade inicial de fichas que todos os jogadores receberao: ")))
            qtd_players = int(input(print("Digite a quantidade de jogadores: ")))
            self.initial_players(qtd_players, initial_chips)
            print("Embaralhando cartas...")
            self.distribute_cards()
            time.sleep(1)
            

            
            
if __name__ == '__main__':
    cards=[]
    cards.append(Card("Hearts", 10))
    cards.append(Card("Hearts", 11))
    cards.append(Card("Hearts", 12))
    cards.append(Card("Hearts", 13))
    cards.append(Card("Hearts", 14))
    cards.append(Card("Spades", 5))
    cards.append(Card("Spades", 8))
    cards.append(Card("Spades", 12))
    cards.append(Card("Spades", 11))
    cards.append(Card("Spades", 4))
    
 
        
    
    hearts, spades, diamonds, clubs = [], [], [], []
    
    for card in cards:
        if card.suit_getter() == "Hearts":
            hearts.append(card.value_getter())
        elif card.suit_getter() == "Spades":
            spades.append(card.value_getter())
        elif card.suit_getter == "Diamonds":
            diamonds.append(card.value_getter())
        else:
            clubs.append(card.value_getter())
    
    print(hearts)
    print(spades)
    print(diamonds)
    print(clubs)
    
    hearts_cards = generate_combinations(hearts,5)
    spades_cards = generate_combinations(spades,5)
    diamonds_cards = generate_combinations(diamonds,5)
    clubs_cards = generate_combinations(clubs,5)
            
    total_sequences = hearts_cards + spades_cards +  diamonds_cards + clubs_cards
            
    #print(total_sequences)
    
    royal_flush = [10, 11, 12, 13, 14]
            
    for sequence in total_sequences:
        sequence.sort()
        if sequence == royal_flush:
            print("galooooooo")     
            
         







    

     
        