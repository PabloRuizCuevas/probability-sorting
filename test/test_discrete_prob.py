from onsort.discrete_prob import int_opt, opt, P, hyp
from sympy import Rational


def test_int_opt_same_buckets_as_items():
    assert list(int_opt(1, 1)) == [(0, 0)]
    assert list(int_opt(2, 2)) == [(0, 0), (1, 1)]
    assert list(int_opt(3, 3)) == [(0, 0), (1, 1), (2, 2)]


def test_int_opt_more_items():
    assert list(int_opt(3, 5)) == [(0, 1), (2, 3), (4, 4)]
    assert list(int_opt(2, 5)) == [(0, 2), (3, 4)]
    assert list(int_opt(2, 10)) == [(0, 4), (5, 9)]


def test_opt():
    assert opt(3, 3) == [0, Rational(1, 3), Rational(5, 3), 2]
    assert opt(3, 5) == [0, 1, 3, 4]
    assert opt(4, 7) == [0, 1, 3, 5, 6]


def test_p():
    assert P(2, 3) == Rational(5, 6)  # 1 + 1/2 + 1   /3
    assert P(2, 4) == Rational(5, 6)  # 1 + 2/3 + 2/3 + 1   /4
    assert P(2, 5) == Rational(4, 5)  # 1 + 2/3 + 2/3 + 1   /4
    assert P(2, 6) == Rational(4, 5)
    assert P(3, 4) == Rational(3, 4)
    assert P(4, 5) == Rational(13, 20)

def test_pb_n():
    assert hyp(3,3,1,1) == 1  #  [_][1][_]
    assert hyp(3,3,2,1) == 0  #  [_][_][1]
    assert hyp(3,3,1,2) == 0  #  [_][2][_]
    
    assert hyp(4,4,1,2) == 0  #  [_][2][_][_]
    assert hyp(4,4,1,1) == 1  #  [_][1][_][_]   0,1,2,3
    assert hyp(4,5,1,1) == Rational(3, 4)  #  [_][1][_][_]  0,1,2,3,4   0,2,3,4  -> 3 over 4 times we have the 0