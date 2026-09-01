"""
EcoLoop AI - Logging Utility
Configures structured, colored logging for debugging and system audit.
"""

import logging
import sys


def setup_logger(name: str = "ecoloop", level: int = logging.INFO) -> logging.Logger:
    """
    Creates and returns a configured logger instance with formatted stream output.
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
