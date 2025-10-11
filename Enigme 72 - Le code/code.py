'''
Une nouvelle énigme à base de permutations.
J'ai déjà codé les permutations, je vais me servir des permutation du module itertools.
'''
from itertools import permutations
import math

class CodeNumbers:
    '''Classe permettant d'itérer au travers des deux nombres à additionner - ou plus précisément:
    des chiffres composant les deux nombes à additionner'''

    def __init__(self, *digits: int) -> None:
        if len(digits) % 2 != 0:
            raise ValueError('Le nombre de chiffres doit être pair')
        self.digits: tuple[int] = digits
        self.__number_len = int(len(self.digits) / 2)
        self.__permutations = None
    
    def __iter__(self):
        self.__permutations = permutations(self.digits)
        return self
    
    def __next__(self) -> tuple[int]:
        permutation = next(self.__permutations)
        return (permutation[:self.__number_len], permutation[self.__number_len:])
    
# Retourne l'entier (base 10) composé des chiffres digits
# On peut passer par un ''.join() mais c'est moche et ça foire sur les 0 initiaux, s'il y en a
digits2number = lambda digits: sum( digits[index] * pow(10, len(digits) - (index + 1)) for index in range(len(digits)) )

def check_digits_sums(digits1: tuple[int], digits2: tuple[int]) -> bool:
    '''Retourne vrai si:
    - les longueurs des deux tuples sont identiques
    - la somme des nombres de rangs identiques dans les deux tuples est
        - supérieure à 10 pour le dernier rang
        - supérieure à 9 pour les autres rangs (grâce à la retenue)
    Sinon retourne faux
    '''
    if len(digits1) != len(digits2):
        return False
    carry = 0
    for index in range(len(digits1) - 1, -1, -1):
        if digits1[index] + digits2[index] + carry < 10:
            return False
        carry = 1
    return True

def find_codes(digits: tuple[int]) -> set:
    '''Trouve tous les codes possibles avec des nombres répondant aux règles du problème'''
    output: set = set()
    for digits1, digits2 in CodeNumbers(*digits):
        if check_digits_sums(digits1, digits2):
            number1, number2 = digits2number(digits1), digits2number(digits2)
            key = tuple(sorted((number1, number2), reverse=True))
            key += (number1 + number2, )
            output.add(key)
    return output

def summary(digits: tuple[int], codes: set) -> None:
    '''Affiche le sommaire des recherches'''

    def columns(iterable, columns, width: int=0, separator: str=' '):
        '''Présentation sous forme de colonnes des réultats'''
        strings = tuple(map(lambda e: f'{e:<{width}}', iterable))
        for line in range(math.ceil(len(strings) / columns)):
            print(separator.join(strings[line * columns: (line+1) * columns]))

    distinct = set( map(lambda x: x[2], codes) )
    biggest = max(distinct)
    biggest_numbers = set( (code[0], code[1]) for code in codes if code[2] == biggest )

    if len(codes) == 0:
        print(f'Aucun code trouvé avec les chiffres {digits}')

    print()
    print(f'--> Plus grand code : {biggest} <--')
    
    print()
    print(f'{len(codes)} codes possibles avec les chiffres {digits} (parmi {math.factorial(len(digits))} permutations)')

    print()
    print(f'{len(distinct)} codes distincts trouvés')
    
    print()
    columns(sorted(distinct, reverse=True), 7, width=10, separator=' ')

    print()
    print(f'{len(biggest_numbers)} combinaisons pour arriver au plus grand code')
    
    print()
    columns([ f'{comb[0]} + {comb[1]} = {comb[0]+ comb[1]}' for comb in sorted(biggest_numbers, reverse=True)], columns=3, separator='   |   ')

    print()
    print(f'--> Plus grand code : {biggest} <--')
    
digits = (2, 3, 4, 5, 6, 7, 8, 9)
codes = find_codes(digits)
summary(digits, codes)
