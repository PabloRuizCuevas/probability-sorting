from typing import Generator, TypeAlias
import numpy as np
import numpy.typing as npt

from onsort.cont_thresholds import THRESHOLDS
from onsort.my_sort import index_from_thresholds, return_subarray


FArray: TypeAlias = npt.NDArray[np.float64]


def sort(n_buckets: int) -> Generator[FArray, float, None]:
    """online uniform sort for n number of elements waited"""
    slots = np.tile(np.nan, n_buckets)
    n = yield slots
    for _ in range(n_buckets):
        slots = sort_item(n, slots)
        n = yield slots
    yield None


def sort_item(n: float, slots: FArray) -> FArray:
    """Place the nuber n in his slot,
    the usage of THRESHOLDS makes this function only work for n<= 10 but can be easily changed
    """
    sub, start, end = return_subarray(slots, n)
    if len(sub) == 0:
        raise ValueError("No subarray found, not optimally sortable")
    nip = (n - start) / (end - start)
    idx = index_from_thresholds(THRESHOLDS[len(sub)], nip)
    sub[idx] = n  # this changes slots in memory, not very explicit
    return slots


if __name__ == "__main__":
    arr = [0.76931784, 0.06506234, 0.07066391, 0.70643678, 0.94615554]
    sort_gen = sort(5)
    slots = next(sort_gen)  # initialize generator
    for n in arr:
        slots = sort_gen.send(n)
        print(slots)
