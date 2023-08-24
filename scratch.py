import logging
import time
import typing

LOGGER_NAME: typing.Final[str] = "LoggerName"

logger = logging.getLogger(LOGGER_NAME)  # (1)!
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
