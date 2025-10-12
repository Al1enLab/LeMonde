'''
Une nouvelle énigme à base de permutations.
J'ai déjà codé les permutations, je vais me servir des permutation du module itertools.
'''
from itertools import permutations
import math

# Retourne l'entier (base 10) composé des chiffres digits
# On peut passer par un ''.join() mais c'est moche et ça foire sur les 0 initiaux, s'il y en a
# digits2number = lambda digits: sum( digits[index] * pow(10, len(digits) - (index + 1)) for index in range(len(digits)) )
digits2number = lambda digits: sum( digits[::-1][index] * pow(10, index) for index in range(len(digits)))

class CodeNumbers:
    '''Classse CodeNumbers
    Itère parmi les nombres répondant aux conditions suivantes :
    - tous les chiffres doivent être différents
    - la somme des chiffres en colonne doit toujours être supérieure à 10 (en comptant la retenue)
    Pour que les chiffres soient tous différents, on itère parmi les permutations des chiffres disponibles.
    Pour s'assurer que toutes les additions donnent une retenue, on vérifie que:
    - la somme des chiffres de tous les rangs soit supérieure ou égale à 9
    - la somme des chiffres du dernier rang soit supérieure ou égale à 10
    '''

    def __init__(self, digits: int) -> None:
        '''digits est les tuple comporant l'ensemble des chiffres à utiliser pour la recherche
        des nombres répondant aux contraintes'''
        if len(digits) % 2 != 0:
            raise ValueError('Le nombre de chiffres doit être pair')
        self.digits: tuple[int] = digits
        self.__number_len = int(len(self.digits) / 2)
        # Itérateur des permutations
        self.__permutations = None
    
    def __iter__(self):
        self.__permutations = permutations(self.digits)
        return self
    
    def __next__(self) -> tuple[int]:
        '''On retourne le prochain couple de nombres répondant aux confitions'''
        condition_check = False
        while not condition_check:
            permutation = next(self.__permutations)
            digits1 = permutation[:self.__number_len]
            digits2 = permutation[self.__number_len:]
            # Vérification de la condition de la retenue
            # On commence par calculer la somme des chiffres...
            sums = tuple( sum(digits) for digits in zip(digits1, digits2) )
            # ... et on vérifie que toutes les sommes sont supérieures ou égales à 9 et la dernière à 10
            condition_check = all([ s >= 9 for s in sums ]) and sums[-1] >= 10
        return digits2number(digits1), digits2number(digits2)
    
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

if __name__ == '__main__':
    digits = (2, 3, 4, 5, 6, 7, 8, 9)
    codes = set()
    # On itére parmi les nombres répondant aux critères
    for number1, number2 in CodeNumbers(digits):
        # On stocke chaque résultat dans un set pour éviter les doublons
        key = tuple(sorted((number1, number2), reverse=True))
        key += (number1 + number2, )
        codes.add(key)

    summary(digits=digits, codes=codes)
