

from matplotlib import pyplot as plt
import numpy as np
from sympy import Symbol, plot

from onsort.discrete_prob import all_dist, hyp, opt, pnb
from onsort.my_sort import InfinitesimalSort


def plot_p_dist(buckets: int, items: int):
    assert buckets<=items, "items cannot be less than buckets"
    n1 = Symbol("n1")
    plot(*[hyp(buckets, items, b, n1) for b in range(buckets)], (n1, 0,items-1))
    
    
def plot_real_p(buckets, items):

    x = np.arange(buckets)
    for i in range(items):
        y = [pnb(buckets, items, b, i) for b in range(buckets)]
        plt.plot(x, y)

    
def plot_p(buckets: int, items: int, lines=False):
    all_di = all_dist(buckets,items)
    opts = opt(buckets, items)
    plt.plot(all_di.T)
    if lines:
        for op in opts:
            plt.axvline(x=op)
    plt.show()
    
    
def plot_optimal_asymptotic(buckets=4, items=10):
    for b in range(1,buckets):
        plt.plot([P(b,i) for i in range(items)], label=f'{b} Slots')
        plt.axhline(y=float(InfinitesimalSort(False).mP(b)))
    plt.title('Optimal success asymptotic behaviour with Items')
    plt.axhline(y=1, label='Infinite Items')
    plt.ylabel('Optimal Success Rate')
    plt.xlabel('Number of Items to place')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper right')
    plt.savefig(
        f"figures/OSR_asymptotic_{buckets}_{items}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()