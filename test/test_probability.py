import numpy as np
import pytest
from sympy import Rational

from onsort.my_sort import InfinitesimalSort, sort

test_cases = [(1, 1), (2, Rational(3, 4)), (3, Rational(377, 726))]


@pytest.mark.parametrize("n, Prob", test_cases)
def test_probabilities_exact(n: int, Prob: float) -> None:
    optimal = InfinitesimalSort(True)
    p = optimal.mP(n)
    assert p == Prob, f"mP({n}) = {p} != {Prob}"


err = 0.0001
test_cases2 = [(1, 1), (2, 0.75), (3, 0.519283), (4, 0.3435841)]


@pytest.mark.parametrize("n, Prob", test_cases2)
def test_probabilities(n: int, Prob: float) -> None:
    optimal = InfinitesimalSort()
    assert (
        abs(float(optimal.mP(n)) - Prob) < err
    ), f"mP({n}) = {optimal.mP(n)} != {Prob}"


err2 = 0.05
test_cases3 = [1, 2, 3, 4]


@pytest.mark.parametrize("n", test_cases3)
def test_theory_with_algorithm(n: int) -> None:
    # this test is probabilistic, maybe not the best thing... but it can fail just because of that
    # ideally you put here a while and a epsilon, but would need to put a couple of conditions
    l = []
    trials = 10000
    optimal = InfinitesimalSort()
    thresholds = {i: optimal.thresholds(i)[1] for i in range(10)}
    arrays = np.random.uniform(0, 1, (trials, n))
    for random in arrays:
        try:
            a = sort(random, thresholds)
            l.append(a)
        except:
            pass

    proportion = len(l) / trials
    proportion_expected = optimal.mP(n)
    num = (proportion + proportion_expected) / proportion_expected - 2
    assert num < err2, f"mP({n}) = {proportion} != {proportion_expected}"
