from typing import Iterator
from sympy import Sum, Symbol, floor, plot, solve, Float, Function
from sympy.stats import Hypergeometric, density
from functools import lru_cache
import numpy as np
from matplotlib import pyplot as plt


@lru_cache
def hyp(buckets: int, items: int, bucket: int, n: int):
    """ 
    Probabilty of getting the correct distribution:
        /= bucket
    [_][n][_]  items 0...n...items
    ^buckets^
    """
    trials = buckets - 1
    return density(Hypergeometric("H", items - 1, n, trials))(bucket)


def opt_o(buckets: int, items: int):
    """ Optimal threshold of the probability distribution,
    we are using hyp as it would be continuous which is tremendoulsy inncesary,
    but can be plotted nicely for checking what is happening"""
    sols = [0]
    current = 0
    n1 = Symbol("n1")

    for i in range(0, buckets):
        # this is wrong!! it should use pnb D:  !! terrible, cause it is discrete
        sol = solve(hyp(buckets, items, i, n1) - hyp(buckets, items, i + 1, n1))
        for j in sol:
            if j > current:
                sols.append(j)
                current = j
                break
        # print(sol)
    sols.append(items - 1)
    return sols

def dist(buckets, items, n):
    return [pnb(buckets, items, b, n) for b in range(buckets)]

def all_dist(buckets, items):
    return np.array([dist(buckets, items, i) for i in range(items)]).T

def opt(buckets, items):
    all_di = all_dist(buckets,items)
    return [0] + [np.where(all_di[i] > all_di[i+1])[0][-1]  for i in range(buckets-1)] + [items-1]


def int_opt(buckets: int, items: int) -> Iterator[tuple[int, int]]:
    """ convert the continoues values to int ones """
    opts = (floor(i) for i in opt(buckets, items))
    i = next(opts)
    for k in opts:
        f = k if k > i else i
        yield i, f
        i = f + 1

@lru_cache
def pnb(buckets:int, items:int, b:int, n:int) -> Float:
    """ Probability of winning with optimal strategy given that you place
    item at place b
    """
    return hyp(buckets, items, b, n) * P(b, n) * P(buckets - 1 - b, items - n - 1)

@lru_cache
def P(buckets: int, items: int) -> Float:
    """ Calculates The probability of winning with optimal strategy for 
    buckets and items
    
    For instance:s
    
    buckets = 2, items = 3
    [_][_]  0,1,2  P-> 5/6 , 0,2 you win allways by placing it in extrem, 1 you win 1/2 times
    
    buckets = 4, items = 4
    [_][_][_][_]  0,1,2,3  P -> 1 as you only need to place each at index
    """
    if buckets in (0, 1):
        return 1
    if items == buckets:
        return 1
    if items < buckets:
        return 1
    s = 0
    for b, (mi, ma) in enumerate(int_opt(buckets, items)):
        s += sum(pnb(buckets, items, b, n) for n in range(mi, ma + 1))
    return s / items


def P_print():
    # min included max not included, as python convention
    opt_min, opt_max = Function("optmin"), Function("optmax")
    P = Function("P")
    b1 = Symbol("b1")
    n1 =  Symbol("n1")
    buckets = Symbol("B")
    items = Symbol("I")
    pnb_s = lambda buckets, items, b, n: hyp(buckets, items, b, n) * P(b, n - 1) * P(buckets - 1 - b, items - n - 1)
    s = Sum(Sum(pnb_s(buckets, items, b1, n1), (n1, opt_min(b1, buckets, items), opt_max(b1, buckets, items))),
            (b1, 0, buckets-1))
    return s / items

def plot_p_dist(buckets: int, items: int):
    assert buckets<=items, "items cannot be less than buckets"
    n1 = Symbol("n1")
    plot(*[hyp(buckets, items, b, n1) for b in range(buckets)], (n1, 0,items-1))
    
def plot_real_p(buckets, items):

    x = np.arange(buckets)
    for i in range(items):
        y = [pnb(buckets, items, b, i) for b in range(buckets)]
        plt.plot(x, y)
        
def plot_p(buckets, items, lines=False):
    all_di = all_dist(buckets,items)
    opts = opt(buckets, items)
    plt.plot(all_di.T)
    if lines:
        for op in opts:
            plt.axvline(x=op)
    plt.show()