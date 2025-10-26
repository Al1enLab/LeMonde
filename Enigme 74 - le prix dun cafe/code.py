from itertools import permutations
from typing import NamedTuple

# Représentation de la monnaie
class Cents(NamedTuple):
    cents: int

    def __str__(self) -> str:
        if self.cents < 100:
            return f'{self.cents} cents'
        else:
            return f'{int(self.cents / 100)} €'

# Représentation des boîtes
class Boxes(NamedTuple):
    box1: int
    box2: int
    box3: int

    def __repr__(self) -> str:
        return f'<Boxes : 1 x {self.box1}, 2 x {self.box2}, 3 x {self.box3}>'

# Les pièves existances, en centimes
coins: tuple = (Cents(1), Cents(2), Cents(5), Cents(10), Cents(20), Cents(50), Cents(100), Cents(200))

# Oneliner : avg est la moyenne des trois boîtes, en centimes
solver = lambda avg: tuple([ Boxes(*p) for p in permutations(coins, 3) if p[0].cents + (2 * p[1].cents) + (3 * p[2].cents) == (3 * avg) ])

if __name__ == '__main__':
    print(solver(150))
