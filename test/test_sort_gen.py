import pytest
from onsort.continuous.online_sort import sort


sortable_cases = [
    [0.1406, 0.4243, 0.967, 0.334],
    [0.1406, 0.4243, 0.534, 0.267],
    [0.76931784, 0.06506234, 0.07066391, 0.70643678, 0.94615554],
]


@pytest.mark.parametrize("array_to_sort", sortable_cases)
def test_sort_gen(array_to_sort):
    sort_gen = sort(len(array_to_sort))
    slots = next(sort_gen)  # initialize generator
    for n in array_to_sort:
        slots = sort_gen.send(n)
        print(slots)
