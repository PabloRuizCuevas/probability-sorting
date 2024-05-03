
import sys
from functools import lru_cache
from math import comb
from sympy import Expr, Interval, Rational, Symbol
from sympy import integrate as ʃ
from sympy import solve

sys.set_int_max_str_digits(0)

RATIONAL = True


@lru_cache
def p_distributions(buckets: int) -> list[Expr]:
    """ n is the number of boxes """ 
    n1 = Symbol("n1", domain=Interval(0, 1))
    
    result = [binomial(buckets - 1, b, n1) * P(buckets - 1 - b) * P(b) for b in range(buckets)]
    if RATIONAL:
        return result
    return [r.evalf() for r in result]

@staticmethod
def binomial(buckets: int, k: int, n: float) -> Expr: 
    # n successes over k trials
    # faster that using sympy Binomial
    # n1 is prob of success tha is integrated latter
    sol: Expr = comb(buckets, k) * (1 - n) ** (buckets - k) * n ** (k)
    # density(Binomial("X", n, n1))(k) #sympy version
    return sol

@lru_cache
def thresholds(buckets: int) -> tuple[list[Expr], list[float]]:
    # need to take out p_distributions for lru cache, which may be important
    B = p_distributions(buckets)
    I = [0]
    for i in range(0, buckets - 1):
        sol = solve(B[i + 1] - B[i])
        sol = sol[1] if sol[0] == 0 else sol[0]
        sol = sol if RATIONAL else sol.evalf()
        I.append(sol)
    I.append(1)
    return B, I

@lru_cache
def P(buckets: int = 1) -> float | Rational:
    # if n> 9  better using rational = False, otherwise it takes ages
    # as the integrals are symbolic and makes gdc of very large fractions
    # further optimization can be achieved by using symmetry, as the integral
    # evaluate symetrically in the array, same for thresholds
    
    probability: float | Rational
    if buckets in [0, 1, 2]:
        probability = [1, 1, Rational(3, 4)][buckets]
    else:
        B, I = thresholds(buckets)
        # maybe a base transformation avoid the gdc as well
        probability = sum(ʃ(B[b], (I[b], I[b + 1])) for b in range(buckets))
    return probability