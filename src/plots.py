from abc import abstractclassmethod

import numpy as np
from matplotlib import pyplot as plt
from sympy import Interval, Symbol, lambdify

n1 = Symbol("n1", domain=Interval(0, 1))  # better not here


class StreamSort:
    @abstractclassmethod
    def thresholds(self, n, B=None):
        pass

    @abstractclassmethod
    def p_distributions(self, n):
        pass

    @abstractclassmethod
    def mP(self, n=1):
        pass

    def plot_OSR(self, n):
        x = range(1, n)
        prob = np.array([self.mP(i) for i in x])

        plt.scatter(x, prob.astype(float))
        # plt.ylim([0,1])
        plt.xlabel("Number of buckets")
        plt.ylabel("OSR (Log Scale)")
        plt.yscale("log")
        # plt.yticks(np.arange(0, 1, 0.1))
        plt.xticks(np.arange(0, 21, 1))
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.savefig(
            f"figures/{self.__class__.__name__}_osr_{n}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()

    def plot_partition_tree(self, n=20):
        # plot the partition tree from 1 to  n buckets
        plt.figure(figsize=(10, 6))
        for i in range(1, n + 1):
            x = [i] * (i - 1)
            y = np.array(self.thresholds(i)[1]).astype(float)
            plt.scatter(y, x)

        plt.xlabel("$n_1$ k decision threshold")
        plt.ylabel("$n$ numeber of slots")
        plt.xticks(np.arange(0, 1.1, 0.1))
        plt.yticks(np.arange(0, n + 1, 1))
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.savefig(
            f"figures/{self.__class__.__name__}_tree_{n}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()

    def plot_strategy_domains(self, n):
        # Convert symbolic expressions to numerical functions
        functions = self.p_distributions(n)
        numerical_funcs = [lambdify(n1, func, "numpy") for func in functions]

        # Evaluate and plot each function over the interval (0,1)
        x_vals = np.linspace(0, 1, 400)
        plt.figure(figsize=(10, 6))
        for func in numerical_funcs:
            plt.plot(x_vals, func(x_vals))

        # Setting plot details
        plt.xlabel("$n_1$")
        plt.ylabel("Optimal Success Rate (OSR) given $n_1$ placed in kth bucket")
        plt.title("$p_{nk}$ for 7 slots")
        plt.legend([f"$p_{{n{i}}}$" for i in range(1, n + 1)])
        plt.grid(True)
        plt.savefig(
            f"figures/{self.__class__.__name__}_domains_{n}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()

    def plot_strategy_domains_at_optimal_range(self, n):
        # Convert symbolic expressions to numerical functions
        functions, ranges = self.thresholds(n)
        numerical_funcs = [lambdify(n1, func, "numpy") for func in functions]

        # Evaluate and plot each function over the interval (0,1)

        plt.figure(figsize=(10, 6))
        ranges = [0] + ranges + [1]
        for i, func in enumerate(numerical_funcs):
            x_vals = np.linspace(float(ranges[i]), float(ranges[i + 1]), 2000)
            plt.plot(x_vals, func(x_vals))
            plt.fill_between(
                x_vals,
                func(x_vals),
                color="gray",
                alpha=0.2,
                edgecolor="none",
                label="_nolegend_",
            )

        # Setting plot details
        plt.xlabel("$n_1$")
        plt.ylabel("Optimal Success Rate (OSR)")
        plt.ylim(0)
        plt.title("$P_{nk}$ OSR given $n_1$ placed in kth bucket")
        plt.legend([f"$n_1$ at slot k={i}" for i in range(1, n + 1)])
        plt.grid(True)
        plt.savefig(
            f"figures/{self.__class__.__name__}_domains_in_range_{n}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()
