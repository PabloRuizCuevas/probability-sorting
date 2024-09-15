from sympy import Float, Integer
from functools import cache
import numpy as np
import math
from sympy.stats import Hypergeometric, density


@cache
def comb(n, k):
    # this optimization doesn't save that much time
    return math.comb(n, k)


def hyper(k, M, n, N):
    """faster implementation I could do for hypergeometrical"""
    return comb(n, k) * comb(M - n, N - k) / comb(M, N)


# Actual algorithm:


def hyp(buckets: int, items: int, bucket: int, n: int) -> float:
    """
    Probabilty of getting the correct distribution:
        /= bucket
    [_][n][_]  items 0...n...items
    ^buckets^

    trials = buckets - 1
    """
    return hyper(bucket, items - 1, n, buckets - 1)


def distn(buckets: int, items: int, b: int) -> list[float]:
    """Probabiliby of winning for each possible item when placed in the bucket b"""
    return [pnb(buckets, items, b, n) for n in range(items)]


def all_dist(buckets: int, items: int) -> np.ndarray:
    """Probability map of winning with best possible stegy for each bucket and item"""
    return np.array([distn(buckets, items, i) for i in range(buckets)])


def best_bucket_for_item(buckets: int, items: int) -> np.ndarray:
    """Brute forces the best bucket to place the each item,
    Technically may be possible to get it in a smarter or even analytical way.
    """
    return np.argmax(all_dist(buckets, items), axis=0)  # brute force


def pnb(buckets: int, items: int, b: int, n: int) -> float:
    """PNB -> Probability of winning by placing the item N in bucket B"""
    return hyp(buckets, items, b, n) * P(b, n) * P(buckets - 1 - b, items - n - 1)


@cache
def P(buckets: int, items: int) -> float:
    """Calculates The probability of winning with optimal strategy for
    buckets and items

    buckets = 2, items = 3
    [_][_]  0,1,2  P-> 5/6 , 0,2 you win allways by placing it in extrem, 1 you win 1/2 times

    buckets = 4, items = 4
    [_][_][_][_]  0,1,2,3  P -> 1 as you only need to place each at index
    """
    print(f"P({buckets}, {items})")
    if buckets in (0, 1):
        return Integer(1)
    if items <= buckets:
        return 1

    best_b = best_bucket_for_item(buckets, items)  # brute force
    return sum(pnb(buckets, items, best_b[n], n) for n in range(items)) / items


if __name__ == "__main__":
    import time

    start = time.time()
    p = P(10, 999)
    print(f"P20 = {p}")
    end = time.time()
    print(end - start)
