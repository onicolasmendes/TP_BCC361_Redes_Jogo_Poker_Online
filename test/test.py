import random
from itertools import combinations

cartas = [11,12,34,11,12,34]

random.shuffle(cartas)

sequences = combinations(cartas,5)

for sequence in sequences:
    print(list(sequence))
print(cartas)
c = [5,6,4,3,7]
c = cartas
print(c)

def counting_double_triple(sequence, doubles, triples):
    for i in sequence:
        if (i == 2):
            doubles.append(1)
        elif (i == 3):
            triples.append(1)
            
doubles = []
triples = []
sequence = [2,4,3,4]

counting_double_triple(sequence, doubles, triples)

print(doubles)
print(triples)

