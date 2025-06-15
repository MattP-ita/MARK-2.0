import time
import functools
import traceback

def log_and_time(label=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = label or func.__name__
            print(f"[DEBUG] Start: {func_name}")
            start = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] Exception in {func_name}")
                traceback.print_exc()
                raise
            duration = time.time() - start
            print(f"[INFO] {func_name} completed in {duration:.2f}s")
            return result
        return wrapper
    return decorator
