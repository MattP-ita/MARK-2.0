import logging
import os
from datetime import datetime


def get_logger(name: str = "MARK", log_dir: str = "logs") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"mark_2_{timestamp}.log")

    logger = logging.getLogger(name)

    # Evita di aggiungere handler multipli se il logger è già configurato
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
