from Card import Card
import random

class Deck: #Classe que representa o baralho
    #Constructor
    def __init__(self):
        self._cards = [] #Atributo protegido que representa todas as cartas do baralho
        self._suits = {"Hearts":"♡", "Spades":"♠", "Diamonds":"♢", "Clubs":"♣"} #Atributo protegido que reprenta o dicionário de todos os naipes das cartas
        self._values = {
              "Two":2,
              "Three":3,
              "Four":4,
              "Five":5,
              "Six":6,
              "Seven":7,
              "Eight":8,
              "Nine":9,
              "Ten":10,
              "Jack":11,
              "Queen":12,
              "King":13,
              "Ace":14 } #Atributo protegido que reprenta o dicionário de todos os valores das cartas
        
        #Preencher vetor de cartas
        for suit in self._suits:
            for value in self._values:
                self._cards.append(Card(self._suits[suit], self._values[value]))

    def shuffle(self): #Metodo para embaralhar o baralho
        random.shuffle(self._cards)
            
    def pop(self): #Metodo para tirar uma carta do baralho
        return self._cards.pop()
    
    def cards_getter(self): #Metodo para retornar todas as cartas do Deck
        return self._cards