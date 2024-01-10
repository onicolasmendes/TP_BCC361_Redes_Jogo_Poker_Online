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
            i = i + 1
        print("\n")
    
    def poker_sequences(self, player_cards):
        
        cards = self._table_cards + player_cards
        cards = sorted(cards, key=lambda card: card.value_getter())
        
        #Royal Flush
        
                    
    
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
            
            
            
            
            
            
         







    

     
        