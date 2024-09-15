from sympy import Symbol
from sympy import Interval, Expr, Rational, Integral, S, solveset
from sympy.stats import Binomial, density
from functools import cache


n1 = Symbol("n1", positive=True)


def dist(buckets: int, b: int, n: int) -> list[Expr]:
    """buckets"""
    return binomial(buckets - 1, b, n) * Pn(buckets - 1 - b) * Pn(b)


@staticmethod
def binomial(buckets: int, b: int, n) -> Expr:
    return density(Binomial("X", buckets, n))(b)


def opt(buckets: int, b: int) -> Interval:
    """Optimal threshold of n buckets we get it by placing on b and check with buckets-1"""
    if b == 0:
        return solveset(
            dist(buckets, 0, n1) > dist(buckets, 1, n1), domain=Interval(0, 1)
        )
    if b == buckets - 1:
        return solveset(
            dist(buckets, buckets - 2, n1) < dist(buckets, buckets - 1, n1),
            domain=Interval(0, 1),
        )
    else:
        i1 = dist(buckets, b - 1, n1) > dist(buckets, b, n1)
        i2 = dist(buckets, b, n1) > dist(buckets, b + 1, n1)
        return Interval(
            solveset(i1, domain=Interval(0, 1)).end,
            solveset(i2, domain=Interval(0, 1)).end,
        )


@cache
def Pn(buckets: int = 1) -> float | Rational:
    # print("AQUI", buckets)
    # if n> 9  better using rational = False, otherwise it takes ages
    # as the integrals are symbolic and makes gdc of very large fractions
    # further optimization can be achieved by using symmetry, as the integral
    # evaluate symetrically in the array, same for thresholds
    if buckets < 2:
        return S(1)
    else:
        # b = Symbol("b", integer=True, positive=True)
        # return Sum(Integral(dist(buckets, b, n1), (n1, opt(buckets, b))), (b,0,buckets))
        return sum(
            Integral(dist(buckets, b, n1), (n1, opt(buckets, b)))
            for b in range(buckets)
        )


if __name__ == "__main__":
    print(Pn(3))
