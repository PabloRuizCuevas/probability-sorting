from sympy import Float, Integer
from functools import cache
import numpy as np
from sympy.stats import Hypergeometric, density


def hyp_sym(buckets: int, items: int, bucket: int, n: int) -> Float:
    """Use this if you want exact solutions, no float arithmetic"""
    trials = buckets - 1
    return density(Hypergeometric("H", items - 1, n, trials))(bucket)


def dist(buckets: int, items: int, n: int) -> list:
    """Probabiliby of winning for each bucket by placing the first element n on it"""
    return [pnb(buckets, items, b, n) for b in range(buckets)]


def pnb_sim(buckets: int, items: int, b: int, n: int) -> Float:
    """Same as pnb but exploiting symmetries, use if cache is used"""
    if ((buckets - b - 1) < b) or ((items - n - 1) < items):
        return pnb(buckets, items, buckets - b - 1, items - n - 1)
    return pnb(buckets, items, b, n)


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
    return hyp_sym(buckets, items, b, n) * P(b, n) * P(buckets - 1 - b, items - n - 1)


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
