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

expected_scores = (
    [ 2, 2, 3, 1, 1 ]
  + [ 2, 1, 2, 2, 3 ]
  + [ 1, 2, 3, 1, 1 ]
  + [ 1, 3, 1, 2, 2 ]
  + [ 1, 2, 1, 1, 2 ]
)

def gridstring(elements: Iterable, columns: int) -> str:
    '''
    Retourne la chaîne représentant les éléments elements
    dans une grille de columns colonnes.
    '''
    lines = ceil(len(elements) / columns)
    width = max([ len(str(element)) for element in elements ])
    line_parts = [ '-' * (width + 2) ] * columns
    hline = '+' + '+'.join(line_parts) + '+'
    output = hline + '\n'
    for line in range(lines):
        output += '| ' + ' | '.join(map(lambda x: f'{x:>{width}}', elements[line * columns:(line + 1) * columns])) + ' |\n'
        output += hline + '\n'
    return output

# De quoi représenter une grille de 5 colonnes
grid5str = partial(gridstring, columns=5)

def positions(pawns: int, slots: range, _other_positions: list=None):
    '''
    Retourne toutes les combinaisons des index où peuvent se trouver
    pawns pions parmi slots cases
    '''
    if _other_positions is None:
        _other_positions = [ ]
    if pawns < len(slots) + 1:
        for slot in slots:
            actual_positions = _other_positions + [ slot ]
            if pawns == 1:
                yield actual_positions
            else:
                yield from positions(pawns - 1, range(slot + 1, max(slots) + 1), actual_positions)

class ScoreGrid:
    '''
    Classe de manipulation de la grille des dames.
    Met à disposition le calcul des scores de la grille pour chaque dame ajoutée.
    '''
    def __init__(self, *indexes: int):
        '''
        indexes : entiers, index de la grille sur laquelle sont posées les dames
        '''
        self.scores = [ 0 ] * 25
        self.queens = [ ]
        for index in indexes:
            self.set_queen(index)
    
    def _get_scores(self, index: int) -> list:
        '''
        Retourne la grille des scores de la position de la dame.
        Chaque case à portée de la dame vaut 1, les autres 0.
        '''
        # Initialisation des scores de la position
        scores = [ 0 ] * 25
        # On trouve la ligne et la colonne de notre index...
        line, column = divmod(index, 5)
        # Scores de la ligne
        for i in range(line * 5, (line + 1) * 5):
            scores[i] = 1
        # Scores de colonne
        for i in range(column, 25, 5):
            scores[i] = 1
        # On calcule les index de début et de fin des diagonales
        top_left = index - (min(line, column) * 6)
        bottom_right = index + ((4 - max(line, column)) * 6)
        if (4 - column) >= line:
            top_right = index - (line * 4)
            bottom_left = index + (column * 4)
        else:
            top_right = index - ((4 - column) * 4)
            bottom_left = index + ((4 - line) * 4)
        # Premier et dernier index des diagonales
        diagonal1 = (top_left, bottom_right)
        diagonal2 = (top_right, bottom_left)
        # Première diagonale : décalage de 6 entre les index
        for i in range(diagonal1[0], diagonal1[1] + 1, 6):
            scores[i] = 1
        # Seconde diagonale : décalage de 4 entre les index
        for i in range(diagonal2[0], diagonal2[1] + 1, 4):
            scores[i] = 1
        return scores

    def set_queen(self, index: int) -> None:
        '''
        Ajout d'une dame sur la grille.
        index est l'index de la case sur laquelle la dame est ajourée.
        '''
        if index in self.queens:
            return
        if index not in range(25):
            raise ValueError(f'Index must be in {range(25)}, not {index}')
        self.queens.append(index)
        # On calcule le score de la dame...
        queen_score = self._get_scores(index)
        # ... qu'on ajoute aux scores existants de la grille - donc des autres dames
        for i in range(25):
            self.scores[i] += queen_score[i]

if __name__ == '__main__':
    import time
    print('Recherche des positions des dames')
    print()
    print('Tableau des scores attendu :')
    print(grid5str(expected_scores))
    print()
    count, solutions = 0, 0
    start = time.time()
    for position in positions(3, range(25)):
        count += 1
        grid = ScoreGrid(*position)
        if grid.scores == expected_scores:
            solutions += 1
            print('Combinaison trouvée :')
            board = [ ' ' ] * 25
            for p in position:
                board[p] = 'X'
            print(grid5str(board))
            print()
    elapsed = time.time() - start
    print(f'{count} combinaisons testées, {solutions} solution(s) trouvée(s) en {elapsed} secondes.')
