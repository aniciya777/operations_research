from io import TextIOWrapper

from sympy import Symbol, latex as __latex, Number


def _latex(s: Symbol) -> str:
    num_digits = 3
    s = s.xreplace({n : round(n, num_digits) for n in s.atoms(Number)})
    return __latex(s, decimal_separator='comma')


def latex(s: Symbol) -> str:
    return f'$ {_latex(s)} $'


def init() -> TextIOWrapper:
    df = open('out.tex', 'w', encoding='utf-8')
    df.write(r'''\documentclass[12pt]{article}
    
\usepackage[english,russian]{babel}

\usepackage[left=2cm,right=1cm,
    top=1cm,bottom=2cm,bindingoffset=0cm]{geometry}
    
\author{Остапчук А.В.}
\title{Задача распределения ресурсов}

\begin{document}
\maketitle
\renewcommand{\abstractname}{Вариант 5}
''')
    return df

def out(fd: TextIOWrapper):
    def out_wrapper(*args, sep=' ', end='\n'):
        text = sep.join(map(str, args)) + end
        text = text.replace('\n', '\n\n')
        print(text, end='')
        print(text, end='', file=fd)

    return out_wrapper


def close(fd: TextIOWrapper):
    fd.write(r'''\end{document}''')
    fd.close()
