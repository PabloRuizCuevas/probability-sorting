# export PYTHONPATH=$PYTHONPATH:$(pwd)
import numpy as np
import pytest

from src.my_sort import InfinitesimalSort, sort, return_subarray

optimal = InfinitesimalSort()
nan = np.nan

test_cases = [
    ([nan, nan, nan, nan, nan, nan], 0.3, [nan, nan, nan, nan, nan, nan], 0, 1),
    ([nan, nan, 0.2, nan, nan, nan], 0.3, [nan, nan, nan], 0.2, 1),
    ([nan, nan, 0.2, nan, 0.4, nan], 0.3, [nan], 0.2, 0.4),
    ([0.1, nan, 0.4, nan, nan, 0.8], 0.5, [nan, nan], 0.4, 0.8),
    ([nan, nan, 0.4, nan, nan, 0.8], 0.2, [nan, nan], 0.0, 0.4),
    ([nan], 0.2, [nan], 0.0, 1.0),
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
    thresholds = {i: sorti.thresholds(i)[1] for i in range(5)}
    assert np.array_equal(sort(i_array, thresholds), i_sorted)


sort_cases2 = [([0.1406, 0.4243, 0.967, 0.334], [0.1406, 0.334, 0.4243, 0.967])]


@pytest.mark.parametrize("array, arr_sorted", sort_cases2)
def test_sorting_2(array: list[float], arr_sorted: list[float]) -> None:
    i_array = np.array(array)
    i_sorted = np.array(arr_sorted)
    assert np.array_equal(sort(i_array), i_sorted)


sort_cases = [
    [0.1406, 0.4243, 0.967, 0.534], 
    [0.1406, 0.4243, 0.534, 0.967],
    [0.76931784, 0.06506234, 0.04066391, 0.70643678, 0.34615554]
]


@pytest.mark.parametrize("array", sort_cases)
def test_not_sortable(array: list[float]) -> None:
    i_array = np.array(array)
    sorti = InfinitesimalSort()
    thresholds = {i: sorti.thresholds(i)[1] for i in range(5)}
    try:
        sort(i_array, thresholds)
        assert False, "This should fail, with raise_error=True"
    except ValueError:
        print("all good we expected a not sortable array here")


sort_casess = [
    [0.1406, 0.4243, 0.967, 0.334],
    [0.1406, 0.334],
    [0.1406, 0.4243, 0.967, 0.334, 0.534],
    [0.1406, 0.4243, 0.967, 0.334, 0.511, 0.534],
    [0.506, 0.4243, 0.967],
    [0.76931784, 0.06506234, 0.04066391, 0.70643678, 0.34615554],
    [0.76931784, 0.06506234, 0.04066391, 0.70643678, 0.34615554, 0.54615554],
]


@pytest.mark.parametrize("array", sort_casess)
def test_more_sortable(array: list[float]) -> None:
    i_array = np.array(array)
    sorti = InfinitesimalSort()
    thresholds = {i: sorti.thresholds(i)[1] for i in range(7)}
    try:
        sort(i_array, thresholds, False)
    except:
        assert False, "This should not fail, with raise_error=False"

