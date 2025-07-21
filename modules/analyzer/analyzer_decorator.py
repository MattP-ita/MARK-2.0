"""Decorator to log execution time and handle exceptions with optional labels."""

import time
import functools
import traceback

from modules.utils.logger import get_logger

logger = get_logger(__name__)


def log_and_time(label=None):
    """Decorator to log execution time and exceptions for a function.

    Args:
        label (str, optional):
            Custom label for logging. Defaults to function name.

    Returns:
        Callable: Wrapped function with logging and timing.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = label or func.__name__
            logger.info("Start: %s", func_name)
            start = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception:
                logger.error("Exception in %s", func_name)
                traceback.print_exc()
                raise
            duration = time.time() - start
            logger.info("%s completed in %.2fs", func_name, duration)
            return result
        return wrapper
    return decorator
