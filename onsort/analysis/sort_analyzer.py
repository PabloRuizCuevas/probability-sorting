from typing import Any, TypeAlias

import numpy as np
import numpy.typing as npt

from onsort.discrete.my_sort import (
    InfinitesimalSort,
    index_from_thresholds,
    create_thresholds,
)

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
