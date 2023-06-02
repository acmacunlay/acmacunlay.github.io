---
hide:
  - footer
tags:
  - Python
---

# How to use Python's logging module?

---

Python's `logging` module is a powerful tool to help track and debug events in your software application. This article will guide you through the basics of logging and demonstrate how to implement it in your Python projects. With logging, you can keep track of important events and detect errors more easily, making your software more robust and reliable. Learning how to use logging will be a valuable asset to your skill set.

## Setup

In your favorite terminal application, do the following:

1. **Create a directory for your project.**

    ```bash

    mkdir python-logging-tutorial
    cd python-logging-tutorial

    ```

2. **Set up a virtual environment.** This will keep you, the developer, from "polluting" your Python installation of unnecessary libraries and modules. Having a virtual environment will also isolate your project from other projects, preventing conflicts in your dependencies.

    ```bash

    python -m venv .venv

    ```

3. **Activate your virtual environment.** Activating the virtual environment will direct your project to the "localized" copy of Python. Once activated, all dependencies you will install will be stored only in that localized Python.

    ```bash

    .venv/scripts/activate

    ```

4. **Update `pip`.** Update pip and let it do its thing. This is important to stay up to date with anything that they flag as deprecated and/or whatnot.

    ```bash

    python -m pip install --upgrade --no-cache-dir pip

    ```

5. _(Recurring)_ **Save your dependencies.** Everytime you install a new module or package, save all your dependenciesusing `pip`. This will list down all your 3rd party dependencies in a file.

    ```bash

    python -m pip freeze > requirements.txt

    ```

---

## Usage

The `logging` module is already a part of Python's standard library so there's no need to install anything. I will be using the `logging` module in a slightly different way compared to other tutorials you might have already watched or read. I can't say that this is the best way of using it, but it has worked pretty well for me, even in production environments.

So first, create a directory structure as shown below:

```bash

python-logging-tutorial
├── src
│   ├── core
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── logging.py
│   │   └── __init__.py
│   └── __init__.py
├── .venv
├── app.py
└── __init__.py

```

```python

import logging

DEFAULT_LOG_FORMAT: logging.Formatter = logging.Formatter(
    fmt=(
        "%(asctime)s.%(msecs)03d "
        "| %(levelname)-8s "
        "| %(process)-6d"
        "| %(thread)-6d"
        "| %(module)-32s | %(funcName)-32s | %(lineno)-5d "
        "| %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)


def create_logger(
    logger_id: str,
    log_level: int = logging.DEBUG,
) -> logging.Logger:
    logger = logging.getLogger(logger_id)
    logger.setLevel(log_level)
    return logger


def get_logger(logger_id: str) -> logging.Logger:
    return logging.getLogger(logger_id)


def add_file_handler(
    logger: logging.Logger,
    log_file_path: str,
    log_format: logging.Formatter = DEFAULT_LOG_FORMAT,
) -> logging.Logger:

    if log_file_path == None:
        raise ValueError(f"Invalid log file path: {log_file_path}")

    handler = logging.FileHandler(log_file_path)

    handler.setFormatter(log_format)
    logger.addHandler(handler)

    return logger


def add_stream_handler(
    logger: logging.Logger,
    log_format: logging.Formatter = DEFAULT_LOG_FORMAT,
) -> logging.Logger:

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    return logger

```

---

## (Un)common Mistake/s

---

## References

---

- **Author:** _Achilles C. Macunlay_
- **Published:** _2023-01-31_
- **Updated:** _2023-01-31_

---
