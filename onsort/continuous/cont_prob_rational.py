from functools import cache
from math import comb
from sympy import integrate, solve, Expr, Interval, Symbol
import sys


sys.set_int_max_str_digits(0)
n1 = Symbol("n1", domain=Interval(0, 1))


@cache
def Pn(n: int = 1) -> float:
    """Probability of winning continous version with n slots"""
    if n in [0, 1]:
        return 1
    s, l = 0, 0
    for i in range(n):
        r = thresholds(n, i)
        s += integrate(pnb(n - 1, i), (n1, Interval(l, r)))
        l = r
    return s


def thresholds(n: int, i: int):
    """Bucket thresholds"""
    if (n - 1) == i:
        return 1
    sol = solve(pnb(n - 1, i + 1) - pnb(n - 1, i), n1)
    return sol[1] if sol[0] == 0 else sol[0]


def pnb(n: int, i: int):
    """Probability of winning continous version with n slots
    placing the first number at slot 1
    """
    return binomial(n, i) * Pn(n - i) * Pn(i)


def binomial(n: int, k: int) -> Expr:
    """binomial distribution"""
    return comb(n, k) * (1 - n1) ** (n - k) * n1 ** (k)


if __name__ == "__main__":
    print(Pn(4))
