'''
De quoi traiter une liste comme une grille
'''
import itertools
import time
from functools import singledispatchmethod
import math
from typing import Any, Iterable, NamedTuple

class PuzzleGrid(list):
    '''
    La grille de l'énigme, un carré de 3x3
    Index des cases de la grille :
    0 1 2
    3 4 5
    6 7 8
    '''
    # Les index des cases formant les carrés inscrits
    _squares = (
        (0, 1, 3, 4),
        (1, 2, 4, 5),
        (3, 4, 6, 7),
        (4, 5, 7, 8),
        (0, 2, 6, 8)
    )

    def __init__(self, digits: list) -> None:
        super().__init__(digits)
    
    def show(self):
        hline = '+---' * 3 + '+'
        print(hline)
        for line in range(0, 3):
            digits = map(str, self[(line * 3):(line * 3 + 3)])
            print('| ' + ' | '.join(digits) + ' |')
            print(hline)
    
    @property
    def sums(self):
        '''Retourne la liste des sommes des carrés inscrits'''
        sums = [ ]
        for coords in self._squares:
            sums.append(sum([self[coord] for coord in coords]))
        return sums


if __name__ == "__main__":
    total_tests, matching_grids, tested_grids = math.factorial(9), 0, 0
    start_time = time.time()
    print(f'Testing {total_tests} permutations.')
    print()
    for combination in list(itertools.permutations(list(range(1, 10)))):
        tested_grids += 1
        pct = tested_grids * 100 / total_tests
        if ( pct % 10) == 0:
            print(f'{pct} % tests achieved - {round(time.time() - start_time, 2)}s')
        G = PuzzleGrid(combination)
        sums = G.sums
        if len(set(sums)) == 1:
            matching_grids += 1
            G.show()
            print(f'All sums equal: {sums}')
            print()
    print(f'Matching grids : {matching_grids}, {tested_grids} tested, {round(time.time() - start_time, 2)}s elapsed')
