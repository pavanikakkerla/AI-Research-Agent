"""
Centralized logger for the Research Assistant.
"""

import logging
import sys
from config import LOG_LEVEL


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger("ResearchAssistant")

        logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

        if not logger.handlers:

            console_handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
                "%H:%M:%S"
            )

            console_handler.setFormatter(formatter)

            logger.addHandler(console_handler)

        cls._logger = logger

        return logger


logger = Logger.get_logger()