from sympy.stats import Binomial, density
from sympy import Symbol, integrate, solve, Interval, Rational
from sympy import integrate as ʃ 
from functools import lru_cache
from math import comb
import sys
from matplotlib import pyplot as plt
from sympy import lambdify, Symbol, Interval
import numpy as np
sys.set_int_max_str_digits(0)

n1 = Symbol("n1", domain=Interval(0, 1))

@lru_cache
def mP(n=1, rational=False):
    # if n> 9  better using rational = False, otherwise it takes ages
    # as the integrals are symbolic and makes gdc of very large fractions
    # further optimization can be achieved by using symetry, as the inthegral
    # evaluate symetrically in the array.
    if n in [0, 1, 2]:
        return [1, 1, Rational(3, 4)][n]

    B = p_distributions(n, rational=rational)
    I = [0]
    for i in range(0, n-1):
        sol = solve(B[i+1]-B[i], n1)
        sol = sol[1] if sol[0] == 0 else sol[0]
        sol = sol if rational else sol.evalf()
        I.append(sol)
    I.append(1)
    return sum([ʃ(B[i], (n1, Interval(I[i],I[i+1]))) for i in range(n)])


@lru_cache
def p_distributions(n, rational=False):
    # n is the number of boxes
    result = [binomial(n-1,i) * mP(n-1-i, rational) * mP(i, rational) for i in range(n)]
    if rational:
        return result
    return [r.evalf() for r in result]


def binomial(n,k):
    # faster that using sympy Binomial
    return comb(n, k)*(1-n1)**(n-k)*n1**(k)

@lru_cache
def binomial2(n, k):
    # this way slower but more sympy :)
    X = Binomial('X', n, n1)
    return density(X)(k)


def naive_thresholds(n):
    # naive version of thesholds
    return np.linspace(0, 1, n-1)

@lru_cache
def thresholds(n, rational=False):
    B = p_distributions(n, rational=rational)
    I = []
    for i in range(0, n-1):
        sol = solve(B[i+1]-B[i], n1)
        sol = sol[1] if sol[0] == 0 else sol[0]
        sol = sol if rational else sol.evalf()
        I.append(sol)

    return I
    
def normalization(n):
    # todo, but it serves to normalize real use cases
    n = 458
    maxi = 473
    mini = 0
    elements = 9
    print(n-mini)
    (np.array(thresholds(elements))*(maxi-mini)).astype(int)

def plot_partition_tree(n = 20, rational=False):
    # plot the partition tree from 1 to  n buckets
    for i in range(1,n+1):
        x = [i]*(i-1)
        y = np.array(thresholds(i, rational)).astype(float)
        plt.scatter(y,x )
    plt.xlabel('partition threshold')
    plt.ylabel('Buckets')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, n, 1))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()


def plot_strategy_domains(n, rational=False):
    # Convert symbolic expressions to numerical functions
    functions = p_distributions(n, rational)
    numerical_funcs = [lambdify(n1, func, "numpy") for func in functions]

    # Evaluate and plot each function over the interval (0,1)
    x_vals = np.linspace(0, 1, 400)
    plt.figure(figsize=(10, 6))
    for func in numerical_funcs:
        plt.plot(x_vals, func(x_vals))

    # Setting plot details
    plt.xlabel('n1')
    plt.ylabel('Value')
    plt.title('Plot of the given functions over (0,1)')
    plt.legend([f"Strategy_{i}" for i in range(1, n+1)])
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    print(mP(10, rational=False))