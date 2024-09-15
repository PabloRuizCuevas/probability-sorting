import sys
from typing import TypeAlias

import numpy as np
import numpy.typing as npt

from onsort.continuous.cont_prob import thresholds


sys.set_int_max_str_digits(0)


FArray: TypeAlias = npt.NDArray[np.float64]


# Sort algorithm


def index_from_thresholds(tresholds: list[float], x: float) -> int:
    """returns the index of the tresholds where x is located"""
    # need to reimplement this with no for loop
    for i, lim in enumerate(tresholds):
        if x < lim:
            return i
    return len(tresholds)


def return_subarray(arr: FArray, n: float) -> tuple[FArray, float, float]:
    """returns the possible positions to place n in arr as well as the limits"""
    tmp = np.append(np.append([0], arr), 1)
    mini = np.argwhere(tmp < n)[-1][0]
    maxi = np.argwhere(tmp > n)[0][0]
    return arr[mini : maxi - 1], tmp[mini], tmp[maxi]


def create_thresholds(n: int) -> dict[int, list[float]]:
    """creates the thresholds for each n"""
    return {i: thresholds(n, i)[1] for i in range(n + 1)}


def sort(
    arr: FArray,
    thresholds: dict[int, list[float]] | None = None,
    raise_error: bool = True,
) -> FArray:
    """Uses tthe best possible strategy to sort, it works with probability mP(n)
    otherwise it fails to sort.
    This is far from optimized code"""
    # if not isinstance(np.array, arr):
    n = len(arr)
    slots = np.tile(np.nan, n)
    if thresholds is None or len(thresholds.keys()) <= n:
        thresholds = create_thresholds(n)

    for i, ni in enumerate(arr):
        sub, start, end = return_subarray(slots, ni)
        if len(sub) == 0:
            # If enters here it means it is not optimally sortable
            if raise_error:
                raise ValueError("No subarray found, not optimally sortable")
            # As of my resarch now, this part algorithm, i.e
            # when fails, it does not satisfy some desirable properties.
            slots[np.isnan(slots)] = sort(arr[i:], thresholds, raise_error)
            break
        else:
            nip = (ni - start) / (end - start)
            idx = index_from_thresholds(thresholds[len(sub)], nip)
            sub[idx] = ni
    return slots
