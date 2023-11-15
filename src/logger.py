from functools import wraps
from typing import Any, Callable
from typing import TypeVar, Type

T = TypeVar('T')


def log_method_call(method: Callable) -> Callable:
    """Decorator to log method calls."""

    @wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(
            f"Calling method {method.__name__} with args {args[1:]} and kwargs {kwargs}"
        )
        return method(*args, **kwargs)

    return wrapper


class LoggingMeta(type):
    """Metaclass that logs method calls."""

    def __new__(cls: Type[T], name: str, bases: tuple, dct: dict[str, Any]) -> T:
        # Iterate over items in the class dictionary
        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = log_method_call(attr_value)
        return super().__new__(cls, name, bases, dct)
