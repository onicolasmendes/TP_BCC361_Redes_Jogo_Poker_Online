class Jogador:
    def __init__(self, name, chips):
        self._cards = [] 
        self._name = name 
        self._chips = chips
        self._chipsbet = 0
        self._fold = False

    def name_getter(self):
        return self._name
    
    def chips_getter(self):
        return self._chips
    
    def chipsbet_getter(self):
        return self._chipsbet
    
    def fold_getter(self):
        return self._fold
    
    def name_setter(self, name):
        self._name = name
        
    def chips_setter(self, chips):
        self._chips = chips
        
    def chipsbet_setter(self, chipsbet):
        self._chipsbet = chipsbet
        
    def fold_setter(self, fold):
        self._fold = fold
    
    def cards_pop(self):
        return self._cards.pop()
    
    def cards_push(self, card):
        self._cards.append(card)
        
    def call(self, current_bet):
        if current_bet <= self._chips:
            self._chipsbet += current_bet
            self._chips -= current_bet
            return True
        return False
            
    def fold(self):
        self._fold = True
        
    def raise_bet(self, value):
        if value <= self._chips:
            self._chipsbet += value 
            self._chips -= value
            return True
        return False
    
    def all_in(self, current_value):
        if current_value <= self._chips:
            self._chipsbet += self._chips
            self._chips = 0
            return True
        return False
        
    def check(self):
        return True
    
    def print_cards(self):
        i = 1;
        print("Deck do jogador" + self._nome+ ":\n")
        for card in self._cards:
            print("Carta "+ i+": "+card.suit_getter()+ " "+ card.value_getter()+"\n")
            i = i + 1
             
            
            
    