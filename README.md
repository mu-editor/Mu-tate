# Mu-tate

An experimental version of [Mu](https://codewith.mu) made in JavaScript. 
Packaged via [Electron](https://www.electronjs.org/).

The application is in the `mu` directory. Embedded Python for each supported
platform is in a directory indicating the platform, in the `python` directory.

Tests (unit and integration) are in `tests` and documentation (using Sphinx) is
in `docs`.

Most of the common processes for developing Mu can be found in the `Makefile`.
Type `make` to see what you can do:

```
$ make

There is no default Makefile target right now. Try:

make ace - check for and download the latest version of Ace editor.
make clean - reset the project and remove auto-generated assets.
make docs - run sphinx to create project documentation.
make python - check for and download the latest stand-alone Python.
make run - run the application locally.
make setup - setup and install a development environment for Mu.
make test - run the jasmine based unit tests.
make tidy - tidy project Python code with black.
```

## Developer Setup

In a new Python 3 virtual environment on a machine with node and npm installed:

```
$ pip install -r requirements.txt
$ make ace
$ make python
$ make setup
```

To run the tests `make test`, to run the application `make run`. Steps for
packaging the application will be added very soon.
