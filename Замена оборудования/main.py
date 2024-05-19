from rich.console import Console
from rich.table import Table

import data_input
from utils import max_print, lower_index


console = Console()
table = Table(show_header=True, header_style="bold magenta")
table.add_column('')
for t in range(data_input.N + 1):
    table.add_column(str(t), justify='center')
table.add_row(
    '[bold][italic]φ[/italic]([italic]t[/italic][/bold])',
    *(str(data_input.fi(t)) for t in range(data_input.N + 1))
)
table.add_row(
    '[bold][italic]s[/italic]([italic]t[/italic][/bold])',
    *(str(data_input.s(t)) for t in range(data_input.N + 1))
)
console.print('Дана таблица:')
console.print(table)
table.add_section()
table.add_row(
    '', *map(str, range(data_input.N, -1, -1))
)




console.print('Уравнения имеют следующий вид:')
max_print(
    ('φ(t) + fₙ₋₁(t+1)', 's(t) - p + φ(t) + fₙ₋₁(1)'),
    prefix='fₙ(t)'
)
max_print(
    ('φ(t)', 's(t) - p + φ(0)'),
    prefix='f₁(t)'
)
console.print('Последовательно вычислим максимальные значения [italic]fₙ[/italic]([italic]t[/italic]) '
              f'для [italic]N[/italic] = 1, 2, … , {data_input.N} при '
              f'[italic]t[/italic] = 1,2, … ,{data_input.N}, используя таблицу значений функции [italic]φ[/italic]([italic]t[/italic]).'
              ' При [italic]N[/italic] = 1 процесс одноэтапный, поэтому значения '
              '[italic]f₁[/italic]([italic]t[/italic]) находим с помощью уравнения')
results = [[] for _ in range(data_input.N + 1)]
for t in range(data_input.N + 1):
    case_1 = data_input.fi(t)
    case_2 = data_input.s(t) - data_input.p + data_input.fi(0)
    results[1].append(max(case_1, case_2))
    max_print(
        (f'φ({t})', f's({t}) - p + φ(0)'),
        (data_input.fi(t), f'{data_input.s(t)} - {data_input.p} + {data_input.fi(0)}'),
        (case_1, case_2),
        prefix=f'f₁({t})',
        suffix=results[1][t]
    )
console.print('Величину функции [italic]fₙ[/italic]([italic]t[/italic]) при [italic]N[/italic] ≥ 2 находим '
              'с помощью уравнения, используя ранее найденные значения [italic]f₁[/italic]([italic]t[/italic]).')
console.print('Вычисления продолжаем до тех пор, пока не будет выполняться условие '
              '[italic]fₙ₋₁[/italic](1) > [italic]fₙ[/italic]([italic]t[/italic]). '
              'В этот момент оборудование необходимо заменить, так как величина прибыли, получаемая в результате '
              'замены оборудования, больше, чем в случае использования старого. '
              'Отмечаем в таблице этот момент знаком :exclamation: и дальнейшие вычисления прекращаем.')
for n in range(2, data_input.N + 1):
    console.print(f'При [italic]N[/italic] = {n} и [italic]t[/italic] = 1,2, … ,{data_input.N} последовательно получаем:')
    for t in range(data_input.N):
        if t + 1 >= len(results[n - 1]):
            slg2 = results[n - 1][-1]
        else:
            slg2 = results[n - 1][t + 1]
        case_1 = data_input.fi(t) + slg2
        case_2 = data_input.s(t) - data_input.p + data_input.fi(0) + results[n - 1][1]
        results[n].append(max(case_1, case_2))
        max_print(
            (f'φ({t}) + f{lower_index(n - 1)}({t + 1})', f's({t}) - p + φ(0) + f{lower_index(n - 1)}(1)'),
            (f'{data_input.fi(t)} + {slg2}', f'{data_input.s(t)} - {data_input.p} + {data_input.fi(0)} + {results[n - 1][1]}'),
            (case_1, case_2),
            prefix=f'f{lower_index(n)}({t})',
            suffix=results[n][-1]
        )
        if results[n - 1][1] > results[n][t]:
            results[n][-1] = results[n - 1][1]
            console.print(f'[italic]f[/italic]{lower_index(n - 1)}(1) > [italic]f[/italic]{lower_index(n)}({t}),\t '
                          f'[italic]f[/italic]{lower_index(n)}({t}) = {results[n][-1]}')
            break

table.add_section()
for i, row in enumerate(results[1:], 1):
    if len(row) < data_input.N + 1:
        row[-1] = ':exclamation:' + str(row[-1])
    table.add_row(
        'f' + lower_index(i) + '(t)', *map(str, row)
    )
console.print(table)

console.print('По результатам вычислений, приведенным в таблице, и линии, разграничивающей '
              'области решений сохранения и замены оборудования, находим оптимальный цикл замены оборудования.')
n = data_input.N
while n > 1:
    period = len(results[n]) - 1
    if period > n:
        raise ValueError
    if period == n:
        console.print(
            f'\t- в {n}-этапном процессе оборудование должно быть заменено также через лет {period}.')
        break
    console.print(f'\t- в {n}-этапном процессе оборудование должно быть заменено через лет {period}, т.е. на {n - period}-м этапе;')
    n -= period
console.print('Таким образом, для получения максимальной прибыли от использования оборудования в '
              f'{data_input.N}-этапном процессе оптимальный цикл состоит в замене оборудования через каждые лет {n}.')
