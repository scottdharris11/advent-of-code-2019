"""Module providing decorator for each day run"""

import time

def runner(day, part):
    """Decorator for printing results and timing solutions"""
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = time.time() * 1000
            ans = function(*args, **kwargs)
            end = time.time() * 1000
            duration = end-start
            print(f"{day}, {part} ({duration:0.2f} ms): {ans}")
            return ans
        return wrapper
    return decorator
