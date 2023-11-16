from typing import Any, Callable, Type


class LoggingMeta(type):
    """Metaclass that logs method calls."""

    def __new__(
        cls: Type["LoggingMeta"],
        name: str,
        bases: tuple[Type, ...],
        dct: dict[str, Any],
    ) -> "LoggingMeta":
        # Iterate over items in the class dictionary
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not isinstance(attr_value, staticmethod):
                dct[attr_name] = cls.log_method_call(attr_value)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def log_method_call(method: Callable) -> Callable:
        """Wraps a method to log its calls."""

        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
            print(f"Calling {method.__name__}")
            return method(*args, **kwargs)

        return wrapper
