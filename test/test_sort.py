from typing import TypeAlias
# export PYTHONPATH=$PYTHONPATH:$(pwd)
import numpy as np
import pytest
from numpy import testing as npt

from src.my_sort import InfinitesimalSort, best_quasi_sort, return_subarray


optimal = InfinitesimalSort()
nan = np.nan

test_cases = [
    ([nan, nan, nan, nan, nan, nan], 0.3, [nan, nan, nan, nan, nan, nan], 0, 1),
    ([nan, nan, 0.2, nan, nan, nan], 0.3, [nan, nan, nan], 0.2, 1),
    ([nan, nan, 0.2, nan, 0.4, nan], 0.3, [nan], 0.2, 0.4),
    ([0.1, nan, 0.4, nan, nan, 0.8], 0.5, [nan, nan], 0.4, 0.8),
    ([nan, nan, 0.4, nan, nan, 0.8], 0.2, [nan, nan], 0.0, 0.4),
]


@pytest.mark.parametrize("input, threshold, expected, mini, maxi", test_cases)
def test_return_subarray(
    input: list[float],
    threshold: float,
    expected: list[float],
    mini: float,
    maxi: float,
) -> None:
    test_input = np.array(input)
    expected_arr = np.array(expected)
    subarray, smini, smaxi = return_subarray(test_input, threshold)
    assert np.array_equal(subarray, expected_arr, equal_nan=True)
    assert smini == mini
    assert smaxi == maxi


sort_cases = [([0.1406, 0.4243, 0.967, 0.334], [0.1406, 0.334, 0.4243, 0.967])]


@pytest.mark.parametrize("array, arr_sorted", sort_cases)
def test_sorting(array: list[float], arr_sorted: list[float]) -> None:
    i_array = np.array(array)
    i_sorted = np.array(arr_sorted)
    sorti = InfinitesimalSort()
    thresholds = {i: sorti.thresholds(i)[1] for i in range(10)}
    assert np.array_equal(best_quasi_sort(i_array, thresholds), i_sorted)


sort_cases2 = [([0.1406, 0.4243, 0.967, 0.334], [0.1406, 0.334, 0.4243, 0.967])]


@pytest.mark.parametrize("array, arr_sorted", sort_cases2)
def test_sorting_2(array: list[float], arr_sorted: list[float]) -> None:
    i_array = np.array(array)
    i_sorted = np.array(arr_sorted)
    assert np.array_equal(best_quasi_sort(i_array), i_sorted)


sort_cases = [([0.1406, 0.4243, 0.967, 0.534], [0.1406, 0.4243, 0.534, 0.967])]


@pytest.mark.parametrize("array, arr_sorted", sort_cases)
def test_not_sortable(array: list[float], arr_sorted: list[float]) -> None:
    i_array = np.array(array)
    sorted_arr = np.array(arr_sorted)
    sorti = InfinitesimalSort()
    thresholds = {i: sorti.thresholds(i)[1] for i in range(10)}
    try:
        np.array_equal(best_quasi_sort(i_array, thresholds), sorted_arr)
    except ValueError:
        assert True, "we expected a not sortable array here"
