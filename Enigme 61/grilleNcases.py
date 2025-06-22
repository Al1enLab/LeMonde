'''
De quoi traiter une liste comme une grille
'''
# import itertools
import time
from functools import singledispatchmethod
import math
from typing import Any, Iterable, NamedTuple

class Coords(NamedTuple):
    x: int
    y: int

def permutations(elements: Iterable, slots: int=None, _combination: list=[ ]):
    '''
    Itère dans les permutations des éléments elements parmi slots
    elements     : itérable contenant les éléments à permuter
    slots        : nombre d'éléments par permutation (défaut : nombre d'éléments)
    _combination : réservé, combinaison de la permutation en cours
    La permutation des éléments parmi n est l'ensemble des éléments à permuter
    suivis de la permutation des éléments restants parmi n-1
    '''
    if slots is None:
        slots = len(elements)
    elif slots > len(elements):
        raise ValueError('Slots must be lower or equal to length of elements')
    for index in range(len(elements)):
        combination = _combination + [ elements[index] ]
        if slots == 1:
            yield combination
        else:
            left_elements = elements[:index] + elements[(index + 1):]
            yield from permutations(left_elements, slots - 1, combination)

class Grid(list):

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.data = [ None for _ in range(width * height) ]
    
    def coords(self, index: int) -> tuple[int, int]:
        '''
        Retourne le tuple des coordonnées (x, y) de la case index
        '''
        if index not in range(len(self.data)):
            raise IndexError("Index out of bounds")
        x = index % self.width
        y = index // self.width
        return Coords(x, y)
    
    def index(self, x: int, y: int) -> int:
        '''
        Retourne l'index de la liste ayant pour coordonnées (x, y)
        '''
        if x not in range(self.width) or y not in range(self.height):
            raise IndexError("Coordinates out of bounds")
        return y * self.width + x

    @singledispatchmethod
    def __getitem__(self, reference):
        '''On accepte la référence à une case de la grille sous forme d'entier ou de Coords'''
        raise TypeError(f'Reference must be int or tuple, not {type(reference).__name__}')
    
    @__getitem__.register
    def _(self, coords: Coords) -> Any:
        if coords.x not in range(self.width) or coords.y not in range(self.height):
            raise IndexError("Coordinates out of bounds")
        # return y * self.width + x
        index = coords.y + (self.width * coords.x)
        return self.data[index]
    
    @__getitem__.register
    def _(self, reference: int) -> Any:
        return self.data[reference]

class PuzzleGrid(Grid):
    '''
    La grille de l'énigme est toujours carrée, et il faut trouver les sommes des carrés inscrits
    '''
    def __init__(self, size: int) -> None:
        self.size = size
        super().__init__(size, size)
    
    @property
    def squares(self) -> list:
        '''
        Retourne une liste de tuples des coordonnées des carrés inscrits dans le carré principal de la grille
        '''
        corners = [ ]
        for y in range(self.size):
            for x in range(self.size):
                for offset in range(1, self.size - x):
                    if y + offset < self.size:
                        corners.append((
                            Coords(x, y),
                            Coords(x + offset, y),
                            Coords(x, y + offset),
                            Coords(x + offset, y + offset)
                        ))
                    else:
                        break
        return corners
    
    def show(self):
        cell_width = len(str(pow(self.size, 2)))
        hline = '+' + '+'.join([ '-' * (cell_width + 2) ] * self.size) + '+'
        print(hline)
        for y in range(self.size):
            line_elements = [ ]
            for x in range(self.size):
                line_elements.append(f'{self[Coords(x, y)]:>{cell_width}}')
            print('| ' + ' | '.join(line_elements) + ' |')
            print(hline)
    
    @property
    def sums(self):
        sums = [ ]
        for coords in self.squares:
            sums.append(sum([self[coord] for coord in coords]))
        return sums


if __name__ == "__main__":
    import itertools
    print('Input square size : ', end='')
    size = int(input())
    G = PuzzleGrid(size)

    # On peut confier la génération des combinaisons à itertools
    # for combination in list(itertools.permutations(list(range(1, pow(size, 2) + 1)), pow(size, 2))):
    matching_grids = 0
    tested_grids = 0
    total_tests = math.factorial(pow(size, 2))
    start_time = time.time()
    print(f'Testing {total_tests} permutations.')
    print()
    # for combination in permutations(list(range(1, pow(size, 2) + 1))):
    for combination in list(itertools.permutations(list(range(1, pow(size, 2) + 1)), pow(size, 2))):

        tested_grids += 1
        pct = tested_grids * 100 / total_tests
        if ( pct % 10) == 0:
            print(f'{pct} % tests acheived - {round(time.time() - start_time, 2)}s')
        G.data = combination
        sums = G.sums
        if len(set(sums)) == 1:
            matching_grids += 1
            G.show()
            print(f'All sums equal: {sums}')
            print()
    print(f'Matching grids : {matching_grids}, {tested_grids} tested, {round(time.time() - start_time, 2)}s elapsed')
