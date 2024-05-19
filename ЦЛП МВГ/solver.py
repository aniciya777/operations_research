from typing import Iterable, Dict, Optional, Tuple

from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD


def lower_index(index: int) -> str:
    indexes = '₀₁₂₃₄₅₆₇₈₉'
    return f'x{indexes[index]}'


def custom_eval(expression: str, vars: Dict[str, float]) -> float:
    for i in range(1, 1 + len(vars)):
        expression = expression.replace(lower_index(i), f"x{i}")
    return eval(expression, None, vars)


def LPMaxSolution(
        x_count: int,
        target_function: str,
        expressions: Iterable[str],
        is_int: bool = False
) -> Optional[Tuple[Dict[str, float], float]]:
    model = LpProblem(name='', sense=LpMaximize)

    vars = {}
    for i in range(x_count):
        name_var = f"x{i + 1}"
        if is_int:
            var = LpVariable(name=name_var, lowBound=0, cat="Integer")
        else:
            var = LpVariable(name=name_var, lowBound=0)
        vars[name_var] = var
    for i, expression in enumerate(expressions, 1):
        model += custom_eval(expression, vars), f'Constraint_{i}'
    model += custom_eval(target_function, vars)

    status = model.solve(PULP_CBC_CMD(msg=False))
    if status != 1:
        return
    result = {var.name: var.value() for var in model.variables()}
    return result, model.objective.value()
