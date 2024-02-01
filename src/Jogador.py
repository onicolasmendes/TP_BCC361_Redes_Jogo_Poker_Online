class Jogador: #Classe Jogador
    def __init__(self, name, chips,socket):
        self._cards = []  #Atributo para cartas do jogador
        self._name = name #Atributo para nome do jogador
        self._chips = chips #Atributo para as fichas do jogador
        self._chipsbet = 0 #Atributo para as fichas apostadas do jogador
        self._fold = False #Atributo para checar a desistencia do jogador
        self._check = False #Atributo para passar a vez do jogador
        self._card_points = 0 #Atributo para os pontos das cartas do jogador
        self._sequence = "" #Atributo para a sequencia do jogador
        self._socket = socket #Atributo para o socket do jogador
        self._atual_bet = 0 #Atributo referente a aposta do jogador na rodada corrente
        self._victories = 0 #Atributo para a quantidade de vitórias na sessão
        self._defeats = 0 #Atributo para a quantidade de derrotas na sessão
        self._draws = 0 #Atributo para a quantidade de empates na sessão
    
    #Getters e Setters para conferir o estado de aumentar a aposta
    
    def victories_getter(self):
        return self._victories
    
    def victories_setter(self, value):
        self._victories = value
        
    def defeats_getter(self):
        return self._defeats
    
    def defeats_setter(self, value):
        self._defeats = value
        
    def draws_getter(self):
        return self._draws
    
    def draws_setter(self, value):
        self._draws = value
    
    def atual_bet_getter(self):
        return self._atual_bet
    
    def atual_bet_setter(self, value):
        self._atual_bet = value
    
    #Instacia para comparacao da classe Jogador
    def __eq__(self, outro_objeto):
        if isinstance(outro_objeto, Jogador):
            return self._socket == outro_objeto.socket_getter()
        return False


    #Getters e Setters para o Socket de cada jogador
    def socket_getter(self):
        return self._socket
    
    def socket_setter(self, socket):
        self._socket = socket
    
    
    #Getters e Setters para a sequencia de cada jogador
    def sequence_getter(self):
        return self._sequence
    
    def sequence_setter(self, sequence):
        self._sequence = sequence
    
    #Getters e Setters para o nome de cada jogador
    def name_getter(self):
        return self._name
    
    def name_setter(self, name):
        self._name = name
    
    
    #Getters e Setters para as fichas de cada jogador
    def chips_getter(self):
        return self._chips
    
    def chips_setter(self, chips):
        self._chips = chips
    
    
    #Getters e Setters para as fichas apostadas de cada jogador
    def chipsbet_getter(self):
        return self._chipsbet
      
    def chipsbet_setter(self, chipsbet):
        self._chipsbet = chipsbet
        
    
    #Getters e Setters para o estado de desistencia de cada jogador
    def fold_getter(self):
        return self._fold
    
    def fold_setter(self, fold):
        self._fold = fold
    
    
    #Getters e Setters para os pontos de cada jogador
    def card_points_getter(self):
        return self._card_points
    
    def card_points_setter(self, cards_points):
        self._card_points = cards_points
    
    
    #Metodos para adicionar e remover cartas do jogador
    def cards_pop(self):
        return self._cards.pop()
    
    def cards_push(self, card):
        self._cards.append(card)
    
    
    #Getter para saber as cartas de cada jogador
    def cards_getter(self):
        return self._cards
        
    
    #Metodo para igualar a aposta da mesa
    def call(self, current_bet):
        if current_bet <= self._chips and current_bet != 0:
            self._chipsbet += current_bet
            self._chips -= current_bet
            return True
        return False
            
    #Metodo para desistir da rodada
    def fold(self):
        self._fold = True
        
    
    #Metodo para aumentar a aposta da mesa
    def raise_bet(self, value, current_bet):
        if value <= self._chips and value > current_bet:
            self._chipsbet += value 
            self._chips -= value
            return True
        return False
    
    
    #Metodo para apostar todas as fichas
    def all_in(self, current_value):
        if current_value <= self._chips:
            self._chipsbet += self._chips
            return True
        return False
        
    
    #Metodo para apenas passar a vez na rodada
    def check(self, value):
        if value == 0:
            self._check = True
            return True
        return False
    
    
    #Metodo para imprimir as cartas do jogador
    def print_cards(self):
        msg = f"Deck do jogador {self._name}:\n"
        msg = msg + "Cartas: "
        for card in self._cards:
            msg = msg + f"{card.suit_getter()} {card.value_getter()} "
        return msg
             
            
            
    