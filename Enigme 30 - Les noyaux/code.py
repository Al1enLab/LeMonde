'''
Enigme 30 : les noyaux
'''
import random
from typing import Iterable, NamedTuple

normal_stone = ( 'black', 'white' )
loaded_stone = ( 'black', 'black', 'black', 'white' )
throws_amount = 1000000

class ThrowResult(NamedTuple):
    '''Un résultat est défini par le nombres de noyaux noirs et blancs'''
    blacks: int
    whites: int

def throws(amount: int, stone: Iterable) -> dict:
    '''Retourne un dictionnaire associant la clé (nombre de noyaux noirs, nombre de noyaux blancs)
    au nombre de lancers de cette combinaison'''
    summary = { }
    for t in range(amount):
        result = tuple([ random.choice(stone[s]) for s in range(len(stone)) ])
        index = ThrowResult(blacks=result.count('black'), whites=result.count('white'))
        summary[index] = summary.get(index, 0) + 1
    return summary

def winratio(resultset: dict):
    '''Retourne le pourcentage de victoires sur le resultset'''
    total_throws = sum(resultset.values())
    wins = sum([ resultset[result] for result in resultset if result.blacks % 2 != 0 ])
    return 100 * wins / total_throws

def show_results(resultset: dict) -> None:
    print('------+--------+---------')
    print('Noirs | Blancs | Lancers')
    print('------+--------+---------')
    for summary, counts in sorted(resultset.items()):
        print(f'{summary.blacks:>5} | {summary.whites:>6} | {counts:>7}')
    print('------+--------+---------')
    

if __name__ == '__main__':
    print('Lancer de 8 noyaux non pipés')
    resultset = throws(throws_amount, [ normal_stone ] * 8)
    show_results(resultset)
    print(f'Taux de victoires : {winratio(resultset)} %')
    print()

    print('Lancer de 8 noyaux dont 4 pipés')
    resultset = throws(throws_amount, [ normal_stone ] * 4 + [ loaded_stone ] * 4)
    show_results(resultset)
    print(f'Taux de victoires : {winratio(resultset)} %')
    print()

    print('Lancer de 8 noyaux pipés')
    resultset = throws(throws_amount, [ loaded_stone ] * 8)
    show_results(resultset)
    print(f'Taux de victoires : {winratio(resultset)} %')

