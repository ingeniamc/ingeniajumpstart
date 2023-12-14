********
Codebase
********

K2 Base Camp is meant to serve as a starting point for futher development.

Before we get into the details of how to properly set up the development environment, let's get an overview of how the codebase of the project is structured.

Tech Stack
==========

The application is built with the Qt-framework, using the open source variant PySide6.

As such, most of the code is writting in python. However, the interface (GUI) is written in QML.

Here's a list of the most important libraries and frameworks we are using:

* **PySide6** - main graphics framework
* **QML** - declarative language for creating interfaces
* **javascript** - small parts of the logic in the QML code is written in this language
* **ingenialink** - communication library for Ingenia servo drives
* **pytest** - testing library
* **sphinx** - facilitates creating documentation
* **mypy** (typing), **black** (formatting), **ruff** (linting) - improve code quality
* **pre-commit** - run scripts before commiting to git to improve code quality

Project folder structure
========================

| root
| ├── .vscode *(editor-specific configuration)*
| ├── assets *(static files such as images)*
| ├── docs *(this documentation)*
| ├── src
| │   ├── controllers
| │   ├── models
| │   ├── services
| │   ├── utils
| │   ├── views
| │   └── __main__.py
| ├── tests *(unit and gui tests)*
| ├── Pipfile & Pipfile.lock *(dependencies)*
| └── *misc. configuration files & license*

Architecture
============

The *src* directory contains the application code and is composed of several important parts.

Everything that is visible to the user is contained in the *views* - folder and written in QML (all QML and javascript code is contained in the *views* - folder). 
The user interface and all it's components are defined here. 
It also contains a subfolder *js* where some slightly more complex javascript - functions are defined.

The application state is saved in instances of the classes defined in the *models* - folder.

However, the *views* cannot directly communicate with the *models*. 
Instead, they use *controllers* to interface between GUI and application state.

*controllers* in turn make use of *services* to communicate with the servo drives. 
An important thing to note is that all communication with the drives should be happening in a separate thread, as we want to avoid blocking the GUI while the operation is running. This should be handled by the corresponding *service*.

With this knowledge, we can now understand what happens when we start the application by executing the **__main__.py** file:

#. A new QApplication is created. 
#. The QML code is injected into it by passing it the views/main.qml file.
#. A controller object is created, which is then connected to the qml files.
#. The controller will instantiate a service, which will automatically start a separate thread that is used for the communication with the drive.
#. Finally, the application is started.

Examples
========

To illustrate the flow of the application while it is running, consider the following examples.

* Selecting a connection protocol:

    #. We choose a different connection protocol using the dropdown in the GUI.
    #. A javascript function handles the event and calls a function in the controller (this only works if the function is declared as a **Slot**).
    #. The controller receives the new value and sets the corresponding property of its model.

* Connecting the drives:

    #. We configured the connection parameters correctly and hit the **Connect** - button.
    #. A javascript function handles the event and calls a function in the controller.
    #. The controller passes a function it wants executed to the service, along with a callback function.
    #. The service puts the function and its parameters in the queue of its drive communication thread.
    #. The thread notices the incoming task, completes it, and sends a success signal.
    #. The signal is received by the service which then executes the callback function it received from the controller earlier (the callback function is defined in the controller).
    #. The callback function is used to emit a signal that the connection has been completed successfully.
    #. The frontend receives the signal and exectues a javascript function that opens a new page in the interface.

Services can also start additional threads when necessary, for example it is sometimes necessary to continuosly receive data from a drive.

* One such example is the data that we use to plot the changes in velocity:

    #. We press one of the checkboxes that enable a motor in the GUI.
    #. As in the example before, the controller and service enable the motor of the drive (GUI -> controller -> service -> thread -> service -> controller).
    #. The callback function in the controller uses the service to start a new PollerThread.
    #. The controller connects the signal the PollerThread emits when it reads new data to one of its functions.
    #. The connected function in turn emits a signal that is received by the GUI.
    #. The GUI updates the graph when it receives new data through the signal.