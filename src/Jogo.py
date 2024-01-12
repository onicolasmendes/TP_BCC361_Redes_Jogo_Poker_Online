from Deck import Deck
from Jogador import Jogador
import time

class Jogo:
    def __init__(self):
        self._jogadores = []
        self._deck = Deck()
        self._current_value = 0
        self._total = 0
        self._table_cards = []
        self._check_bets = True

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
        cards = sorted(cards, key=lambda card: card.value_getter())

        hearts, spades, diamonds, clubs = [0], [0], [0], [0]
        for card in cards:
            if card.suit_getter() == "♡":
                hearts.append(card)
                hearts[0] += card.value_getter()
            elif card.suit_getter() == "♠":
                spades.append(card)
                spades[0] += card.value_getter()
            elif card.suit_getter == "♢":
                diamonds.append(card)
                diamonds[0] += card.value_getter()
            else:
                clubs.append(card)
                clubs[0] += card.value_getter()
        
        
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
        

        if len(hearts) == 5 or len(spades) == 5 or len(diamonds) == 5 or len(clubs) == 5:
            if hearts[0] == 60 or spades[0] == 60 or diamonds == 60 or clubs == 60:
                return sequences_weights["Royal Flush"]
            else:
                sf_possibilites = [20,25,30,35,40,45,50,55]
                for number in sf_possibilites:
                    if hearts[0] == number or spades[0] == number or diamonds[0] == number or clubs[0] == number:
                        return sequences_weights["Straight Flush"]
                
                return sequences_weights["Flush"]
        
        

            




        
                    
    
    def run(self):
        
        self.menu()
        menu_choice = int(input("Opção: "))

        if menu_choice is 1:
            self.print_line()
            initial_chips = int(input(print("Digite a quantidade inicial de fichas que todos os jogadores receberao: ")))
            qtd_players = int(input(print("Digite a quantidade de jogadores: ")))
            self.initial_players(qtd_players, initial_chips)
            print("Embaralhando cartas...")
            self.distribute_cards()
            time.sleep(1)
            
            
            
            
            
            
         







    

     
        