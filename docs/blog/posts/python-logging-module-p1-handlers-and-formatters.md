---
draft: true
date: 2023-08-22
authors:
  - acmacunlay
categories:
  - Python
  - Software Development

tags:
  - Python
  - Software Development
---

# Python `logging` Module Part 1: Handlers and Formatters

---

Python's standard logging module offers a robust solution for developers to track and manage an application's behavior. This post delves into the practical usage of Python's logging module and sheds light on the role of Handlers and Formatters. Understanding these elements equips developers with the tools needed to enhance code reliability and streamline troubleshooting processes.

<!-- more -->

## Handlers

In Python's logging module, handlers are components responsible for determining what should be done with log messages once they have been emitted by loggers. Log messages are generated using loggers, and handlers define where these messages are sent, such as to the console, files, remote servers, etc.

Handlers in the logging module provide an interface for sending log messages to various destinations. Each handler has a specific purpose and configuration options to control the formatting and filtering of log messages. Some common types of handlers include:

- `StreamHandler` : This handler sends log messages to a specified stream, typically the console (`sys.stdout` or `sys.stderr`). It's useful for displaying log messages in a terminal or command prompt.
- `FileHandler` : This handler writes log messages to a specified file. It's often used to create log files for tracking application behavior over time.
- `RotatingFileHandler` : This handler extends FileHandler and automatically rotates log files based on size or time, creating a new file when the current one reaches a certain size or when a certain time interval has passed.
- `TimedRotatingFileHandler` : Another extension of FileHandler, this handler rotates log files based on specific time intervals, creating new files at specified intervals (e.g., daily, hourly).
- `SocketHandler` : This handler sends log messages to a remote server via a network socket. It's useful for logging in distributed systems or remote applications.
- `SMTPHandler` : This handler sends log messages as emails using the Simple Mail Transfer Protocol (SMTP). It's often used to notify administrators or developers about critical events.
- `SysLogHandler` : This handler sends log messages to the system log (on Unix-like systems) or the Event Log (on Windows systems).
- `NullHandler` : This handler is used when you want to disable logging entirely. It's often used as a placeholder when no other suitable handler is configured.

## Formatters

In Python's logging module, a formatter is an object used to define the structure and content of log messages. Formatters determine how log records are transformed into human-readable text when they are emitted by loggers and sent to various output destinations like files, console, or remote servers.

Formatters allow you to control the layout and appearance of log messages, making them easier to read and understand. You can customize the format using placeholders, which are placeholders enclosed in percentage signs (%). These placeholders are replaced with actual values from the log records when log messages are formatted.

Common placeholders include:

- `%asctime%` : The timestamp when the log record was created.
- `%levelname%` : The log level name (e.g., INFO, WARNING, ERROR).
- `%name%` : The name of the logger that emitted the log record.
- `%message%` : The actual log message itself.
- `%filename%` : The name of the source file where the logging call was made.
- `%lineno%` : The line number in the source file where the logging call was made.
- `%funcName%` : The name of the function where the logging call was made.

## Usage

### Example: Using StreamHandler

```python title="logging_stream_handler.py" linenums="1"
import logging
import time
import typing

LOGGER_NAME: typing.Final[str] = "LoggerName"

logger = logging.getLogger(LOGGER_NAME) # (1)!
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    (
        "%(asctime)s.%(msecs)03d" + time.strftime("%z") + " "
        "| %(process)-8d "
        "| %(thread)-16d "
        "| %(levelname)-8s "
        "| %(lineno)-4d "
        "| %(message)s"
    ),
    "%Y-%m-%dT%H:%M:%S",
)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.addHandler(handler)

# Sample
logger.debug("Debug message.")
logger.info("Info message.")
logger.warning("Warning message.")
logger.error("Error message.")
logger.critical("Warning message.")
logger.exception("Exception message.")

```

1. Return a `Logger` object named `LOGGER_NAME`. If such `Logger` does not exist, then it will be created and returned.
