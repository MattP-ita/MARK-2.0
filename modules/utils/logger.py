"""Logging utility for the MARK project."""

import logging
import os
import sys
from datetime import datetime


def get_logger(name: str = "MARK", log_dir: str = "logs") -> logging.Logger:
    """
    Create and return a configured logger instance.

    Args:
        name (str): Name of the logger.
        log_dir (str): Directory where log files are saved.

    Returns:
        logging.Logger: Configured logger instance.
    """
    is_debug = hasattr(sys, "gettrace") and sys.gettrace() is not None
    logging.raiseExceptions = is_debug

    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"mark_2_{timestamp}.log")

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger  # Prevent duplicate handlers if already configured

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
