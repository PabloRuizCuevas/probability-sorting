[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)


# Online Optimal Sort


## Installation

Install poetry at  https://python-poetry.org/

Then run

> poetry config --local virtualenvs.in-project true

> poetry install

Then run (only first time):

> git submodule update --init --recursive

other times -> git submodule update --recursive --remote
for getting last commit of submodule -> git submodule update --remote --merge


## Run test

> poetry shell

> pytest .

> pytest  --cov=pytrade tests/
