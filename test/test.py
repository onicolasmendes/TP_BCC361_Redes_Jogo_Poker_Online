import random
from itertools import combinations

cartas = [11,12,34]

random.shuffle(cartas)

sequences = combinations(cartas,4)

for sequence in sequences:
    print(list(sequence))
#print(cartas)
#c = [5,6,4,3,7]
#c = cartas
#print(c)
