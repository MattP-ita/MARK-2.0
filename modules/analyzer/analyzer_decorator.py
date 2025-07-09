import time
import functools
import traceback

from modules.utils.logger import get_logger
logger = get_logger(__name__)

def log_and_time(label=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = label or func.__name__
            logger.info(f"Start: {func_name}")
            start = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception in {func_name}")
                traceback.print_exc()
                raise
            duration = time.time() - start
            logger.info(f"{func_name} completed in {duration:.2f}s")
            return result
        return wrapper
    return decorator



