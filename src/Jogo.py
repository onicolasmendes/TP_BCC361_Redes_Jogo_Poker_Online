from Deck import Deck
from Card import Card
from Jogador import Jogador
from Funcoes_auxiliares import separate_cards_by_suit, separate_cards_by_number, verify_straight_flush, generate_combinations, generate_all_combinations, verify_royal_flush, big_sequence, verify_four, menu, player_menu, verify_double_triple, counting_double_triple, verify_full_house, big_triple_or_pair, verify_straight, verify_triple, verify_two_doubles,  verify_double, verify_highest_card 
import time

class Jogo:
    def __init__(self):
        self._jogadores = []
        self._deck = Deck()
        self._current_value = 0
        self._total_bets = 0
        self._table_cards = []
        self._check_bets = True
        
    def set_table_cards(self):
        for i in range(5):
            self._table_cards.append(self._deck.pop())

    def print_table_cards(self, qtd):
        print("Cartas na mesa:")
        for i in range(qtd):
            print(f"{self._table_cards[i].suit_getter()}{self._table_cards[i].value_getter()}  ")
        
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
            name = input("Digite o nome do jogador: ")
            self._jogadores.append(Jogador(name, chips))
        
    
    
    
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
                    return sequences_weights["Royal Flush"], "Royal Flush"
                
            #Straight Flush
            potentials_straight_flush = []
            
            for sequence in total_sequences:
                if verify_straight_flush(sequence):
                    potentials_straight_flush.append(sequence)
            
            sequence_value = 0  
            sequence_value = big_sequence(potentials_straight_flush)          
            if(sequence_value != 0):
                return sequences_weights["Straight Flush"] * sequence_value, "Straight Flush"
                
            #Flush
            sequence_value = big_sequence(total_sequences)
            return sequences_weights["Flush"] * sequence_value , "Flush"
        
        elif len(two) == 4 or len(three) == 4 or len(four) == 4 or len(five) == 4 or len(six) == 4 or len(seven) == 4 or len(eight) == 4 or len(nine) == 4 or len(ten) == 4 or len(eleven) == 4 or len(twelve) == 4 or len(thirteen) == 4 or len(fourteen) == 4:
            #Four
            sequence_value = 0
            
            sequence_value = verify_four(two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen)
            
            if sequence_value != 0:
                return sequences_weights["Quadra"] * sequence_value, "Quadra"
        
        else:
            sequences =  two + three + four + five + six + seven + eight + nine +  ten + eleven + twelve + thirteen + fourteen
            total_sequences = generate_combinations(sequences, 5)
            
            #Full House
            doubles = 0
            triples = 0
            frequency = []
            potentials_full_house = []
            
            for sequence in total_sequences:
                sequence.sort()
                frequency = verify_double_triple(sequence)
                doubles, triples = counting_double_triple(frequency)
                
                if verify_full_house(doubles, triples):
                    potentials_full_house.append(sequence)
            
            sequence_value = 0
            sequence_value = big_triple_or_pair(potentials_full_house)
            
            if sequence_value != 0:
                return sequences_weights["Full House"] * sequence_value, "Full House"
            
            #Straight
            frequency = []
            potentials_straight = []
            
            for sequence in total_sequences:
                frequency = verify_double_triple(sequence)
                
                if verify_straight(frequency):
                    potentials_straight.append(sequence)
            
            sequence_value = 0
            sequence_value = big_sequence(potentials_straight)

            if sequence_value != 0:
                return sequences_weights["Straight"] * sequence_value, "Straight"
            
            #Trinca
            frequency = []
            potentials_trinca = []
            
            for sequence in total_sequences:
                frequency = verify_double_triple(sequence)
                doubles, triples = counting_double_triple(frequency)
                
                if verify_triple(triples):
                    potentials_trinca.append(sequence)
            
            sequence_value = 0
            sequence_value = big_triple_or_pair(potentials_trinca)
            
            if sequence_value != 0:
                return sequences_weights["Trinca"] * sequence_value, "Trinca"
            
            #Dois pares
            frequency = []
            potentials_dois_pares = []
            
            for sequence in total_sequences:
                frequency = verify_double_triple(sequence)
                doubles, triples = counting_double_triple(frequency)
                
                if verify_two_doubles(doubles):
                    potentials_dois_pares.append(sequence)
            
            sequence_value = 0
            sequence_value = big_triple_or_pair(potentials_dois_pares)
            
            if sequence_value != 0:
                return sequences_weights["Dois Pares"] * sequence_value, "Dois Pares"
            
            #Par
            frequency = []
            potentials_par = []
            
            for sequence in total_sequences:
                frequency = verify_double_triple(sequence)
                doubles, triples = counting_double_triple(frequency) 
                
                if verify_double(doubles):
                    potentials_par.append(sequence)
            
            sequence_value = 0
            sequence_value = big_triple_or_pair(potentials_par)
            
            if sequence_value != 0:
                return sequences_weights["Par"] * sequence_value, "Par"
            
            #Carta mais alta
            higher_card = verify_highest_card(cards)
            return sequences_weights["Carta mais alta"] * higher_card, "Carta mais alta"


    def bet_time(self):
        for jogador in self._jogadores:
            if jogador.fold_getter() == True:
                continue
                    
            jogador.print_cards()
            print(f"Fichas: {jogador.chips_getter()}         TOTAL BET: {self._total_bets}")
            
            while True:
                player_menu()
                player_choice = int(input("Opção: "))
                        
                if player_choice == 1:
                    try:
                        value = int(input("Valor: "))
                        if jogador.raise_bet(value) == True:
                            self._current_value = value
                            self._total_bets += value
                            self._check_bets = False
                            break
                    except:
                        print("Valor Invalido!")
                elif player_choice == 2:
                    try:
                        if jogador.call(self._current_value) == True:
                            self._total_bets += self._current_value
                            break
                    except:
                        print("Saldo Insuficiente")
                elif player_choice == 3:
                    jogador.fold()
                    break
                elif player_choice == 4:
                    jogador.check()
                    break
                elif player_choice == 5:
                    try:
                        if jogador.all_in() == True:
                            if jogador.chipsbet_getter() > self._current_value:
                                self._current_value = jogador.chipsbet_getter()
                    except:
                        print("Fichas Zeradas!")


    def victory_verification(self):
        game_sequences = []
        
        for jogador in self._jogadores:
            if jogador.fold_getter() == True:
                continue
            
            points, sequence = self.poker_sequences(jogador.cards_getter())
            game_sequences.append(sequence)

            jogador.card_points_setter(points)
            bigger_points = 0

            if jogador.card_points_getter() > bigger_points:
                bigger_points = jogador.card_points_getter()
                winner = jogador
                winner_sequence = sequence
        
        return winner, game_sequences, winner_sequence

            
    def run(self):
        
        menu()
        menu_choice = int(input("Opção: "))

        if menu_choice == 1:
            initial_chips = int(input("Digite a quantidade inicial de fichas que todos os jogadores receberao: "))
            qtd_players = int(input("Digite a quantidade de jogadores: "))
            self.initial_players(qtd_players, initial_chips)
            print("Embaralhando cartas...")
            self.distribute_cards()
            self.set_table_cards()
            time.sleep(1)

            show_table_cards = 3
            while(show_table_cards <= 5):
                while True:
                    self._check_bets = True
                    self.bet_time()
                    
                    if self._check_bets == True:
                        self.print_table_cards(show_table_cards)
                        show_table_cards += 1
                        break

            winner, game_sequences, sequence = self.victory_verification()
            print(f"O jogador {winner.name_getter()} venceu com {sequence}")

            print("Sequencia de todos os Jogadores:")
            for sequence in game_sequences:
                print(sequence)           
        elif menu_choice == 2:
            print("Saindo...")
            time.sleep(1)
            exit    
                

                                


                        
                        
                    
                    
                

            
            

            
            
if __name__ == '__main__':
    jogo = Jogo()

    jogo.run()
            
         







    

     
        