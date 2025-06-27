from typing import Iterable

def splitint(number: int) -> tuple:
    # Retourne la liste des chiffres composant number
    digits = [ ]
    while number > 0:
        number, digit = divmod(number, 10)
        digits.append(digit)
    return tuple(reversed(digits))

def joinint(digits: Iterable) -> int:
    # Retourne l'entier compose des chiffres de digits
    return sum([ digits[-i - 1] * pow(10, i) for i in range(len(digits)) ])

def cheat(number: int, divider: int):
    # Retourne le nombre modifié qui est divisible par divider, ou None s'il n'y en a pas
    digits = splitint(number)
    for digit_index in range(len(digits)):
        cheat_digits = list(digits)
        for cheat_digit in range(10):
            cheat_digits[digit_index] = cheat_digit
            cheated = joinint(cheat_digits)
            if cheated % divider == 0:
                return cheated
    return None

def show_cheats(test_range: range, divider: int):
     '''Montre l'ensemble des nombres 'trichés' dans test_range pour le diviseur divider'''
     for number in test_range:
        cheated = cheat(number, divider)
        if cheated is not None:
            print(f'{number:>5} -> {cheated:>4} ({cheated / divider:>5} x {divider})')
        else:
            print(f'{number:>5} -> No cheat !')

if __name__ == '__main__':
    # On va parcourir tous les entiers entre 1 et 1000 et tous les diviseurs entre 1 et 20
    number_range, divider_range = range(1, 1000), range(1, 20)
    found = False
    for divider in divider_range:
        for number in number_range:
            if cheat(number, divider) is None:
                print(f'{divider = }, {number = } (number range : {number_range})')
                found = True
                break
        if found:
            break
    print()
    show_cheats(range(number - 15, number + 15), divider)
