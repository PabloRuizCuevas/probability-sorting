import sys
from functools import lru_cache
from math import comb

import numpy as np
from sympy import Interval, Rational, Sum, Symbol
from sympy import integrate
from sympy import integrate as ʃ
from sympy import simplify, solve
from sympy.stats import Binomial, density

from src.my_sort import StreamSort

sys.set_int_max_str_digits(0)

n1 = Symbol("n1", domain=Interval(0, 1))


class InfinitesimalSort(StreamSort):
    def __init__(self, rational=False):
        self.maxi = 1
        self.rational = rational

    @lru_cache
    def mP(self, n=1):
        # if n> 9  better using rational = False, otherwise it takes ages
        # as the integrals are symbolic and makes gdc of very large fractions
        # further optimization can be achieved by using symetry, as the inthegral
        # evaluate symetrically in the array.
        if n in [0, 1, 2]:
            return [1, 1, Rational(3, 4)][n]

        B, I = self.thresholds(n)
        I = [0] + I + [1]
        # maybe a base transformation avoid the gdc as well
        return sum([ʃ(B[i], (n1, Interval(I[i], I[i + 1]))) for i in range(n)])

    @lru_cache
    def p_distributions(self, n):
        # n is the number of boxes
        result = [
            self.binomial(n - 1, i) * self.mP(n - 1 - i) * self.mP(i) for i in range(n)
        ]
        if self.rational:
            return result
        return [r.evalf() for r in result]

    @staticmethod
    def binomial(n, k):  # n successes over k trials
        # faster that using sympy Binomial
        # n1 is prob of success tha is integrated latter
        return comb(n, k) * (1 - n1) ** (n - k) * n1 ** (k)

    @lru_cache
    def binomial2(n, k):
        # this way slower but more sympy :)
        return density(Binomial("X", n, n1))(k)

    def naive_thresholds(self, n):
        # naive version of thesholds
        return np.linspace(0, 1, n - 1)

    def thresholds(self, n):
        # need to take out p_distributions for lru cache, which may be important
        B = self.p_distributions(n)
        I = []
        for i in range(0, n - 1):
            sol = solve(B[i + 1] - B[i], n1)
            sol = sol[1] if sol[0] == 0 else sol[0]
            sol = sol if self.rational else sol.evalf()
            I.append(sol)
        return B, I

    def normalization(self, n):
        # todo, but will serves to normalize real use cases
        n = 458
        maxi = 473
        mini = 0
        elements = 9
        print(n - mini)
        (np.array(self.thresholds(elements)) * (maxi - mini)).astype(int)


class NaiveInfinitesimalSort(InfinitesimalSort):
    """The naive version of infinitesimal sort, it turns out to be quite good, but ofc not optimal"""

    def thresholds(self, n):
        # need to take out p_distributions for lru cache, which may be important
        B = self.p_distributions(n)
        I2 = list(np.linspace(0, 1, n + 1)[1:-1])
        return B, I2


# seems constains do not work very well,
# n1 = Symbol('n1', domain=Interval(0,maxi)) # integer=True, positive=True, bounded=True,


class DiscreteSort(StreamSort):
    """it is still bad as maxi should be dinamically calculated"""

    def __init__(self, maxi=1000, rational=False):
        self.maxi = maxi
        self.rational = rational

    def binomial(self, n, k):
        # faster that using sympy Binomial

        # maybe something like n1/(self.maxi - n2?)
        return comb(n, k) * (1 - n1 / self.maxi) ** (n - k) * (n1 / self.maxi) ** (k)

    @lru_cache
    def mP(self, n=1):
        if n in [0, 1]:
            return [1, 1][n]

        B, I = self.thresholds(n)
        I = [0] + I + [self.maxi]
        return simplify(
            sum([Sum(B[i], (n1, I[i] + 1, I[i + 1])) for i in range(n)]) / self.maxi
        )

    @lru_cache
    def p_distributions(self, n):
        # n is the number of boxes
        result = [
            self.binomial(n - 1, i) * self.mP(n - 1 - i) * self.mP(i) for i in range(n)
        ]
        if self.rational:  # not sure if needed anymore
            return result
        return [simplify(r).evalf() for r in result]

    @lru_cache
    def thresholds(self, n):
        B = self.p_distributions(n)
        I = []
        for i in range(0, n - 1):
            #  should be reduce_inequalities with constrains but do not work well
            sol = solve(B[i + 1] - B[i], n1, rational=self.rational)
            sol = sol[1] if sol[0] == 0 else sol[0]
            sol = int(sol)
            I.append(sol)
        return B, I


def index_from_thresholds(tresholds: np.array, x: float):
    """returns the index of the tresholds where x is located"""
    # need to reimplement this with no for loop
    for i, lim in enumerate(tresholds):
        if x < lim:
            return i
    return len(tresholds)


def return_subarray(arr: np.array, n: float):
    """returns the possible positions to place n in arr as well as the limits"""
    tmp = np.append(np.append([0], arr), 1)
    mini = np.argwhere(tmp < n)[-1][0]
    maxi = np.argwhere(tmp > n)[0][0]
    return arr[mini : maxi - 1], tmp[mini], tmp[maxi]


def best_quasi_sort(arr: np.array, thresholds=None):
    """Uses tthe best possible strategy to sort, it works with probability mP(n)
    otherwise it fails to sort.
    This is far from optimized code"""
    # if not isinstance(np.array, arr):
    arr = np.array(arr)
    n = len(arr)
    slots = np.tile(np.nan, n)
    if thresholds is None:
        sorti = InfinitesimalSort()
        thresholds = {i: sorti.thresholds(i)[1] for i in range(n + 1)}
    for ni in arr:
        sub, start, end = return_subarray(slots, ni)
        if len(sub) == 0:
            raise ValueError("No subarray found, not optimally sortable")
        nip = (ni - start) / (end - start)
        idx = index_from_thresholds(thresholds[len(sub)], nip)
        sub[idx] = ni
    return slots


if __name__ == "__main__":
    print(InfinitesimalSort().mP(6))
