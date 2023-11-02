from sympy.stats import Binomial, density
from sympy import Symbol, integrate, solve, Interval, Rational, Sum, simplify
from sympy import integrate as ʃ 
from functools import lru_cache
from math import comb
import sys
from matplotlib import pyplot as plt
from sympy import lambdify, Symbol, Interval
import numpy as np
from abc import ABC, abstractclassmethod


sys.set_int_max_str_digits(0)

n1 = Symbol("n1", domain=Interval(0, 1))

class StreamSort:


    @abstractclassmethod
    def thresholds(self, n, B=None):
        pass

    @abstractclassmethod
    def p_distributions(self, n):
        pass

    
    def plot_OSR(self, n):
        x =  range(1, n)
        prob = np.array([self.mP(i) for i in x])

        plt.scatter(x, prob.astype(float))
        # plt.ylim([0,1])
        plt.xlabel('Number of buckets')
        plt.ylabel('Probability of winning with best strategy')
        # plt.yticks(np.arange(0, 1, 0.1))
        plt.xticks(np.arange(0, 21, 1))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.savefig(f'figures/osr{n=}.png', dpi=300, bbox_inches='tight')
        plt.show()

    def plot_partition_tree(self, n = 20):
        # plot the partition tree from 1 to  n buckets
        plt.figure(figsize=(10, 6))
        for i in range(1,n+1):
            x = [i]*(i-1)
            y = np.array(self.thresholds(i)[1]).astype(float)
            plt.scatter(y,x )
        
        plt.xlabel('$n_1$ k decision threshold')
        plt.ylabel('$n$ numeber of slots')
        plt.xticks(np.arange(0, 1.1, 0.1))
        plt.yticks(np.arange(0, n+1, 1))
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.savefig(f'figures/partition_tree{n=}.png', dpi=300, bbox_inches='tight')
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
        plt.xlabel('$n_1$')
        plt.ylabel('Optimal Success Rate (OSR) given $n_1$ placed in kth bucket')
        plt.title('$p_{nk}$ for 7 slots')
        plt.legend([f"$p_{{n{i}}}$" for i in range(1, n+1)])
        plt.grid(True)
        plt.savefig(f'figures/strategy_domains_{n=}.png', dpi=300, bbox_inches='tight')
        plt.show()
        

    def plot_strategy_domains_at_optimal_range(self, n):
        # Convert symbolic expressions to numerical functions
        functions, ranges = self.thresholds(n)
        numerical_funcs = [lambdify(n1, func, "numpy") for func in functions]

        # Evaluate and plot each function over the interval (0,1)
        
        plt.figure(figsize=(10, 6))
        ranges = [0]    + ranges + [1]
        for i, func in enumerate(numerical_funcs):
            x_vals = np.linspace(float(ranges[i]), float(ranges[i+1]), 2000)
            plt.plot(x_vals, func(x_vals))
            plt.fill_between(x_vals, func(x_vals), color='gray', alpha=0.2, edgecolor='none', label="_nolegend_")

        # Setting plot details
        plt.xlabel('$n_1$')
        plt.ylabel('Optimal Success Rate (OSR)')
        plt.ylim(0)
        plt.title('$P_{nk}$ OSR given $n_1$ placed in kth bucket')
        plt.legend([f"$n_1$ at slot k={i}" for i in range(1, n+1)])
        plt.grid(True)
        plt.savefig(f'figures/strategy_domains_in_range{n=}.png', dpi=300, bbox_inches='tight')
        plt.show()
        



class InfinitesimalSort(StreamSort):

    def __init__(self, rational=False):
        self.maxi = 1
        self.rational = rational


    @lru_cache
    def mP(self, n=1):
        # if n> 9  better using rational = False, otherwise it takes ages
        # as the integrals are symbolic and makes gdc of very large fractions
        # further optimization can be achieved by using symetry, as the inthegral
        # evaluate symetrically in the array.
        if n in [0, 1, 2]:
            return [1, 1, Rational(3, 4)][n]

        B, I = self.thresholds(n) 
        I = [0] + I + [1]
        # maybe a base transformation avoid the gdc as well
        return sum([ʃ(B[i], (n1, Interval(I[i],I[i+1]))) for i in range(n)])


    @lru_cache
    def p_distributions(self, n):
        # n is the number of boxes
        result = [self.binomial(n-1,i) * self.mP(n-1-i) * self.mP(i) for i in range(n)]
        if self.rational:
            return result
        return [r.evalf() for r in result]

    @staticmethod
    def binomial(n,k): # n successes over k trials
        # faster that using sympy Binomial
        # n1 is prob of success tha is integrated latter 
        return comb(n, k)*(1-n1)**(n-k)*n1**(k) 

    @lru_cache
    def binomial2(n, k):
        # this way slower but more sympy :)
        return density(Binomial('X', n, n1))(k)


    def naive_thresholds(self, n):
        # naive version of thesholds
        return np.linspace(0, 1, n-1)


    def thresholds(self, n):
        # need to take out p_distributions for lru cache, which may be important
        B = self.p_distributions(n)
        I = []
        for i in range(0, n-1):
            sol = solve(B[i+1]-B[i], n1)
            sol = sol[1] if sol[0] == 0 else sol[0]
            sol = sol if self.rational else sol.evalf()
            I.append(sol)
        return B, I
        

    def normalization(self, n):
        # todo, but will serves to normalize real use cases
        n = 458
        maxi = 473
        mini = 0
        elements = 9
        print(n-mini)
        (np.array(self.thresholds(elements))*(maxi-mini)).astype(int)

class NaiveInfinitesimalSort(InfinitesimalSort):
    """ The naive version of infinitesimal sort, it turns out to be quite good, but ofc not optimal"""
    def thresholds(self, n):
        # need to take out p_distributions for lru cache, which may be important
        B = self.p_distributions(n)
        I2 = list(np.linspace(0, 1, n+1)[1: -1])
        return B, I2


# seems constains do not work very well, 
# n1 = Symbol('n1', domain=Interval(0,maxi)) # integer=True, positive=True, bounded=True,  

class DiscreteSort(StreamSort):
    ''' it is still bad as maxi should be dinamically calculated'''

    def __init__(self, maxi=1000, rational=False):
        self.maxi = maxi
        self.rational = rational

    def binomial(self, n, k):
        # faster that using sympy Binomial

        # maybe something like n1/(self.maxi - n2?)
        return comb(n, k)*(1-n1/self.maxi)**(n-k)*(n1/self.maxi)**(k)

    @lru_cache
    def mP(self, n=1):
        if n in [0, 1]:
            return [1, 1][n]

        B, I = self.thresholds(n) 
        I = [0] + I + [self.maxi]
        return simplify(sum([Sum(B[i], (n1, I[i]+1,I[i+1])) for i in range(n)])/self.maxi)

    @lru_cache
    def p_distributions(self, n):
        # n is the number of boxes
        result = [self.binomial(n-1,i) * self.mP(n-1-i) * self.mP(i) for i in range(n)]
        if self.rational: # not sure if needed anymore
            return result
        return [simplify(r).evalf() for r in result]

    @lru_cache
    def thresholds(self, n):
        B = self.p_distributions(n)
        I = []
        for i in range(0, n-1):
            #  should be reduce_inequalities with constrains but do not work well
            sol = solve(B[i+1]-B[i], n1, rational=self.rational)
            sol = sol[1] if sol[0] == 0 else sol[0]
            sol = int(sol)
            I.append(sol)
        return B, I


if __name__ == "__main__":
    print(InfinitesimalSort().mP(6))



from functools import wraps

def log_method_call(method):
    """Decorator to log method calls."""
    @wraps(method)
    def wrapper(*args, **kwargs):
        print(f"Calling method {method.__name__} with args {args[1:]} and kwargs {kwargs}")
        return method(*args, **kwargs)
    return wrapper

class LoggingMeta(type):
    """Metaclass that logs method calls."""
    def __new__(cls, name, bases, clsdict):
        # Iterate over items in the class dictionary
        for key, value in clsdict.items():
            if callable(value) and not isinstance(value, staticmethod): 
                clsdict[key] = log_method_call(value) 
            
        return super().__new__(cls, name, bases, clsdict)