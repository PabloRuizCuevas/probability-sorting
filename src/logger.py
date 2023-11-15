from functools import wraps
from typing import Callable, Any


def log_method_call(method: Callable) -> Callable:
    """Decorator to log method calls."""

    @wraps(method)
    def wrapper(*args, **kwargs) -> Callable:
        print(
            f"Calling method {method.__name__} with args {args[1:]} and kwargs {kwargs}"
        )
        return method(*args, **kwargs)

    return wrapper


class LoggingMeta(type):
    """Metaclass that logs method calls."""

    def __new__(cls, name: str, bases, clsdict):
        # Iterate over items in the class dictionary
        for key, value in clsdict.items():
            if callable(value) and not isinstance(value, staticmethod):
                clsdict[key] = log_method_call(value)

        return super().__new__(cls, name, bases, clsdict)
