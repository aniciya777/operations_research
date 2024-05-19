from typing import List

from sympy import Symbol, simplify
from sympy.logic.boolalg import BooleanAtom

import data_input
from utils import init, out, close, latex, _latex

fd = init()
out = out(fd)


x = Symbol('x', float=True, positive=True)
y = Symbol('y', float=True, positive=True)
N = Symbol('N', integer=True, positive=True)
k = Symbol('k', integer=True, positive=True)

out(r'\begin{abstract}')
out(f'Для развития двух предприятий П1 и П2 на {data_input.N} года выделено {latex(x)} средств. '
    f'Количество средств {latex(y)}, вложенных в П1, обеспечивает годовой доход в размере {latex(data_input.income_1(y))} '
    f'и уменьшается за год до величины {latex(data_input.cost_1(y))}. '
    f'Количество средств {latex(x - y)}, вложенных в П2'
    f' обеспечивает годовой доход в размере {latex(data_input.income_2(x, y))} и уменьшается за год до величины {latex(data_input.cost_2(x, y))}. '
    f'Необходимо так распределить выделенные средства по годам планируемого периода, чтобы получить максимальный доход.')
out(r'\end{abstract}')
out(r'\noindent\rule{\textwidth}{1pt}\newline')
out(r'\textit{Решение.}')
out()
out(f'Период времени продолжительностью {data_input.N} лет разобьем на {data_input.N} этапов, поставив '
    f'в соответствие каждому году один этап, т.е. {latex(N)} = {data_input.N}, {latex(k)} = '
    + ', '.join(str(i + 1) for i in range(data_input.N)) +
    f'. Хотя рассматривается '
    f'непрерывный процесс, величины {latex(x)} и {latex(y)} для наглядности на каждом этапе будем отмечать индексами.')

total_cases: List[bool] = []
total_income: List[Symbol] = []
total_x = [x] + [None] * data_input.N
total_y = [y] + [None] * data_input.N
for step in range(data_input.N):
    n = data_input.N - step
    y_step = Symbol(f'y_{n}', float=True, positive=True)
    total_y[n] = y_step
    x_prev_step = Symbol(f'x_{n - 1}', float=True, positive=True)
    if n == 1:
        x_prev_step = x
    total_x[n - 1] = x_prev_step
    out(f'{step + 1}. ', end='')
    if step == 0:
        out(f'Отыскание оптимального решения начинаем с {n}-го этапа, в начале которого необходимо '
            f'распределить средства $ x_{n - 1} $, оставшиеся после {n - 1}-го этапа. '
            f'Для этого следует определить оптимальное значение $ y_{n} $. '
            f'Составим выражения для функций, входящих в уравнение:')
        t_step = data_input.income_1(y_step) + data_input.income_2(x_prev_step, y_step)
        t_step_latex = fr't_{n} ( x_{n - 1}, y_{n} )'

        out(fr'$$ {t_step_latex} = \varphi ( y_{n} ) + \xi ( x_{n - 1} - y_{n} ) = {_latex(t_step)} ;$$')
        out(fr'$$ f_{n} ( x_{n - 1} ) = \max_{{ 0 \le y_{n} \le x_{n - 1} }}{{\left[ {_latex(t_step)} \right]}} .$$')
        out(f'Для определения значения переменной {latex(y_step)} на отрезке [0, {latex(x_prev_step)}], '
            f'в которой функция $ {t_step_latex} = {_latex(t_step)} $ '
            f'принимает наибольшее значение можно использовать метод дифференциального исчисления. Однако, если учесть, '
            f'что {latex(x_prev_step)} для {n}-го этапа есть величина постоянная, нетрудно заметить, что '
            f'$ g_{n} ( x_{n - 1}, y_{n} ) = {_latex(t_step)} $ – уравнение параболы, ветви которой направлены вверх. '
            f'Стало быть, наибольшее значение на отрезке [0,~{latex(x_prev_step)}] функция принимает на одном из его концов.')
        out(f'Определим значение функции на концах отрезка [0,~{latex(x_prev_step)}]:')

        t_step_0 = data_input.income_1(0) + data_input.income_2(x_prev_step, 0)
        t_step_1 = data_input.income_1(x_prev_step) + data_input.income_2(x_prev_step, x_prev_step)
        out(fr'$$ {t_step_latex} = {_latex(t_step_0)} \textrm{{ при }} {_latex(y_step)} = 0,$$')
        out(fr'$$ {t_step_latex} = {_latex(t_step_1)} \textrm{{ при }} {_latex(y_step)} = {_latex(x_prev_step)}.$$')

        case = simplify(t_step_0 > t_step_1)
        assert isinstance(case, BooleanAtom), f'case is {type(case)}'
        case = bool(case)
        total_cases.append(case)
        if case:
            out(f'Так как {latex(t_step_0)} > {latex(t_step_1)}, то функция $ {t_step_latex} $ '
                f'принимает максимальное значение на отрезке [0,~{latex(x_prev_step)}] при {latex(y_step)} = 0, '
                f'следовательно, $ f_{n}({_latex(x_prev_step)}) = {_latex(t_step_0)} $.')
            total_income.append(t_step_0)
        else:
            out(f'Так как {latex(t_step_0)} < {latex(t_step_1)}, то функция $ {t_step_latex} $ '
                f'принимает максимальное значение на отрезке [0,~{latex(x_prev_step)}] при {latex(y_step)} = {latex(x_prev_step)}, '
                f'следовательно, $ f_{n}({_latex(x_prev_step)}) = {_latex(t_step_1)} $.')
            total_income.append(t_step_1)
        out(f'Таким образом, максимальный доход на последнем этапе достигается в том случае, если в начале его '
            f'все оставшиеся средства вложить в развитие предприятия П{2 if case else 1}.')
        out('Последовательно определим оптимальные распределения средств на ' +
            ', '.join(map(str, range(data_input.N - 1, 1, -1))) +
            ' и 1-м этапах.')
    else:
        if n == 1:
            out('Этапы ' + ', '.join(f'{i}-й' for i in range(n, data_input.N)) + f' и {data_input.N}-й.', end=' ')
        else:
            out(f'Ищем оптимальное распределение для {step + 1} последних этапов – ' +
                ',  '.join(f'{i}-го' for i in range(n, data_input.N)) +
                f' и {data_input.N}-го. Средства, доступные после {n - 1}-го этапа равны {latex(x_prev_step)}.', end=' ')
        out('Функциональное уравнение имеет вид:')
        max_s = fr'max_{{ 0 \le y_{n} \le {_latex(x_prev_step)} }}'

        t_step = data_input.income_1(y_step) + data_input.income_2(x_prev_step, y_step)
        out(fr'$$ f_{n} ( {_latex(x_prev_step)} ) = {max_s}{{\left\{{ t_{n} ( {_latex(x_prev_step)}, y_{n} ) + f_{n + 1} ( x_{n} ) )\right\}}}}'
            fr'= {max_s}{{\left\{{ {_latex(t_step)} + {_latex(total_income[-1])} \right\}}}}.$$')
        t_step += total_income[-1]

        out(f'Здесь $ x_{n} $ – сумма оставшихся средств после {n}-го этапа (на {n}-м этапе было израсходовано '
            f'{latex(y_step)} средств на предприятии П1 и {latex(x_prev_step - y_step)} – на предприятии П2), т.е.')

        x_step = data_input.cost_1(y_step) + data_input.cost_2(x_prev_step, y_step)
        out(fr'$$ x_{n} = {_latex(data_input.cost_1(y_step))} + {_latex(data_input.cost_2(x_prev_step, y_step))} = '
            fr'{_latex(x_step)} .$$')
        out(f'Заменяя $ x_{n} $ его выражением через {latex(x_prev_step)} и {latex(y_step)}, '
            f'окончательно получаем функциональное уравнение:')

        t_step = simplify(t_step.subs({total_x[n]: x_step}))
        out(fr'$$ f_{n} ( {_latex(x_prev_step)} ) = {max_s}{{\left\{{ {_latex(t_step)} \right\}}}}.$$')
        out(f'Находим значение {latex(y_step)}, при котором функция, заключенная в фигурные скобки, на отрезке '
            f'[0,~{latex(x_prev_step)}] достигает наибольшего значения (для простоты обозначим ее через $ Z_{n} $). '
            f'Так как {latex(x_prev_step)} – для {n}-го этапа есть величина постоянная, то')
        out(f'$$ Z_{n} = Z_{n} ( y_{n} ) =  {_latex(t_step)} $$')
        out(f'есть уравнение параболы, ветви которой направлены вверх. Наибольшее значение на отрезке '
            f'[0, {latex(x_prev_step)}] функция $ Z_{n} ( y_{n} ) $ принимает на одном из его концов. Имеем:')

        t_step_0 = t_step.subs({y_step: 0})
        t_step_1 = t_step.subs({y_step: x_prev_step})
        out(fr'$$ Z_{n} ( 0 ) = {_latex(t_step_0)}, $$')
        out(fr'$$ Z_{n} ( {_latex(x_prev_step)} ) = {_latex(t_step_1)}. $$')

        case = simplify(t_step_0 > t_step_1)
        assert isinstance(case, BooleanAtom), f'case is {type(case)}'
        case = bool(case)
        total_cases.append(case)
        if case:
            total_income.append(t_step_0)
        else:
            total_income.append(t_step_1)
        out(f'Поэтому $ f_{n} ( {_latex(x_prev_step)} ) = {_latex(total_income[-1])} $. Следовательно, максимальный доход '
            f'на {n}-м этапе будет достигнут в том случае, если в начале его все '
            f'{"выделенные" if n == 1 else "оставшиеся"} средства вложить в развитие предприятия П{2 if case else 1}.')
total_income = total_income[::-1]
total_cases = total_cases[::-1]

out(r'\noindent\rule{\textwidth}{1pt}\newline')
out('Найденное оптимальное управление справедливо для любого $ x > 0 $, поэтому, не придавая '
    '$ x $ определенного значения, определим величину средств, '
    'подлежащих перераспределению на каждом году планируемого периода.')
out('На основании полученного решения можно сделать вывод, что оптимальное управление '
    'процессом распределения выделенных средств состоит в следующем:')
out(r'\begin{itemize}')
capital = x
for step in range(data_input.N):
    out(r'\item', end=' ')
    case = total_cases[step]
    if case:
        new_capital = data_input.cost_2(capital, 0)
    else:
        new_capital = data_input.cost_1(capital)
    new_capital = simplify(new_capital)

    if step == 0:
        out(f'В начале первого года все средства {latex(capital)} вкладывают в предприятие '
            f'П{2 if case else 1}, и их количество уменьшается до {latex(new_capital)}.')
    else:
        out(f'В начале {step + 1} года остаток средств {latex(capital)} вкладывают в предприятие '
            f'П{2 if case else 1}, и их количество уменьшается до величины {latex(new_capital)}.')
    capital = new_capital
out(r'\end{itemize}')
out(f'При таком распределении средств за {data_input.N} лет '
    f'будет получен максимальный доход, равный $ f(x) = {_latex(total_income[0])} $.')

close(fd)
