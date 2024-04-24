# K2 Base Camp

Simple open source app to plug &amp; play with your servo drive.

## Getting started

### Prerequisites

The project requires [python 3.9](https://www.python.org/downloads/release/python-390/) and [pipenv](https://pipenv.pypa.io/en/latest/installation/).

### Installation

1. Clone the repository

   `git clone https://github.com/ingeniamc/k2-base-camp.git`

2. Install dependencies

   `pipenv sync`

3. Run the project

   `pipenv run python -m k2basecamp`

## Development

### Install development dependencies

`pipenv sync -d`

### Pre-commit hooks (optional)

We have setup pre-commit hooks that run several tools to improve code quality.
Installing the hooks (this will run the tools every time you attempt to make a commit)

`pipenv run pre-commit install`

You can also run the tools manually

`pipenv run pre-commit run -a`

One of the tools that we are using is linting the qml files.
For this to work properly, we need to create some qml types from our python files

`pipenv run pyside6-project build`

### Documentation (optional)

Documentation added to the source code can be compiled into several output formats using [sphinx](https://www.sphinx-doc.org/en/master/)

```
cd docs
pipenv run make clean
pipenv run make html
```

### Running tests

Run tests using pytest

`pipenv run pytest src/tests`

## License

The project is licensed under the Creative Commons Public Licenses.
