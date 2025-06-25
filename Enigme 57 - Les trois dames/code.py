'''
Enigme 57 - Les trois dames

Index de la grille 5x5
+----+----+----+----+----+
|  0 |  1 |  2 |  3 |  4 |
+----+----+----+----+----+
|  5 |  6 |  7 |  8 |  9 |
+----+----+----+----+----+
| 10 | 11 | 12 | 13 | 14 |
+----+----+----+----+----+
| 15 | 16 | 17 | 18 | 19 |
+----+----+----+----+----+
| 20 | 21 | 22 | 23 | 24 |
+----+----+----+----+----+
'''
from math import ceil
from typing import Iterable
from functools import partial

scores = (
    [ 2, 2, 3, 1, 1 ]
  + [ 2, 1, 2, 2, 3 ]
  + [ 1, 2, 3, 1, 1 ]
  + [ 1, 3, 1, 2, 2 ]
  + [ 1, 2, 1, 1, 2 ]
)

def gridstring(elements: Iterable, columns: int) -> str:
    '''Retourne la liste elements sous forme de grille de columns colonnes'''
    lines = ceil(len(elements) / columns)
    width = max([ len(str(element)) for element in elements ])
    line_parts = [ '-' * (width + 2) ] * columns
    hline = '+' + '+'.join(line_parts) + '+'
    output = hline + '\n'
    for line in range(lines):
        output += '| ' + ' | '.join(map(lambda x: f'{x:>{width}}', elements[line * columns:(line + 1) * columns])) + ' |\n'
        output += hline + '\n'
    return output

grid5str = partial(gridstring, columns=5)

def positions(pawns: int, slots: range, _others: list=None):
    '''
    Retourne toutes les combinaisons des index où peuvent se trouver
    pawns pions parmi slots cases'''
    if _others is None:
        _others = [ ]
    if pawns < len(slots) + 1:
        for slot in slots:
            actual_positions = _others + [ slot ]
            if pawns == 1:
                yield actual_positions
            else:
                yield from positions(pawns - 1, range(slot + 1, max(slots) + 1), actual_positions)

class ScoreGrid:

    def __init__(self, *indexes: int):
        self.scores = [ 0 ] * 25
        self.queens = [ ]
        for index in indexes:
            self.set_queen(index)
    
    def _get_scores(self, index: int) -> list:
        '''
        Retourne la grille des scores de la position de la dame
        '''
        # Initialisation des scores de la position
        score = [ 0 ] * 25
        # On trouve la ligne et la colonne de notre index...
        line, column = divmod(index, 5)
        # Score de la ligne
        for i in range(line * 5, (line + 1) * 5):
            score[i] = 1
        # Score de colonne
        for i in range(column, 25, 5):
            score[i] = 1
        # TODO : scores des diagonales
        return score

    def set_queen(self, index: int) -> None:
        if index in self.queens:
            raise ValueError(f'Queen already set at index {index}')
        if index not in range(25):
            raise ValueError(f'Index must be in {range(25)}, not {index}')
        self.queens.append(index)
        queen_score = self._get_scores(index)
        print(grid5str(queen_score))
        for i in range(25):
            self.scores[i] += queen_score[i]


S = ScoreGrid(3, 10, 17, 23, 15, 19)
print(grid5str(S.scores))
# print(grid5str(range(25)))
# for p in positions(pawns=5, slots=range(7)):
#     print(p)
# for p in positions(pawns=3, slots=range(25)):
#     elements = [ ' ' ] * 25
#     for index in p:
#         elements[index] = 'X'
#     print(grid5str(elements))