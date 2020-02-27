# Team 94 FIRST Robotics FRC Robot Code

[![Build Status](https://travis-ci.org/TechnoJays/robot2019.svg?branch=develop)](https://travis-ci.org/TechnoJays/robot2019)

[FIRST Robotics FRC] is a high school robotics program.  This repository contains the code used in the
Southfield High School Team 94 (NinetyFouriors) robot.

## Getting Started

### Development Requirements

* **Python 3.8**: This codebase uses Python 3.8
* [pyfrc]: Be sure to follow the [pyfrc instructions] for the latest roboPy setup. This is largely handled by the install of this project mentioned below.

It is highly recommended that you use an python environment manager with python to help as the version
of python required by pyfrc changes.

* [pyenv] is useful for managing multiple python versions (3.8) on your computer: **NOTE your python version and pip version/dependencies are highly correlated**
  * `brew install pyenv` for macOS and [Homebrew]
  * `scoop install python` with [Scoop] is the closest thing if you have the misfortune to be using Windows and possibly follow [this page] for more instructions on supporting different python versions
  * [pipenv] is useful for dependency management for this project as well
  * `pipenv --python 3.8` to create a python 3.8 environment for this project
  * `pipenv install -e .` to setup this project in the created virtualenv
  * `pipenv shell` to enter the environment for this project
  * `tox` after that to run the tests

IDEs like [Pycharm also support pipenv].

Note: If you are confident that your system version of python is exactly python 3.8, then you can simply use:

```bash
pip3 install -e .
tox
```

Good luck!

### Project Formatting

To be soothing to your mind, the project attempts to make python/PEP formatting not an issue. Given you
think you are ready to commit your code changes. Just run:

```bash
black --check .
```

To show which files **[black]** will reformat.

```bash
black --diff .
```

Shows the changes black will make, and then:

```bash
black .
```

will let the reformatting goodness happen. Black comes with the `pipenv install -e .` of the project.

## Deploying to the Robot

* Copy/install all .py files in the src/robot folder to the robot.

RobotPy has some great [robot code deployment instructions and automation].
Note that the RobotPy deployment process will automatically run the tests for the project as
part of the deployment to try and protect us from ourselves.

```bash
python3 robot.py deploy

# in the virtual environment python3 may not be available
python robot.py deploy
```

## Running Tests

1. Make sure, you have `tox` installed:

    ```bash
    pipenv install -e .[tests]
    pipenv shell
    ```

2. Run the projects tests:

   ```bash
   tox
   ```

`tox` is running `python src/robot.py coverage test` from [RobotPy Unit Testing]
[FIRST Robotics FRC]:(<http://www.usfirst.org/>)
[pyfrc]:(<https://github.com/robotpy/pyfrc>)
[pyfrc instructions]:(<http://pyfrc.readthedocs.org/en/latest/>)
[black]:(<https://github.com/ambv/black>)
[RobotPy Unit Testing]:(<https://robotpy.readthedocs.io/en/stable/guide/testing.html>)
[pyenv]:(<https://github.com/pyenv/pyenv>)
[pipenv]:(<https://github.com/pypa/pipenv>)
[Homebrew]:(<https://brew.sh/>)
[Scoop]:(<https://scoop.sh/>)
[this page]:(<https://github.com/lukesampson/scoop/wiki/Switching-Ruby-and-Python-Versions>)
[robot code deployment instructions and automation]:(<https://robotpy.readthedocs.io/en/stable/guide/deploy.html>)
[Pycharm also support pipenv]:(<https://www.jetbrains.com/help/pycharm/pipenv.html>)
