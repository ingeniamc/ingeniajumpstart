**********
Quickstart
**********

If you have python 3.9 installed on your system, running K2 Base Camp is as simple as:

#. Cloning the repository from `github <https://github.com/ingeniamc/k2-base-camp.git>`_
#. Installing the dependencies::

    pipenv install --ignore-pipfile

#. Running the program::

    pipenv run python src/__main__.py

Installing python
=================

K2 Base Camp needs a specific python version to run (3.9).

To install python, go to the official `website <https://www.python.org/downloads>`_.

.. NOTE::
    If you have multiple versions of python installed on your system, you can prefix commands with ``py -3.9`` to ensure a specific version (in this case 3.9) is used.

You might have to explicitly specify the python location when creating the virtual environment (on Windows, this is something like *~[username]/AppData/Local/Programs/Python/Python39/python.exe*)::

    py -3.9 -m pipenv --python [path to python.exe]

Subsequently, the quickstart commands would be adapted to::

    py -3.9 -m pipenv install --ignore-pipfile
    py -3.9 -m pipenv run python src/__main__.py