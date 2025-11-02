
from itertools import product
from typing import Callable, Iterable, NamedTuple

class UnknownOperation(Exception): pass

class StrangeCalculator:

    class OperationDefinition(NamedTuple):
        func: Callable
        string: str = None

        def __str__(self) -> str:
            if self.string:
                return self.string
            else:
                return f'<{self.func.__name__}>'
        
        def run(self, *args, **kwargs):
            return self.func(*args, **kwargs)

    class HistoryItem(NamedTuple):
        operation: "StrangeCalculator.OperationDefinition"
        result: int|float
        args: tuple = tuple( )

    def __init__(self, base_value: int|float=0):
        self._operations: dict = { }
        self._history: list["StrangeCalculator.HistoryItem"] = [ ]
        self._base_value: int|float = base_value
        self._total: int = base_value
    
    def __getattr__(self, operation: str):
        def wrapper(*args):
            return self.calc(operation, *args)
        return wrapper

    @property
    def operations(self) -> tuple:
        return tuple(self._operations)
    
    def register(self, name: str, func: Callable, string: str=None) -> None:
        self._operations[name] = StrangeCalculator.OperationDefinition(func=func, string=string)
    
    def calc(self, operation: str, *args) -> int|float:
        if not operation in self._operations:
            raise UnknownOperation(f'{operation} is not a registered operation')
        else:
            self._total = self._operations[operation].run(self._total, *args)
            self._history.append(StrangeCalculator.HistoryItem(operation=self._operations[operation], result=self._total, args=args))
            return self._total
    
    def sequence(self, operations: Iterable) -> int|float:
        for operation in operations:
            self.calc(operation)
        return self._total
    
    def AC(self) -> None:
        self._total = self._base_value
        self._history = [ ]

    def __str__(self) -> str:
        if self._history:
            strings: list = [ ]
            for index in range(len(self._history)):
                item = self._history[index]
                if index == 0:
                    previous_total = self._base_value
                else:
                    previous_total = self._history[index - 1].result
                strings.append(f'{previous_total} {item.operation} = {item.result}')
            return ' ; '.join(strings)
        else:
            return '0'

if __name__ == '__main__':
    C = StrangeCalculator()
    step: int = 2003
    C.register(name='addition', func=lambda total: total + step, string=f'+ {step}')
    C.register(name='substraction', func=lambda total: total - step, string=f'- {step}')
    C.register(name='multiplication', func=lambda total: total * step, string=f'* {step}')
    C.register(name='division', func=lambda total: total / step, string=f'/ {step}')

    max_operations, expected = 5, 2004
    for i in range(1, max_operations + 1):
        for sequence in product(C.operations, repeat=i):
            C.AC()
            if C.sequence(sequence) == expected:
                print(f'Solution ({len(sequence)} operations): {C}')
