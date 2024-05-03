from sympy import Float
from sympy.stats import Hypergeometric, density
from functools import lru_cache
import numpy as np


@lru_cache
def hyp(buckets: int, items: int, bucket: int, n: int) -> Float:
    """
    Probabilty of getting the correct distribution:
        /= bucket
    [_][n][_]  items 0...n...items
    ^buckets^
    """
    trials = buckets - 1
    return density(Hypergeometric("H", items - 1, n, trials))(bucket)


def dist(buckets: int, items: int, n: int) -> list:
    """Probabiliby of winning for each bucket by placing the first element n on it"""
    return [pnb(buckets, items, b, n) for b in range(buckets)]


def distn(buckets: int, items: int, b: int) -> list:
    """Probabiliby of winning for each possible item when placed in the bucket b"""
    return [pnb(buckets, items, b, n) for n in range(items)]


def all_dist(buckets: int, items: int) -> np.ndarray:
    """Probability map of winning with best possible strategy for each bucket and item"""
    return np.array([distn(buckets, items, i) for i in range(buckets)])


@lru_cache
def best_bucket_for_item(buckets: int, items: int) -> np.ndarray:
    """Brute forces the best bucket to place the each item, 
    Technically may be possible to get it in a smarter or even analytical way.
    """
    return np.argmax(all_dist(buckets, items), axis=0)  # brute force


@lru_cache
def pnb(buckets: int, items: int, b: int, n: int) -> Float:
    """PNB -> Probability of winning by placing the item N in bucket B"""
    return hyp(buckets, items, b, n) * P(b, n) * P(buckets - 1 - b, items - n - 1)


@lru_cache
def P(buckets: int, items: int) -> Float:
    """Calculates The probability of winning with optimal strategy for
    buckets and items

    For instance:s

    buckets = 2, items = 3
    [_][_]  0,1,2  P-> 5/6 , 0,2 you win allways by placing it in extrem, 1 you win 1/2 times

    buckets = 4, items = 4
    [_][_][_][_]  0,1,2,3  P -> 1 as you only need to place each at index
    """
    if buckets in (0, 1):
        return 1
    if items <= buckets:
        return 1

    best_b = best_bucket_for_item(buckets, items)  # brute force
    return sum(pnb(buckets, items, best_b[n], n) for n in range(items)) / items
