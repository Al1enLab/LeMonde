'''
Fonction de génération de permutations
'''
import math

from typing import Iterable

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

class Permutation:

    def __init__(self, digits: Iterable, slots: int=None, _sequence: list=[ ]):
        self.digits = list(digits)
        self._sequence = _sequence
        if slots is None:
            self.slots = len(self.digits)
        else:
            if slots > len(self.digits):
                raise ValueError('Slots must be lower or equal to length of elements')
            self.slots = slots
    
    @property
    def digit(self):
        return self.digits[self._index]
    @property
    def left_digits(self):
        return self.digits[:self._index] + self.digits[(self._index + 1):]
    @property
    def combinations(self):
        return int(math.factorial(len(self.digits)) / math.factorial(len(self.digits) - self.slots))
    
    def __iter__(self):
        self._index = 0
        if self.slots == 1:
            self._iterator = iter(self.digits)
        else:
            self._iterator = iter(__class__(self.digits[1:], self.slots - 1, self._sequence + [ self.digits[0] ]))
        return self
    
    def __next__(self):
        if self.slots == 1:
            return self._sequence + [ next(self._iterator) ]
        try:
            return next(self._iterator)
        except StopIteration:
            if self._index == len(self.digits) - 1:
                raise StopIteration
            else:
                self._index += 1
                self._iterator = iter(__class__(self.left_digits, self.slots - 1, self._sequence + [ self.digits[self._index] ]))
                return next(self._iterator)

    


if __name__ == '__main__':
    import time
    from pprint import pprint
    # elements = [ 'a', 'b', 'c', 'd', 'e' ]
    # slots = 2

    # for combination in permutations(elements):
    #     print(combination)

    # P = Permutation(elements, 3)
    # pprint(vars(P))
    # count = 1
    # for combination in P:
    #     print(f'Combination {count:>3}: {combination}')
    #     count += 1
    # print(f'{P.combinations = }')

    # Performances
        
    test_permutations = list(range(1, 10))
    print(f'Performance test : permutations {test_permutations}')

    import itertools
    iterations = 0
    start_time = time.time()
    for perm in itertools.permutations(test_permutations):
        iterations += 1
    print(f'Elapsed (itertools.permutations): {time.time() - start_time}s - {iterations} iterations')

    iterations = 0
    start_time = time.time()
    for perm in permutations(test_permutations):
        iterations += 1
    print(f'Elapsed (function permutations): {time.time() - start_time}s - {iterations} iterations')

    P = Permutation(test_permutations)
    iterations = 0
    start_time = time.time()
    for perm in P:
        iterations += 1
    print(f'Elapsed (class Permutation): {time.time() - start_time}s - {iterations} iterations')
