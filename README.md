# How use this project with poetry

Poetry is a Python package manager that makes it easy to manage dependencies and create virtual environments for your Python project.

To add a new dependency, run:

'poetry add <package-name>´

To install dependencies listed in the pyproject.toml file, run:

'poetry install'

To create a virtual environment and activate it, run:

poetry shell

To run a Python script within the context of the project, run:

arduino

poetry run python <script-name>.py

That's it! For more information on using Poetry, check out the official documentation.

# You can run the pre-commit hooks using 

pre-commit install
pre-commit run
