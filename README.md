# Books to scrap

## Prerequisite

`python` >= 3.x, `pip` and `virtualenv` must be installed on your system.

## How to get started

- Create a Python virtual environment in the project root directory

```shell
$ python -m venv venv
$ source ./venv/bin/activate
```

- Install the required packages

```shell
$ pip install -r requirements.txt
```

## How to run the program

```shell
$ python main.py [OPTIONS]
OPTIONS: getall, --save-img, bookurl [URL], category [CATEGORY]
```

#### Get data from all categories and download the images

```shell
$ python main.py getall --save-img
```
