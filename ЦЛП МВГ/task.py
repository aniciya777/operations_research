from copy import deepcopy
from typing import Iterable, Optional, List, Union

from solver import LPMaxSolution


def lower_index(index: int) -> str:
    indexes = '₀₁₂₃₄₅₆₇₈₉'
    return f'x{indexes[index]}'


class Task:
    def __init__(self,
                 x_count: int,
                 target_function: str,
                 expressions: Iterable[str],
                 indexes_parts: Optional[List[int]] = None
                 ):
        self.x_count = x_count
        self.target_function = target_function
        self.expressions = expressions
        self.x: List[Optional[Union[float, int]]] = [None] * x_count
        self.solution: Optional[float] = None
        self.status = False
        self.indexes_parts = indexes_parts
        if self.indexes_parts is None:
            self.indexes_parts = []
        self.parent: Optional['Task'] = None
        self.new_constraint: Optional[str] = None

    def add_constraint(self, constraint: str) -> None:
        if constraint.endswith('<= 0'):
            constraint = constraint.replace('<= 0', '== 0')
        self.expressions.append(constraint)
        self.new_constraint = constraint

    @property
    def name(self) -> str:
        return '-'.join(map(str, self.indexes_parts))

    def get_subtask(self, index: int) -> 'Task':
        obj = Task(self.x_count, self.target_function, deepcopy(self.expressions), deepcopy(self.indexes_parts))
        obj.indexes_parts.append(index)
        obj.parent = self
        return obj

    def solve(self):
        result = LPMaxSolution(self.x_count, self.target_function, self.expressions)
        if result:
            self.status = True
            self.solution = result[1]
            if round(self.solution) == self.solution:
                self.solution = int(self.solution)
            for key, value in result[0].items():
                index = int(key[1:]) - 1
                if round(value) == value:
                    value = int(value)
                self.x[index] = value

    def is_not_int(self) -> int:
        for i in range(self.x_count):
            if not isinstance(self.x[i], int):
                return i + 1
        return 0

    @staticmethod
    def __x_to_str(x: Union[int, float]) -> str:
        if isinstance(x, int):
            return str(x)
        return f'{x:.3f}'

    def print_сonstraints(self) -> None:
        print()
        print(' ' * 10, 'Z =', self.target_function, '→ max,')
        for i, expression in enumerate(self.expressions):
            print(' ' * 10, '|' if i else '┌', end=' ')
            expression = expression.replace('<=', '≤').replace('>=', '≥').replace('==', '=')
            print(expression, ',', sep='')
        print(' ' * 10, '└', ', '.join(lower_index(i + 1) for i in range(self.x_count)), '∈ Z≥0')
        print('')

    def print_x(self) -> None:
        result = []
        for i, x in enumerate(self.x, 1):
            result.append(f'{lower_index(i)} = {self.__x_to_str(x)}')
        print(', '.join(result))

    def print_solution(self) -> None:
        result = 'F(x) = ' + self.target_function + f' = '
        if isinstance(self.solution, int):
            result += str(self.solution)
        else:
            result += f'{self.solution:.3f}'
        for i, x in enumerate(self.x, 1):
            x_str = self.__x_to_str(x)
            if x < 0:
                x_str = f'({x_str})'
            result = result.replace(lower_index(i), x_str)
        print(result)
