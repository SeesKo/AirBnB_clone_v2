# AirBnB Clone Project

## Project Description

This repository contains the continuation an implementation of a command-line interface (CLI) for the initial `AirBnB clone` project. This stage implements a backend interface, or console, to manage program data. The command interpreter allows users to perform various operations on objects, such as creating, retrieving, updating, and deleting, as well as managing file storage.

## Command Interpreter

The command interpreter is implemented using the Python `cmd` module. It provides a set of commands to interact with and manipulate objects. Users can create new objects, retrieve objects from storage, perform operations, update attributes, and destroy objects.

### How to Start

To start the command interpreter, run the `console.py` script in the terminal.

    $ ./console.py

### How to Use

Once the command interpreter is running, use the following commands to manage AirBnB objects:

- `create`: Create a new object (e.g., User, State, City, Place).
- `show`: Retrieve information about a specific object.
- `all`: Display information about all objects or objects of a specific class.
- `update`: Update attributes of a specific object.
- `destroy`: Destroy a specific object.
- `quit`: Exit the command interpreter.

## Project Requirements

### Python Scripts

- All files will be interpreted/compiled on Ubuntu 20.04 LTS using python3 (version 3.8.5).
- Code should use the pycodestyle (version 2.8.*).
- All files must be executable.
- All modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All functions (inside and outside a class) should have documentation `(python3 -c
    -'print(__import__("my_module").my_function.__doc__)' and python3 -c
    -'print(__import__("my_module").MyClass.my_function.__doc__)'`)

### Python Unit Tests

- All tests should be executed by using this command: `python3 -m unittest discover tests`.
- Individual test files can also be tested by using this command: `python3 -m unittest tests/test_models/test_base_model.py`.

### SQL Scripts

- All files will be executed on Ubuntu 20.04 LTS using `MySQL 8.0`.
- Files will be executed with `SQLAlchemy` version `1.4.x`.
- All SQL keywords should be in uppercase (`SELECT, WHERE`…).
