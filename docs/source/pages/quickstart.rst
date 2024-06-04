.. _quickstart:

**********
Quickstart
**********

.. WARNING::
    **K2 Base Camp** currently only supports Windows. We cannot guarantee that the application works as expected if you are using another operating system.

Prerequisites
=============

* `python 3.9 <https://www.python.org/downloads/release/python-390/>`_ 
* `pipenv <https://pipenv.pypa.io/en/latest/installation/>`_
* `WinPcap <https://www.winpcap.org/install/default.htm>`_

Installing python
=================

**K2 Base Camp** needs a specific python version to run (3.9).

To install python, go to the official `website <https://www.python.org/downloads/release/python-390/>`_.

.. NOTE::
    If you have multiple versions of python installed on your system, you can prefix commands with ``py -3.9`` to ensure a specific version (in this case 3.9) is used.

You might have to explicitly specify the python location when creating the virtual environment (on Windows, this is something like *~[username]/AppData/Local/Programs/Python/Python39/python.exe*)::

    py -3.9 -m pipenv --python [path to python.exe]

Subsequently, the quickstart commands would be adapted to::

    py -3.9 -m pipenv sync
    py -3.9 -m pipenv run python -m k2basecamp

Installation
============

.. NOTE::
    Some functions of the application require WinPcap to be installed on your system. You can install it using the `Installer for Windows <https://www.winpcap.org/install/default.htm>`_. Once installed, no further action is required.

If you have python 3.9 and pipenv installed on your system, running **K2 Base Camp** is as simple as:

#. Cloning the repository from `github <https://github.com/ingeniamc/k2-base-camp.git>`_
#. Installing the dependencies::

    pipenv sync

#. Running the program::

    pipenv run python -m k2basecamp