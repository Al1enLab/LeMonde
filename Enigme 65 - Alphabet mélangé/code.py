from pprint import pprint
import os

class Counter(dict):
    '''Un compteur reposant sur un dictionnaire ne nécessitant pas d'initialisation
    d'une clé à 0 pour commencer à compter.'''
    def __missing__(self, key):
        '''Retourne 0 en cas de clé manquante'''
        self[key] = 0
        return self[key]
    
    def merge(self, counter):
        '''Ajoute les valeurs de counter aux valeurs actuelles de ce compteur'''
        for key, value in counter.items():
            self[key] += value

class SpecialString:
    '''Une classe pour manipuler une chaîne de manière un peu particulière, spécifiquement pour ce problème.'''

    # Coloration des remplacements
    _colorcode = "\033[31;1;4m"
    _resetcode = "\033[0m"

    def __init__(self, string: str):
        '''On a besoin de la chaîne encodée, c'est tout'''
        self._string = string
        self.replacements = { }
    
    @property
    def _replaced_chars(self) -> dict:
        '''Retourne un dictionnaire dont la clé est l'index de la lettre dand la chaîne originale
        et dont la valeur est le remplacement de cet index'''
        replaced = { }
        for original, replacement in self.replacements.items():
            for search in (original.lower(), original.upper()):
                index = 0
                while index >= 0:
                    index = self._string.find(search, index)
                    if index >= 0:
                        if search.islower():
                            replaced[index] = replacement.lower()
                        else:
                            replaced[index] = replacement.upper()
                        index += len(search)                
        return replaced

    def __str__(self):
        return self.replace_once(colorize=False)

    @property
    def colorized(self):
        '''Comme __str__, mais avec les lettres remplacées colorisées'''
        return self.replace_once(colorize=True)
    
    def replace_once(self, colorize: bool=True):
        '''Remplace l'ensemble des lettres à remplacer, définies dans .replacements.
        A noter qu'un remplacement ne peut pas être surchargé par un remplacement successif.
        Ainsi, si A remplace B, et C remplace A, le remplacement de B par A ne sera pas surchargé
        par le remplace postérieur de A par C.'''
        replaced = [ char for char in self._string ]
        if colorize:
            prefix, suffix = self._colorcode, self._resetcode
        else:
            prefix, suffix = '', ''
        for index, replacement in self._replaced_chars.items():
            replaced[index] = prefix + replacement + suffix
        return ''.join(replaced)

    @property
    def occurrences(self):
        occurrences = Counter()
        for char in self._string:
            if char.lower() in 'abcdefghijklmnopqrstuvwxyz':
                occurrences[char.lower()] += 1
        return occurrences

words_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scrabble.txt')
message1_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'message1.txt')
message2_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'message2.txt')

def show_occurrences(counter):
    '''Affiche un compteur d'occurrences de manière lisible'''
    total = sum(counter.values())
    for char, occurrences in sorted(counter.items(), key= lambda x: x[1], reverse=True):
        print(f'{char} : {occurrences:>7} ({round(occurrences * 100 / total, 2):>6}%)')

def shift_letters(amount):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    mapping = { }
    for i in range(len(alphabet)):
        shifted_index = (i + amount) % len(alphabet)
        mapping[alphabet[i]] = alphabet[shifted_index]
    return mapping


print('=== Répartition des lettres dans le dictionnaire du Scrabble')
with open(words_file, 'r') as file:
    occurrences = Counter()
    for word in file:
        occurrences.merge(SpecialString(word).occurrences)
show_occurrences(occurrences)
print()

print('=== Répartition des lettres dans le message codé')
with open(message2_file, 'r') as file:
    occurrences = Counter()
    for word in file:
        occurrences.merge(SpecialString(word).occurrences)
show_occurrences(occurrences)
print()

replacements = {
    'x': 'i',
    's': 'l',
    'c': 'y',
    'o': 'a',
    'r': 's',
    't': 'c',
    'v': 't',
    'e': 'u',
    'n': 'o',
    'l': 'm',
    'q': 'p',
    'h': 'r',
    'b': 'b',
    'j': 'v',
    'w': 'n',
    'f': 'q',
    'y': 'd',
    'p': 'h',
    'z': 'c',
    'd': 'j',
    'u': 'f',
    'g': 'g'
}

with open(message2_file, 'r') as file:
    encoded = SpecialString(file.read())

encoded.replacements = replacements
print('=== Remplacements dans le message codé')
print(encoded)
print()

print('=== Lettres remplacées (en rouge)')
print(encoded.colorized)
print()

print('=== Répartition des lettres dans le message décodé')
show_occurrences(SpecialString(str(encoded)).occurrences)
print()

test_range = range(22, 25)
for shift in test_range:
    print(f'=== Remplacements du premier message, décalage de {shift}')
    with open(message1_file, 'r') as file:
        encoded = SpecialString(file.read())
    encoded.replacements = shift_letters(shift)
    print(encoded)
    print()
