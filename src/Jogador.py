class Jogador:
    def __init__(self, name, chips,socket):
        self._cards = [] 
        self._name = name 
        self._chips = chips
        self._chipsbet = 0
        self._fold = False
        self._check = False
        self._card_points = 0
        self._sequence = ""
        self._socket = socket

    def socket_getter(self):
        return self._socket
    
    def __eq__(self, outro_objeto):
        if isinstance(outro_objeto, Jogador):
            return self._socket == outro_objeto.socket_getter()
        return False
    
    def socket_setter(self, socket):
        self._socket = socket
    
    def sequence_getter(self):
        return self._sequence
    
    def sequence_setter(self, sequence):
        self._sequence = sequence
    
    def name_getter(self):
        return self._name
    
    def chips_getter(self):
        return self._chips
    
    def chipsbet_getter(self):
        return self._chipsbet
    
    def name_setter(self, name):
        self._name = name
        
    def chips_setter(self, chips):
        self._chips = chips
        
    def chipsbet_setter(self, chipsbet):
        self._chipsbet = chipsbet
        
    def fold_getter(self):
        return self._fold
    
    def fold_setter(self, fold):
        self._fold = fold
    
    def card_points_getter(self):
        return self._card_points
    
    def card_points_setter(self, cards_points):
        self._card_points = cards_points
    
    def cards_pop(self):
        return self._cards.pop()
    
    def cards_push(self, card):
        self._cards.append(card)
    
    def cards_getter(self):
        return self._cards
        
    def call(self, current_bet):
        if current_bet <= self._chips and current_bet != 0:
            self._chipsbet += current_bet
            self._chips -= current_bet
            return True
        return False
            
    def fold(self):
        self._fold = True
        
    def raise_bet(self, value, current_bet):
        if value <= self._chips and value > current_bet:
            self._chipsbet += value 
            self._chips -= value
            return True
        return False
    
    def all_in(self, current_value):
        if current_value <= self._chips:
            self._chipsbet += self._chips
            return True
        return False
        
    def check(self, value):
        if value == 0:
            self._check = True
            return True
        return False
    
    def print_cards(self):
        msg = f"Deck do jogador {self._name}:\n"
        msg = msg + "Cartas: "
        for card in self._cards:
            msg = msg + f"{card.suit_getter()} {card.value_getter()} "
        return msg
             
            
            
    