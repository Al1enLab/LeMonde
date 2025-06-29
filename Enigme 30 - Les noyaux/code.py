import random
from typing import Hashable, Iterable, NamedTuple

basic_stone = ( 'black', 'white' )
loaded_stone = ( 'black', ) * 3 + ( 'white', )

class StonesThrower:
    '''De quoi simuler le jet d'un ensemble de noyaux'''
    def __init__(self, stones: Iterable) -> None:
        self.stones = stones
    
    def throw(self, amount: int=1) -> tuple:
        '''Retourne amount lancers de noyaux sous la forme d'un tuple contenant des tuples.
        Chaque tuple comporte une série de couleurs tirées au hasard dans self.stones'''
        # Court mais pas simple à comprendre
        # return tuple([ tuple([ random.choice(stone) for stone in self.stones ]) for _ in range(amount)])
        output = [ ]
        for _ in range(amount):
            output.append(tuple([ random.choice(stone) for stone in self.stones ]))
        return tuple(output)

class Result(NamedTuple):
    '''Résultat d'un lancer : nombre de noyaux noirs et blancs issus du lancer'''
    blacks: int
    whites: int
    
class Summary(dict):

    def __missing__(self, key: Hashable) -> int:
        '''On veut un compteur qui commence à zéro si l'entrée n'est pas initialisée. Facie !'''
        return 0

    def add(self, *throws: tuple) -> None:
        '''Ajout d'un lancer au résumé
        On garde une trace du nombre de noyaux noirs et blancs'''
        for throw in throws:
            result = Result(blacks=throw.count('black'), whites=throw.count('white'))
            self[result] += 1

    def __str__(self) -> str:
        '''Retourne une chaîne représentant le résumé'''
        hline = '------+--------+---------'
        output = [ hline, 'Noirs | Blancs | Lancers', hline ]
        output += [ f'{summary.blacks:>5} | {summary.whites:>6} | {amount:>7}' for summary, amount in sorted(self.items()) ]
        output.append(hline)
        return '\n'.join(output)
    
    @property
    def throws(self) -> int:
        '''Retourne le nombre de lancers'''
        return sum(self.values())
    
    @property
    def wins(self) -> int:
        '''Retourne le nombre de victoires'''
        return sum([ count for result, count in self.items() if result.blacks % 2 == 1 ])
    
    @property
    def losses(self) -> int:
        '''Retourne le nombre de défaites'''
        return sum([ count for result, count in self.items() if result.blacks % 2 == 0 ])

    @property
    def winratio(self) -> float:
        '''Retourne le taux de victoire'''
        return round(self.wins * 100 / self.throws, 2)

def simulate(throws: int, normal: int, loaded: int):
    '''Simule throws lancers composés de normal noyaux non pipés et loaded noyaux pipés'''
    stones = StonesThrower((basic_stone, ) * normal + (loaded_stone, ) * loaded )
    summary = Summary()
    summary.add(*stones.throw(throws))
    print(f'{throws} lancers de {normal} noyaux non pipés et {loaded} noyaux pipés :')
    print(summary)
    print(f'Taux de victoire : {summary.winratio}%')
    print()

if __name__ == '__main__':
    simulate(throws=1000000, normal=8, loaded=0)
    simulate(throws=1000000, normal=4, loaded=4)
    simulate(throws=1000000, normal=0, loaded=8)
