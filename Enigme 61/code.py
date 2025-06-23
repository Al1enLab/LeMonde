'''
Résolution de l'énigme 61 : le carré fantastique
'''

def permutations(elements: tuple, slots: int=None, _combination: tuple=None) -> tuple:
    '''
    Itère au travers des permutations des éléments elements parmi slots
    Si slots n'est pas défini, il est égal au nombre d'éléments de elements.
    _combination est réservée - il s'agit de la combinaison en cours de confection.
    A noter que itertools.permutations fait le même boulot, mais on est ici pour coder ;-)
    '''
    if slots is None:
        slots = len(elements)
    if slots > len(elements):
        raise ValueError('Slots must be lower or equal to elements length')
    if _combination is None:
        _combination = tuple()
    for index in range(len(elements)):
        next_elements = list(elements)
        this_combination = _combination + (next_elements.pop(index), )
        if slots == 1:
            yield this_combination
        else:
            yield from permutations(tuple(next_elements), slots - 1, this_combination)

class PuzzleGrid:
    '''
    Classe de représentation de la grille du problème
    Grille de 3x3, nombre de 1 à 9
    Index de la grille, stockée sous forme de liste :
    0 1 2
    3 4 5
    6 7 8
    '''
    # Les index de la liste avec lesquels on doit calculer les sommes
    _sums_indexes = (
        (0, 1, 3, 4),
        (1, 2, 4, 5),
        (3, 4, 6, 7),
        (4, 5, 7, 8),
        (0, 2, 6, 8)
    )

    def __init__(self, elements: tuple):
        '''
        elements: tuple listant les 9 éléments de la grille, de l'index 0 à l'index 8
        '''
        if len(elements) != 9:
            raise ValueError(f'Expected 9 elements, got {len(elements)}')
        self.elements = elements
    
    @property
    def sums(self) -> tuple:
        '''
        Retourne la somme des sommets des carrés de la grille
        '''
        sums = [ ]
        for indexes in self._sums_indexes:
            values = [ self.elements[i] for i in indexes ]
            sums.append(sum(values))
        return tuple(sums)
    
    def __str__(self) -> str:
        '''
        Retourne la chaîne de représentation de la grille 3x3
        '''
        hline = '+---' * 3 + '+\n'
        output = hline
        for line in range(3):
            output += '| ' + ' | '.join(map(str, self.elements[line * 3: line * 3 + 3])) + ' |\n' + hline
        return output

if __name__ == '__main__':
    # On génèrele les grilles résultant des permutations de 9 éléments parmi 9...
    for permutation in permutations(tuple(range(1, 10))):
        grid = PuzzleGrid(permutation)
        # Si toutes les sommes sont identiques, le set ne comportera qu'un seul élément
        if len(set(grid.sums)) == 1:
            print(f'{permutation = }, {grid.sums = }')
            print(grid)
