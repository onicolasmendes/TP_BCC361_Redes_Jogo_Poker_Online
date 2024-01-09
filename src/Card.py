class Card:

    #Constructor
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value
    
    #Suit getter
    def suit_getter(self):
        return self._suit
        
    #Value getter
    def value_getter(self):
        return self._value 

    #Suit setter
    def suit_setter(self, suit):
        self._suit = suit
    
    #Value setter
    def value_getter(self, value):
        self._value = value
        
    
        