'''
CustomCalculator
Calculatrice dont on peut paramétrer les opérations.

TODO : commentaires
'''
from typing import Callable, Hashable
from typing import NamedTuple

class CustomCalculator:

    class UnknownOperation(Exception): pass

    class Operation(NamedTuple):
        '''Représentation d'une opération de la calculatrice'''
        func: Callable
        string: str = None
        args: tuple = tuple()

        def calc(self, *args) -> int|float:
            return self.func(*(args + self.args))

        def __str__(self) -> str:
            if self.string:
                string = self.string
            else:
                string = self.func.__name__
            string += '('
            if self.args:
                string += ', '.join(map(str, self.args))
            return string + ')'
        
        def __repr__(self) -> str:
            return f'<Operation: {self}>'

    def __init__(self, base_value: int|float = 0) -> None:
        self._base_value: int|float = base_value
        self._total: int|float = base_value
        self._history: list = [ ]
        self._operations: dict = dict()
    
    def __getattr__(self, operation: Hashable) -> Callable:
        def wrapper(*args):
            return self.calc(operation, *args)
        return wrapper
    
    def __str__(self) -> str:
        total = self._base_value
        strings = [ str(self._base_value) ]
        if self._history:
            for operation in self._history:
                total = operation.calc(total)
                strings.append(f'{operation} -> {total}')
        return ' ; '.join(strings)

    def __calc(self, operation: Hashable, *args) -> int|float:
        if operation in self._operations:
            return self._operations[operation].calc(*args)
        else:
            raise CustomCalculator.UnknownOperation(f'Unknown operation : {operation}')

    @property
    def operations(self) -> tuple:
        return tuple(self._operations.keys())
    
    def calc(self, operation: Hashable, *args) -> int|float:
        self._total = self.__calc(operation, self._total, *args)
        self._history.append(CustomCalculator.Operation(func=self._operations[operation].func, string=self._operations[operation].string, args=args + self._operations[operation].args))
        return self._total

    def register(self, name: Hashable, operation: "CustomCalculator.Operation") -> None:
        self._operations[name] = operation
    
    def AC(self):
        self._total = self._base_value
        self._history = [ ]
    
if __name__ == '__main__':
    from itertools import product
    import operator

    C = CustomCalculator()
    step: int = 2003
    C.register('add', operation=CustomCalculator.Operation(operator.add, args=(step, )))
    C.register('sub', operation=CustomCalculator.Operation(operator.sub, args=(step, )))
    C.register('div', operation=CustomCalculator.Operation(operator.truediv, string='div', args=(step, )))
    C.register('mul', operation=CustomCalculator.Operation(operator.mul, args=(step, )))
    
    max_operations: int = 5
    expected: int = 2004

    for repeat in range(1, max_operations + 1):
        print(f'{f"[ {repeat} operation(s) ]":=^40}')
        for sequence in product(C.operations, repeat=repeat):
            C.AC()
            if list(map(C.calc, sequence))[-1] == expected:
                print(C)
        print()