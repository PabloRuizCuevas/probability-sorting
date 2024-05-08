from matplotlib import pyplot as plt
from sympy import Symbol, plot, Sum, Symbol, Function

from onsort.discrete_prob import hyp, pnb, P
from onsort.my_sort import InfinitesimalSort
import numpy as np


def plot_p_dist(buckets: int, items: int):
    assert buckets <= items, "items cannot be less than buckets"
    n1 = Symbol("n1")
    plot(*[hyp(buckets, items, b, n1) for b in range(buckets)], (n1, 0, items - 1))


def plot_real_p(buckets: int, items: int):
    x = np.arange(buckets)
    for i in range(items):
        y = [pnb(buckets, items, b, i) for b in range(buckets)]
        plt.plot(x, y)


def plot_optimal_asymptotic(buckets=4, items=10):
    for b in range(1, buckets):
        plt.plot([P(b, i) for i in range(items)], label=f"{b} Slots")
        plt.axhline(y=float(InfinitesimalSort(False).mP(b)))
    plt.title("Optimal success asymptotic behaviour with Items")
    plt.axhline(y=1, label="Infinite Items")
    plt.ylabel("Optimal Success Rate")
    plt.xlabel("Number of Items to place")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend(loc="upper right")
    plt.savefig(
        f"figures/OSR_asymptotic_{buckets}_{items}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()


def bprint(buckets, items, bucket, item, eq=False):
    trials = buckets - 1
    h = f" 0-{items-1}"
    print("".join("[_]" if i != bucket else f"[{item}]" for i in range(trials + 1)) + h)
    if eq:  # print continous approx
        print()
        print(
            f"Items: 0-{1}: \n"
            + "".join(
                "[_]" if i != bucket else f"[{item/items:f}]" for i in range(trials + 1)
            )
        )


def P_print():
    # min included max not included, as python convention
    opt_min, opt_max = Function("optmin"), Function("optmax")
    P = Function("P")
    b1 = Symbol("b1")
    n1 = Symbol("n1")
    buckets = Symbol("B")
    items = Symbol("I")
    pnb_s = (
        lambda buckets, items, b, n: hyp(buckets, items, b, n)
        * P(b, n - 1)
        * P(buckets - 1 - b, items - n - 1)
    )
    s = Sum(
        Sum(
            pnb_s(buckets, items, b1, n1),
            (n1, opt_min(b1, buckets, items), opt_max(b1, buckets, items)),
        ),
        (b1, 0, buckets - 1),
    )
    return s / items


def continous_comparison(buckets, items):
    
    from onsort.my_sort import InfinitesimalSort, n1

    buckets = 4
    items = 40
    opts = plot_p(buckets, items)
    plot(*InfinitesimalSort(False).p_distributions(buckets), (n1, 0, 1))
