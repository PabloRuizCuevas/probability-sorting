import pytest
from sympy import Rational

from onsort.discrete.discrete_prob_symb import hyp, P


def test_p():
    assert P(2, 3) == Rational(5, 6)  # 1 + 1/2 + 1   /3
    assert P(2, 4) == Rational(5, 6)  # 1 + 2/3 + 2/3 + 1   /4
    assert P(2, 5) == Rational(4, 5)  # 1 + 2/3 + 2/3 + 1   /4
    assert P(2, 6) == Rational(4, 5)
    assert P(3, 4) == Rational(3, 4)
    assert P(4, 5) == Rational(13, 20)


def test_pb_n():
    assert hyp(3, 3, 1, 1) == 1  #  [_][1][_]
    assert hyp(3, 3, 2, 1) == 0  #  [_][_][1]
    assert hyp(3, 3, 1, 2) == 0  #  [_][2][_]

    assert hyp(4, 4, 1, 2) == 0  #  [_][2][_][_]
    assert hyp(4, 4, 1, 1) == 1  #  [_][1][_][_]   0,1,2,3
    assert hyp(4, 5, 1, 1) == Rational(
        3, 4
    )  #  [_][1][_][_]  0,1,2,3,4   0,2,3,4  -> 3 over 4 times we have the 0
