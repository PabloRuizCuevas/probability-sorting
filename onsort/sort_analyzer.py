from typing import Any, TypeAlias

import numpy as np
import numpy.typing as npt

from onsort.my_sort import InfinitesimalSort, index_from_thresholds, create_thresholds

FArray: TypeAlias = npt.NDArray[np.float64]


def disorder(arr: FArray) -> list[float]:
    # Sort the array and create a mapping from value to its sorted position
    sorted_positions = {value: idx for idx, value in enumerate(sorted(arr))}

    # Calculate the absolute distance between each element's position and its sorted position
    return [abs(idx - sorted_positions[value]) for idx, value in enumerate(arr)]


def measure_disorder(arr: FArray) -> tuple[float, float, float]:
    distances = disorder(arr)
    # Calculate average, max, and median distance
    average_distance = float(np.mean(distances))
    max_distance = float(np.max(distances))
    median_distance = float(np.median(distances))

    return average_distance, max_distance, median_distance


# -------------------------# from here DEPRECATED # -------------------------#


def placeit_dir(slots: FArray, idx: int, ni: float, direction: int) -> FArray:
    if idx in [-1, len(slots)]:
        # reached the end of the array change direction
        direction = -direction
        idx = idx + 2 * direction

    if slots[idx] != 0:
        slots = placeit_dir(slots, idx + direction, ni, direction)
    else:
        slots[idx] = ni
    return slots


def quasi_sort_dir(arr: FArray, thresholds: list[float] | None = None) -> FArray:
    """Uses thresholds to sort the array into slots, if slot occupied,
    place in next  empsty slot"""
    arr = np.array(arr)
    n = len(arr)
    slots = np.zeros(n)
    if thresholds is None:
        thresholds = InfinitesimalSort().thresholds(n)[1]

    for ni in arr:
        idx = index_from_thresholds(thresholds, ni)
        # idx = [ i for i, v in enumerate(np.append([0],tresholds)) if v < ni][-1]

        if slots[idx] != 0:
            direction = 1 if ni > slots[idx] else -1
            slots = placeit_dir(
                slots, idx + direction, ni, direction
            )  # better pass idx+direction
        else:
            slots[idx] = ni

    return slots


# almost the best algorithm, but still not aligned with theoretical best.


def placeit(slots: FArray, idx: int, ni: float, direction: int) -> FArray:
    # tries to place it in the allowed direction, if not possible, raises error
    if idx in [-1, len(slots)]:
        raise ValueError("Out of bounds")
    if slots[idx] != 0:
        if direction == 1 and slots[idx] < ni:
            return placeit(slots, idx + direction, ni, direction)
        elif direction == -1 and slots[idx] > ni:
            return placeit(slots, idx + direction, ni, direction)
        else:
            raise ValueError("Cannot place")
    else:
        slots[idx] = ni
        return slots


def quasi_sort(arr: FArray, thresholds: list[float] | None = None) -> FArray:
    """Uses thresholds to sort the array into slots, if slot occupied,
    this function tries to directly place, it fails it goes right and left looking for placing
    the element
    if element cannot be placed, then it uses the empty slots as the full array to sort
    """
    arr = np.array(arr)
    n = len(arr)
    slots = np.zeros(n)
    if thresholds is None:
        thresholds = InfinitesimalSort().thresholds(n)[1]

    for i, ni in enumerate(arr):
        idx = index_from_thresholds(thresholds, ni)
        if slots[idx] != 0:
            direction = 1 if ni > slots[idx] else -1
            try:
                slots = placeit(slots, idx + direction, ni, direction)
            except ValueError:
                # fall here when it cannot place something
                # so we try to sort the rest of the array in the empty slots
                slots[slots == 0] = quasi_sort(arr[i:])
                break
        else:
            slots[idx] = ni
    return slots


def quasi_sort_two(
    arr: FArray, thresholds: dict[int, list[float]] | None, k: int = 1
) -> FArray:
    """Uses thresholds to sort the array into slots, if slot occupied, it uses the empty slots
    to sort them in a recursive way,

    This is still not he best algorithm because it ignores the values on the extremes, so it does
    not renormalize the n_m"""
    n = len(arr)
    slots = np.zeros(n)
    if thresholds is None or len(thresholds.keys()) <= n:
        thresholds = create_thresholds(n)

    for i, ni in enumerate(arr):
        idx = index_from_thresholds(thresholds, ni)
        if slots[idx] != 0:
            k = slots[idx]
            slots[slots == 0] = quasi_sort_two(arr[i:], thresholds, k=k)
            break
        else:
            slots[idx] = ni
    return slots


def quasi_sort_three(
    arr: FArray, thresholds: dict[int, list[float]] | None = None
) -> FArray:
    """This is similar to best algorithm but ignoring whatever is place as it would not
    exist, so it is not optimal, but is close to optimal"""
    n = len(arr)
    if n == 1:
        return arr
    slots = np.tile(np.nan, n)
    if thresholds is None or len(thresholds.keys()) <= n:
        thresholds = create_thresholds(n)

    element = arr[0]
    idx = index_from_thresholds(thresholds[len(arr)], element)
    slots[idx] = element
    slots[np.isnan(slots)] = quasi_sort_three(arr[1:], thresholds)
    return slots


def plot_sort_analysis(n: int, trials: int = 500) -> None:
    from matplotlib import pyplot as plt

    my_random = np.random.uniform(0, 1, [trials, n])
    tresholds = InfinitesimalSort().thresholds(n)[1]
    original_disorder = []
    disorder_after_sort = []
    disorder_after_sort_dir = []
    for random in my_random:
        original_disorder.append(np.mean(disorder(random)))
        disorder_after_sort.append(np.mean(disorder(quasi_sort(random, tresholds))))
        disorder_after_sort_dir.append(
            np.mean(disorder(quasi_sort_dir(random, tresholds)))
        )

    kargs: dict[str, Any] = {"alpha": 0.5, "density": True, "bins": 20, "range": (0, 3)}

    plt.hist(original_disorder, label="original", **kargs)
    plt.hist(disorder_after_sort, label="recursive", **kargs)
    plt.hist(disorder_after_sort_dir, label="directional", **kargs)
    plt.title("Mean disorder distribution after and before sorting")
    plt.xlabel("Mean disorder")
    plt.ylabel("Density")
    plt.legend(loc="upper right")
    plt.savefig(f"figures/plot_sort_analiysis_{n}.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    trials = 100
    n = 3
    my_random = np.random.uniform(0, 1, [trials, n])
    thresholds = InfinitesimalSort().thresholds(n)[1]
    dis = []
    for random in my_random:
        dis.append(np.mean(disorder(quasi_sort_two(random, thresholds))))
    dis = np.array(dis)
    len(dis[dis == 0]) / trials
