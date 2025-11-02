'''
Court et bête
'''
from itertools import product
from typing import Callable

step: int = 2003

def addition(amount): return amount + step
def substraction(amount): return amount - step
def multiplication(amount): return amount * step
def division(amount): return amount / step

def main(expected: int, operations: tuple[Callable], max_operations: int):
    for operation_count in range(1, max_operations + 1):
        for combination in product(operations, repeat=operation_count):
            total = 0
            for operation in combination:
                total = operation(total)
            if total == expected:
                return combination

if __name__ == '__main__':
    expected, max_operations = 2004, 5
    solution = main(expected=expected, operations=(addition, substraction, multiplication, division), max_operations=max_operations)
    if solution:
        total, strings = 0, [ 'Start : 0' ]
        for operation in solution:
            total = operation(total)
            strings.append(f'{operation.__name__} : {total}')
        print(f'Solution found in {len(solution)} operations : {" -> ".join(strings)}')
    else:
        print(f'No solution found with {max_operations} operations max')
        