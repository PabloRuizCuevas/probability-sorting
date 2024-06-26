import sys
from functools import lru_cache
from math import comb
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from sympy import Expr, Interval, Rational, Sum, Symbol
from sympy import integrate as ʃ
from sympy import simplify, solve

from onsort.plots import StreamSort

sys.set_int_max_str_digits(0)

n1 = Symbol("n1", domain=Interval(0, 1))

FArray: TypeAlias = npt.NDArray[np.float64]


class InfinitesimalSort(StreamSort):
    def __init__(self, rational: bool = False):
        self.maxi = 1
        self.rational = rational

    @lru_cache
    def mP(self, n: int = 1) -> float | Rational:
        # if n> 9  better using rational = False, otherwise it takes ages
        # as the integrals are symbolic and makes gdc of very large fractions
        # further optimization can be achieved by using symmetry, as the integral
        # evaluate symetrically in the array, same for thresholds
        probability: float | Rational
        if n in [0, 1, 2]:
            probability = [1, 1, Rational(3, 4)][n]
        else:
            B, I = self.thresholds(n)
            I = [0] + I + [1]
            # maybe a base transformation avoid the gdc as well
            probability = sum(
                [ʃ(B[i], (n1, Interval(I[i], I[i + 1]))) for i in range(n)]
            )
        return probability

    @lru_cache
    def p_distributions(self, n: int) -> list[Expr]:
        # n is the number of boxes
        result = [
            self.binomial(n - 1, i) * self.mP(n - 1 - i) * self.mP(i) for i in range(n)
        ]
        if self.rational:
            return result
        return [r.evalf() for r in result]

    @staticmethod
    def binomial(n: int, k: int) -> Expr:  # n successes over k trials
        # faster that using sympy Binomial
        # n1 is prob of success tha is integrated latter
        sol: Expr = comb(n, k) * (1 - n1) ** (n - k) * n1 ** (k)
        # density(Binomial("X", n, n1))(k) #sympy version
        return sol

    @lru_cache
    def thresholds(self, n: int) -> tuple[list[Expr], list[float]]:
        # need to take out p_distributions for lru cache, which may be important
        B = self.p_distributions(n)
        I = []
        for i in range(0, n - 1):
            sol = solve(B[i + 1] - B[i], n1)
            sol = sol[1] if sol[0] == 0 else sol[0]
            sol = sol if self.rational else sol.evalf()
            I.append(sol)
        return B, I


class NaiveInfinitesimalSort(InfinitesimalSort):
    """The naive version of infinitesimal sort, it turns out to be quite good, but ofc not optimal"""

    @lru_cache
    def thresholds(self, n: int) -> tuple[list[Expr], list[float]]:
        # need to take out p_distributions for lru cache, which may be important
        B = self.p_distributions(n)
        I2 = list(np.linspace(0, 1, n + 1)[1:-1])
        return B, I2


# seems constains do not work very well,
# n1 = Symbol('n1', domain=Interval(0,maxi)) # integer=True, positive=True, bounded=True,


class DiscreteSort(StreamSort):
    """it is still bad as maxi should be dinamically calculated"""

    def __init__(self, maxi: int = 1000, rational: bool = False):
        self.maxi = maxi
        self.rational = rational

    def binomial(self, n: int, k: int) -> Expr:
        # faster that using sympy Binomial
        # bad, it should be hypergeometric distribution
        # maybe something like n1/(self.maxi - n2?)
        sol: Expr = (
            comb(n, k) * (1 - n1 / self.maxi) ** (n - k) * (n1 / self.maxi) ** (k)
        )
        return sol

    @lru_cache
    def mP(self, n: int = 1) -> float | Rational:
        if n in [0, 1]:
            return [1, 1][n]

        B, I = self.thresholds(n)
        I = [0] + I + [self.maxi]
        sol: float | Rational = simplify(
            sum([Sum(B[i], (n1, I[i] + 1, I[i + 1])) for i in range(n)]) / self.maxi
        )  # type: ignore
        return sol

    @lru_cache
    def p_distributions(self, n: int) -> list[Expr]:
        # n is the number of boxes
        result = [
            self.binomial(n - 1, i) * self.mP(n - 1 - i) * self.mP(i) for i in range(n)
        ]
        if self.rational:  # not sure if needed anymore
            return result
        return [simplify(r).evalf() for r in result]  # type: ignore

    def thresholds(self, n: int) -> tuple[list[Expr], list[int]]:
        B = self.p_distributions(n)
        I = []
        for i in range(0, n - 1):
            #  should be reduce_inequalities with constrains but do not work well
            sol = solve(B[i + 1] - B[i], n1, rational=self.rational)
            sol = sol[1] if sol[0] == 0 else sol[0]
            sol = int(sol)
            I.append(sol)
        return B, I


# Sort algorithm


def index_from_thresholds(tresholds: list[float], x: float) -> int:
    """returns the index of the tresholds where x is located"""
    # need to reimplement this with no for loop
    for i, lim in enumerate(tresholds):
        if x < lim:
            return i
    return len(tresholds)


def return_subarray(arr: FArray, n: float) -> tuple[FArray, float, float]:
    """returns the possible positions to place n in arr as well as the limits"""
    tmp = np.append(np.append([0], arr), 1)
    mini = np.argwhere(tmp < n)[-1][0]
    maxi = np.argwhere(tmp > n)[0][0]
    return arr[mini : maxi - 1], tmp[mini], tmp[maxi]


def create_thresholds(n: int) -> dict[int, list[float]]:
    """creates the thresholds for each n"""
    return {i: InfinitesimalSort().thresholds(i)[1] for i in range(n + 1)}


def sort(
    arr: FArray,
    thresholds: dict[int, list[float]] | None = None,
    raise_error: bool = True,
) -> FArray:
    """Uses tthe best possible strategy to sort, it works with probability mP(n)
    otherwise it fails to sort.
    This is far from optimized code"""
    # if not isinstance(np.array, arr):
    n = len(arr)
    slots = np.tile(np.nan, n)
    if thresholds is None or len(thresholds.keys()) <= n:
        thresholds = create_thresholds(n)

    for i, ni in enumerate(arr):
        sub, start, end = return_subarray(slots, ni)
        if len(sub) == 0:
            # If enters here it means it is not optimally sortable
            if raise_error:
                raise ValueError("No subarray found, not optimally sortable")
            # As of my resarch now, this part algorithm, i.e
            # when fails, it does not satisfy some desirable properties.
            slots[np.isnan(slots)] = sort(arr[i:], thresholds, raise_error)
            break
        else:
            nip = (ni - start) / (end - start)
            idx = index_from_thresholds(thresholds[len(sub)], nip)
            sub[idx] = ni
    return slots


if __name__ == "__main__":
    print(InfinitesimalSort().mP(6))


# Find algo for optimize for all metrics.

# [1,5,3,8,6,0,4]

# Algo x -> y

[0, 1, 3, 4, 5, 8, 6]  # output
[0, 0, 0, 0, 0, 1, 1]  # ->2/7
[0, 1, 3, 4, 5, 6, 8]  # perfection

# 0-1 # we know the distribution.

# [0.1][_]    0.1 # E[avg distance|n1=0.1] -> 0.1
# you have 0.1 if smaller -> 2
# and 90% is bigger -> 0      avg dist = 0.2

# n2 = 0.05      [0.1][0.05]
#                [0.05][0.1]  # only had 0.1% this happened
#              d   [1]  [1]

#                               P1     P1        P2
#  [0.1][_][_]                 [_][0.1][_]    [_][_][0.1]
#  P of having 2n>0.1       P of having n>0.1 and n<0.1    P()*P()
#


# binomial is not needed anymore!
# [_][0.2][_]


# sum int  from smthg to smght  f(x) P()*P() #


# [][] 0-1   0-100
