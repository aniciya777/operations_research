from sys import exit
from math import ceil, floor
from collections import deque
from typing import Optional

from task import Task, lower_index

LIMIT_DEPTH = 3


def branch_and_bound_method(task: Task) -> None:
    global best_solution, best_task
    print('-' * 80)
    print('Задача', task.name)
    task.print_сonstraints()
    task.solve()
    if not task.status:
        print(f'Задача {task.name} не имеет решения.')
        return
    print(f'Для задачи {task.name} имеем следующее решение')
    task.print_x()
    task.print_solution()
    index_x = task.is_not_int()
    if task.solution <= best_solution:
        if best_task:
            print(f'Так как решение не лучше {best_task.name}, то не будем разбивать задачу {task.name}')
        return
    if not index_x:
        if best_task:
            print(f'Так как решение лучше {best_task.name}, то теперь лучшая задача {task.name}')
        best_solution = task.solution
        best_task = task
        return
    else:
        current_value = task.x[index_x - 1]
        upper_bound = int(ceil(current_value))
        lower_bound = int(floor(current_value))
        print(f'''Получили дробные решения.
Возьмем переменную {lower_index(index_x)} = {task.x[index_x - 1]}.
Разобьём задачу на две подзадачи, где {lower_index(index_x)} ≤ {lower_bound} и {lower_index(index_x)} ≥ {upper_bound}.''')
        task1 = task.get_subtask(1)
        task1.add_constraint(f'{lower_index(index_x)} <= {lower_bound}')
        task2 = task.get_subtask(2)
        task2.add_constraint(f'{lower_index(index_x)} >= {upper_bound}')
        tasks.append(task1)
        tasks.append(task2)


task = Task(
    3,
    '2.5 * x₁ + 4 * x₂ + 4.2 * x₃',
    [
        '3 * x₁ + 4 * x₂ + 2 * x₃ <= 22',
        '1 * x₁ + 3 * x₂ + 5 * x₃ <= 31',
        '2 * x₁ + 4 * x₂ + 5 * x₃ <= 27',
    ]
)
tasks = deque([task])

print('Решим задачу динамического программирования методом ветвей и границ.')
best_solution = float('-inf')
best_task: Optional[Task] = None
step = 0
while tasks:
    current_task = tasks.popleft()
    branch_and_bound_method(current_task)
    step += 1
    if step > 2 ** (LIMIT_DEPTH + 1):
        break
if not best_task:
    print('Задача не имеет решения.')
    exit(0)
print('-' * 80)
print('Получили оптимальное решение')
best_task.print_x()
best_task.print_solution()
