from sympy import Symbol


# Количество этапов
N = 4


# Функция дохода 1-го производства
def income_1(y: Symbol) -> Symbol:
    return 1.4 * y ** 2


# Функция дохода 2-го производства
def income_2(x: Symbol, y: Symbol) -> Symbol:
    return 2 * (x - y) ** 2


# Функция уменьшения вложенных средств 1-го производства
def cost_1(y: Symbol) -> Symbol:
    return 0.55 * y


# Функция уменьшения вложенных средств 2-го производства
def cost_2(x: Symbol, y: Symbol) -> Symbol:
    return 0.6 * (x - y)



# # Количество этапов
# N = 5
#
#
# # Функция дохода 1-го производства
# def income_1(y: Symbol) -> Symbol:
#     return y ** 2
#
#
# # Функция дохода 2-го производства
# def income_2(x: Symbol, y: Symbol) -> Symbol:
#     return 2 * (x - y) ** 2
#
#
# # Функция уменьшения вложенных средств 1-го производства
# def cost_1(y: Symbol) -> Symbol:
#     return 0.75 * y
#
#
# # Функция уменьшения вложенных средств 2-го производства
# def cost_2(x: Symbol, y: Symbol) -> Symbol:
#     return 0.3 * (x - y)
