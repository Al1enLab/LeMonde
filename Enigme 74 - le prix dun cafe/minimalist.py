from itertools import permutations
print([ p for p in permutations((1, 2, 5, 10, 20, 50, 100, 200), 3) if p[0] + (2 * p[1]) + (3 * p[2]) == 450 ])