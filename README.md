[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)


# Online Optimal Sort

Onsort is a small library providing utilities for online ranking (sorting) numbers comming from a know distribution at random.

It was inspired by the game Place-it and here you will find the algorithms to compute the probability of winning the game with the best strategy as well as the continuous variant.

## Content 

The library contains two modules:

- Continuous: where we have the scripts for calculating the probability of winning the continous version as well as one script for sorting numbers in a random continous distriboutin from 0 to 1.

- discrete: where we have a script for getting the probability for solving the original game. We also provide as a the c++ implementation.


As the probability can be calculated analytically the code is semi-symbolic, notice that the full symbolic solution for more than 8-10 slots can take very long time.

## Usage example:

If wanting to use the library for sorting we have the following script:

```python
from onsort.continuous.online_sort import sort

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
