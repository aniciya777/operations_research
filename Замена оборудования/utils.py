from typing import Tuple, Optional


def lower_index(index: int) -> str:
    INDEXES = "₀₁₂₃₄₅₆₇₈₉"
    return ''.join(INDEXES[int(pos)] for pos in str(index))


def max_print(
        *pairs: Tuple,
        prefix: Optional = None,
        suffix: Optional = None,
) -> None:
    row_1 = row_2 = ''
    if prefix is not None:
        prefix = str(prefix)
        row_1 = '\x1B[3m' + prefix + '\x1B[0m'
        row_2 = ' ' * len(prefix)
    for s1, s2 in pairs:
        if row_1:
            row_1 += ' = '
            row_2 += '   '
        s1 = str(s1)
        s2 = str(s2)
        size = max(len(s1) + 1, len(s2)) + 1
        row_1 += 'max┌ \x1B[3m' + s1 + '\x1B[0m,' + ' ' * (size - len(s1) - 1)
        row_2 += '   └ \x1B[3m' + s2 + '\x1B[0m' + ' ' * (size - len(s2))
    if suffix is not None:
        row_1 += ' = ' + str(suffix)
    print(row_1)
    print(row_2)
