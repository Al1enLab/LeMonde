'''
Enigme 56
Trouver le code composé de chiffres formant deux à deux des nombres étant soit des carrés, soit des premiers, soit... ?
'''
import math

# get_squares = lambda x: tuple([pow(i, 2) for i in range(1, int(math.sqrt(x)) + 1)])

def get_squares(max: int) -> tuple:
    '''Retourne la liste des carrés jusqu'à max compris'''
    squares = [ pow(i, 2) for i in range(1, int(math.sqrt(max)) + 1) ]
    return tuple(squares)

def get_primes(max: int) -> list:
    pass

if __name__ == '__main__':
    pass




