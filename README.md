[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)


# Online Optimal Sort

Onsort is a small library providing utilities for online ranking (sorting) numbers comming from a know distribution at random.



## How use:

```python
from onsort.online_sort import sort

# the data can be generated randomly, comming from online stream
arr = [0.76931784, 0.06506234, 0.07066391, 0.70643678, 0.94615554]
sort_gen = sort(5)
slots = next(sort_gen) # initialize generator
for n in arr:
    slots = sort_gen.send(n)
    print(slots)
```




## Run test

> poetry shell

> pytest .

> pytest  --cov=pytrade tests/
