'''
Enigme 49 : Les monstres des lochs
'''
# Une lambda pour calculer le niveau de danger en fonction de la longueur
danger_level = lambda x: x - pow(x // 10 + x % 10, 2)

# La liste des niveaux de danger associés aux longueurs de ce niveau de danger
classification = { }
for length in range(1, 101):
    level = danger_level(length)
    classification[level] = classification.get(level, [ ]) + [ length ]

# Affichage des niveaux de danger triés du plus grand au plus petit
print('Danger | Longueur(s)')
for level, lengths in sorted(classification.items(), reverse=True):
    print(f'{level:>6} | {", ".join(map(str, lengths))}')
