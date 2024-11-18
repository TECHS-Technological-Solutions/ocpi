"""Logging configuration."""
import logging

from py_ocpi.core.enums import EnvironmentType


class CustomFormatter(logging.Formatter):
    """Custom logging formatter."""

    grey = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    blue = "\x1b[34;20m"
    reset = "\x1b[0m"
    form = "%(asctime)s | [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.INFO: f"{grey}{form}{reset}",
        logging.WARNING: f"{yellow}{form}{reset}",
        logging.ERROR: f"{red}{form}{reset}",
        logging.DEBUG: f"{blue}{form}{reset}",
    }

    def format(self, record):
        """Return formatted logging message."""
        log_fmt = self.FORMATS.get(record.levelno)  # noqa
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LoggingConfig:
    def __init__(self, environment: str, logger) -> None:
        self.environment = environment
        self.logger = logger

    def configure_logger(self):
        if self.environment == EnvironmentType.production.value:
            self.logger.setLevel(logging.INFO)
        elif self.environment == EnvironmentType.development.value:
            self.logger.setLevel(logging.DEBUG)
        elif self.environment == EnvironmentType.testing.value:
            self.logger.setLevel(logging.DEBUG)
        else:
            raise ValueError("Invalid environment")


logger = logging.getLogger("OCPI-Logger")

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
