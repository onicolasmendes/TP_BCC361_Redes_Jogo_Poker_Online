from Deck import Deck
from Card import Card
from Jogador import Jogador
from Funcoes_auxiliares import separate_cards_by_suit, separate_cards_by_number, verify_straight_flush, generate_combinations, generate_all_combinations, verify_royal_flush, big_sequence, verify_four,verify_double_triple, counting_double_triple, verify_full_house, big_triple_or_pair, verify_straight, verify_triple, verify_two_doubles,  verify_double, verify_highest_card 
import time


class Jogo:#Classe Jogo
    def __init__(self, jogadores):
        self._jogadores = jogadores #Atributo para lista de jogadores
        self._deck = Deck() #Atributo para o Deck da mesa
        self._current_value = 0 #Atributo para a aposta atual da mesa
        self._total_bets = 0 #Atributo para somar as bets totais
        self._table_cards = [] #Atributo para lista de cartas da mesa
        self._check_bets = True #Atributo para validar as apostas
        
    #Coloca as cartas em uma lista de cartas da mesa
    def set_table_cards(self):
        for i in range(5):
            self._table_cards.append(self._deck.pop())

    #Retorna uma mensagem que mostrara determinada quantidade de cartas no jogo
    def print_table_cards(self, qtd):
        #print("\nCARTAS NA MESA:")
        #for i in range(qtd):
        #    print(f"{self._table_cards[i].suit_getter()}{self._table_cards[i].value_getter()}  ", end="")
        #print("\n")
        msg = "\nCARTAS NA MESA:\n=================================================================\n"
        for i in range(qtd):
            msg = msg + f"{self._table_cards[i].suit_getter()}{self._table_cards[i].value_getter()}  "
        msg = msg + "\n================================================================="
        msg = msg + "\n"
        return msg
    
    def distribute_cards(self):
        self._deck.shuffle()
        
        for jogador in self._jogadores:
            for i in range(2):
                jogador.cards_push(self._deck.pop())
                
    def check_bets_getter(self):
        return self._check_bets
    
    def current_value_setter(self, value):
        self._current_value = value
        
    def total_bets_getter(self):
        return self._total_bets
    
    def players_getter(self):
        return self._jogadores

    def verify_equal_all_bets(self):
        for jogador in self._jogadores:
            if jogador.fold_getter() == True:
                continue
            if jogador.atual_bet_getter() != self._current_value:
                return False
        return True
    
    def reset_all_atual_bet(self):
        for jogador in self._jogadores:
            jogador.atual_bet_setter(0)
            
    def players_setter(self, jogadores):
        self._jogadores = jogadores
    
    def total_bets_setter(self, value):
        self._total_bets = value
        
    def table_cards_getter(self):
        return self._table_cards
    
    def deck_setter(self, value):
        self._deck = value
        
    def current_value_getter(self):
        return self._current_value
            
    def raise_current_value(self, value):
        self._current_value = value
        
    def check_bets_setter(self, value):
        self._check_bets = value
    
    def remove_folds(self):
        for jogador in self._jogadores:
            if jogador.fold_getter() == True:
                self._jogadores.pop()
    
    def initial_players(self, qtd, chips):
        for i in range(qtd):   
            name = input(f"Digite o nome do jogador {i + 1}:")
            self._jogadores.append(Jogador(name, chips))

    def remove_player(self, jogador):
        self._jogadores.remove(jogador)

    
    def add_player(self, player):
        self._jogadores.append(player)   
    
    #Atualiza o número de vitórias do jogador vencedor
    def update_victories(self, winners):
        for winner in winners:
            for jogador in self._jogadores:
                if winner == jogador:
                    jogador.victories_setter(jogador.victories_getter() + 1)

    #Atualiza o número de derrotas dos jogadores vencedores
    def update_defeats(self, winners):
        for jogador in self._jogadores:
            is_winner = 0
            for winner in winners:
                if jogador == winner:
                    is_winner += 1
            if is_winner == 0:
                jogador.defeats_setter(jogador.defeats_getter() + 1)
    
    #Atualiza o número de empates dos jogadores que empataram
    def update_draws(self, draws):
        for draw in draws:
            for jogador in self._jogadores:
                if draw == jogador:
                    jogador.draws_setter(jogador.draws_getter() + 1)   
                         
    def poker_sequences(self, player_cards):
        
        cards = self._table_cards + player_cards
        
        hearts, spades, diamonds, clubs = [], [], [], []
        
        separate_cards_by_suit(hearts, spades, diamonds, clubs, cards)
        
        two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen = [], [], [], [], [], [], [], [], [], [], [], [], []
        
        separate_cards_by_number(two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, cards)
                
        sequences_weights = {
            "Royal Flush": 22136835840,
            "Straight Flush": 1581202561,
            "Quadra": 112943041,
            "Full House": 8067361,
            "Flush": 576241,
            "Straight": 41161,
            "Trinca": 2941,
            "Dois Pares": 211,
            "Par": 15,
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
            if self.verify_number_valid_players() == False:
                break
            
            if jogador.fold_getter() == True:
                continue
            
            while True:
                print(f"\nFICHAS: {jogador.chips_getter()}         MAIOR APOSTA DA RODADA: {self._current_value}        BUCKET: {self._total_bets}\n")
                jogador.print_cards()
                self.show_player_menu()
                while True:
                    player_choice = int(input("Opção:"))
                    if player_choice > 0 and player_choice < 7:
                        break
                    else:
                        print("Opção Inválida!")
                        
                if player_choice == 1:
                    value = int(input("Valor: "))
                    if jogador.raise_bet(value, self._current_value) == True:
                        self._current_value = value
                        self._total_bets += value
                        self._check_bets = False
                        break
                    else:
                        print("Acao Invalida")
                elif player_choice == 2:
                    if jogador.call(self._current_value) == True:
                        self._total_bets += self._current_value
                        self._check_bets = True
                        break
                    else:
                        print("Acao Invalida")
                elif player_choice == 3:
                    jogador.fold()
                    break
                elif player_choice == 4:
                    jogador.check()
                    break
                elif player_choice == 5:
                    if jogador.all_in(self._current_value) == True:
                        self._current_value = jogador.chips_getter()
                        self._total_bets += self._current_value
                        jogador.chips_setter(0)
                        break
                    else:
                        print("Acao Invalida")

    def victory_verification(self):

        players = []
        list_points = []
        
        for jogador in self._jogadores:
            if jogador.fold_getter() == True:
                continue
            
            points, sequence = self.poker_sequences(jogador.cards_getter())
            jogador.card_points_setter(points)
            jogador.sequence_setter(sequence)

            players.append(jogador)
            list_points.append(points)

        players = sorted(self._jogadores, key= lambda jogador : jogador.card_points_getter())
        players.reverse()

        list_points.sort()
        list_points.reverse()

        victory_count = list_points.count(players[0].card_points_getter())
         
        winners = []
        for i in range(victory_count):
            winners.append(players[i])
        
        return winners, victory_count

    
    def show_menu(self):
        print("Poker Texas Hold'em")
        print("1 - Iniciar")
        print("2 - Sair")

        
    
    def show_player_menu(self):
        msg = "Ação:\n"
        msg = msg + "1 - Aumentar a aposta\n"
        msg = msg + "2 - Call\n"
        msg = msg + "3 - Fold\n"
        msg = msg + "4 - Check\n"
        msg = msg + "5 - AllIn\n"
        return msg
        
    def clear_players(self):
        for jogador in self._jogadores:
            jogador._cards.clear()
            jogador.chipsbet_setter(0)
            jogador.atual_bet_setter(0)
            if jogador.chips_getter() != 0:
                jogador.fold_setter(False)
            else:
                jogador.fold_setter(True)
            jogador.sequence_setter("")
    
    def verify_fold(self):
        active = 0
        for jogador in self._jogadores:
            if jogador.fold_getter() == False:
                active += 1
        
        if active == 1:
            return True

                
    def verify_number_valid_players(self):
        valid_players = 0
        for jogador in self._jogadores:
            if jogador.fold_getter() == False:
                valid_players += 1
        if valid_players == 1 or valid_players == 0:
            return False
        return True  

