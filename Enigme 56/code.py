'''
Enigme 56
Trouver le code composé de chiffres formant deux à deux des nombres étant soit des carrés, soit des premiers, soit... ?
'''
import math

def get_squares(max: int) -> tuple:
    '''Retourne la liste des carrés jusqu'à max compris'''
    squares = [ pow(i, 2) for i in range(1, int(math.sqrt(max)) + 1) ]
    return tuple(squares)

def get_primes(max: int) -> tuple:
    '''Simple et pas vraiment rapide : retourne la liste des nombres premiers jusqu'à max compris'''
    if max < 2:
        return tuple()
    primes, number = [ 2 ], 3
    while number <= max:
        is_prime = True
        for p in primes:
            if number % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(number)
        number += 2
    return tuple(primes)

allowed_squares = get_squares(99)
allowed_primes = get_primes(99)

allowed = (
    allowed_primes,
    allowed_squares,
    allowed_primes,
    allowed_squares,
) 

def bruteforce():
    '''Teste toutes les combinaisons à 5 chiffres et yield celles qui correspondent aux contraintes'''
    for combination in range(pow(10, 5)):
        combination_str = f'{combination:>05}'
        is_allowed = True
        for index in range(4):
            if int(combination_str[index:index+2]) not in allowed[index]:
                is_allowed = False
                break
        if is_allowed:
            yield ' '.join(combination_str + '?')

def smarter(_index: int=0, _previous: list=None):
    '''Trouve les nombres à deux chiffres possibles en fonction des contraintes'''
    if _previous is None:
        for number in allowed[_index]:
            yield from smarter(_index + 1, [ number ])
    else:
        first_digit = _previous[-1] % 10
        for digit in [ allowed[_index][i] for i in range(len(allowed[_index])) if allowed[_index][i] // 10 == first_digit ]:
            combination = _previous + [ digit ]
            if _index == 3:
                combination_str = ' '.join(f'{combination[0]:>02}' + ''.join(map(lambda x: str(x % 10), combination[1:]))) + ' ?'
                yield combination_str
            else:
                yield from smarter(_index + 1, combination)
            
if __name__ == '__main__':
    print('-- bruteforce --')
    for combination in bruteforce():
        print(combination)
    
    print()
    print('-- smarter --')
    for combination in smarter():
        print(combination)
